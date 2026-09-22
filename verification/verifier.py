import os
import py_compile
import logging
from typing import Dict, Any, List

logger = logging.getLogger("AI_Zavod.Verifier")

class ProjectVerifier:
    def __init__(self, target_dir: str):
        self.target_dir = target_dir

    def verify_all(self) -> Dict[str, Any]:
        """Runs full suite of static syntax, structure, and integrity checks."""
        python_results = self._verify_python_syntax()
        frontend_results = self._verify_frontend()
        devops_results = self._verify_devops()

        all_passed = (
            python_results.get("all_passed", False) and
            frontend_results.get("all_passed", False) and
            devops_results.get("all_passed", False)
        )

        return {
            "all_passed": all_passed,
            "python": python_results,
            "frontend": frontend_results,
            "devops": devops_results
        }

    def _verify_python_syntax(self) -> Dict[str, Any]:
        py_files = []
        for root, _, files in os.walk(self.target_dir):
            for f in files:
                if f.endswith(".py"):
                    py_files.append(os.path.join(root, f))

        errors = []
        passed = []
        for pf in py_files:
            try:
                py_compile.compile(pf, doraise=True)
                passed.append(os.path.relpath(pf, self.target_dir))
            except py_compile.PyCompileError as e:
                errors.append({"file": os.path.relpath(pf, self.target_dir), "error": str(e)})

        return {
            "all_passed": len(errors) == 0,
            "files_checked": len(py_files),
            "passed": passed,
            "errors": errors
        }

    def _verify_frontend(self) -> Dict[str, Any]:
        index_html = os.path.join(self.target_dir, "frontend", "index.html")
        exists = os.path.exists(index_html)
        size = os.path.getsize(index_html) if exists else 0
        return {
            "all_passed": exists and size > 100,
            "index_html_exists": exists,
            "size_bytes": size
        }

    def _verify_devops(self) -> Dict[str, Any]:
        dockerfile = os.path.join(self.target_dir, "Dockerfile")
        compose = os.path.join(self.target_dir, "docker-compose.yml")
        df_ok = os.path.exists(dockerfile)
        dc_ok = os.path.exists(compose)
        return {
            "all_passed": df_ok and dc_ok,
            "dockerfile_exists": df_ok,
            "compose_exists": dc_ok
        }
