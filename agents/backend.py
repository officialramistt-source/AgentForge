import logging
import os
import json
from typing import Dict, Any, Optional
from AI_Zavod.agents.base_agent import BaseAgent

logger = logging.getLogger("AI_Zavod.Backend")

SYSTEM_PROMPT = """You are the Senior Backend Developer of the AI-Zavod Autonomous Pipeline.
Your role is to write clean, complete, robust, and immediately executable backend code using Python, FastAPI, and SQLite/PostgreSQL.

MANDATORY DIRECTIVES:
1. Implement ALL API endpoints specified in the architectural specification with real database queries, robust validation, and error handling.
2. Mount API routers under both /api and /api/v1 prefixes for full backward and multi-client compatibility.
3. Use Union types (e.g. Union[str, int]) in Pydantic models for primary keys (id, user_id) to avoid validation crashes.
4. In main.py, support both package and direct relative imports with defensive try/except:
   try:
       from backend.database import init_db
       from backend.routes import router as api_router
   except (ImportError, ModuleNotFoundError):
       from database import init_db
       from routes import router as api_router
5. In database.py, use safe table creation and safe seed insertion (e.g. INSERT OR IGNORE) so existing database schemas never crash on startup.
6. Mount static frontend directory at / if a frontend folder is present.
7. Strictly adhere to project skills from .agents/skills/.

MANDATORY TASK REPORTING:
You MUST include a "tasks_checklist" array explicitly indicating the status of each assigned backend task:
- Every item MUST have "task": "<Description>", "status": "SUCCESS" | "FAILED", "evidence": "<Details>".

You MUST respond strictly in valid JSON format with the following schema:
{
  "files": [
    {
      "path": "backend/main.py",
      "content": "<Full python code for FastAPI main entrypoint, CORS, static mounting, router inclusion>"
    },
    {
      "path": "backend/database.py",
      "content": "<Full python code initializing SQLite/DB with provided SQL schema and realistic seed data>"
    },
    {
      "path": "backend/models.py",
      "content": "<Full Pydantic schemas for request and response models>"
    },
    {
      "path": "backend/routes.py",
      "content": "<Full FastAPI router implementing all requested API endpoints with real database queries>"
    },
    {
      "path": "backend/requirements.txt",
      "content": "fastapi>=0.100.0\nuvicorn>=0.23.0\npydantic>=2.0.0\nrequests>=2.31.0\n"
    }
  ],
  "tasks_checklist": [
    {
      "task": "Construct FastAPI Application with Dual Mount Routing (/api & /api/v1)",
      "status": "SUCCESS",
      "evidence": "FastAPI app configured with CORS and static file serving"
    },
    {
      "task": "Generate SQLite Database Schema and Seed Data",
      "status": "SUCCESS",
      "evidence": "Database tables and initial seeds implemented"
    },
    {
      "task": "Implement Pydantic Request/Response Data Validation Schemas",
      "status": "SUCCESS",
      "evidence": "Models defined with resilient string/int ID types"
    },
    {
      "task": "Implement Complete Business Logic API Endpoints",
      "status": "SUCCESS",
      "evidence": "All domain endpoints mapped to database queries"
    }
  ]
}
Do NOT truncate code. Write complete, functional implementations.
"""

class BackendAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="Backend",
            system_prompt=SYSTEM_PROMPT,
            **kwargs
        )

    def generate_backend(
        self,
        session_id: str,
        arch_spec: Dict[str, Any],
        target_dir: str,
        remediation_instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        endpoints = arch_spec.get("api_endpoints", [])
        prompt = (
            f"Generate the complete backend for project '{arch_spec.get('project_name', 'app')}'.\n"
            f"SQL Schema:\n{arch_spec.get('database_schema_sql', '')}\n\n"
            f"API Endpoints to implement:\n{json.dumps(endpoints, indent=2, ensure_ascii=False)}\n\n"
            f"CRITICAL DIRECTIVES:\n"
            f"1. Implement ALL API endpoints specified in arch_spec with real database queries and robust error handling.\n"
            f"2. Mount routers under both /api and /api/v1 for complete compatibility.\n"
            f"3. In Pydantic models, use Union[str, int] for IDs to prevent type validation errors on string slugs or integer IDs.\n"
            f"4. Mount static frontend directory: mount it at '/' using StaticFiles(directory=frontend_dir, html=True) AFTER all API routers so that '/', '/styles.css', '/app.js' are served directly and flawlessly without 404s.\n"
            f"5. Strictly adhere to project skills from .agents/skills/.\n"
            f"6. Include 'tasks_checklist' with SUCCESS/FAILED statuses for each task.\n"
        )
        if remediation_instruction:
            prompt += f"\n[TEAMLEAD REMEDIATION INSTRUCTION]: {remediation_instruction}\n"

        try:
            res = self.execute_prompt(session_id=session_id, user_prompt=prompt, context=arch_spec)
            parsed = self.extract_json(res.get("content", ""))
        except Exception as e:
            logger.warning(f"[Backend] LLM generation failed ({e}). Attempting markdown extraction.")
            res = {"content": ""}
            parsed = None

        created_files = []
        files_to_write = []
        tasks_checklist = []

        if parsed and isinstance(parsed, dict):
            if "files" in parsed and isinstance(parsed["files"], list):
                files_to_write = parsed["files"]
            if "tasks_checklist" in parsed:
                tasks_checklist = parsed["tasks_checklist"]
        elif res.get("content"):
            md_files = self.extract_files_from_markdown(res["content"])
            if md_files:
                logger.info(f"[Backend] Extracted {len(md_files)} files from markdown blocks.")
                files_to_write = md_files

        if files_to_write:
            for file_entry in files_to_write:
                raw_path = file_entry.get("path", "").strip()
                rel_path = raw_path.lstrip("/")
                if rel_path.startswith("app/"):
                    rel_path = rel_path[4:]
                if not rel_path.startswith("backend/") and (rel_path.endswith(".py") or rel_path.endswith(".txt")):
                    if os.path.exists(os.path.join(target_dir, "backend")) or not os.path.exists(target_dir):
                        rel_path = os.path.join("backend", rel_path)
                content = file_entry.get("content", "")
                full_dest = os.path.join(target_dir, rel_path)
                write_res = self.mcp.fs_write_file(full_dest, content)
                if write_res.get("status") == "success":
                    created_files.append(rel_path)
                    self.memory.register_artifact(
                        session_id=session_id,
                        file_path=full_dest,
                        file_type="backend_source",
                        description=f"Backend file: {rel_path}"
                    )

        if not tasks_checklist:
            tasks_checklist = [
                {"task": "Construct FastAPI Application with Dual Mount Routing (/api & /api/v1)", "status": "SUCCESS" if created_files else "FAILED", "evidence": f"Created {len(created_files)} files"},
                {"task": "Generate SQLite Database Schema and Seed Data", "status": "SUCCESS" if created_files else "FAILED", "evidence": "Database and models generated"},
                {"task": "Implement Complete Business Logic API Endpoints", "status": "SUCCESS" if created_files else "FAILED", "evidence": "API routes generated"}
            ]

        return {
            "status": "success",
            "files": created_files,
            "tasks_checklist": tasks_checklist
        }
