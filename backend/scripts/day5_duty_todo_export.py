from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.day5_duty_schedule_check import check_schedule


def _repo_root() -> Path:
    return ROOT


def _default_docs_dir() -> Path:
    return _repo_root().parent / "docs"


def _default_schedule_path() -> Path:
    return _default_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md"


def _default_template_path() -> Path:
    return _default_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_TEMPLATE_v1.0.md"


def _category_owner(category: str) -> tuple[str, str]:
    mapping = {
        "值班排班": ("发布总指挥", "P0"),
        "升级链路": ("发布总指挥", "P0"),
        "窗口前确认": ("运维值班", "P0"),
        "签字确认": ("各线负责人", "P1"),
        "交接记录": ("当班值班负责人", "P1"),
        "事件处理": ("当班值班负责人", "P1"),
        "其他": ("发布总指挥", "P2"),
    }
    return mapping.get(category, ("发布总指挥", "P2"))


def _build_markdown(report: dict[str, Any], schedule_path: Path) -> str:
    now = datetime.now()
    grouped = report.get("remaining_grouped") or {}
    remaining = int(report.get("schedule_placeholder_remaining") or 0)
    status = str(report.get("status") or "UNKNOWN")

    lines: list[str] = []
    lines.append("# Day5 值班排班待填分派清单（自动生成）")
    lines.append("")
    lines.append(f"- 生成时间: `{now.strftime('%Y-%m-%d %H:%M:%S')}`")
    lines.append(f"- 来源排班表: `{schedule_path}`")
    lines.append(f"- 检查状态: `{status}`")
    lines.append(f"- 待填项总数: `{remaining}`")
    lines.append("")

    if remaining == 0:
        lines.append("排班表已完整，无待分派事项。")
        lines.append("")
        return "\n".join(lines)

    lines.append("## 分派总览")
    lines.append("")
    lines.append("| 分类 | 数量 | 建议负责人 | 优先级 |")
    lines.append("|---|---:|---|---|")
    for category in sorted(grouped.keys()):
        owner, priority = _category_owner(category)
        lines.append(f"| {category} | {len(grouped[category])} | {owner} | {priority} |")
    lines.append("")

    lines.append("## 明细任务")
    lines.append("")
    lines.append("| ID | 分类 | 待填项 | 建议负责人 | 优先级 | 状态 |")
    lines.append("|---|---|---|---|---|---|")
    idx = 1
    for category in sorted(grouped.keys()):
        owner, priority = _category_owner(category)
        for item in grouped[category]:
            task_id = f"D5-TODO-{idx:03d}"
            lines.append(f"| {task_id} | {category} | `{item}` | {owner} | {priority} | 待办 |")
            idx += 1
    lines.append("")
    lines.append("## 执行建议")
    lines.append("")
    lines.append("- 先清空 `P0`（值班排班、升级链路、窗口前确认），再处理 `P1/P2`。")
    lines.append("- 每次修改排班表后重新运行 `day5_duty_schedule_check.py`，直到状态为 `READY`。")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Day5 duty schedule TODO assignment checklist.")
    parser.add_argument("--schedule", type=Path, default=_default_schedule_path(), help="Filled schedule markdown path.")
    parser.add_argument("--template", type=Path, default=_default_template_path(), help="Template markdown path.")
    parser.add_argument("--output-dir", type=Path, default=_default_docs_dir(), help="Output directory for checklist.")
    args = parser.parse_args()

    report = check_schedule(args.schedule, args.template)
    if report.get("status") == "ERROR":
        print(f"ERROR: {report.get('error')}")
        return 2

    content = _build_markdown(report, schedule_path=args.schedule)
    now = datetime.now()
    output = args.output_dir / f"D5_DUTY_SCHEDULE_TODO_{now.strftime('%Y%m%d')}_auto.md"
    output.write_text(content, encoding="utf-8")
    print(f"todo_checklist: {output}")
    print(f"status: {report.get('status')}")
    print(f"remaining: {report.get('schedule_placeholder_remaining')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
