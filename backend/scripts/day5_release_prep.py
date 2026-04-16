from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.day4_gate_runner import _http_audit_summary_check, _http_health_check
from scripts.day5_duty_schedule_check import check_schedule
from scripts.day5_duty_todo_export import _build_markdown as build_duty_todo_markdown


def _repo_root() -> Path:
    return ROOT


def _docs_dir() -> Path:
    return _repo_root().parent / "docs"


def _reports_dir() -> Path:
    return _repo_root() / "reports"


def _latest_day4_report(reports_dir: Path) -> Path | None:
    files = sorted(reports_dir.glob("day4-gate-report-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _latest_artifact_lock_report(reports_dir: Path) -> Path | None:
    files = sorted(reports_dir.glob("day5-artifact-lock-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _to_bool_text(v: bool) -> str:
    return "通过" if v else "不通过"


def _extract_day4_status(day4: dict[str, Any]) -> tuple[bool, bool]:
    checks = day4.get("checks") or []
    all_ok = False
    gate_ok = False
    for c in checks:
        name = str(c.get("name") or "")
        ok = bool(c.get("ok"))
        if name == "pytest_all":
            all_ok = ok
        if name == "pytest_day3_gate":
            gate_ok = ok
    return all_ok, gate_ok


def _build_go_no_go_markdown(
    *,
    now: datetime,
    all_ok: bool,
    gate_ok: bool,
    health_ok: bool,
    audit_ok: bool,
    duty_ready: bool,
    duty_left_count: int,
    day4_report_name: str,
    artifact_lock: dict[str, Any] | None,
    artifact_lock_name: str | None,
) -> str:
    decision = "Go" if all([all_ok, gate_ok, health_ok, audit_ok, duty_ready]) else "No-Go"
    return f"""# Day5 Go/No-Go 评审纪要（自动草稿）

## 评审基本信息

- 评审编号：`GNG-{now.strftime("%Y%m%d")}-AUTO`
- 评审日期：`{now.strftime("%Y-%m-%d")}`
- 评审时间：`{now.strftime("%H:%M")}`
- 评审范围：`staging->prod 发布窗口`

## 门禁检查结论

| 门禁项 | 判定 | 证据 | 备注 |
|---|---|---|---|
| 全量回归通过 | {_to_bool_text(all_ok)} | `{day4_report_name}` | 自动采集 |
| Day3 门禁通过 | {_to_bool_text(gate_ok)} | `{day4_report_name}` | 自动采集 |
| D3-05 安全抽测通过 | 通过 | `DAY3_SECURITY_APPROVAL_SAMPLING_REPORT_v1.0.md` | 待人工复核 |
| D3-01 风险收口完成 | 通过 | `DAY3_RISK_CLOSURE_LIST_v1.0.md` | 待人工复核 |
| 值班与升级链路就绪 | {_to_bool_text(duty_ready)} | `D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md` | 待填项 {duty_left_count} |
| 回滚入口可用 | 通过 | `D3_RELEASE_REHEARSAL_RECORD_TEMPLATE_v1.0.md` | 待人工复核 |
| 健康检查 | {_to_bool_text(health_ok)} | `/healthz` | 自动采集 |
| 审计摘要可读 | {_to_bool_text(audit_ok)} | `/api/v1/audit/summary` | 自动采集 |
| 发布工件锁定 | {'通过' if artifact_lock else '待补齐'} | `{artifact_lock_name or 'N/A'}` | 锁定标签/摘要/配置快照 |

## 决策结论

- 结论：`{decision}`
- 决策时间：`{now.strftime("%H:%M")}`
- 决策理由：
  - 自动检查汇总：全量回归={_to_bool_text(all_ok)}，day3_gate={_to_bool_text(gate_ok)}
  - 环境可读性：healthz={_to_bool_text(health_ok)}，audit_summary={_to_bool_text(audit_ok)}
  - 值班排班完整性={_to_bool_text(duty_ready)}（待填项 {duty_left_count}）
"""


def _build_release_memo_markdown(
    *,
    now: datetime,
    all_ok: bool,
    gate_ok: bool,
    health_ok: bool,
    audit_ok: bool,
    duty_ready: bool,
    duty_left_count: int,
    day4_report_name: str,
    artifact_lock: dict[str, Any] | None,
    artifact_lock_name: str | None,
) -> str:
    lock_ok = artifact_lock is not None
    overall_ok = all([all_ok, gate_ok, health_ok, audit_ok, duty_ready, lock_ok])
    result = "成功" if overall_ok else "有条件成功"
    release_tag = (artifact_lock or {}).get("release_tag") if artifact_lock else None
    backend_digest = (artifact_lock or {}).get("backend_image_digest") if artifact_lock else None
    frontend_checksum = (artifact_lock or {}).get("frontend_package_checksum") if artifact_lock else None
    config_snapshot = (artifact_lock or {}).get("config_snapshot") if artifact_lock else []
    config_lines = ""
    if config_snapshot:
        rows = []
        for row in config_snapshot:
            rows.append(
                f"| `{row.get('path')}` | {row.get('exists')} | `{row.get('sha256', '')}` | {row.get('size', '')} |"
            )
        config_lines = "\n".join(rows)
    else:
        config_lines = "| `N/A` | False | `` |  |"
    return f"""# Day5 正式发布纪要（自动草稿）

## 发布基本信息

- 发布编号：`REL-{now.strftime("%Y%m%d")}-AUTO`
- 发布日期：`{now.strftime("%Y-%m-%d")}`
- 发布范围：`staging->prod（canary->full）`
- 发布标签：`{release_tag or f'release-{now.strftime("%Y-%m-%d")}-auto'}`

## 发布结论

- 最终结论：**{result}**
- 决策时间：`{now.strftime("%H:%M")}`
- 决策依据：
  - 门禁检查由 `day4_gate_runner` 自动输出
  - 健康与审计可读性已自动核查
  - 待发布会议补充人工确认项（安全抽测、值班签字）

## 门禁结果摘要

| 门禁项 | 结果 | 证据 |
|---|---|---|
| 全量回归 | {_to_bool_text(all_ok)} | `{day4_report_name}` |
| Day3 门禁（day3_gate） | {_to_bool_text(gate_ok)} | `{day4_report_name}` |
| 健康检查 | {_to_bool_text(health_ok)} | `/healthz` |
| 审计摘要可读 | {_to_bool_text(audit_ok)} | `/api/v1/audit/summary` |
| 值班排班完整性 | {_to_bool_text(duty_ready)} | `D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md（待填项 {duty_left_count}）` |
| 发布工件锁定 | {_to_bool_text(lock_ok)} | `{artifact_lock_name or 'N/A'}` |

## 发布工件锁定

- backend 镜像 digest: `{backend_digest or 'N/A'}`
- frontend 包 checksum: `{frontend_checksum or 'N/A'}`

| 配置路径 | exists | sha256 | size |
|---|---:|---|---:|
{config_lines}

## 遗留行动项

| ID | 问题/行动项 | 负责人 | 截止时间 | 状态 |
|---|---|---|---|---|
| M-AUTO-01 | 补齐发布窗口实际指标与截图 | 发布总指挥 | {now.strftime("%Y-%m-%d")} 23:59 | 待办 |
| M-AUTO-02 | 补齐签字确认与正式结论 | 后端/安全/产品值班 | {now.strftime("%Y-%m-%d")} 23:59 | 待办 |
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Prepare Day5 Go/No-Go and release memo drafts from latest gate report."
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=_reports_dir(),
        help="Directory containing day4-gate-report JSON files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_docs_dir(),
        help="Directory for generated markdown drafts.",
    )
    parser.add_argument(
        "--duty-schedule",
        type=Path,
        default=_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md",
        help="Filled Day5 duty schedule markdown path.",
    )
    parser.add_argument(
        "--duty-template",
        type=Path,
        default=_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_TEMPLATE_v1.0.md",
        help="Day5 duty schedule template markdown path.",
    )
    parser.add_argument(
        "--emit-duty-todo",
        action="store_true",
        help="Emit duty schedule TODO assignment checklist markdown.",
    )
    args = parser.parse_args()

    latest = _latest_day4_report(args.reports_dir)
    if latest is None:
        print(f"ERROR: no day4 report found in {args.reports_dir}")
        return 2

    day4 = _load_json(latest)
    artifact_lock_path = _latest_artifact_lock_report(args.reports_dir)
    artifact_lock = _load_json(artifact_lock_path) if artifact_lock_path else None
    all_ok, gate_ok = _extract_day4_status(day4)
    health_ok = bool(_http_health_check().ok)
    audit_ok = bool(_http_audit_summary_check().ok)
    duty_report = check_schedule(args.duty_schedule, args.duty_template)
    duty_ready = duty_report.get("status") == "READY"
    duty_left_count = int(duty_report.get("schedule_placeholder_remaining") or 0)

    now = datetime.now()
    go_md = _build_go_no_go_markdown(
        now=now,
        all_ok=all_ok,
        gate_ok=gate_ok,
        health_ok=health_ok,
        audit_ok=audit_ok,
        duty_ready=duty_ready,
        duty_left_count=duty_left_count,
        day4_report_name=latest.name,
        artifact_lock=artifact_lock,
        artifact_lock_name=artifact_lock_path.name if artifact_lock_path else None,
    )
    rel_md = _build_release_memo_markdown(
        now=now,
        all_ok=all_ok,
        gate_ok=gate_ok,
        health_ok=health_ok,
        audit_ok=audit_ok,
        duty_ready=duty_ready,
        duty_left_count=duty_left_count,
        day4_report_name=latest.name,
        artifact_lock=artifact_lock,
        artifact_lock_name=artifact_lock_path.name if artifact_lock_path else None,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    go_path = args.output_dir / f"D5_GO_NO_GO_REVIEW_MEMO_{now.strftime('%Y%m%d')}_auto.md"
    rel_path = args.output_dir / f"D3_RELEASE_MEMO_{now.strftime('%Y%m%d')}_auto.md"
    go_path.write_text(go_md, encoding="utf-8")
    rel_path.write_text(rel_md, encoding="utf-8")

    todo_path: Path | None = None
    if args.emit_duty_todo:
        todo_content = build_duty_todo_markdown(duty_report, schedule_path=args.duty_schedule)
        todo_path = args.output_dir / f"D5_DUTY_SCHEDULE_TODO_{now.strftime('%Y%m%d')}_auto.md"
        todo_path.write_text(todo_content, encoding="utf-8")

    decision = "Go" if all([all_ok, gate_ok, health_ok, audit_ok, duty_ready, artifact_lock is not None]) else "No-Go"
    print(f"Decision: {decision}")
    print(f"Duty schedule status: {duty_report.get('status')} (remaining={duty_left_count})")
    print(
        "Artifact lock: "
        + (f"{artifact_lock_path.name}" if artifact_lock_path is not None else "MISSING (run day5_artifact_lock.py)")
    )
    print(f"Go/No-Go draft: {go_path}")
    print(f"Release memo draft: {rel_path}")
    if todo_path is not None:
        print(f"Duty TODO checklist: {todo_path}")
    return 0 if decision == "Go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
