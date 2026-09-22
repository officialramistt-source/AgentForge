import os
import subprocess
import json
import logging
from typing import Dict, Any, List, Optional
from AI_Zavod.config import default_config

logger = logging.getLogger("AI_Zavod.MCP")

class MCPManager:
    """
    Simulated & Native Model Context Protocol (MCP) Adapter Layer.
    Provides standard tools: server-filesystem, server-postgres, mcp-server-docker, browser-verifier.
    """
    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or default_config.workspace_root

    # --- server-filesystem ---
    def fs_write_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Safe file creation and writing."""
        full_path = file_path if os.path.isabs(file_path) else os.path.join(self.workspace_root, file_path)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return {"status": "success", "file_path": full_path, "bytes_written": len(content)}
        except Exception as e:
            return {"status": "error", "error": str(e), "file_path": full_path}

    def fs_read_file(self, file_path: str) -> Dict[str, Any]:
        """Safe file reading."""
        full_path = file_path if os.path.isabs(file_path) else os.path.join(self.workspace_root, file_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            return {"status": "success", "file_path": full_path, "content": content}
        except Exception as e:
            return {"status": "error", "error": str(e), "file_path": full_path}

    def fs_list_dir(self, dir_path: str) -> Dict[str, Any]:
        """List files in directory."""
        full_path = dir_path if os.path.isabs(dir_path) else os.path.join(self.workspace_root, dir_path)
        try:
            items = os.listdir(full_path)
            return {"status": "success", "dir": full_path, "items": items}
        except Exception as e:
            return {"status": "error", "error": str(e), "dir": full_path}

    # --- server-postgres / SQL ---
    def sql_validate_schema(self, sql_content: str) -> Dict[str, Any]:
        """Validates basic SQL schema syntax."""
        statements = [s.strip() for s in sql_content.split(";") if s.strip()]
        valid_keywords = ["CREATE TABLE", "CREATE INDEX", "INSERT INTO", "ALTER TABLE", "DROP TABLE", "CREATE TYPE"]
        passed = []
        for s in statements:
            if any(s.upper().startswith(kw) for kw in valid_keywords):
                passed.append(s[:50] + "...")
        return {
            "status": "valid" if len(passed) == len(statements) else "warnings",
            "statements_count": len(statements),
            "validated": passed
        }

    # --- mcp-server-docker ---
    def docker_validate_config(self, dockerfile_content: str, compose_content: str) -> Dict[str, Any]:
        """Validates Dockerfile and docker-compose.yml structure."""
        has_from = "FROM " in dockerfile_content
        has_services = "services:" in compose_content
        return {
            "status": "success" if (has_from and has_services) else "error",
            "dockerfile_valid": has_from,
            "compose_valid": has_services
        }

    # --- browser-verifier ---
    def verify_static_html(self, html_path: str) -> Dict[str, Any]:
        """Checks HTML for syntax completeness and critical tags."""
        full_path = html_path if os.path.isabs(html_path) else os.path.join(self.workspace_root, html_path)
        if not os.path.exists(full_path):
            return {"status": "error", "error": f"File {full_path} not found"}
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        has_doctype = "<!DOCTYPE" in content.upper()
        has_body = "<body" in content.lower()
        has_root = "id=\"root\"" in content or "id=\"app\"" in content
        
        return {
            "status": "verified" if (has_doctype and has_body) else "incomplete",
            "has_doctype": has_doctype,
            "has_body": has_body,
            "has_root_mount": has_root,
            "file_size": len(content)
        }
