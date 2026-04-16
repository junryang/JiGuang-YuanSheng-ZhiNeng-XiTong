from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


PLACEHOLDER_PATTERN = re.compile(r"\[待填\]|\[ \]|^\s*-\s*\[\s\]\s", flags=re.MULTILINE)


def _default_schedule_path() -> Path:
    return Path(__file__).resolve().parents[2] / "docs" / "D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md"


def _default_template_path() -> Path:
    return Path(__file__).resolve().parents[2] / "docs" / "D5_RELEASE_DUTY_SCHEDULE_TEMPLATE_v1.0.md"


def _scan_placeholders(text: str) -> list[str]:
    lines = text.splitlines()
    issues: list[str] = []
    for i, line in enumerate(lines, start=1):
        if PLACEHOLDER_PATTERN.search(line):
            issues.append(f"L{i}: {line.strip()}")
    return issues


def _category_of_line(line: str) -> str:
    text = line.strip()
    if "发布总指挥" in text or "后端值班" in text or "安全值班" in text or "测试值班" in text or "产品值班" in text:
        return "值班排班"
    if "L1" in text or "L2" in text or "L3" in text or "升级" in text:
        return "升级链路"
    if "交接" in text:
        return "交接记录"
    if "事件" in text or "成功/失败" in text:
        return "事件处理"
    if text.startswith("- [ ]"):
        return "窗口前确认"
    if "签字" in text:
        return "签字确认"
    return "其他"


def check_schedule(schedule_path: Path, template_path: Path) -> dict[str, Any]:
    if not template_path.exists():
        return {"status": "ERROR", "error": f"template not found: {template_path}"}
    if not schedule_path.exists():
        return {"status": "ERROR", "error": f"schedule not found: {schedule_path}"}

    template_text = template_path.read_text(encoding="utf-8")
    schedule_text = schedule_path.read_text(encoding="utf-8")

    template_fields = len(_scan_placeholders(template_text))
    schedule_issues = _scan_placeholders(schedule_text)
    grouped: dict[str, list[str]] = {}
    for row in schedule_issues:
        _, _, line = row.partition(":")
        cat = _category_of_line(line)
        grouped.setdefault(cat, []).append(row)

    remaining = len(schedule_issues)
    return {
        "status": "READY" if remaining == 0 else "INCOMPLETE",
        "template_placeholder_count": template_fields,
        "schedule_placeholder_remaining": remaining,
        "remaining_placeholders": schedule_issues,
        "remaining_grouped": grouped,
        "schedule_path": str(schedule_path),
        "template_path": str(template_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Day5 duty schedule completeness.")
    parser.add_argument("--schedule", type=Path, default=_default_schedule_path(), help="Filled schedule markdown path.")
    parser.add_argument("--template", type=Path, default=_default_template_path(), help="Template markdown path.")
    parser.add_argument("--json", action="store_true", help="Print full JSON report.")
    args = parser.parse_args()

    report = check_schedule(args.schedule, args.template)
    if report.get("status") == "ERROR":
        print(f"ERROR: {report.get('error')}")
        return 2

    template_fields = int(report["template_placeholder_count"])
    schedule_fields_left = int(report["schedule_placeholder_remaining"])
    schedule_issues = list(report["remaining_placeholders"])
    grouped = dict(report["remaining_grouped"])

    print(f"template_placeholder_count: {template_fields}")
    print(f"schedule_placeholder_remaining: {schedule_fields_left}")
    if schedule_issues:
        print("remaining_placeholders:")
        for row in schedule_issues[:50]:
            print(f"  - {row}")
        if len(schedule_issues) > 50:
            print(f"  ... and {len(schedule_issues) - 50} more")
        print("grouped_summary:")
        for k in sorted(grouped.keys()):
            print(f"  - {k}: {len(grouped[k])}")
    if args.json:
        print("json_report:")
        print(json.dumps(report, ensure_ascii=False, indent=2))

    if schedule_fields_left > 0:
        print("status: INCOMPLETE")
        return 1

    print("status: READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
