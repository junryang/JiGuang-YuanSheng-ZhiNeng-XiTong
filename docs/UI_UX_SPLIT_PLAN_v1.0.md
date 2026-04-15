# UI文档拆分计划 v1.0

## 一、目标

将 `UI_UX_DESIGN_v1.0.md` 从超长单体文档拆分为可维护的模块文档，降低重复标题、重复版本记录和跨模块冲突。

## 二、拆分原则

1. 保留 `UI_UX_DESIGN_v1.0.md` 作为总索引，不再承载大段模块细节。  
2. 每个业务中心独立一个文档，统一“概述/导航结构/角色权限/版本记录”模板。  
3. 模块文档更新必须遵循 `DOCUMENTATION_BASELINE_v1.0.md`。  
4. 验收、性能、接口口径不得在 UI 文档自定义，统一引用基线文档。  
5. 全局顶栏（壳导航）以 `UI_UX_DESIGN_v1.0.md`「全局壳导航规范」为准；各中心线框节选不视为缺入口。

## 三、拟拆分模块

- `UI_PM_CENTER_v1.0.md`：项目管理中心（项目全景、项目团队、风险协作）  
- `UI_FINANCE_CENTER_v1.0.md`：财务中心  
- `UI_MARKETING_CENTER_v1.0.md`：营销中心  
- `UI_RESEARCH_CENTER_v1.0.md`：市场调研中心  
- `UI_CAPABILITY_CENTER_v1.0.md`：能力库与工具库中心  
- `UI_EXTERNAL_TOOLS_PERMISSIONS_v1.0.md`：外部工具与人类员工权限  
- `UI_EXTERNAL_ACCOUNTS_CENTER_v1.0.md`：外部平台账号管理  
- `UI_SECURITY_CENTER_v1.0.md`：系统安全中心  
- `UI_AGENT_MANAGEMENT_CENTER_v1.0.md`：智能体管理中心

## 四、迁移步骤

1. 在新文档创建固定模板（概述、导航结构、角色权限、协作机制、版本记录）。  
2. 从原文档按模块复制内容，补充“来源区块”标记，避免遗漏。  
3. 在原文档保留模块摘要和跳转链接。  
4. 删除原文档中重复主标题与重复版本记录，仅保留全局版本记录。  
5. 对每个新文档执行一致性检查（术语、层级、能力ID、API前缀、验收口径）。  

## 五、完成标准

- 每个模块有独立文档且能被 `DOCS_MODULE_INDEX_v1.0.md` 检索。  
- 原 `UI_UX_DESIGN_v1.0.md` 总行数下降到 2000 行以内。  
- 不再出现重复主标题与多套冲突版本记录。  
- 与 `API_REFERENCE_v1.0.md`、`quality_standards.md`、`PERFORMANCE_METRICS_v1.0.md` 无冲突。

## 六、当前迁移进度（执行态）

### 已完成（第一批）

- [x] `UI_PM_CENTER_v1.0.md` 已创建
- [x] `UI_FINANCE_CENTER_v1.0.md` 已创建
- [x] `UI_MARKETING_CENTER_v1.0.md` 已创建
- [x] `UI_UX_DESIGN_v1.0.md` 已增加模块化迁移入口
- [x] `DOCS_MODULE_INDEX_v1.0.md` 已登记第一批模块文档

### 下一批（待执行）

- [x] `UI_RESEARCH_CENTER_v1.0.md`
- [x] `UI_CAPABILITY_CENTER_v1.0.md`
- [x] `UI_EXTERNAL_TOOLS_PERMISSIONS_v1.0.md`
- [x] `UI_EXTERNAL_ACCOUNTS_CENTER_v1.0.md`
- [x] `UI_SECURITY_CENTER_v1.0.md`
- [x] `UI_AGENT_MANAGEMENT_CENTER_v1.0.md`

## 七、执行约束（防回退）

1. 从本版本起，`UI_UX_DESIGN_v1.0.md` 仅新增“索引、摘要、迁移状态”，不再新增大段模块正文。  
2. 模块新增内容必须写入对应 `UI_*_CENTER_v1.0.md` 文件。  
3. 每次迁移后，必须更新 `UI_MIGRATION_WORKLOG_v1.0.md` 的状态看板。  
4. 如发现口径冲突，按 `DOCUMENTATION_BASELINE_v1.0.md` 裁决并在模块文档注明。  
5. 若需从归档恢复或重新生成总文档结构，可使用 `docs/_ui_migration_tool.py`（首次运行会备份 `UI_UX_DESIGN_v1.0.archive_before_slim.md`）。  

## 六、当前迁移进度（执行态）

### 已完成

- [x] 九个 `UI_*_CENTER_v1.0.md` 已写入完整迁移正文
- [x] `UI_UX_DESIGN_v1.0.md` 已精简为总入口（摘要+跳转，约 480 行）
- [x] `DOCS_MODULE_INDEX_v1.0.md` 已登记全部模块与归档说明
- [x] `UI_MIGRATION_WORKLOG_v1.0.md` 已更新为 content_done
