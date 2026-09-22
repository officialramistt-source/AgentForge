import json
import logging
import time
from typing import List, Dict, Any, Optional
import requests
from AI_Zavod.config import GatewayConfig, default_config

logger = logging.getLogger("AI_Zavod.Gateway")

class CircuitBreakerOpenException(Exception):
    """Raised when all candidate models in the pool have failed or rate-limited."""
    pass

class OmniRouteClient:
    def __init__(self, config: Optional[GatewayConfig] = None):
        self.config = config or default_config.gateway
        self.base_url = self.config.base_url.rstrip("/")
        self.api_key = self.config.api_key
        self.primary_model = self.config.primary_model
        self.fallback_models = self.config.fallback_models
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "AI-Zavod-Pipeline/1.0"
        })

    def test_connection(self) -> Dict[str, Any]:
        """Verify connection and authentication against OmniRoute."""
        url = f"{self.base_url}/models"
        try:
            start_t = time.time()
            res = self.session.get(url, timeout=10)
            latency_ms = round((time.time() - start_t) * 1000, 2)
            if res.status_code == 200:
                data = res.json()
                models_count = len(data.get("data", []))
                return {
                    "status": "online",
                    "status_code": res.status_code,
                    "latency_ms": latency_ms,
                    "models_count": models_count,
                    "endpoint": url
                }
            else:
                return {
                    "status": "error",
                    "status_code": res.status_code,
                    "message": res.text,
                    "endpoint": url
                }
        except Exception as e:
            return {
                "status": "unreachable",
                "error": str(e),
                "endpoint": url
            }

    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 8192,
        response_format: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Sends chat completion request with Circuit Breaker & Context Relay.
        Automatically falls back through available model candidates upon HTTP 429/50x.
        """
        candidate_models = []
        if model:
            candidate_models.append(model)
        else:
            candidate_models.append(self.primary_model)
        
        for fb in self.fallback_models:
            if fb not in candidate_models:
                candidate_models.append(fb)

        last_error = None
        for attempt_idx, candidate in enumerate(candidate_models):
            url = f"{self.base_url}/chat/completions"
            payload: Dict[str, Any] = {
                "model": candidate,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            if response_format:
                payload["response_format"] = response_format
            if tools:
                payload["tools"] = tools

            try:
                logger.info(f"[OmniRoute] Dispatching prompt to model '{candidate}' (Attempt {attempt_idx+1}/{len(candidate_models)})")
                res = self.session.post(url, json=payload, timeout=self.config.timeout_seconds)
                
                if res.status_code == 200:
                    resp_json = res.json()
                    choice = resp_json.get("choices", [{}])[0]
                    message = choice.get("message", {})
                    usage = resp_json.get("usage", {})
                    
                    return {
                        "success": True,
                        "model_used": candidate,
                        "content": message.get("content", ""),
                        "tool_calls": message.get("tool_calls", None),
                        "usage": usage,
                        "fallback_triggered": attempt_idx > 0
                    }
                
                elif res.status_code in (429, 500, 502, 503, 504):
                    logger.warning(
                        f"[CircuitBreaker] HTTP {res.status_code} received from model '{candidate}'. "
                        f"Activating Context Relay to next candidate."
                    )
                    last_error = f"HTTP {res.status_code}: {res.text}"
                    time.sleep(1.0)
                    continue
                else:
                    logger.error(f"[OmniRoute] Request failed: HTTP {res.status_code} - {res.text}")
                    last_error = f"HTTP {res.status_code}: {res.text}"
                    # For client errors (e.g. 400 Bad Request with tool schema), try next model or break
                    continue

            except requests.RequestException as exc:
                logger.warning(f"[CircuitBreaker] Network/timeout exception with model '{candidate}': {exc}")
                last_error = str(exc)
                continue

        raise CircuitBreakerOpenException(
            f"All model candidates failed in OmniRoute pool. Last error: {last_error}"
        )
