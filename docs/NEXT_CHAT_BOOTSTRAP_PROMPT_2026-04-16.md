# 下个对话初始提示词（可直接复制）

你现在接手项目 `JiGuang-YuanSheng-ZhiNeng-XiTong`，请严格按以下优先级继续推进并直接落地代码：

1. 优先保证 Git 自动化与远程同步机制持续可用；  
2. 在此基础上继续推进项目主线开发（后端优先）；  
3. 最后再做细节优化。

当前已完成状态（本轮新增）：
- 阶段生命周期能力已落地（后端 + 项目详情页 UI）：
  - `GET /api/v1/projects/{project_id}/stages` / `POST …/start|complete|approve` / `…/deliverables/{deliverable_name}`
  - StageEngine 支持：9 阶段定义、交付物必需校验、`complete->review`（需审批）、`approve` 后推进下一阶段
  - 交付物元数据已回填：`deliverables[].template/schema`
  - `participants[]` 与 `approval` 元数据已回填并在 `project.html` 展示（含条件审批提示）
- 审批治理闭环已增强：
  - 条件审批（P04）：新增项目 `budget` 字段，并按 `budget > 100000` 动态选择实际审批人（老板/L0 vs CEO/L1）
  - staging/prod：`approve/reject` 强制携带 `approver_role/approver_level`；dev 保持兼容（但一旦出现任一字段要求两者齐全）
  - `approval_history[]` 已落盘，项目页展示最近审批记录
  - `approve/reject` 成功会同步写入项目讨论 `[STAGE_APPROVAL]`，便于 discussion/audit/stage 三处互证
- 审计闭环：
  - 阶段动作 start/complete/approve/upload 会写 `project_stage_*` 审计事件（成功/失败均可追溯）
- 测试稳定性工程修复：
  - pytest 环境默认使用进程级临时 state 文件（避免并行写 `backend/data/state.json` 导致偶发 404）

请先阅读并基于以下文件继续：
- `docs/HANDOFF_2026-04-15_phase_update.md`（最新编号已到 144，包含每轮测试证据与字段口径）
- `backend/app/api/stages_router.py`
- `backend/app/services/project_stage_engine.py`
- `backend/web/project.html`
- `docs/PROJECT_LIFECYCLE_SPEC_v1.0.md`
- `docs/DEVELOPMENT_PLAN_v1.0.md`

执行要求：
- 直接编码，不要只给方案；
- 每完成一个阶段再输出交接包（变更文件、测试结果、下一步）；
- 默认不做无关重构；
- 若遇阻塞（权限/凭据/外部依赖），给出最小阻塞解法并继续可做部分；
- 每轮开始先 `git status --short`，避免提交 `backend/data/state.json` 或脚本日志噪音。

