# API变更日志 - 纪光元生智能系统

| 文档版本 | 修改日期 | 修改人 | 修改内容 |
|---------|---------|--------|---------|
| v1.0 | 2026-01-20 | AI助手 | 初始版本，基于通用能力模块整合优化 |

---

## 一、概述

### 1.1 文档说明

本文档记录纪光元生智能系统（JYIS）API的所有版本变更，包含新增API端点、废弃API端点、参数变更、响应格式变更及迁移指南。所有API端点均与 `AGENT_ABILITY_SPEC_v1.0.md` 中定义的通用能力对齐。

### 1.2 版本规则

版本格式：`v{major}.{minor}.{patch}`

| 类型 | 说明 | 示例 |
|------|------|------|
| major | 不兼容的重大变更（如权限模型变更、核心API重构） | v1.0.0 → v2.0.0 |
| minor | 向后兼容的功能新增（新增端点或可选字段） | v1.0.0 → v1.1.0 |
| patch | 向后兼容的问题修复（Bug修复、性能优化） | v1.0.0 → v1.0.1 |

### 1.3 API版本策略

- API路径中包含版本号：`/api/v1/xxx`
- 每个大版本至少维护6个月
- 废弃API提前3个月通过 `Deprecation` Header 和文档发布通知

---

## 二、v1.0.0（当前版本）

**发布日期**：2026-01-20

### 2.1 新增API

#### 认证模块（对齐 SC-04, SC-20）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| POST | `/api/v1/auth/login` | 用户登录 | SC-20 访问令牌管理 |
| POST | `/api/v1/auth/register` | 用户注册 | SC-04 权限检查 |
| POST | `/api/v1/auth/refresh` | 刷新令牌 | SC-20 访问令牌管理 |
| POST | `/api/v1/auth/logout` | 退出登录 | SC-20 访问令牌管理 |
| GET | `/api/v1/auth/me` | 获取当前用户信息 | SC-04 权限检查 |

#### 智能体管理（对齐 AGENT-RUNTIME, HR-01, META-05）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/agents` | 获取智能体列表 | AGENT-RUNTIME-06 心智模型维护 |
| GET | `/api/v1/agents/{id}` | 获取智能体详情 | HR-03 人事绩效评估 |
| POST | `/api/v1/agents` | 创建智能体 | HR-01 智能体创建与配置 |
| PUT | `/api/v1/agents/{id}` | 更新智能体 | HR-01 智能体创建与配置 |
| DELETE | `/api/v1/agents/{id}` | 删除智能体 | - |
| GET | `/api/v1/agents/{id}/skills` | 获取智能体技能 | META-01 能力扩展 |
| PUT | `/api/v1/agents/{id}/skills` | 更新智能体技能 | META-01 能力扩展 |
| GET | `/api/v1/agents/{id}/memory` | 获取智能体记忆 | MM-04 记忆检索 |
| GET | `/api/v1/agents/{id}/stats` | 获取智能体统计 | HR-03 人事绩效评估 |
| PUT | `/api/v1/agents/{id}/config` | 更新智能体配置 | HR-01 智能体创建与配置 |
| GET | `/api/v1/agents/org-tree` | 获取组织架构树 | AGENT-RUNTIME-06 心智模型维护 |

#### 项目管理（对齐 DC-01, DC-02, PM-01）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/projects` | 获取项目列表 | EX-03 API调用 |
| GET | `/api/v1/projects/{id}` | 获取项目详情 | - |
| POST | `/api/v1/projects` | 创建项目 | DC-01 任务规划 |
| PUT | `/api/v1/projects/{id}` | 更新项目 | - |
| DELETE | `/api/v1/projects/{id}` | 删除项目 | - |
| GET | `/api/v1/projects/{id}/tasks` | 获取项目任务列表 | DC-02 子任务分解 |
| GET | `/api/v1/projects/{id}/team` | 获取项目团队 | CL-03 消息通信 |
| GET | `/api/v1/projects/{id}/progress` | 获取项目进度 | CG-04 数值推理 |
| GET | `/api/v1/projects/{id}/export` | 导出项目报表 | EX-05 文件操作 |

#### 任务管理（对齐 DC-05, EX-10, AUTO-05）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/tasks` | 获取任务列表 | DC-05 优先级排序 |
| GET | `/api/v1/tasks/{id}` | 获取任务详情 | - |
| POST | `/api/v1/tasks` | 创建任务 | DC-02 子任务分解 |
| PUT | `/api/v1/tasks/{id}` | 更新任务 | - |
| DELETE | `/api/v1/tasks/{id}` | 删除任务 | - |
| POST | `/api/v1/tasks/{id}/assign` | 指派任务 | CL-01 任务委托范围 |
| GET | `/api/v1/tasks/schedule` | 获取调度配置 | AUTO-05 智能定时与触发任务 |
| PUT | `/api/v1/tasks/{id}/schedule` | 更新调度配置 | AUTO-05 智能定时与触发任务 |

#### 对话系统（对齐 PC-01, AGENT-RUNTIME-03, EM-13）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/chat/sessions` | 获取会话列表 | MM-02 短期记忆时长 |
| POST | `/api/v1/chat/sessions` | 创建会话 | MM-01 工作记忆容量 |
| GET | `/api/v1/chat/sessions/{id}/messages` | 获取会话消息 | MM-03 长期记忆 |
| POST | `/api/v1/chat/sessions/{id}/messages` | 发送消息（SSE流式） | PC-01 自然语言理解, EM-13 模型流式处理 |
| GET | `/api/v1/chat/history` | 获取对话历史 | MM-04 记忆检索 |
| GET | `/api/v1/chat/sessions/{id}/thinking` | 获取思考过程 | AGENT-RUNTIME-03 决策可解释性 |

#### 代码生成（对齐 EX-01, EX-02, SC-01）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| POST | `/api/v1/code/generate` | 生成代码 | EX-01 代码生成 |
| POST | `/api/v1/code/modify` | 修改代码 | EX-02 代码修改 |
| POST | `/api/v1/code/validate` | 验证代码 | SC-01 代码沙箱 |
| GET | `/api/v1/code/history` | 获取生成历史 | MM-03 长期记忆 |

#### 营销中心（对齐 MK-01~MK-30）

> 规范说明：基础URL固定包含 `/api/v1`，下表端点默认写相对路径，避免出现 `/api/v1/api/v1/...` 的重复前缀。

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/marketing/dashboard` | 获取营销数据 | CG-04 数值推理 |
| GET | `/api/v1/marketing/contents` | 获取内容列表 | FILE-01 多格式文档读写 |
| POST | `/api/v1/marketing/contents` | 创建内容 | MK-01 文本内容生成 |
| PUT | `/api/v1/marketing/contents/{id}` | 更新内容 | - |
| DELETE | `/api/v1/marketing/contents/{id}` | 删除内容 | - |
| POST | `/api/v1/marketing/ai/generate` | AI生成内容 | EM-01 多模型路由 |
| POST | `/api/v1/marketing/distribute` | 多平台分发 | WEB-05 社交媒体交互, EX-09 并行执行 |
| GET | `/api/v1/marketing/projects/matched` | 项目匹配筛选 | PC-02 代码理解, CG-01 推理能力 |
| POST | `/api/v1/marketing/quote/generate` | 生成报价方案 | DC-06 方案生成, DC-11 成本效益分析 |

#### 系统监控（对齐 AGENT-RUNTIME-04, AGENT-RUNTIME-05）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/system/status` | 获取系统状态 | AGENT-RUNTIME-04 元认知监控 |
| GET | `/api/v1/system/metrics` | 获取系统指标 | CG-04 数值推理 |
| GET | `/api/v1/system/resources` | 获取资源使用 | RS-01 资源分配 |
| GET | `/api/v1/system/alerts` | 获取告警列表 | AGENT-RUNTIME-05 健康自检与自愈 |
| POST | `/api/v1/system/alerts/rules` | 创建告警规则 | - |

#### 审批管理（对齐 APPROVE-01~APPROVE-06）

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v1/approvals/pending` | 获取待审批列表 | APPROVE-05 审批通知与待办管理 |
| POST | `/api/v1/approvals/{id}/approve` | 批准 | APPROVE-02 多级审批与流转 |
| POST | `/api/v1/approvals/{id}/reject` | 拒绝 | APPROVE-02 多级审批与流转 |
| POST | `/api/v1/approvals/applications` | 发起申请 | APPROVE-01 申请发起与申报 |

### 2.2 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2026-01-20T10:30:00Z",
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2.3 通用错误码

| 错误码 | 说明 | 关联通用能力 |
|--------|------|-------------|
| 10001 | 参数验证失败 | QL-04 质量自检 |
| 10002 | 资源不存在 | - |
| 10003 | 权限不足 | SC-04 权限检查 |
| 10004 | 认证失败 | SC-04 权限检查 |
| 10005 | Token过期 | SC-20 访问令牌管理 |
| 20001 | 智能体不存在 | - |
| 20002 | 智能体离线 | AGENT-RUNTIME-05 健康自检与自愈 |
| 30001 | 项目不存在 | - |
| 40001 | 模型调用失败 | EM-03 模型降级 |
| 50001 | 数据库错误 | - |
| 50002 | 内部服务错误 | - |
| 60001 | 并发配额不足 | EM-06 并发配额感知 |
| 60002 | 速率限制 | SC-06 速率限制 |

---

## 三、v1.1.0（计划中）

**预计发布日期**：2026-02-20

### 3.1 新增API

| 方法 | 端点 | 说明 | 关联通用能力 | 状态 |
|------|------|------|-------------|------|
| POST | `/api/v1/agents/batch` | 批量创建智能体 | EX-12 批量执行 | 计划中 |
| GET | `/api/v1/analytics/reports` | 获取分析报告 | QL-07 质量趋势分析 | 计划中 |
| POST | `/api/v1/webhooks` | 创建Webhook | WEB-04 API调用与集成 | 计划中 |
| GET | `/api/v1/audit/logs` | 获取审计日志 | SC-07 操作审计 | 计划中 |
| POST | `/api/v1/agents/{id}/reflect` | 触发自我反思 | AGENT-RUNTIME-11 自我反思 | 计划中 |

### 3.2 参数变更

| 端点 | 变更类型 | 变更内容 | 说明 |
|------|---------|---------|------|
| POST `/api/v1/projects` | 新增参数 | `tags` | 项目标签（对齐 FILE-04 分类） |
| GET `/api/v1/tasks` | 新增参数 | `assignee_id` | 按负责人筛选 |
| GET `/api/v1/agents` | 新增参数 | `capability_id` | 按能力ID筛选（对齐 META-05） |

### 3.3 响应变更

| 端点 | 变更类型 | 变更内容 |
|------|---------|---------|
| GET `/api/v1/agents` | 新增字段 | `tags`, `runtime_state.cognitive_load` |
| GET `/api/v1/projects/{id}` | 新增字段 | `tags`, `last_activity` |
| POST `/api/v1/chat/sessions/{id}/messages` | 新增事件 | `thinking_steps` (SSE) |

---

## 四、v2.0.0（计划中）

**预计发布日期**：2026-04-20

### 4.1 重大变更

#### 1. API路径变更

| v1.x | v2.0 | 说明 |
|------|------|------|
| `/api/v1/agents` | `/api/v2/agents` | 路径升级 |
| `/api/v1/projects` | `/api/v2/projects` | 路径升级 |
| `/api/v1/marketing/*` | `/api/v2/marketing/*` | 营销中心重构 |

#### 2. 响应格式变更

**v1.x格式**：
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

**v2.0格式**：
```json
{
  "status": "success",
  "code": 200,
  "message": "success",
  "data": {},
  "meta": {
    "version": "2.0.0",
    "request_id": "xxx",
    "timestamp": "2026-01-20T10:30:00Z"
  }
}
```

#### 3. 分页格式变更（对齐 EX-03 规范）

**v1.x格式**：
```json
{
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

**v2.0格式**：
```json
{
  "data": {
    "items": [],
    "pagination": {
      "total": 100,
      "current_page": 1,
      "per_page": 20,
      "total_pages": 5,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

### 4.2 废弃API

| 端点 | 替代方案 | 废弃时间 | 关联通用能力 |
|------|---------|---------|-------------|
| POST `/api/v1/auth/register` | POST `/api/v2/users` | 2026-04-20 | SC-04 权限检查 |
| GET `/api/v1/agents/{id}/memory` | GET `/api/v2/memories?agent_id={id}` | 2026-04-20 | MM-04 记忆检索 |

### 4.3 新增API

| 方法 | 端点 | 说明 | 关联通用能力 |
|------|------|------|-------------|
| GET | `/api/v2/users` | 用户列表 | SC-04 权限检查 |
| GET | `/api/v2/memories` | 统一记忆检索接口 | MM-04 记忆检索 |
| POST | `/api/v2/workflows` | 创建工作流 | AUTO-03 工作流自动化编排 |
| GET | `/api/v2/insights` | 获取智能洞察 | CG-01 推理能力, CG-06 因果推断 |
| POST | `/api/v2/counterfactual` | 反事实分析 | AGENT-RUNTIME-07 反事实思考 |

---

## 五、迁移指南

### 5.1 从v1.0.0迁移到v1.1.0

**向后兼容**：v1.1.0完全兼容v1.0.0，无需修改代码。

**新增功能**：
- 项目创建时可添加`tags`参数
- 任务列表支持`assignee_id`筛选
- 对话流式响应支持`thinking_steps`事件

### 5.2 从v1.x迁移到v2.0

**迁移步骤**：

1. **更新API路径**
   ```diff
   - fetch('/api/v1/agents')
   + fetch('/api/v2/agents')
   ```

2. **更新响应处理**
   ```javascript
   // v1.x
   const { code, data } = response;
   
   // v2.0
   const { status, code, data, meta } = response;
   ```

3. **更新分页处理**
   ```javascript
   // v1.x
   const { items, total, page } = data;
   
   // v2.0
   const { items, pagination } = data;
   const { current_page, total_pages, has_next } = pagination;
   ```

4. **替换废弃API**
   ```diff
   - POST /api/v1/auth/register
   + POST /api/v2/users
   
   - GET /api/v1/agents/{id}/memory
   + GET /api/v2/memories?agent_id={id}
   ```

### 5.3 迁移时间线

| 时间节点 | 事件 |
|---------|------|
| 2026-01-20 | v1.0.0发布 |
| 2026-02-20 | v1.1.0发布 |
| 2026-03-20 | 发布v1.x废弃通知 |
| 2026-04-20 | v2.0.0发布，v1.x进入维护模式 |
| 2026-07-20 | v1.x停止维护 |

---

## 六、API文档链接

| 环境 | Swagger UI | ReDoc |
|------|------------|-------|
| 开发环境 | https://dev.jyis.com/docs | https://dev.jyis.com/redoc |
| 测试环境 | https://test.jyis.com/docs | https://test.jyis.com/redoc |
| 生产环境 | https://api.jyis.com/docs | https://api.jyis.com/redoc |

---

## 七、变更通知

### 7.1 订阅变更通知

通过以下方式接收API变更通知：
- 邮件订阅：访问 `https://jyis.com/api/changes/subscribe`
- Webhook：配置接收地址（对齐 WEB-04 API调用与集成）
- RSS：`https://jyis.com/api/changes/rss`

### 7.2 变更日志格式

```json
{
  "version": "v1.1.0",
  "release_date": "2026-02-20",
  "type": "minor",
  "changes": [
    {
      "type": "added",
      "endpoint": "POST /api/v1/agents/batch",
      "description": "批量创建智能体",
      "related_ability": "EX-12"
    },
    {
      "type": "changed",
      "endpoint": "POST /api/v1/projects",
      "description": "新增tags参数",
      "related_ability": "FILE-04"
    }
  ],
  "breaking_changes": false,
  "migration_guide": null
}
```

---

**文档结束**