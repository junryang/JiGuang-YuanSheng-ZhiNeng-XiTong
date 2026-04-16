# 下个对话初始提示词（前端科幻风统一，可直接复制）

你现在接手项目 `JiGuang-YuanSheng-ZhiNeng-XiTong`，请严格按以下优先级继续推进并直接落地代码：

1. 优先保证 Git 自动化与远程同步机制持续可用；
2. 在此基础上继续推进项目主线开发（后端优先，保持接口兼容）；
3. 本轮重点：新增并落地“前端界面科幻未来风格设计文件”，并应用到所有前端页面，确保视觉风格统一。

## 当前已完成状态（与本轮相关）

- 阶段生命周期后端能力已完整落地（stage 列表、动作、审批、交付物上传、健康检查、超时提醒）。
- 审计聚合能力已增强：
  - `GET /api/v1/audit/summary` 新增 `stage_timeout_hit_only / stage_timeout_env / stage_timeout_policy_id / stage_timeout_reason_code / stage_timeout_group_by`。
  - 返回新增 `stage_timeout_alert_total / hit_count / miss_count / hit_rate / env_breakdown / grouped`。
- 项目详情页已支持提醒统计查询：
  - 支持按环境、原因码、命中状态过滤；
  - 支持 `stage_timeout_group_by` 分组；
  - 支持分组简表展示与排序（`hit_rate_desc` / `total_desc`）；
  - 保留原始 JSON 折叠查看区，便于排查。
- 测试现状稳定：`test_ui_pages_smoke.py + test_api_smoke.py + test_project_stages_api.py` 已通过。

## 下个对话必须先做的事情（前端统一风格主线）

请先阅读并基于以下文件继续：
- `docs/DEVELOPMENT_PLAN_v1.0.md`
- `docs/PROJECT_LIFECYCLE_SPEC_v1.0.md`
- `backend/web/index.html`
- `backend/web/project.html`
- `backend/web/api-client.js`
- `backend/tests/test_ui_pages_smoke.py`

### 目标

在不破坏现有功能与交互的前提下，引入一套统一的“科幻未来风”前端设计体系，并覆盖所有现有前端页面（至少 `index.html`、`project.html`，以及其他 `backend/web/*.html` 页面）。

### 强制落地要求

- 必须新增独立风格文件（建议）：
  - `backend/web/styles/theme-future.css`（设计令牌、颜色、字体、阴影、动效、组件样式）
  - 如有必要可新增 `backend/web/styles/components-future.css`
- 所有页面统一引入该风格文件，不允许仅在单页内联样式“临时改色”。
- 定义并统一使用设计令牌（CSS Variables），至少包含：
  - `--bg-*`、`--surface-*`、`--text-*`、`--primary-*`、`--accent-*`、`--success-*`、`--warn-*`、`--danger-*`
  - `--border-*`、`--shadow-*`、`--radius-*`、`--space-*`、`--transition-*`
- 组件层统一（按钮、输入框、表格、卡片、pill、section、提示文本、code/pre 区域）。
- 兼容性要求：
  - 不改动现有 API 路由与页面逻辑；
  - 不删除既有 DOM id（避免破坏测试与脚本绑定）；
  - 保持可读性与对比度，避免炫光导致文本不可读；
  - 动效需克制，避免影响性能与操作可用性。

### 验收标准

- 视觉层：
  - 所有前端页面风格一致（色板、字体层级、组件形态一致）；
  - 页面不存在“旧风格残留块”或明显不一致组件。
- 功能层：
  - 所有原有页面功能可用，按钮/表单/表格交互不回归。
- 测试层：
  - 至少运行并通过：`python -m pytest tests/test_ui_pages_smoke.py`
  - 若涉及 API 联动页面，请补跑：`python -m pytest tests/test_api_smoke.py tests/test_project_stages_api.py`

### 执行纪律

- 直接编码，不只给方案；
- 每轮开始先 `git status --short`；
- 避免提交噪音文件（`backend/data/state.json`、脚本日志等）；
- 默认不做无关重构；
- 每完成一个阶段输出交接包（变更文件、测试结果、下一步）。
