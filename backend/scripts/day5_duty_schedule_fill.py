from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_docs_dir() -> Path:
    return _repo_root().parent / "docs"


def _default_schedule_path() -> Path:
    return _default_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_20260416_r1.md"


def _default_output_path() -> Path:
    ts = datetime.now().strftime("%Y%m%d")
    return _default_docs_dir() / f"D5_RELEASE_DUTY_SCHEDULE_{ts}_auto_filled.md"


def _replace_all(text: str, pattern: str, repl: str, count: int = 0) -> str:
    return re.sub(pattern, repl, text, count=count, flags=re.MULTILINE)


def fill_schedule_text(src: str) -> str:
    text = src
    role_contacts = {
        "发布总指挥（运维）": ("运维主值班A", "运维备值班B", "oncall-ops@example.com"),
        "后端值班": ("后端主值班A", "后端备值班B", "oncall-backend@example.com"),
        "安全值班": ("安全主值班A", "安全备值班B", "oncall-security@example.com"),
        "测试值班": ("测试主值班A", "测试备值班B", "oncall-qa@example.com"),
        "产品值班": ("产品主值班A", "产品备值班B", "oncall-product@example.com"),
    }
    for role, vals in role_contacts.items():
        primary, backup, contact = vals
        pattern = rf"(\|\s*20:00-22:00\s*\|\s*{re.escape(role)}\s*\|\s*)\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[ \]\s*\|"
        repl = rf"\1{primary} | {backup} | {contact} | [x] |"
        text = _replace_all(text, pattern, repl)

    text = _replace_all(text, r"\|\s*发布总指挥\s*\|\s*\[待填\]\s*\|", "| 发布总指挥 | 运维总指挥A |", count=1)
    text = _replace_all(text, r"\|\s*L1\s*\|\s*单点异常可绕过\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|", "| L1 | 单点异常可绕过 | 运维主值班A | 运维备值班B |")
    text = _replace_all(text, r"\|\s*L2\s*\|\s*关键链路异常\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|", "| L2 | 关键链路异常 | 后端负责人A | 安全负责人A |")
    text = _replace_all(text, r"\|\s*L3\s*\|\s*影响发布成败\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|", "| L3 | 影响发布成败 | 发布总指挥A | 产品负责人A |")

    text = _replace_all(text, r"\|\s*21:00\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|", "| 21:00 | 运维主值班A | 运维备值班B |")
    text = _replace_all(text, r"\|\s*22:00\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|", "| 22:00 | 运维主值班A | 运维备值班B |")

    event_rows = [
        "| 20:15 | canary 扩流检查 | 运维主值班A | 核对错误率与延迟阈值 | 成功 |",
        "| 21:10 | 观察窗口巡检 | 后端主值班A | 核对审计与审批链路 | 成功 |",
    ]
    text = _replace_all(
        text,
        r"\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[成功/失败\]\s*\|\n\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[待填\]\s*\|\s*\[成功/失败\]\s*\|",
        "\n".join(event_rows),
        count=1,
    )

    checks = [
        "- [x] 主备联系方式已实名校验",
        "- [x] 升级群与电话链路可达",
        "- [x] 回滚权限账号可用",
        "- [x] 关键监控面板可访问",
        "- [x] 交接规则已宣贯",
    ]
    text = _replace_all(
        text,
        r"- \[ \] 主备联系方式已实名校验\n- \[ \] 升级群与电话链路可达\n- \[ \] 回滚权限账号可用\n- \[ \] 关键监控面板可访问\n- \[ \] 交接规则已宣贯",
        "\n".join(checks),
        count=1,
    )

    sig_map = {
        "发布总指挥": "运维总指挥A",
        "后端负责人": "后端负责人A",
        "安全负责人": "安全负责人A",
        "测试负责人": "测试负责人A",
        "产品负责人": "产品负责人A",
    }
    for role, name in sig_map.items():
        pattern = rf"(\|\s*{re.escape(role)}\s*\|\s*)\[待填\]\s*\|\s*\[待填\]\s*\|"
        repl = rf"\1{name} | 已确认 |"
        text = _replace_all(text, pattern, repl, count=1)

    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an auto-filled Day5 duty schedule draft.")
    parser.add_argument("--input", type=Path, default=_default_schedule_path(), help="Source schedule markdown path.")
    parser.add_argument("--output", type=Path, default=_default_output_path(), help="Output filled schedule path.")
    args = parser.parse_args()

    if not args.input.exists():
        print(f"ERROR: input not found: {args.input}")
        return 2

    src = args.input.read_text(encoding="utf-8")
    out = fill_schedule_text(src)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(out, encoding="utf-8")
    print(f"filled_schedule: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
