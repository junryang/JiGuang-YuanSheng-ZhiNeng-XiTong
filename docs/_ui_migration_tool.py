# -*- coding: utf-8 -*-
"""Extract UI sections from UI_UX_DESIGN_v1.0.md into module files and rebuild slim master."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "UI_UX_DESIGN_v1.0.md"
lines = SRC.read_text(encoding="utf-8").splitlines(keepends=True)

# (out_name, start_line_1based, end_line_1based, header_lines)
MODULES = [
    (
        "UI_PM_CENTER_v1.0.md",
        124,
        683,
        [
            "# 项目管理中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第124–683行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载项目管理中心的 UI 设计。术语与层级以 `DOCUMENTATION_BASELINE_v1.0.md` 为准。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- API 路径规则以 `API_REFERENCE_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_FINANCE_CENTER_v1.0.md",
        685,
        1532,
        [
            "# 财务中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第685–1532行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载财务中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 安全与敏感数据展示以 `SECURITY_REQUIREMENTS_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_MARKETING_CENTER_v1.0.md",
        1818,
        2573,
        [
            "# 营销中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第1818–2573行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载营销中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- MK-01 等验收口径以 `PERFORMANCE_METRICS_v1.0.md` 与 `ACCEPTANCE_CHECKLIST_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_RESEARCH_CENTER_v1.0.md",
        2575,
        3302,
        [
            "# 市场调研中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第2575–3302行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载 AI 全领域市场调研中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 数据分析口径以 `DATA_ANALYTICS_INSIGHT_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_CAPABILITY_CENTER_v1.0.md",
        3304,
        4013,
        [
            "# 能力库与工具库中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第3304–4013行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载能力库与工具库中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 能力 ID 以 `AGENT_ABILITY_SPEC_v1.0.md` 为唯一基线。\n",
        ],
    ),
    (
        "UI_EXTERNAL_TOOLS_PERMISSIONS_v1.0.md",
        4020,
        5061,
        [
            "# 外部工具与权限管理界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第4020–5061行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载外部工具配置与人类员工权限管理界面。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 权限与审计以 `SECURITY_REQUIREMENTS_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_EXTERNAL_ACCOUNTS_CENTER_v1.0.md",
        5063,
        5641,
        [
            "# 外部平台账号管理中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第5063–5641行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载外部平台账号管理中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 多平台分发相关语义以 `MULTI_PLATFORM_DISTRIBUTION_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_SECURITY_CENTER_v1.0.md",
        5647,
        6318,
        [
            "# 系统安全中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第5647–6318行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载系统安全中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 安全策略以 `SECURITY_REQUIREMENTS_v1.0.md` 为准。\n",
        ],
    ),
    (
        "UI_AGENT_MANAGEMENT_CENTER_v1.0.md",
        6324,
        7117,
        [
            "# 智能体管理中心界面设计 v1.0\n",
            "\n",
            "> 迁移说明：本节正文自 `UI_UX_DESIGN_v1.0.md` 第6324–7117行提取。总文档中对应区块已替换为摘要与跳转。\n",
            "\n",
            "## 一、模块定位\n",
            "\n",
            "本文件承载智能体管理中心的 UI 设计。\n",
            "\n",
            "## 二、基线约束\n",
            "\n",
            "- 组织与智能体管理以 `AGENT_MANAGEMENT_MODULE_v1.0.md` 与 `AGENT_ORG_SPEC_v1.0.md` 为准。\n",
        ],
    ),
]


def slice_lines(a: int, b: int) -> list:
    """1-based inclusive line numbers."""
    return lines[a - 1 : b]


def write_module(path: Path, header: list, start: int, end: int) -> None:
    body = slice_lines(start, end)
    out = header + ["\n", "## 迁移正文\n", "\n"] + body
    path.write_text("".join(out), encoding="utf-8")


STUBS = [
    (
        "项目管理中心",
        "UI_PM_CENTER_v1.0.md",
        "项目全景、任务看板、甘特图、风险与项目团队协同等。",
    ),
    (
        "财务中心",
        "UI_FINANCE_CENTER_v1.0.md",
        "收支、成本、预算、模型费用、现金流、税务与对账等。",
    ),
    (
        "营销中心",
        "UI_MARKETING_CENTER_v1.0.md",
        "内容、分发、分析、竞品、接单、媒体与自动化等。",
    ),
    (
        "市场调研中心",
        "UI_RESEARCH_CENTER_v1.0.md",
        "全领域机会扫描、行业研究与报告生成等。",
    ),
    (
        "能力库与工具库中心",
        "UI_CAPABILITY_CENTER_v1.0.md",
        "能力盘点、工具与模型库、缺口通知主脑等。",
    ),
    (
        "外部工具与权限管理",
        "UI_EXTERNAL_TOOLS_PERMISSIONS_v1.0.md",
        "第三方工具连接、人类员工权限与审计等。",
    ),
    (
        "外部平台账号管理",
        "UI_EXTERNAL_ACCOUNTS_CENTER_v1.0.md",
        "各平台账号、健康度与监控等。",
    ),
    (
        "系统安全中心",
        "UI_SECURITY_CENTER_v1.0.md",
        "安全态势、威胁、漏洞、合规与访问控制等。",
    ),
    (
        "智能体管理中心",
        "UI_AGENT_MANAGEMENT_CENTER_v1.0.md",
        "智能体全生命周期、培训、绩效与动态处理等。",
    ),
]


def stub_block(title: str, file_name: str, desc: str) -> str:
    return (
        f"## [{title}]（已迁移至模块文档）\n\n"
        f"完整界面原型与说明见：`{file_name}`。\n\n"
        f"摘要：{desc}\n\n"
        "---\n\n"
    )


def build_slim_master() -> str:
    # Lines 1-123: preamble + 指挥舱 + duplicate title line
    head = "".join(lines[0:123])
    mid = "".join(lines[1532:1817])  # lines 1533-1817: 团队管理～对话流版本记录
    parts = [head]
    for t, fn, d in STUBS:
        parts.append(stub_block(t, fn, d))
    parts.append(mid)
    return "".join(parts)


def main() -> None:
    for name, start, end, header in MODULES:
        write_module(ROOT / name, header, start, end)
    slim = build_slim_master()
    bak = ROOT / "UI_UX_DESIGN_v1.0.archive_before_slim.md"
    if not bak.exists():
        bak.write_text(SRC.read_text(encoding="utf-8"), encoding="utf-8")
    SRC.write_text(slim, encoding="utf-8")
    print("OK: modules written and UI_UX_DESIGN_v1.0.md slimmed.")
    print(f"Backup: {bak.name}")


if __name__ == "__main__":
    main()
