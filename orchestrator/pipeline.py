import os
import time
import uuid
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional, Callable

from AI_Zavod.config import default_config, Config
from AI_Zavod.gateway.client import OmniRouteClient
from AI_Zavod.memory.sqlite_store import ContextMemoryStore
from AI_Zavod.memory.skill_rag import SkillRAGEngine
from AI_Zavod.mcp.server_registry import MCPManager
from AI_Zavod.agents.teamlead import TeamLeadAgent
from AI_Zavod.agents.product_manager import ProductManagerAgent
from AI_Zavod.agents.designer import DesignerAgent
from AI_Zavod.agents.architect import ArchitectAgent
from AI_Zavod.agents.backend import BackendAgent
from AI_Zavod.agents.frontend import FrontendAgent
from AI_Zavod.agents.qa_security import QASecurityAgent
from AI_Zavod.agents.devops import DevOpsAgent
from AI_Zavod.agents.ui_tester import UITesterAgent
from AI_Zavod.verification.verifier import ProjectVerifier
from AI_Zavod.orchestrator.self_healing import SelfHealingEngine
from AI_Zavod.orchestrator.hitl_matrix import generate_matrix_html, prompt_cli_selection
from AI_Zavod.orchestrator.vk_hitl import VKHITLDispatcher

logger = logging.getLogger("AI_Zavod.Pipeline")

class AIZavodPipeline:
    def __init__(self, config: Optional[Config] = None):
        self.config = config or default_config
        self.gateway = OmniRouteClient(self.config.gateway)
        self.memory = ContextMemoryStore(self.config.memory.db_path)
        self.skill_rag = SkillRAGEngine()
        self.mcp = MCPManager(self.config.workspace_root)
        
        # Initialize Team Lead + 8 specialized subagents (total 9 agents)
        self.teamlead = TeamLeadAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.pm = ProductManagerAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.designer = DesignerAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.architect = ArchitectAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.backend = BackendAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.frontend = FrontendAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.qa_security = QASecurityAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.devops = DevOpsAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        self.ui_tester = UITesterAgent(gateway=self.gateway, memory=self.memory, mcp=self.mcp)
        
        # Self-healing engine and VK HITL dispatcher
        self.self_healing = SelfHealingEngine(pipeline=self)
        self.vk_dispatcher = VKHITLDispatcher(
            token=self.config.vk.token,
            default_peer_id=self.config.vk.default_peer_id
        )

    def _log_tasks_matrix(self, stage_name: str, tasks: List[Dict[str, Any]]):
        """Helper to print and log task execution statuses cleanly."""
        if not tasks:
            return
        logger.info(f"📋 [{stage_name}] Tasks Execution Matrix ({len(tasks)} items):")
        for t in tasks:
            task_desc = t.get("task", "Unnamed Task")
            status = t.get("status", "UNKNOWN")
            evidence = t.get("evidence", "")
            if status == "SUCCESS":
                logger.info(f"   ✅ [SUCCESS] {task_desc} -> {evidence}")
            else:
                logger.error(f"   ❌ [FAILED]  {task_desc} -> {evidence}")

    def default_cli_checkpoint(self, checkpoint_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Interactive CLI prompt when auto_mode=False for developer review/modifications."""
        print(f"\n🛑 [CHECKPOINT: {checkpoint_name.upper()}] Developer Review Required:")
        if checkpoint_name == "checkpoint_prd":
            print(f"• Product Name: {payload.get('product_name')}")
            print(f"• Tagline: {payload.get('tagline')}")
            print(f"• Target Audience: {payload.get('target_audience')}")
        elif checkpoint_name == "checkpoint_architecture":
            print(f"• ADR Decision: {payload.get('adr', {}).get('decision')}")
            print(f"• DDL Schema:\n{payload.get('database_schema_sql', '')[:300]}...")
            print(f"• API Endpoints: {len(payload.get('api_endpoints', []))} routes planned")
        elif checkpoint_name == "checkpoint_code":
            print(f"• Target Dir: {payload.get('target_dir')}")
            print(f"• Generated Files Ready for Verification")

        print("\nOptions: [y] Approve and continue | [e] Edit/Inject feedback | [q] Abort")
        try:
            choice = input(">>> Action [y/e/q]: ").strip().lower()
        except EOFError:
            choice = "y"

        if choice == "q":
            raise KeyboardInterrupt("Pipeline cancelled by developer.")
        elif choice == "e":
            feedback = input(">>> Enter feedback or modifications for agents: ").strip()
            return {"approved": True, "feedback": feedback}
        return {"approved": True, "feedback": None}

    def execute(
        self,
        goal_prompt: str,
        target_dir_name: Optional[str] = None,
        source_file: Optional[str] = None,
        image_file: Optional[str] = None,
        auto_mode: Optional[bool] = None,
        checkpoint_handler: Optional[Callable[[str, Dict[str, Any]], Dict[str, Any]]] = None,
        forced_concept_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Task Mode: Full 8-stage lifecycle with Full Parallel DAG Concurrency,
        multimodal image ingestion, dynamic skill enforcement, and task tracking matrix.
        """
        is_auto = self.config.pipeline.auto_mode if auto_mode is None else auto_mode
        chk_handler = checkpoint_handler or self.default_cli_checkpoint

        session_id = f"zavod_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        logger.info(f"=== [AI-Zavod] Starting Session: {session_id} (AutoMode={is_auto}, Parallel=True) ===")
        start_time = time.time()

        temp_slug = target_dir_name or f"app_{session_id}"
        target_dir = os.path.join(self.config.workspace_root, temp_slug)
        os.makedirs(target_dir, exist_ok=True)
        self.memory.create_session(session_id, goal=goal_prompt, target_dir=target_dir, mode="task")

        # Ingest active skills
        skill_context = self.skill_rag.format_skill_context(goal_prompt)
        enhanced_prompt = f"{goal_prompt}\n{skill_context}" if skill_context else goal_prompt

        # 1. Multimodal image ingestion via OmniRoute vision
        if image_file and os.path.exists(image_file):
            import base64
            try:
                with open(image_file, "rb") as f:
                    b64_img = base64.b64encode(f.read()).decode("utf-8")
                mime = "image/png" if image_file.lower().endswith(".png") else "image/jpeg"
                data_url = f"data:{mime};base64,{b64_img}"
                
                logger.info(f"[Pipeline] Analyzing user image specification '{image_file}' via multimodal vision...")
                vision_messages = [
                    {"role": "user", "content": [
                        {"type": "text", "text": "Extract all tasks, formulas, notes, and specifications from this image in complete technical detail."},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]}
                ]
                vision_res = self.gateway.chat_completion(messages=vision_messages)
                img_analysis = vision_res.get("content", "")
                enhanced_prompt += (
                    f"\n\n========================================\n"
                    f"PRIMARY IMAGE SPECIFICATION ANALYSIS ({image_file}):\n"
                    f"{img_analysis}\n"
                    f"========================================\n"
                    f"CRITICAL DIRECTIVE FOR ALL 8 AGENTS:\n"
                    f"You MUST implement all technical tasks and features extracted from the image directly into architecture and code!\n"
                )
            except Exception as e:
                logger.warning(f"[Pipeline] Image extraction warning: {e}")

        # 2. Source file ingestion via MCP
        if source_file:
            file_res = self.mcp.fs_read_file(source_file)
            if file_res.get("status") == "success":
                logger.info(f"[Pipeline] Ingested primary source document: {source_file}")
                enhanced_prompt += (
                    f"\n\n========================================\n"
                    f"PRIMARY SOURCE SPECIFICATION DOCUMENT ({source_file}):\n"
                    f"{file_res.get('content')}\n"
                    f"========================================\n"
                    f"CRITICAL DIRECTIVE FOR ALL 8 SUBAGENTS:\n"
                    f"You MUST parse and incorporate the REAL data from the source document directly into your SQL seeds and code!\n"
                )

        session_tasks_matrix: List[Dict[str, Any]] = []

        # Stage 0: Teamlead Kickoff
        t0 = time.time()
        logger.info(">>> [Stage 0] 🍊 TeamLead: Planning Sprint Delegation...")
        sprint_plan = self.teamlead.plan_sprint(session_id=session_id, goal_prompt=enhanced_prompt)
        tl_tasks = sprint_plan.get("tasks_checklist", [])
        session_tasks_matrix.extend(tl_tasks)
        self._log_tasks_matrix("TeamLead Kickoff", tl_tasks)
        self.memory.log_stage_metric(session_id, "TeamLead_Kickoff", (time.time() - t0) * 1000)

        # Stage 1: Product Management
        t1 = time.time()
        logger.info(">>> [Stage 1] 💼 Product Manager: Formulating PRD & User Personas...")
        prd_spec = self.pm.analyze_product_requirements(session_id=session_id, goal_prompt=enhanced_prompt)
        pm_tasks = prd_spec.get("tasks_checklist", [])
        session_tasks_matrix.extend(pm_tasks)
        self._log_tasks_matrix("Product Manager", pm_tasks)
        self.memory.log_stage_metric(session_id, "ProductManager", (time.time() - t1) * 1000)

        # [CHECKPOINT 1]: PRD Review (if not in auto_mode)
        if not is_auto:
            chk1_res = chk_handler("checkpoint_prd", prd_spec)
            if chk1_res.get("feedback"):
                enhanced_prompt += f"\n\n[DEVELOPER PRD FEEDBACK]: {chk1_res['feedback']}"

        # Stage 1.5: Synthesize 5 Competitive Interactive Facades & Preview Matrix
        t_facades = time.time()
        logger.info(">>> [Stage 1.5] 🎨 Designer: Synthesizing 5 Competitive Interactive Facades...")
        concepts = self.designer.generate_5_concept_facades(session_id, prd_spec)
        matrix_path = os.path.join(target_dir, "design_preview_matrix.html")
        generate_matrix_html(session_id, prd_spec, concepts, matrix_path)
        self.memory.register_artifact(session_id, matrix_path, "html_matrix", "HITL 5-Concept Preview Matrix")

        # Publish matrix to WebPlanner live preview if available
        preview_url = None
        for wp_candidate in [
            os.path.join(self.config.workspace_root, "WebPlanner", "frontend"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "WebPlanner", "frontend"),
            r"c:\Users\rvmzk\Desktop\projectAnti\WebPlanner\frontend"
        ]:
            if os.path.exists(wp_candidate):
                try:
                    import shutil
                    shutil.copy(matrix_path, os.path.join(wp_candidate, "matrix.html"))
                    preview_url = f"{self.config.vk.server_base_url}/static/matrix.html"
                    logger.info(f"[Pipeline] Published matrix to WebPlanner live preview: {preview_url}")
                    break
                except Exception as e:
                    logger.warning(f"[Pipeline] Could not copy matrix to WebPlanner: {e}")

        self.memory.log_stage_metric(session_id, "5_Concept_Facades_Matrix", (time.time() - t_facades) * 1000)

        # [HITL CHECKPOINT]: Human-in-the-Loop Concept Selection (VK + CLI)
        selected_concept = None
        user_feedback = None

        if forced_concept_id:
            c_norm = f"concept_{forced_concept_id}" if str(forced_concept_id).isdigit() else str(forced_concept_id).lower()
            selected_concept = next((c for c in concepts if c.get("id") == c_norm or str(forced_concept_id).lower() in c.get("name", "").lower()), None)
            if not selected_concept and concepts:
                selected_concept = concepts[3] if len(concepts) > 3 else concepts[0]
            logger.info(f"[Pipeline HITL] Explicitly locked concept: {selected_concept.get('name')} ({selected_concept.get('id')})")
            if self.config.vk.enabled and self.vk_dispatcher.vk:
                self.vk_dispatcher.send_text(
                    f"🚀 AI-Завод зафиксировал концепт: «{selected_concept.get('name')}»!\n"
                    f"Запуск сборки: Архитектура -> Backend -> Frontend -> Playwright UI Тестирование.",
                    peer_id=self.config.vk.default_peer_id
                )
        elif self.config.vk.enabled and self.vk_dispatcher.vk:
            # 1. VK Dispatch: Send 5 sites and inline keyboard to VK
            logger.info(f">>> [Stage 1.5] 📱 VK HITL Dispatcher: Sending 5 concepts and keyboard to VK (peer_id={self.config.vk.default_peer_id})...")
            vk_ok, vk_msg_id = self.vk_dispatcher.send_concepts_to_vk(
                session_id=session_id,
                prd_spec=prd_spec,
                concepts=concepts,
                preview_url=preview_url,
                peer_id=self.config.vk.default_peer_id
            )
            if vk_ok:
                logger.info(">>> [Stage 1.5] ⏳ Waiting up to 180s for user choice in VK (tap button or send 1..5 in chat)...")
                vk_sel, vk_feed = self.vk_dispatcher.wait_for_vk_selection(
                    peer_id=self.config.vk.default_peer_id,
                    last_msg_id=vk_msg_id,
                    timeout_sec=180.0,
                    concepts=concepts
                )
                if vk_sel:
                    selected_concept = vk_sel
                    user_feedback = vk_feed
                    logger.info(f"[VKHITL] Successfully captured choice from VK: {selected_concept.get('name')}")

        # 2. Fallback to CLI or AutoMode if VK was skipped or timed out
        if not selected_concept:
            if not is_auto:
                selected_concept, user_feedback = prompt_cli_selection(
                    concepts, prd_spec, matrix_path, default_id=prd_spec.get("recommended_archetype_id")
                )
            else:
                dominant_pref = self.memory.get_dominant_preference()
                match = next((c for c in concepts if c.get("name") == dominant_pref or c.get("aesthetic_archetype") == dominant_pref), None)
                selected_concept = match or next((c for c in concepts if c.get("id") == prd_spec.get("recommended_archetype_id")), concepts[0])
                user_feedback = None
                logger.info(f"[AutoMode] Automatically selected concept based on preference history / PM recommendation: {selected_concept.get('name')}")

        # State Injection & SQLite Preference Store
        self.memory.record_concept_decision(
            session_id=session_id,
            prompt=goal_prompt,
            chosen_concept_id=selected_concept.get("id", "concept_3"),
            chosen_archetype_name=selected_concept.get("name", "Executive Monolith"),
            competitor_benchmark=selected_concept.get("benchmark", ""),
            cognitive_law=selected_concept.get("cognitive_law", ""),
            user_feedback=user_feedback or "",
            all_concepts=concepts
        )
        design_spec = self.designer.lock_concept_to_design_spec(session_id, selected_concept, prd_spec)
        prd_spec["selected_archetype"] = selected_concept
        if user_feedback:
            prd_spec["user_hybrid_feedback"] = user_feedback
            enhanced_prompt += f"\n\n[USER HYBRID SPECIFICATION]: {user_feedback}"

        # Stage 2: System Architecture & OpenAPI Design for the Selected Concept
        t_arch = time.time()
        logger.info(f">>> [Stage 2] 📐 Architect: Designing DDL & API for Approved Concept ({selected_concept.get('name')})...")
        arch_prompt = f"Goal: {goal_prompt}\nSelected Concept: {selected_concept['name']} ({selected_concept.get('benchmark')})\nWedge: {selected_concept.get('wedge')}\nPRD: {prd_spec}"
        arch_spec = self.architect.design_architecture(session_id, arch_prompt)

        des_tasks = design_spec.get("tasks_checklist", [])
        arch_tasks = arch_spec.get("tasks_checklist", [])
        session_tasks_matrix.extend(des_tasks + arch_tasks)
        self._log_tasks_matrix("Designer (HITL Approved)", des_tasks)
        self._log_tasks_matrix("Architect", arch_tasks)
        self.memory.log_stage_metric(session_id, "Architect_Design", (time.time() - t_arch) * 1000)

        if not target_dir_name and (arch_spec.get("project_name") or prd_spec.get("product_name")):
            actual_slug = arch_spec.get("project_name") or prd_spec.get("product_name")
            new_target = os.path.join(self.config.workspace_root, actual_slug)
            if new_target != target_dir:
                os.rename(target_dir, new_target)
                target_dir = new_target
                self.mcp.workspace_root = target_dir

        # [CHECKPOINT 2]: Architecture & DDL Review (if not in auto_mode)
        if not is_auto:
            chk2_res = chk_handler("checkpoint_architecture", arch_spec)
            if chk2_res.get("feedback"):
                arch_spec["developer_override"] = chk2_res["feedback"]

        # Stage 3: Full Parallel Code Generation DAG (4 Agents simultaneously: Backend, Frontend, QA, DevOps)
        logger.info(f">>> [Stage 3] ⚡ Full Parallel Code DAG (4 Agents): Backend || Frontend || QA Matrix || DevOps in {target_dir}...")
        merged_front_spec = {**arch_spec, "design_system": design_spec.get("design_system", {})}
        t_par2 = time.time()
        
        with ThreadPoolExecutor(max_workers=2) as executor:
            fut_back = executor.submit(self.backend.generate_backend, session_id, arch_spec, target_dir)
            fut_devops = executor.submit(self.devops.generate_infrastructure, session_id, arch_spec, target_dir)
            backend_result = fut_back.result()
            devops_result = fut_devops.result()
            
            fut_front = executor.submit(self.frontend.generate_frontend, session_id, merged_front_spec, target_dir)
            fut_qa = executor.submit(self.qa_security.audit_and_generate_tests, session_id, arch_spec, {}, target_dir)
            frontend_result = fut_front.result()
            qa_result = fut_qa.result()

        be_tasks = backend_result.get("tasks_checklist", [])
        fe_tasks = frontend_result.get("tasks_checklist", [])
        session_tasks_matrix.extend(be_tasks + fe_tasks)
        self._log_tasks_matrix("Backend", be_tasks)
        self._log_tasks_matrix("Frontend", fe_tasks)
            
        self.memory.log_stage_metric(session_id, "Full_Parallel_CodeGen_DAG", (time.time() - t_par2) * 1000)

        # [CHECKPOINT 3]: Code Review before Verification (if not in auto_mode)
        if not is_auto:
            chk_handler("checkpoint_code", {"target_dir": target_dir, "backend": backend_result, "frontend": frontend_result})

        # Stage 4: Self-Healing & Verification
        logger.info(">>> [Stage 4] 🔄 Self-Healing: Running Static Verification & Self-Correction Loop...")
        healing_result = self.self_healing.repair_if_needed(
            session_id=session_id,
            target_dir=target_dir,
            arch_spec=arch_spec
        )

        # Stage 4.5 & 5: Autonomous Multi-Cycle Remediation Loop
        max_remediation_cycles = 3
        current_cycle = 1
        ui_test_report = {}
        signoff = {}

        while current_cycle <= max_remediation_cycles:
            logger.info(f">>> [Stage 4.5 - Cycle {current_cycle}/{max_remediation_cycles}] 🧪 UI Tester: Auditing all buttons, modals, forms & interactive flows...")
            t_ui = time.time()
            ui_test_report = self.ui_tester.test_ui_interactions(
                session_id=session_id,
                target_dir=target_dir,
                frontend_files=frontend_result.get("files", []),
                backend_files=backend_result.get("files", [])
            )
            uit_tasks = ui_test_report.get("tasks_checklist", [])
            self._log_tasks_matrix(f"UI Tester (Cycle {current_cycle})", uit_tasks)
            self.memory.log_stage_metric(session_id, f"UITester_Cycle_{current_cycle}", (time.time() - t_ui) * 1000)

            logger.info(f">>> [Stage 5 - Cycle {current_cycle}/{max_remediation_cycles}] 🍊 TeamLead: Conducting Release Review & Sign-Off...")
            t_sign = time.time()
            signoff = self.teamlead.review_and_signoff(
                session_id=session_id,
                arch_spec=arch_spec,
                verification_summary=healing_result["verification"],
                target_dir=target_dir,
                ui_tester_report=ui_test_report,
                task_matrix=session_tasks_matrix
            )
            tl_sign_tasks = signoff.get("tasks_checklist", [])
            self._log_tasks_matrix(f"TeamLead Sign-Off (Cycle {current_cycle})", tl_sign_tasks)
            self.memory.log_stage_metric(session_id, f"TeamLead_Signoff_Cycle_{current_cycle}", (time.time() - t_sign) * 1000)

            # Check for failed tasks
            failed_tasks = [t for t in (session_tasks_matrix + uit_tasks) if t.get("status") == "FAILED"]
            ui_passed = ui_test_report.get("test_status") == "PASSED"
            teamlead_approved = "APPROVED" in signoff.get("release_status", "")

            if not failed_tasks and ui_passed and teamlead_approved:
                logger.info(f"🎉 [Autonomous Loop] All checks PASSED and APPROVED on Cycle {current_cycle}! Project completed successfully.")
                break

            if current_cycle >= max_remediation_cycles:
                logger.warning(f"[Autonomous Loop] Max remediation cycles ({max_remediation_cycles}) reached. Proceeding to finalize.")
                break

            # Escalate failed tasks to TeamLead for remediation plan
            logger.warning(f"⚠️ [Autonomous Loop - Sprint {current_cycle}] Found {len(failed_tasks)} failed task(s) or UI issues. Dispatching TeamLead remediation...")
            remediation_plan = self.teamlead.formulate_remediation(
                session_id=session_id,
                failed_tasks=failed_tasks,
                context={"ui_report": ui_test_report, "arch": arch_spec}
            )
            target_agent = remediation_plan.get("target_agent", "Frontend")
            instruction = remediation_plan.get("instruction", "Fix identified defects.")

            logger.info(f"[TeamLead Directive] Target Agent: {target_agent} | Directive: {instruction}")

            if "Frontend" in target_agent:
                logger.info(f">>> [Remediation Cycle {current_cycle}] 💻 Frontend: Re-building UI according to TeamLead directive...")
                frontend_result = self.frontend.generate_frontend(
                    session_id=session_id,
                    arch_spec=merged_front_spec,
                    target_dir=target_dir,
                    remediation_instruction=instruction
                )

            if "Backend" in target_agent:
                logger.info(f">>> [Remediation Cycle {current_cycle}] ⚙️ Backend: Re-building API according to TeamLead directive...")
                backend_result = self.backend.generate_backend(
                    session_id=session_id,
                    arch_spec=arch_spec,
                    target_dir=target_dir,
                    remediation_instruction=instruction
                )

            # Re-run static verification & self-healing
            logger.info(f">>> [Remediation Cycle {current_cycle}] 🔄 Re-running static verification & self-healing...")
            healing_result = self.self_healing.repair_if_needed(
                session_id=session_id,
                target_dir=target_dir,
                arch_spec=arch_spec
            )

            current_cycle += 1

        total_duration = round(time.time() - start_time, 2)
        final_passed = healing_result["verification"].get("all_passed", False) and ui_test_report.get("test_status") == "PASSED"
        self.memory.update_session_status(session_id, "completed" if final_passed else "warnings")

        logger.info(f"=== [AI-Zavod] TeamLead Sign-Off: {signoff.get('release_status')}. Total Wall-Clock: {total_duration}s ===")

        return {
            "session_id": session_id,
            "duration_seconds": total_duration,
            "target_dir": target_dir,
            "auto_mode": is_auto,
            "teamlead": {
                "sprint_plan": sprint_plan,
                "signoff": signoff
            },
            "prd": prd_spec,
            "design": design_spec,
            "architecture": arch_spec,
            "backend": backend_result,
            "frontend": frontend_result,
            "qa": qa_result,
            "devops": devops_result,
            "ui_tester": ui_test_report,
            "tasks_matrix": session_tasks_matrix,
            "self_healing": healing_result,
            "verification": healing_result["verification"],
            "summary": self.memory.get_session_summary(session_id)
        }
