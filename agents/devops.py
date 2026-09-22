import logging
import os
import json
from typing import Dict, Any, Optional
from AI_Zavod.agents.base_agent import BaseAgent

logger = logging.getLogger("AI_Zavod.DevOps")

SYSTEM_PROMPT = """You are the Senior DevOps & Site Reliability Engineer of the AI-Zavod Autonomous Pipeline.
Your role is to containerize the application, generate production-ready Dockerfile, docker-compose.yml, Nginx reverse proxy configuration, and launch scripts.

You MUST respond strictly in valid JSON format with the following schema:
{
  "files": [
    {
      "path": "Dockerfile",
      "content": "<Production multi-stage Dockerfile for Python/FastAPI app>"
    },
    {
      "path": "docker-compose.yml",
      "content": "<docker-compose file defining web service, environment, ports, and volumes>"
    },
    {
      "path": "nginx.conf",
      "content": "<Nginx reverse proxy configuration with TLS/Let's Encrypt support and static caching>"
    },
    {
      "path": "run.sh",
      "content": "<Bash start script to setup venv, install requirements and launch uvicorn locally>"
    }
  ]
}
Do NOT truncate code. Write complete, functional implementations.
"""

class DevOpsAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(
            role="DevOps",
            system_prompt=SYSTEM_PROMPT,
            **kwargs
        )

    def generate_infrastructure(self, session_id: str, arch_spec: Dict[str, Any], target_dir: str) -> Dict[str, Any]:
        prompt = (
            f"Generate Docker, Docker Compose, Nginx, and launch configurations for project '{arch_spec.get('project_name', 'app')}'.\n"
            f"Tech Stack: {json.dumps(arch_spec.get('tech_stack', {}), indent=2)}\n\n"
            f"Requirements:\n"
            f"1. Dockerfile running Python 3.11-slim with uvicorn on port 8000.\n"
            f"2. docker-compose.yml with healthcheck, volume mounts for persistent data, and port mapping 8000:8000.\n"
            f"3. Nginx reverse proxy config forwarding /api to backend and serving / with caching.\n"
            f"4. run.sh script making it 1-click runnable on Linux."
        )

        try:
            res = self.execute_prompt(session_id=session_id, user_prompt=prompt, context=arch_spec)
            parsed = self.extract_json(res.get("content", ""))
        except Exception as e:
            logger.warning(f"[DevOps] LLM call failed or rate limited ({e}). Using robust DevOps fallback templates.")
            parsed = None

        created_files = []
        if parsed and "files" in parsed:
            for file_entry in parsed["files"]:
                raw_path = file_entry.get("path", "").strip()
                # Normalize path: remove leading slashes and app/ prefixes
                rel_path = raw_path.lstrip("/")
                if rel_path.startswith("app/"):
                    rel_path = rel_path[4:]
                content = file_entry.get("content", "")
                full_dest = os.path.join(target_dir, rel_path)
                write_res = self.mcp.fs_write_file(full_dest, content)
                if write_res.get("status") == "success":
                    created_files.append(rel_path)
                    self.memory.register_artifact(
                        session_id=session_id,
                        file_path=full_dest,
                        file_type="devops_config",
                        description=f"DevOps infrastructure: {rel_path}"
                    )
        else:
            logger.warning("[DevOps] Fallback infrastructure generation initiated.")
            dockerfile_content = """FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend /app/backend
COPY frontend /app/frontend
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
            compose_content = """version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
"""
            nginx_content = """events { worker_connections 1024; }
http {
    include /etc/nginx/mime.types;
    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://web:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
"""
            run_sh_content = """#!/usr/bin/env bash
set -e
echo "🚀 Starting AI-Zavod generated application..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r backend/requirements.txt
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
            self.mcp.fs_write_file(os.path.join(target_dir, "Dockerfile"), dockerfile_content)
            self.mcp.fs_write_file(os.path.join(target_dir, "docker-compose.yml"), compose_content)
            self.mcp.fs_write_file(os.path.join(target_dir, "nginx.conf"), nginx_content)
            self.mcp.fs_write_file(os.path.join(target_dir, "run.sh"), run_sh_content)
            os.chmod(os.path.join(target_dir, "run.sh"), 0o755)
            created_files = ["Dockerfile", "docker-compose.yml", "nginx.conf", "run.sh"]

        # Validate Docker configuration
        df_path = os.path.join(target_dir, "Dockerfile")
        dc_path = os.path.join(target_dir, "docker-compose.yml")
        df_content = self.mcp.fs_read_file(df_path).get("content", "")
        dc_content = self.mcp.fs_read_file(dc_path).get("content", "")
        docker_check = self.mcp.docker_validate_config(df_content, dc_content)

        return {
            "status": "success",
            "created_files": created_files,
            "docker_verification": docker_check
        }
