import logging
import json
import re
from typing import Dict, Any, List, Optional
from AI_Zavod.gateway.client import OmniRouteClient
from AI_Zavod.memory.sqlite_store import ContextMemoryStore
from AI_Zavod.mcp.server_registry import MCPManager
from AI_Zavod.config import default_config

logger = logging.getLogger("AI_Zavod.Agent")

SKILL_ADHERENCE_RULE = """
[MANDATORY SYSTEM DIRECTIVE - SKILL & STANDARD ADHERENCE]:
You are operating within an autonomous multi-agent software engineering factory governed by strict Project Skills (.agents/skills/).
You MUST strictly execute and adhere to:
1. All domain rules, user constraints, and functional requirements defined in the active skills.
2. All architectural standards and aesthetic tokens (typography, color palette, anti-ai-trope directives).
3. The Task Execution Matrix: explicitly report your tasks_checklist with SUCCESS or FAILED status for every assigned responsibility.
Any omission, deviation, or unauthorized substitution of requested features is a critical quality failure.
"""

class BaseAgent:
    def __init__(
        self,
        role: str,
        system_prompt: str,
        gateway: Optional[OmniRouteClient] = None,
        memory: Optional[ContextMemoryStore] = None,
        mcp: Optional[MCPManager] = None
    ):
        self.role = role
        self.system_prompt = system_prompt.strip() + "\n" + SKILL_ADHERENCE_RULE
        self.gateway = gateway or OmniRouteClient()
        self.memory = memory or ContextMemoryStore()
        self.mcp = mcp or MCPManager()

    def execute_prompt(
        self,
        session_id: str,
        user_prompt: str,
        context: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a prompt against OmniRoute with role context and mandatory skill adherence.
        """
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        if context:
            messages.append({
                "role": "system",
                "content": f"Shared Pipeline Context:\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            })
        messages.append({"role": "user", "content": user_prompt})

        logger.info(f"[{self.role}] Running task for session '{session_id}'...")
        try:
            res = self.gateway.chat_completion(messages=messages, model=model, max_tokens=8192)
        except Exception as e:
            logger.warning(f"[{self.role}] OmniRoute chat completion failed or rate limited ({e}). Returning empty result for graceful fallback.")
            return {"content": "", "status": "failed", "error": str(e), "model_used": model or "fallback", "usage": {}}
        
        content = res.get("content", "")
        model_used = res.get("model_used", "")
        usage = res.get("usage", {})
        total_tokens = usage.get("total_tokens", 0)

        # Thread-safe log to memory store
        try:
            self.memory.log_agent_run(
                session_id=session_id,
                agent_role=self.role,
                input_prompt=user_prompt[:500],
                output_summary=content[:500],
                model_used=model_used,
                tokens_used=total_tokens,
                status="success"
            )
        except Exception as e:
            logger.warning(f"Memory logging warning: {e}")

        return {
            "role": self.role,
            "content": content,
            "model_used": model_used,
            "tokens_used": total_tokens,
            "raw_response": res
        }

    def extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Robust multi-pattern JSON extractor with strict=False support
        and repair for unescaped control characters and truncated outputs.
        """
        if not text:
            return None
        text_clean = text.strip()

        def try_parse(s: str) -> Optional[Dict[str, Any]]:
            try:
                return json.loads(s, strict=False)
            except Exception:
                pass
            for suffix in ['"\n}\n}', '"\n]}', '"]}', '"}', '}\n}', ']}', '}']:
                try:
                    return json.loads(s + suffix, strict=False)
                except Exception:
                    pass
            return None

        # Pass 1: Direct clean text
        res = try_parse(text_clean)
        if res:
            return res

        # Pass 2: Markdown ```json ... ```
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text_clean)
        if match:
            res = try_parse(match.group(1).strip())
            if res:
                return res

        # Pass 3: First outer { ... } block
        match = re.search(r"\{[\s\S]*\}", text_clean)
        if match:
            res = try_parse(match.group(0).strip())
            if res:
                return res

        return None

    def extract_files_from_markdown(self, text: str) -> List[Dict[str, str]]:
        """Fallback: extracts files structured as markdown blocks or headers."""
        files = []
        pattern = r"(?:###\s*(?:File:\s*)?|####\s*|File:\s*)[`\*]*([a-zA-Z0-9_\-\./\\]+)[`\*]*\s*\n+```[a-zA-Z]*\n([\s\S]*?)```"
        matches = re.findall(pattern, text)
        for filepath, content in matches:
            if "." in filepath:
                files.append({"path": filepath.strip(), "content": content})
        return files
