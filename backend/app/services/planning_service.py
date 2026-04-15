from __future__ import annotations

from typing import Any, Dict, List, Optional, cast

from app.schemas.common_enums import DomainCode, VALID_DOMAIN_CODES


INTENT_RULES: List[tuple[str, tuple[str, ...]]] = [
    ("project_mgmt", ("项目", "里程碑", "进度", "任务", "立项", "审批")),
    ("marketing", ("营销", "活动", "增长", "投放")),
    ("engineering", ("代码", "架构", "部署", "缺陷", "接口", "测试")),
]


def _collect_intent_scores(instruction: str) -> tuple[Dict[str, int], Dict[str, List[str]]]:
    text = str(instruction or "")
    score_map: Dict[str, int] = {}
    hit_map: Dict[str, List[str]] = {}
    for label, keywords in INTENT_RULES:
        hits = [k for k in keywords if k in text]
        score_map[label] = len(hits)
        hit_map[label] = hits
    return score_map, hit_map


def classify_intent(instruction: str) -> Dict[str, Any]:
    score_map, hit_map = _collect_intent_scores(instruction)
    positive = [(label, score) for label, score in score_map.items() if score > 0]
    positive.sort(key=lambda x: (-x[1], x[0]))
    labels = [label for label, _score in positive]
    primary = labels[0] if labels else "general_coordination"
    top_score = positive[0][1] if positive else 0
    # 置信度按命中强度平滑抬升，避免常量分值。
    confidence = 0.55 + min(0.35, 0.08 * top_score + 0.03 * max(0, len(labels) - 1))
    return {
        "primary": primary,
        "labels": labels or [primary],
        "confidence": round(confidence, 2),
        "scores": score_map,
        "matched_keywords": hit_map.get(primary, []),
    }


def _subtasks_for(primary: str, instruction: str, project: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
    ctx = (instruction or "").strip()[:120]
    if primary == "project_mgmt":
        tasks = [
            {"title": "对齐目标与范围", "suggested_domain": "D03", "priority": "P0", "kind": "plan", "context": ctx},
            {"title": "拆解工作包与依赖", "suggested_domain": "D03", "priority": "P0", "kind": "decompose", "context": ctx},
            {"title": "同步风险与资源", "suggested_domain": "D03", "priority": "P1", "kind": "align", "context": ctx},
        ]
        if "风险" in ctx and all(t["title"] != "补充风险闭环与责任人" for t in tasks):
            tasks.append(
                {
                    "title": "补充风险闭环与责任人",
                    "suggested_domain": "D03",
                    "priority": "P2",
                    "kind": "risk",
                    "context": ctx,
                }
            )
        return tasks
    if primary == "marketing":
        tasks = [
            {"title": "明确受众与渠道假设", "suggested_domain": "D05", "priority": "P0", "kind": "plan", "context": ctx},
            {"title": "形成实验与度量指标", "suggested_domain": "D05", "priority": "P1", "kind": "measure", "context": ctx},
            {"title": "定义转化漏斗与复盘节奏", "suggested_domain": "D05", "priority": "P1", "kind": "funnel", "context": ctx},
        ]
        return tasks
    if primary == "engineering":
        tasks = [
            {"title": "澄清技术约束与接口契约", "suggested_domain": "D02", "priority": "P0", "kind": "spec", "context": ctx},
            {"title": "拆分实现与验证步骤", "suggested_domain": "D02", "priority": "P0", "kind": "build", "context": ctx},
            {"title": "安排回归与发布检查", "suggested_domain": "D02", "priority": "P1", "kind": "verify", "context": ctx},
        ]
        if any(k in ctx for k in ("性能", "慢", "优化")):
            tasks.append(
                {
                    "title": "建立性能基线与回归阈值",
                    "suggested_domain": "D02",
                    "priority": "P1",
                    "kind": "perf",
                    "context": ctx,
                }
            )
        return tasks
    return [
        {"title": "澄清意图与成功标准", "suggested_domain": "D03", "priority": "P0", "kind": "clarify", "context": ctx},
        {"title": "生成可执行步骤并指派", "suggested_domain": "D03", "priority": "P1", "kind": "execute", "context": ctx},
        {"title": "输出小结与下一步", "suggested_domain": "D03", "priority": "P2", "kind": "report", "context": ctx},
    ]


def _mix_secondary_subtasks(
    labels: list[str], instruction: str, project: Optional[Dict[str, Any]], primary_tasks: list[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    if len(labels) <= 1:
        return primary_tasks
    seen_titles = {str(t.get("title", "")).strip() for t in primary_tasks}
    mixed = list(primary_tasks)
    for label in labels[1:]:
        candidates = _subtasks_for(label, instruction, project)
        # 每个次意图最多补 1 条关键任务，避免主任务被稀释。
        for task in candidates:
            title = str(task.get("title", "")).strip()
            if not title or title in seen_titles:
                continue
            extended = dict(task)
            extended["source_intent"] = label
            mixed.append(extended)
            seen_titles.add(title)
            break
    return mixed


def _normalize_domain_code(value: Any) -> DomainCode:
    code = str(value or "").strip().upper()
    if code not in VALID_DOMAIN_CODES:
        code = "D03"
    return cast(DomainCode, code)


def build_ceo_plan(instruction: str, project: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """PH3-T01：轻量意图 + 任务分解（可替换为 LLM）。"""
    intent = classify_intent(instruction)
    primary_subtasks = _subtasks_for(intent["primary"], instruction, project)
    subtasks = _mix_secondary_subtasks(intent["labels"], instruction, project, primary_subtasks)
    for st in subtasks:
        st["suggested_domain"] = _normalize_domain_code(st.get("suggested_domain"))
    resources = {
        "suggested_roles": ["L1-CEO", "L2-GM", "L3-PM"],
        "project_name": project.get("name") if project else None,
        "project_id": project.get("id") if project else None,
    }
    rationale = (
        "基于关键词命中与固定工作流模板生成子任务；"
        + ("已注入项目上下文。" if project else "无项目上下文。")
    )
    explainability = {
        "rule_set": "planning_v0.1",
        "signals": [
            {
                "type": "keyword_hit",
                "primary": intent["primary"],
                "labels": intent["labels"],
                "matched_keywords": intent.get("matched_keywords", []),
                "score": int((intent.get("scores") or {}).get(intent["primary"], 0)),
            }
        ],
    }
    return {
        "intent": intent,
        "subtasks": subtasks,
        "resources": resources,
        "rationale": rationale,
        "explainability": explainability,
    }
