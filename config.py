import os
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class GatewayConfig:
    base_url: str = os.getenv("OMNIROUTE_BASE_URL", "http://localhost:20128/v1")
    api_key: str = os.getenv("OMNIROUTE_API_KEY", "sk-dc3f17de0165d3ea-7870cd-e78e4500")
    
    # Primary Model: GPT 5.6 Terra (Codex / ChatGPT Go)
    primary_model: str = "gemini-3.7-flash-high"
    reasoning_model: str = "gemini-3.7-flash-high"
    codegen_model: str = "gemini-3.7-flash-high"
    
    fallback_models: List[str] = field(default_factory=lambda: ["agy/gemini-3.7-flash-high", "agy/claude-sonnet-4-6", "cfp/openai/gpt-oss-120b", "gemini-web/gemini-3.7-flash"])
    timeout_seconds: float = 300.0
    max_retries_circuit_breaker: int = 3
    compression_enabled: bool = True
    max_concurrent_workers: int = 8

@dataclass
class PipelineExecutionConfig:
    auto_mode: bool = True
    max_parallel_agents: bool = True
    checkpoints: List[str] = field(default_factory=lambda: [
        "checkpoint_prd",
        "checkpoint_architecture",
        "checkpoint_code",
        "checkpoint_release"
    ])

@dataclass
class SecurityPolicyConfig:
    auto_allowed_commands: List[str] = field(default_factory=lambda: [
        "npm run build", "npm test", "npm run lint", "npx vite build",
        "pytest", "python3 -m unittest", "python3 -m py_compile",
        "node --check", "curl", "ls", "pwd", "git status", "git diff"
    ])
    prompt_required_patterns: List[str] = field(default_factory=lambda: [
        "rm -rf", "drop table", "drop database", "docker prune", "docker system prune",
        "git push --force", "chmod 777", "mkfs"
    ])

@dataclass
class MemoryConfig:
    db_path: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "ai_zavod_memory.db"
    )

@dataclass
class VKConfig:
    enabled: bool = True
    token: str = os.getenv(
        "VK_TOKEN",
        "vk1.a.AdLTVIRhuQLMTO2HqAriU-7Z3j8oHqtnCxrrE9VAHxpFuSlmeDbMJrI7zh5DzEX3lZl0GLNvqvGWv-i2_0wvQIiYRzpZ1TXx1g6twhLp9rTkQM0jwFAnNhLCiyXKMA6LEumvuX_X42B6-34smrg2j1OdweGSEfJcyof1RhL0E8AJ00-0NmguqTGk1qCjtx_-JLpqf7aHwFDJnEsYbNUDlA"
    )
    default_peer_id: int = int(os.getenv("VK_DEFAULT_PEER_ID", "538881038"))
    server_base_url: str = os.getenv("SERVER_BASE_URL", "http://100.100.89.45:8085")

@dataclass
class Config:
    gateway: GatewayConfig = field(default_factory=GatewayConfig)
    pipeline: PipelineExecutionConfig = field(default_factory=PipelineExecutionConfig)
    security: SecurityPolicyConfig = field(default_factory=SecurityPolicyConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    vk: VKConfig = field(default_factory=VKConfig)
    workspace_root: str = "/home/rama/projectAnti"

default_config = Config()
