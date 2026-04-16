from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _docs_dir() -> Path:
    return _repo_root().parent / "docs"


def _reports_dir() -> Path:
    return _repo_root() / "reports"


def _latest(base: Path, pattern: str) -> Path | None:
    cands = sorted(base.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return cands[0] if cands else None


def _load_json(path: Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _build_summary(date_tag: str, *, reports_dir: Path, final_precheck_path: Path | None = None) -> dict[str, Any]:
    final_precheck_path = final_precheck_path or _latest(reports_dir, "day5-final-precheck-runner-*.json")
    artifact_lock_path = _latest(reports_dir, "day5-artifact-lock-*.json")
    day4_gate_path = _latest(reports_dir, "day4-gate-report-*.json")

    final_precheck = _load_json(final_precheck_path)
    artifact_lock = _load_json(artifact_lock_path)
    day4_gate = _load_json(day4_gate_path)

    precheck_decision = (final_precheck or {}).get("decision", "unknown")
    day4_decision = (day4_gate or {}).get("go_no_go", (day4_gate or {}).get("decision", "unknown"))
    release_tag = (artifact_lock or {}).get("release_tag", "unknown")
    backend_digest = (artifact_lock or {}).get("backend_image_digest", (artifact_lock or {}).get("backend_digest", "unknown"))
    frontend_checksum = (artifact_lock or {}).get(
        "frontend_package_checksum", (artifact_lock or {}).get("frontend_checksum", "unknown")
    )
    config_count = len((artifact_lock or {}).get("config_snapshot", (artifact_lock or {}).get("config_snapshots", [])))
    steps = (final_precheck or {}).get("steps", [])
    failed_steps = [s.get("name", "?") for s in steps if not s.get("ok", False)]
    total_duration_seconds = round(sum(float(s.get("duration_seconds", 0)) for s in steps), 3)
    total_retries = int(sum(int(s.get("retries", 0)) for s in steps))
    owner_mapping = {
        "pytest_day3_gate": "测试值班",
        "day4_gate_runner": "后端值班",
        "day5_artifact_lock": "发布总指挥",
        "day5_release_prep": "发布总指挥",
        "day5_release_finalize": "发布总指挥",
        "day5_management_summary": "项目经理",
    }
    step_execution = []
    for s in steps:
        step_execution.append(
            {
                "step": s.get("name"),
                "ok": bool(s.get("ok", False)),
                "exit_code": int(s.get("exit_code", -1)),
                "duration_seconds": float(s.get("duration_seconds", 0)),
                "retries": int(s.get("retries", 0)),
                "owner": owner_mapping.get(str(s.get("name")), "未分配"),
            }
        )

    # 管理摘要用于归档与汇报，不应被历史一次失败的“摘要步骤自身”反向阻塞。
    overall = "Go" if day4_decision == "Go" and artifact_lock is not None else "No-Go"
    now = datetime.now().isoformat()
    return {
        "title": "Week1 Day5 Management Summary",
        "date": date_tag,
        "generated_at": now,
        "overall_decision": overall,
        "signals": {
            "day5_final_precheck_decision": precheck_decision,
            "day4_gate_decision": day4_decision,
            "artifact_lock_ready": artifact_lock is not None,
        },
        "release": {
            "release_tag": release_tag,
            "backend_digest": backend_digest,
            "frontend_checksum": frontend_checksum,
            "config_snapshot_count": config_count,
        },
        "execution_metrics": {
            "step_count": len(steps),
            "total_duration_seconds": total_duration_seconds,
            "total_retries": total_retries,
        },
        "step_execution": step_execution,
        "risk_items": [
            "继续观察发布窗口内5xx与P95延迟抖动",
            "确认值班主备联系方式在窗口开始前二次核验",
            "若关键接口连续失败，按Runbook触发回滚",
        ],
        "owner_actions": [
            {"owner": "发布总指挥", "action": "确认Go/No-Go与执行口径一致", "due": "发布窗口前"},
            {"owner": "后端值班", "action": "复核健康检查与关键API探活", "due": "T+0"},
            {"owner": "安全值班", "action": "复核拒绝码与审计一致性", "due": "T+0"},
        ],
        "failed_steps": failed_steps,
        "source_files": {
            "final_precheck_report": str(final_precheck_path) if final_precheck_path else None,
            "day4_gate_report": str(day4_gate_path) if day4_gate_path else None,
            "artifact_lock_report": str(artifact_lock_path) if artifact_lock_path else None,
        },
    }


def _to_md(summary: dict[str, Any]) -> str:
    release = summary["release"]
    signals = summary["signals"]
    is_go = summary["overall_decision"] == "Go"
    lines = [
        f"# 首周总结与下周节奏建议（{summary['date']}）",
        "",
        f"- generated_at: `{summary['generated_at']}`",
        f"- overall_decision: **{summary['overall_decision']}**",
        "",
        "## 核心结论",
        "",
        f"- Day5 Final Precheck：`{signals['day5_final_precheck_decision']}`",
        f"- Day4 Gate：`{signals['day4_gate_decision']}`",
        f"- 工件锁定：`{'ready' if signals['artifact_lock_ready'] else 'missing'}`",
        "",
        "## 发布基线",
        "",
        f"- release_tag: `{release['release_tag']}`",
        f"- backend_digest: `{release['backend_digest']}`",
        f"- frontend_checksum: `{release['frontend_checksum']}`",
        f"- config_snapshot_count: `{release['config_snapshot_count']}`",
        "",
        "## 执行态指标",
        "",
        f"- step_count: `{summary['execution_metrics']['step_count']}`",
        f"- total_duration_seconds: `{summary['execution_metrics']['total_duration_seconds']}`",
        f"- total_retries: `{summary['execution_metrics']['total_retries']}`",
        "",
        "## 下周建议节奏",
        "",
        "- 周一：执行一次全链路演练并复核阈值告警",
        "- 周二~周三：按日做窗口前巡检与风险闭环",
        "- 周四：完成一次回滚演练抽检与SLA复盘",
        "",
        "## 风险关注",
        "",
    ]
    if not is_go:
        lines.extend(
            [
                "- 当前为 No-Go：冻结扩流与发布动作，先处理阻断项",
                "- 触发应急会议：发布总指挥 + 后端 + 安全 + 测试",
                "- 完成阻断项修复后，重新执行 Day5 预检总控",
                "",
            ]
        )
    lines.extend([f"- {x}" for x in summary["risk_items"]])
    lines.extend(
        [
            "",
            "## 责任人与截止",
            "",
        ]
    )
    for item in summary["owner_actions"]:
        lines.append(f"- {item['owner']}：{item['action']}（截止：{item['due']}）")
    lines.extend(["", "## 步骤执行详情", ""])
    for step in summary["step_execution"]:
        lines.append(
            f"- {step['step']}｜owner={step['owner']}｜ok={step['ok']}｜"
            f"exit={step['exit_code']}｜duration={step['duration_seconds']}s｜retries={step['retries']}"
        )
    if summary["failed_steps"]:
        lines.extend(["", "## 失败步骤", ""])
        lines.extend([f"- {name}" for name in summary["failed_steps"]])
    return "\n".join(lines) + "\n"


def _broadcast_text(summary: dict[str, Any], *, style: str) -> str:
    decision = summary["overall_decision"]
    is_go = decision == "Go"
    icon = "🟢" if is_go else "🔴"
    action = "按计划进入发布窗口" if is_go else "暂停发布并处理阻断项"
    release = summary["release"]
    signals = summary["signals"]
    if style == "wechat":
        return (
            f"{icon}【Day5管理层摘要】\n"
            f"结论：{decision}\n"
            f"Day4门禁：{signals['day4_gate_decision']}；Day5预检：{signals['day5_final_precheck_decision']}\n"
            f"版本：{release['release_tag']}\n"
            f"工件：backend={release['backend_digest']}；frontend={release['frontend_checksum']}\n"
            f"动作：{action}"
        )
    return (
        f"{icon} **Day5管理层摘要**\n"
        f"- 结论：**{decision}**\n"
        f"- Day4门禁：`{signals['day4_gate_decision']}`；Day5预检：`{signals['day5_final_precheck_decision']}`\n"
        f"- 版本：`{release['release_tag']}`\n"
        f"- 工件：`backend={release['backend_digest']}`；`frontend={release['frontend_checksum']}`\n"
        f"- 动作：{action}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Week1 Day5 management summary from latest reports.")
    parser.add_argument("--date", default=datetime.now().strftime("%Y%m%d"), help="Date tag, e.g. 20260417")
    parser.add_argument("--reports-dir", type=Path, default=_reports_dir(), help="Reports directory")
    parser.add_argument("--docs-dir", type=Path, default=_docs_dir(), help="Docs output directory")
    parser.add_argument(
        "--final-precheck-report",
        type=Path,
        default=None,
        help="Optional explicit day5-final-precheck-runner JSON path.",
    )
    args = parser.parse_args()

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    args.docs_dir.mkdir(parents=True, exist_ok=True)

    summary = _build_summary(args.date, reports_dir=args.reports_dir, final_precheck_path=args.final_precheck_report)
    out_json = args.reports_dir / f"day5-management-summary-{args.date}.json"
    out_md = args.docs_dir / f"WEEK1_SUMMARY_AND_NEXT_WEEK_PLAN_{args.date}_auto.md"
    out_wechat = args.reports_dir / f"day5-management-summary-broadcast-wechat-{args.date}.txt"
    out_feishu = args.reports_dir / f"day5-management-summary-broadcast-feishu-{args.date}.md"
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_to_md(summary), encoding="utf-8")
    out_wechat.write_text(_broadcast_text(summary, style="wechat") + "\n", encoding="utf-8")
    out_feishu.write_text(_broadcast_text(summary, style="feishu") + "\n", encoding="utf-8")

    print(f"summary_json: {out_json}")
    print(f"summary_md: {out_md}")
    print(f"broadcast_wechat: {out_wechat}")
    print(f"broadcast_feishu: {out_feishu}")
    print(f"decision: {summary['overall_decision']}")
    return 0 if summary["overall_decision"] == "Go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
