# 下个对话初始提示词（可直接复制）

你现在接手项目 `JiGuang-YuanSheng-ZhiNeng-XiTong`，请严格按以下优先级继续推进并直接落地代码：

1. 优先保证 Git 自动化与远程同步机制持续可用；  
2. 在此基础上继续推进项目主线开发（后端优先）；  
3. 最后再做细节优化。

当前已完成状态：
- 远程仓库已建立并联通：`https://github.com/junryang/JiGuang-YuanSheng-ZhiNeng-XiTong`
- 自动化脚本已存在：
  - `scripts/setup_github_repo.ps1`
  - `scripts/git_sync_once.ps1`
  - `scripts/git_auto_sync.ps1`
- 风险闭环已增强：
  - `GET /api/v1/projects/{project_id}/progress` 已返回 `risk_summary` 与 `risk_alert_triggered`
  - 高风险会自动写入讨论提醒 `[PROJECT_RISK_ALERT]` 和审计事件 `project_risk_alert`

请先阅读并基于以下文件继续：
- `docs/HANDOFF_2026-04-15_phase_update.md`
- `docs/GIT_AUTOMATION_STANDARD_v1.0.md`
- `backend/app/api/routes.py`
- `backend/tests/test_progress_gantt.py`

执行要求：
- 直接编码，不要只给方案；
- 每完成一个阶段再输出交接包（变更文件、测试结果、下一步）；
- 默认不做无关重构；
- 若遇阻塞（权限/凭据/外部依赖），给出最小阻塞解法并继续可做部分。
