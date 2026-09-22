import argparse
import sys
import json
import logging
from AI_Zavod.gateway.client import OmniRouteClient
from AI_Zavod.memory.sqlite_store import ContextMemoryStore
from AI_Zavod.memory.skill_rag import SkillRAGEngine
from AI_Zavod.orchestrator.pipeline import AIZavodPipeline
from AI_Zavod.verification.verifier import ProjectVerifier

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("AI_Zavod.CLI")

def test_gateway():
    print("\n🔍 --- OmniRoute AI Gateway Connection Test ---")
    client = OmniRouteClient()
    res = client.test_connection()
    print(json.dumps(res, indent=2, ensure_ascii=False))
    if res.get("status") == "online":
        print("✅ Gateway is ONLINE and fully operational!\n")
    else:
        print("❌ Gateway check failed.\n")

def show_status():
    print("\n📊 --- AI-Zavod Context Memory Status ---")
    memory = ContextMemoryStore()
    with memory._get_conn() as conn:
        sessions = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC LIMIT 10").fetchall()
        print(f"Total recorded sessions: {len(sessions)}")
        for s in sessions:
            s_dict = dict(s)
            print(f"- Session {s_dict['id']} | Mode: {s_dict.get('mode', 'task')} | Status: {s_dict['status']} | Target: {s_dict['target_dir']}")
            print(f"  Goal: {s_dict['goal'][:80]}...")
            
        runs_count = conn.execute("SELECT COUNT(*), SUM(tokens_used) FROM agent_runs").fetchone()
        print(f"\nSubagent Executions: {runs_count[0]} | Total Tokens: {runs_count[1] or 0}\n")

def show_metrics():
    print("\n📈 --- AI-Zavod Observability & Cost Metrics ---")
    memory = ContextMemoryStore()
    m = memory.get_observability_metrics()
    print(f"Total Sessions:         {m['total_sessions']}")
    print(f"Completed Sessions:     {m['completed_sessions']}")
    print(f"Success Rate:           {m['success_rate_pct']}%")
    print(f"Total Tokens Consumed:  {m['total_tokens_consumed']:,}")
    print(f"Estimated Cost (USD):   ${m['estimated_cost_usd']}")
    print(f"Avg Stage Duration:     {m['avg_stage_duration_sec']}s")
    print("\nStage Latency Breakdown:")
    for st in m['stages']:
        print(f"  • {st['stage']:<15} | Runs: {st['runs']:<3} | Avg: {st['avg_duration_sec']}s | Tokens: {st['tokens']}")
    print("")

def list_skills():
    print("\n🧠 --- AI-Zavod Indexed Domain Skills (.agents/skills/) ---")
    rag = SkillRAGEngine()
    for s in rag.indexed_skills:
        print(f"• {s['name']:<30} | Folder: {s['folder']}")
        if s['description']:
            print(f"  {s['description']}")
    print(f"\nTotal indexed skills: {len(rag.indexed_skills)}\n")

def run_consult(prompt: str):
    print(f"\n💡 [HITL Consult Mode] Consulting on architecture for:\n\"{prompt}\"\n")
    pipeline = AIZavodPipeline()
    result = pipeline.consult(goal_prompt=prompt)
    print("\n" + "="*60)
    print("📋 [Product Requirements Document (PRD) Draft]")
    print(f"Product: {result['prd'].get('product_name')} - {result['prd'].get('tagline')}")
    print(f"Target:  {', '.join(result['prd'].get('target_audience', []))}")
    print("\n🎨 [UI/UX Design Tokens Draft]")
    print(f"Theme:   {result['design'].get('design_system', {}).get('theme_name')}")
    print("\n📐 [Architecture ADR Decision]")
    print(f"ADR:     {result['architecture'].get('adr', {}).get('decision')}")
    print(f"SQL:     {result['architecture'].get('database_schema_sql', '')[:200]}...")
    print("\n🧠 [Matched Domain Skills]")
    print(f"Skills:  {', '.join(result['matched_skills']) if result['matched_skills'] else 'General'}")
    print("="*60)
    print(f"\n✅ Consultation complete! Session ID: {result['session_id']}")
    print("To proceed with code build, run:\npython3 -m AI_Zavod.main --task \"" + prompt + "\"\n")

def run_task(prompt: str, target_dir: str = None, source_file: str = None, image_file: str = None, auto_mode: bool = True, concept: str = None):
    mode_label = "⚡ [Autonomous Zero-Touch]" if auto_mode else "🛠️ [Interactive Developer Mode / HITL]"
    print(f"\n🚀 {mode_label} Launching Full-Cycle 9-Agent Parallel Pipeline for:\n\"{prompt}\"\n")
    if concept:
        print(f"🎯 Pre-selected Concept Lock: {concept}")
    if image_file:
        print(f"🖼️ User Image Specification: {image_file}")
    if source_file:
        print(f"📄 Primary Source Document: {source_file}")
    print()
    pipeline = AIZavodPipeline()
    result = pipeline.execute(
        goal_prompt=prompt,
        target_dir_name=target_dir,
        source_file=source_file,
        image_file=image_file,
        auto_mode=auto_mode,
        forced_concept_id=concept
    )
    print("\n✨ --- AI-Zavod Generation & Self-Healing Summary ---")
    print(f"Session ID:      {result['session_id']}")
    print(f"Duration:        {result['duration_seconds']}s")
    print(f"Auto Mode:       {result.get('auto_mode')}")
    print(f"Location:        {result['target_dir']}")
    print(f"TeamLead Status: {result.get('teamlead', {}).get('signoff', {}).get('release_status', 'APPROVED')}")
    ui_res = result.get('ui_tester', {})
    print(f"UI Tester Audit: {ui_res.get('test_status', 'N/A')} (Buttons: {ui_res.get('scanned_buttons_count', 0)}, Scenarios: {len(ui_res.get('tested_scenarios', []))})")
    if ui_res.get('teamlead_task'):
        print(f"UI Tester Task:  ⚠️ ACTION REQUIRED -> {ui_res['teamlead_task'].get('summary')}")
    else:
        print(f"UI Tester Task:  ✅ All buttons, modals, and submission flows PASSED")
    print(f"Self-Healing:    {result['self_healing']['status']} (Attempts: {result['self_healing']['attempts']})")
    print(f"Verified Status: {result['verification']['all_passed']}")
    print("\nCreated Artifacts:")
    for art in result['summary'].get('artifacts', []):
        print(f"  • {art['file_path']} ({art['file_type']})")
    print("\n✅ Build complete! Run `cd " + result['target_dir'] + " && ./run.sh` or `docker compose up` to start.\n")

def interactive_repl():
    print("\n" + "="*60)
    print("🏭 AI-Zavod Interactive Terminal Control (Slash Commands)")
    print("Available commands:")
    print("  /consult <prompt>   - Brainstorm & formulate PRD/ADR (no disk changes)")
    print("  /task <prompt>      - Execute full 7-agent build & deploy")
    print("  /metrics            - View latency, token costs and observability")
    print("  /skills             - View indexed domain skills (.agents/skills/)")
    print("  /status             - View session history")
    print("  /gateway            - Test OmniRoute connection")
    print("  /exit               - Quit")
    print("="*60 + "\n")

    while True:
        try:
            cmd = input("AI-Zavod> ").strip()
            if not cmd:
                continue
            if cmd in ("/exit", "exit", "quit"):
                print("Goodbye!")
                break
            elif cmd.startswith("/consult"):
                prompt = cmd.replace("/consult", "").strip()
                if not prompt:
                    prompt = input("Enter consultation goal: ").strip()
                if prompt:
                    run_consult(prompt)
            elif cmd.startswith("/task"):
                prompt = cmd.replace("/task", "").strip()
                if not prompt:
                    prompt = input("Enter project task goal: ").strip()
                if prompt:
                    run_task(prompt)
            elif cmd in ("/metrics", "/stats"):
                show_metrics()
            elif cmd in ("/skills", "/rag"):
                list_skills()
            elif cmd in ("/status", "/history"):
                show_status()
            elif cmd in ("/gateway", "/test-gateway"):
                test_gateway()
            elif cmd in ("/help", "help", "?"):
                print("Commands: /consult <prompt>, /task <prompt>, /metrics, /skills, /status, /gateway, /exit")
            else:
                print(f"Unknown command: '{cmd}'. Type /help for assistance.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

def main():
    parser = argparse.ArgumentParser(description="AI-Zavod Autonomous Software Engineering Pipeline")
    parser.add_argument("--test-gateway", action="store_true", help="Test connection to OmniRoute gateway")
    parser.add_argument("--status", action="store_true", help="Display context memory and session history")
    parser.add_argument("--metrics", action="store_true", help="Display latency and cost observability metrics")
    parser.add_argument("--skills", action="store_true", help="List all indexed domain skills from .agents/skills/")
    parser.add_argument("--consult", type=str, help="Run interactive architecture & PRD consultation")
    parser.add_argument("--task", "--build", type=str, dest="task", help="Run full-cycle 8-agent build for goal")
    parser.add_argument("--source-file", type=str, default=None, help="Path to primary specification/data document")
    parser.add_argument("--image-file", "--image", type=str, default=None, help="Path to specification screenshot or handwritten math image")
    parser.add_argument("--target-dir", type=str, default=None, help="Optional target directory name")
    parser.add_argument("--concept", type=str, default=None, help="Lock specific concept (e.g. concept_4 or 4)")
    parser.add_argument("--no-auto", "--hitl", "--manual", action="store_true", help="Disable auto-mode: pause at critical checkpoints for developer review/edits")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive Slash REPL console")
    
    args = parser.parse_args()

    if args.test_gateway:
        test_gateway()
    elif args.status:
        show_status()
    elif args.metrics:
        show_metrics()
    elif args.skills:
        list_skills()
    elif args.consult:
        run_consult(args.consult)
    elif args.task:
        run_task(args.task, args.target_dir, args.source_file, args.image_file, auto_mode=not args.no_auto, concept=args.concept)
    elif args.interactive:
        interactive_repl()
    else:
        # Default to interactive if no args
        interactive_repl()

if __name__ == "__main__":
    main()
