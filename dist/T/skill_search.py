"""T 条件新增工具：skill_search（参考实现，直接可用）。

放置：autotune 项目的 agent 工具注册处（与其他工具并列），注册名 "skill_search"。
依赖：skills_flat/ 目录 + index.json（本仓库 dist/T/ 下，放法见 docs/放置与代码改动清单.md）。
行为定义见 retrieval_tool_spec.md——刻意从简（关键词匹配），对照变量保持单一。
"""
import json
import os
import re

SKILLS_DIR = os.environ.get("SKILLS_FLAT_DIR", "skills_flat")
_INDEX = None


def _load():
    global _INDEX
    if _INDEX is None:
        with open(os.path.join(SKILLS_DIR, "..", "index.json"), encoding="utf-8") as f:
            _INDEX = json.load(f)["skills"]
    return _INDEX


def skill_search(query: str, top_k: int = 3) -> list[dict]:
    """按关键词在 16 个任务对口 skill 中检索，返回 top_k 个 (name, category, description, path)。

    零命中时返回全量目录（name+description），让 agent 自行挑选。
    """
    index = _load()
    terms = [t.lower() for t in re.split(r"[\s,，;；/]+", query) if t.strip()]

    def score(skill):
        hay = f"{skill['name']} {skill['category']} {skill['description']}".lower()
        return sum(hay.count(t) for t in terms)

    ranked = sorted(index, key=score, reverse=True)
    hits = [s for s in ranked if score(s) > 0][:top_k]
    if not hits:
        return [{"name": s["name"], "category": s["category"],
                 "description": s["description"], "path": s["path"],
                 "note": "零命中，返回全量目录"} for s in index]
    return [{"name": s["name"], "category": s["category"],
             "description": s["description"], "path": s["path"]} for s in hits]
