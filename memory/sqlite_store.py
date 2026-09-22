import sqlite3
import json
import os
import time
from typing import Dict, Any, List, Optional
from AI_Zavod.config import default_config

class ContextMemoryStore:
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or default_config.memory.db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    goal TEXT NOT NULL,
                    status TEXT NOT NULL,
                    target_dir TEXT,
                    mode TEXT DEFAULT 'task',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            # Safe column migration for existing DBs
            try:
                cur.execute("ALTER TABLE sessions ADD COLUMN mode TEXT DEFAULT 'task';")
            except Exception:
                pass
            cur.execute("""
                CREATE TABLE IF NOT EXISTS adrs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    rationale TEXT,
                    schema_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS agent_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    agent_role TEXT NOT NULL,
                    input_prompt TEXT NOT NULL,
                    output_summary TEXT NOT NULL,
                    model_used TEXT,
                    tokens_used INTEGER DEFAULT 0,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS artifacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    file_type TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS stage_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    stage_name TEXT NOT NULL,
                    duration_ms REAL NOT NULL,
                    tokens_used INTEGER DEFAULT 0,
                    cost_usd REAL DEFAULT 0.0,
                    model_used TEXT,
                    status TEXT NOT NULL,
                    retries_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS concept_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    chosen_concept_id TEXT NOT NULL,
                    chosen_archetype_name TEXT NOT NULL,
                    competitor_benchmark TEXT,
                    cognitive_law TEXT,
                    user_feedback TEXT,
                    all_concepts_json TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(session_id) REFERENCES sessions(id)
                );
            """)
            conn.commit()

    def create_session(self, session_id: str, goal: str, target_dir: str, mode: str = "task") -> str:
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO sessions (id, goal, status, target_dir, mode) VALUES (?, ?, ?, ?, ?)",
                (session_id, goal, "in_progress", target_dir, mode)
            )
            conn.commit()
        return session_id

    def update_session_status(self, session_id: str, status: str):
        with self._get_conn() as conn:
            conn.execute(
                "UPDATE sessions SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (status, session_id)
            )
            conn.commit()

    def add_adr(self, session_id: str, title: str, decision: str, rationale: str = "", schema_json: str = ""):
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO adrs (session_id, title, decision, rationale, schema_json) VALUES (?, ?, ?, ?, ?)",
                (session_id, title, decision, rationale, schema_json)
            )
            conn.commit()

    def get_adrs(self, session_id: str) -> List[Dict[str, Any]]:
        with self._get_conn() as conn:
            rows = conn.execute("SELECT * FROM adrs WHERE session_id = ? ORDER BY id ASC", (session_id,)).fetchall()
            return [dict(r) for r in rows]

    def log_agent_run(
        self,
        session_id: str,
        agent_role: str,
        input_prompt: str,
        output_summary: str,
        model_used: str = "",
        tokens_used: int = 0,
        status: str = "success"
    ):
        with self._get_conn() as conn:
            conn.execute(
                """INSERT INTO agent_runs 
                   (session_id, agent_role, input_prompt, output_summary, model_used, tokens_used, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (session_id, agent_role, input_prompt, output_summary, model_used, tokens_used, status)
            )
            conn.commit()

    def log_stage_metric(
        self,
        session_id: str,
        stage_name: str,
        duration_ms: float,
        tokens_used: int = 0,
        model_used: str = "",
        status: str = "success",
        retries_count: int = 0
    ):
        # Gemini Flash pricing estimate: $0.10 / 1M tokens ($0.0000001 per token)
        cost_usd = round(tokens_used * 0.00000015, 6)
        with self._get_conn() as conn:
            conn.execute(
                """INSERT INTO stage_metrics
                   (session_id, stage_name, duration_ms, tokens_used, cost_usd, model_used, status, retries_count)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (session_id, stage_name, duration_ms, tokens_used, cost_usd, model_used, status, retries_count)
            )
            conn.commit()

    def register_artifact(self, session_id: str, file_path: str, file_type: str, description: str = ""):
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO artifacts (session_id, file_path, file_type, description) VALUES (?, ?, ?, ?)",
                (session_id, file_path, file_type, description)
            )
            conn.commit()

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        with self._get_conn() as conn:
            session = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if not session:
                return {}
            adrs = conn.execute("SELECT * FROM adrs WHERE session_id = ?", (session_id,)).fetchall()
            runs = conn.execute("SELECT * FROM agent_runs WHERE session_id = ?", (session_id,)).fetchall()
            artifacts = conn.execute("SELECT * FROM artifacts WHERE session_id = ?", (session_id,)).fetchall()
            metrics = conn.execute("SELECT * FROM stage_metrics WHERE session_id = ?", (session_id,)).fetchall()
            return {
                "session": dict(session),
                "adrs": [dict(a) for a in adrs],
                "runs": [dict(r) for r in runs],
                "artifacts": [dict(art) for art in artifacts],
                "metrics": [dict(m) for m in metrics]
            }

    def get_observability_metrics(self) -> Dict[str, Any]:
        with self._get_conn() as conn:
            total_sessions = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
            completed_sessions = conn.execute("SELECT COUNT(*) FROM sessions WHERE status = 'completed'").fetchone()[0]
            total_tokens = conn.execute("SELECT SUM(tokens_used) FROM agent_runs").fetchone()[0] or 0
            total_cost = conn.execute("SELECT SUM(cost_usd) FROM stage_metrics").fetchone()[0] or 0.0
            avg_duration = conn.execute("SELECT AVG(duration_ms) FROM stage_metrics").fetchone()[0] or 0.0
            stages_breakdown = conn.execute(
                "SELECT stage_name, COUNT(*), AVG(duration_ms), SUM(tokens_used) FROM stage_metrics GROUP BY stage_name"
            ).fetchall()
            return {
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "success_rate_pct": round((completed_sessions / total_sessions * 100), 1) if total_sessions > 0 else 100.0,
                "total_tokens_consumed": total_tokens,
                "estimated_cost_usd": round(total_cost, 4),
                "avg_stage_duration_sec": round(avg_duration / 1000.0, 2),
                "stages": [
                    {
                        "stage": r[0],
                        "runs": r[1],
                        "avg_duration_sec": round((r[2] or 0) / 1000.0, 2),
                        "tokens": r[3] or 0
                    }
                    for r in stages_breakdown
                ]
            }

    def record_concept_decision(
        self,
        session_id: str,
        prompt: str,
        chosen_concept_id: str,
        chosen_archetype_name: str,
        competitor_benchmark: str = "",
        cognitive_law: str = "",
        user_feedback: str = "",
        all_concepts: Optional[List[Dict[str, Any]]] = None
    ):
        """Records an author's HITL concept choice to build an empirical preference dataset."""
        concepts_json = json.dumps(all_concepts or [], ensure_ascii=False)
        with self._get_conn() as conn:
            conn.execute(
                """INSERT INTO concept_decisions 
                   (session_id, prompt, chosen_concept_id, chosen_archetype_name, competitor_benchmark, cognitive_law, user_feedback, all_concepts_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (session_id, prompt, chosen_concept_id, chosen_archetype_name, competitor_benchmark, cognitive_law, user_feedback, concepts_json)
            )
            conn.commit()

    def get_preference_history(self, limit: int = 15) -> List[Dict[str, Any]]:
        """Retrieves recent concept decisions made by the author."""
        with self._get_conn() as conn:
            rows = conn.execute(
                "SELECT * FROM concept_decisions ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]

    def get_dominant_preference(self) -> Optional[str]:
        """Returns the most frequently chosen archetype name from historical decisions."""
        with self._get_conn() as conn:
            row = conn.execute(
                """SELECT chosen_archetype_name, COUNT(*) as cnt 
                   FROM concept_decisions 
                   GROUP BY chosen_archetype_name 
                   ORDER BY cnt DESC LIMIT 1"""
            ).fetchone()
            if row:
                return row["chosen_archetype_name"]
            return None
