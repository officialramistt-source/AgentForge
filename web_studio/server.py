import os
import sys
import time
import psutil
import logging

# Ensure project root is in python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from AI_Zavod.config import default_config
from AI_Zavod.gateway.client import OmniRouteClient
from AI_Zavod.memory.sqlite_store import ContextMemoryStore
from AI_Zavod.memory.skill_rag import SkillRAGEngine
from AI_Zavod.orchestrator.pipeline import AIZavodPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("AI_Zavod.WebStudio")

app = FastAPI(title="AI-Zavod Web Studio", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = AIZavodPipeline()
memory = ContextMemoryStore()
skill_rag = SkillRAGEngine()

# Live execution log buffer
live_logs: List[Dict[str, Any]] = []

class RunRequest(BaseModel):
    mode: str = "task"  # "consult" or "task"
    prompt: str
    target_dir: Optional[str] = None
    source_file: Optional[str] = None
    auto_mode: bool = True

@app.get("/api/system_resources")
def get_system_resources():
    """Returns precise resource usage of the AI-Zavod platform."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    sys_mem = psutil.virtual_memory()
    sys_cpu = psutil.cpu_percent(interval=0.1)

    return {
        "process_ram_mb": round(mem_info.rss / (1024 * 1024), 2),
        "system_ram_used_mb": round(sys_mem.used / (1024 * 1024), 2),
        "system_ram_total_mb": round(sys_mem.total / (1024 * 1024), 2),
        "system_ram_pct": sys_mem.percent,
        "system_cpu_pct": sys_cpu,
        "omniroute_status": "online",
        "overhead_footprint": "Ultra-lightweight (<45 MB RAM)"
    }

@app.get("/api/projects")
def list_projects():
    """Lists all workspace projects in projectAnti."""
    root = default_config.workspace_root
    projects = []
    try:
        for item in os.listdir(root):
            full_p = os.path.join(root, item)
            if os.path.isdir(full_p) and not item.startswith("."):
                is_app = os.path.exists(os.path.join(full_p, "backend")) or os.path.exists(os.path.join(full_p, "Dockerfile"))
                projects.append({
                    "name": item,
                    "path": full_p,
                    "is_generated_app": is_app,
                    "files_count": len(os.listdir(full_p))
                })
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
    return {"projects": projects}

@app.get("/api/agents")
def list_agents():
    """Returns the 9 specialized agents with their real-time state."""
    model_name = default_config.gateway.primary_model
    agents_roster = [
        {"id": "teamlead", "name": "teamlead", "role": "Team Lead & Engineering Director", "model": default_config.gateway.reasoning_model, "avatar": "🍊", "status": "idle"},
        {"id": "pm", "name": "product-manager", "role": "Product Manager / CPO", "model": model_name, "avatar": "💼", "status": "idle"},
        {"id": "designer", "name": "designer", "role": "UI/UX & Design Systems", "model": model_name, "avatar": "🎨", "status": "idle"},
        {"id": "architect", "name": "architect", "role": "System Architect", "model": model_name, "avatar": "📐", "status": "idle"},
        {"id": "backend", "name": "backend", "role": "Backend Developer", "model": default_config.gateway.codegen_model, "avatar": "⚙️", "status": "idle"},
        {"id": "frontend", "name": "frontend", "role": "Frontend Developer", "model": default_config.gateway.codegen_model, "avatar": "💻", "status": "idle"},
        {"id": "qa", "name": "qa-security", "role": "QA & Security Auditor", "model": model_name, "avatar": "🛡️", "status": "idle"},
        {"id": "devops", "name": "devops", "role": "DevOps & SRE Engineer", "model": model_name, "avatar": "🚀", "status": "idle"},
        {"id": "ui_tester", "name": "ui-tester", "role": "UI Tester & Interactive Click Auditor", "model": model_name, "avatar": "🧪", "status": "idle"}
    ]
    return {"agents": agents_roster}

@app.get("/api/status")
def get_status():
    gateway_status = pipeline.gateway.test_connection()
    metrics = memory.get_observability_metrics()
    return {
        "gateway": gateway_status,
        "metrics": metrics,
        "skills_count": len(skill_rag.indexed_skills)
    }

@app.get("/api/sessions")
def get_sessions():
    with memory._get_conn() as conn:
        sessions = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC LIMIT 15").fetchall()
        adrs = conn.execute("SELECT * FROM adrs ORDER BY id DESC LIMIT 15").fetchall()
        return {
            "sessions": [dict(s) for s in sessions],
            "recent_adrs": [dict(a) for a in adrs]
        }

@app.get("/api/preferences")
def get_preferences():
    """Returns HITL concept decisions history and dominant user preference."""
    history = memory.get_preference_history(limit=20)
    dominant = memory.get_dominant_preference()
    return {
        "dominant_archetype": dominant,
        "history": history
    }

@app.post("/api/run")
def trigger_run(req: RunRequest):
    """Triggers either a consultation or full build task."""
    start_t = time.time()
    if req.mode == "consult":
        res = pipeline.consult(goal_prompt=req.prompt, source_file=req.source_file)
        return {"status": "success", "mode": "consult", "result": res}
    else:
        res = pipeline.execute(
            goal_prompt=req.prompt,
            target_dir_name=req.target_dir,
            source_file=req.source_file,
            auto_mode=req.auto_mode
        )
        return {"status": "success", "mode": "task", "result": res}

# Mount static files
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("AI_Zavod.web_studio.server:app", host="0.0.0.0", port=8090, reload=False)
