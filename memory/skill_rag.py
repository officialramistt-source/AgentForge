import os
import re
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger("AI_Zavod.SkillRAG")

class SkillRAGEngine:
    """
    Dynamic Skill-RAG: Scans .agents/skills/, indexes domain instructions,
    and injects relevant skill knowledge into subagent prompts based on topic keywords.
    """
    def __init__(self, skills_dir: str = "/home/rama/projectAnti/.agents/skills"):
        self.skills_dir = skills_dir
        self.indexed_skills: List[Dict[str, Any]] = []
        self._load_skills()

    def _load_skills(self):
        if not os.path.exists(self.skills_dir):
            return
        
        self.indexed_skills = []
        for item in os.listdir(self.skills_dir):
            skill_folder = os.path.join(self.skills_dir, item)
            skill_file = os.path.join(skill_folder, "SKILL.md")
            if os.path.isdir(skill_folder) and os.path.exists(skill_file):
                try:
                    with open(skill_file, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    
                    # Parse YAML frontmatter if present
                    name = item
                    desc = ""
                    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
                    body = content
                    if frontmatter_match:
                        fm_text = frontmatter_match.group(1)
                        body = frontmatter_match.group(2)
                        for line in fm_text.split("\n"):
                            if line.startswith("name:"):
                                name = line.replace("name:", "").strip()
                            elif line.startswith("description:"):
                                desc = line.replace("description:", "").strip()
                    
                    # Also index references folder if present
                    refs_text = ""
                    refs_dir = os.path.join(skill_folder, "references")
                    if os.path.isdir(refs_dir):
                        for ref_f in os.listdir(refs_dir)[:3]:
                            ref_path = os.path.join(refs_dir, ref_f)
                            if os.path.isfile(ref_path) and ref_f.endswith((".md", ".txt")):
                                try:
                                    with open(ref_path, "r", encoding="utf-8", errors="replace") as rf:
                                        refs_text += f"\n[Reference: {ref_f}]:\n" + rf.read()[:2500]
                                except Exception:
                                    pass

                    full_context = (body + "\n" + refs_text).strip()

                    self.indexed_skills.append({
                        "name": name,
                        "description": desc,
                        "folder": item,
                        "body": full_context[:5000],  # up to 5000 chars of deep context
                        "keywords": set(re.findall(r"\w+", (name + " " + desc + " " + body).lower()))
                    })
                except Exception as e:
                    logger.warning(f"Failed to index skill '{item}': {e}")
        
        logger.info(f"[SkillRAG] Successfully indexed {len(self.indexed_skills)} skills from {self.skills_dir}")

    def find_relevant_skills(self, prompt: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """Finds top-k most relevant skills based on query keyword matching."""
        if not self.indexed_skills:
            self._load_skills()
            
        prompt_words = set(re.findall(r"\w+", prompt.lower()))
        scored = []
        
        for s in self.indexed_skills:
            intersection = len(prompt_words.intersection(s["keywords"]))
            # Strong bonus score if skill name is in prompt
            if s["name"].lower() in prompt.lower() or s["folder"].lower() in prompt.lower():
                intersection += 10
            # Contextual bonuses for key technical domains
            if "design" in prompt.lower() and "design" in s["name"].lower():
                intersection += 8
            if "product" in prompt.lower() and "product" in s["name"].lower():
                intersection += 8
            if "plan" in prompt.lower() and ("time" in s["name"].lower() or "plan" in s["name"].lower()):
                intersection += 8
            if intersection > 0:
                scored.append((intersection, s))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    def format_skill_context(self, prompt: str) -> str:
        """Formats matched skills into an authoritative prompt injection block."""
        matched = self.find_relevant_skills(prompt)
        if not matched:
            return ""
        
        lines = [
            "\n========================================================",
            "⚡ MANDATORY ACTIVE PROJECT SKILLS & ARCHITECTURAL GUIDELINES:",
            "ALL AGENTS MUST STRICTLY ADHERE TO THESE SKILLS WITHOUT EXCEPTION.",
            "ANY DEVIATION OR FAILURE TO IMPLEMENT SPECIFIED STANDARDS IS A CRITICAL DEFECT.",
            "========================================================"
        ]
        for s in matched:
            lines.append(f"\n--- [Active Skill: {s['name']}] ---")
            if s['description']:
                lines.append(f"Summary: {s['description']}")
            lines.append(s['body'].strip()[:2500])
            lines.append("--------------------------------------------------")
        
        lines.append("\n========================================================\n")
        return "\n".join(lines)
