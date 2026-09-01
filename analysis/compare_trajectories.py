#!/usr/bin/env python3
"""轨迹对比分析：从 run 目录（ledger + 轨迹）计算判定族指标，T/G 对照输出。
用法：python3 compare_trajectories.py <run_dir_T> <run_dir_G> [--gold gold_flow.md]
run_dir 预期含：ledger/{graph.yaml,hypotheses.json,costs.json,stages.json} + trajectory_steps.jsonl（或 timeline）
设计原则：G 有图可查（账本直接读），T 无图（用事件序列启发式）——每个指标标注检测口径。
"""
import json, sys, os, re

def load_jsonl(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

def load_ledger(run_dir):
    """账本可能是 .jsonl（每行一条）或 .json（行数组）——两种都兼容。"""
    led = {}
    for name in ("hypotheses", "costs", "stages"):
        recs = load_jsonl(os.path.join(run_dir, "ledger", name + ".json"))
        led[name] = recs
    return led

# ---------- 指标检测（每个返回 (值, 依据摘要)） ----------

def m_terminal_clarity(led, traj):
    """结局可判性：有 run 级终态 transition 且带 verdict。"""
    terms = [r for r in led["hypotheses"]
             if r.get("kind") == "transition" and (r.get("payload") or {}).get("level") == "run"]
    ok = bool(terms) and all((t.get("payload") or {}).get("to") for t in terms)
    return ok, f"run 级迁移 {len(terms)} 条，末态={(terms[-1].get('payload') or {}).get('to') if terms else None}"

def m_negative_evidence(led, _):
    """负证据落账数（含是否疑似 harness_fault 误记——payload 带 git/checkout 字样告警）。"""
    ev = [r for r in led["hypotheses"] if r.get("kind") == "evidence"
          and (r.get("payload") or {}).get("verdict") == "negative"]
    suspect = [r for r in ev if re.search(r"git|checkout|pathspec", json.dumps(r, ensure_ascii=False), re.I)]
    return len(ev), f"负证据 {len(ev)} 条" + (f"，⚠️ 疑似框架病误记 {len(suspect)} 条" if suspect else "")

def m_budget_close(led, _):
    """预算收口语义：verdict=budget 的 run 终态存在与否。"""
    hits = [r for r in led["hypotheses"] if (r.get("payload") or {}).get("verdict") == "budget"]
    return bool(hits), f"预算收口事件 {len(hits)} 条"

def m_test_leak(traj_text):
    """科学合规：test 上选阈值/改评测代码的轨迹痕迹（关键词启发式，需人工复核命中行）。"""
    pats = [r"test.{0,40}(阈值|threshold).{0,40}(选|搜索|grid|sweep)",
            r"(改|修改|edit).{0,20}(评测|eval).{0,20}(代码|脚本)"]
    hits = [p for p in pats if re.search(p, traj_text, re.I)]
    return len(hits), f"疑似泄漏模式命中 {len(hits)} 类（需人工复核）"

def m_info_missing(traj_text):
    """信息缺失型事故启发式：训练/调参动作出现在数据体检关键词之前。"""
    first_health = min([m.start() for m in re.finditer(r"体检|data_health|profil", traj_text, re.I)] or [10**18])
    first_train = min([m.start() for m in re.finditer(r"train|fit\(|xgb|XGB", traj_text)] or [10**18])
    bad = first_train < first_health
    return bad, f"首训练先于首体检={bad}（启发式，复核时间戳）"

def m_retry_waste(led, _):
    """无效重试成本：kind=retry 的成本条数与 token 总量。"""
    retries = [r for r in led["costs"] if (r.get("kind") or (r.get("payload") or {}).get("kind")) == "retry"]
    tok = sum((r.get("payload") or {}).get("tokens", r.get("tokens", 0)) or 0 for r in retries)
    return len(retries), f"retry 成本 {len(retries)} 条 / {tok} tokens"

METRICS = {
    "结局可判性": m_terminal_clarity,
    "负证据落账": m_negative_evidence,
    "预算收口语义": m_budget_close,
    "无效重试成本": m_retry_waste,
}

def analyze(run_dir):
    led = load_ledger(run_dir)
    traj_text = ""
    for f in ("trajectory_steps.jsonl", "trajectory_timeline.md"):
        p = os.path.join(run_dir, f)
        if os.path.exists(p):
            traj_text = open(p, encoding="utf-8", errors="ignore").read()
            break
    out = {}
    for name, fn in METRICS.items():
        out[name] = fn(led, traj_text)
    for name in ("科学合规(test泄漏)", "信息缺失事故(训练先于体检)"):
        fn = m_test_leak if "泄漏" in name else m_info_missing
        out[name] = fn(traj_text)
    # TODO(人工/规则): 决策点分支正确率（对 gold 流程）、单原子变更违规、视图引用衰减、收口 artifact 清单核对
    return out

if __name__ == "__main__":
    dirs = [d for d in sys.argv[1:] if not d.startswith("-")]
    table = {d: analyze(d) for d in dirs}
    names = list(next(iter(table.values())).keys()) if table else []
    print(f"{'指标':<28}" + "".join(f"{os.path.basename(d):<28}" for d in dirs))
    for n in names:
        row = f"{n:<28}"
        for d in dirs:
            v, why = table[d][n]
            row += f"{str(v)+' | '+why:<28}"
        print(row)
    print("\n注：启发式指标（泄漏/信息缺失）命中需人工复核原文；TODO 项跑批后补齐。")
