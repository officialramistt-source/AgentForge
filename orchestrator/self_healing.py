import os
import logging
from typing import Dict, Any, Optional
from AI_Zavod.verification.verifier import ProjectVerifier

logger = logging.getLogger("AI_Zavod.SelfHealing")

class SelfHealingEngine:
    def __init__(self, pipeline, max_attempts: int = 3):
        self.pipeline = pipeline
        self.max_attempts = max_attempts

    def repair_if_needed(self, session_id: str, target_dir: str, arch_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reflexion Loop: If static checks or tests fail, passes error traceback
        back to LLM agent to surgically fix the code until verification passes.
        """
        verifier = ProjectVerifier(target_dir=target_dir)
        check = verifier.verify_all()
        
        if check.get("all_passed", False):
            return {"status": "clean", "attempts": 0, "verification": check}

        logger.warning(f"[SelfHealing] Verification failed. Activating Reflexion Loop (Max {self.max_attempts} attempts)...")
        
        for attempt in range(1, self.max_attempts + 1):
            logger.info(f"[SelfHealing] Fix attempt {attempt}/{self.max_attempts}...")
            
            # Case 1: Python syntax error in backend
            py_errors = check.get("python", {}).get("errors", [])
            if py_errors:
                for err in py_errors:
                    err_file = err.get("file", "")
                    err_msg = err.get("error", "")
                    logger.info(f"[SelfHealing] Fixing Python syntax error in '{err_file}': {err_msg}")
                    
                    full_p = os.path.join(target_dir, err_file)
                    current_code = self.pipeline.mcp.fs_read_file(full_p).get("content", "")
                    
                    fix_prompt = (
                        f"CRITICAL FIX REQUIRED: File '{err_file}' has a syntax/compile error:\n"
                        f"{err_msg}\n\n"
                        f"Current code:\n```python\n{current_code}\n```\n\n"
                        f"Fix the error and output ONLY the complete corrected Python code without markdown."
                    )
                    
                    res = self.pipeline.backend.execute_prompt(
                        session_id=session_id,
                        user_prompt=fix_prompt,
                        context=arch_spec
                    )
                    
                    fixed_content = res["content"].strip()
                    if fixed_content.startswith("```"):
                        # strip code fences
                        lines = fixed_content.split("\n")
                        if lines[0].startswith("```"):
                            lines = lines[1:]
                        if lines and lines[-1].startswith("```"):
                            lines = lines[:-1]
                        fixed_content = "\n".join(lines)
                    
                    self.pipeline.mcp.fs_write_file(full_p, fixed_content)

            # Re-verify after attempt
            check = verifier.verify_all()
            if check.get("all_passed", False):
                logger.info(f"[SelfHealing] ✅ Project successfully healed on attempt {attempt}!")
                return {"status": "healed", "attempts": attempt, "verification": check}

        logger.warning("[SelfHealing] Could not fully heal all issues after max attempts.")
        return {"status": "partially_healed", "attempts": self.max_attempts, "verification": check}
