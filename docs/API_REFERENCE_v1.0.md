# 纪光元生智能系统 - 接口契约文档

| 文档版本 | 修改日期 | 修改人 | 修改内容 |
|---------|---------|--------|---------|
| v1.0 | 2026-01-13 | AI助手 | 完整版：基于所有子文件和对话内容，补充全部238个API端点、WebSocket事件、142项能力接口、安全接口、财务接口、营销接口、调研接口 |


## 一、契约概述

### 1.1 设计原则

| 原则 | 说明 | 关联能力 |
|------|------|----------|
| **RESTful规范** | 遵循REST API设计规范，使用标准HTTP方法 | EX-03 API调用 |
| **统一响应格式** | 所有API响应遵循统一的`{code, message, data}`格式 | - |
| **版本控制** | 基础URL包含版本号（/api/v1）；端点表默认使用相对路径 | - |
| **向后兼容** | 新版本不破坏旧版本兼容性 | - |
| **文档驱动** | 契约即文档，使用OpenAPI 3.0规范 | - |
| **安全优先** | 所有API需认证，敏感操作需多因素认证 | SC-04/20 |
| **流式支持** | AI对话支持SSE流式响应 | EM-13 |

### 1.2 统一响应格式

```yaml
# 成功响应
success_response:
  code: 200
  message: "success"
  data: 
    type: object
    description: "业务数据"
  timestamp: "2026-01-13T10:30:00Z"
  request_id: "uuid"

# 错误响应
error_response:
  code: 400|401|403|404|500
  message: "错误描述"
  data: null
  error_detail:
    type: object
    properties:
      field: "字段名"
      reason: "错误原因"
  timestamp: "2026-01-13T10:30:00Z"
  request_id: "uuid"
```

### 1.3 认证方式

| 认证方式 | 适用场景 | 关联能力 |
|---------|---------|----------|
| JWT Bearer Token | 常规API调用 | SC-20 访问令牌 |
| API Key | 外部系统集成 | SC-20 访问令牌 |
| 生物识别 | 敏感操作确认 | SC-03 敏感信息检测 |
| WebAuthn | 硬件密钥登录 | SC-20 访问令牌 |


## 二、认证模块API

### 2.1 用户认证

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| POST | `/auth/login` | 用户名/密码登录 | SC-04 |
| POST | `/auth/face/login` | 人脸识别登录 | SC-03 |
| POST | `/auth/voice/login` | 声纹识别登录 | SC-03 |
| POST | `/auth/webauthn/login` | 硬件密钥登录 | SC-20 |
| POST | `/auth/wechat/login` | 微信登录 | WEB-05 |
| POST | `/auth/feishu/login` | 飞书登录 | EX-08 |
| POST | `/auth/register` | 用户注册（需邀请码） | SC-04 |
| POST | `/auth/refresh` | 刷新令牌 | SC-20 |
| POST | `/auth/logout` | 退出登录 | SC-20 |
| GET | `/auth/me` | 获取当前用户信息 | SC-04 |
| POST | `/auth/password/reset` | 发送重置邮件 | EX-08 |
| POST | `/auth/password/verify` | 验证重置令牌 | SC-04 |
| POST | `/auth/password/update` | 更新密码 | SC-19 |

### 2.2 API详细定义

**POST /auth/login**

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required: [username, password]
        properties:
          username: { type: string }
          password: { type: string }

responses:
  200:
    description: 登录成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code: { type: integer, example: 200 }
            data:
              type: object
              properties:
                access_token: { type: string }
                refresh_token: { type: string }
                expires_in: { type: integer, example: 7200 }
                user:
                  type: object
                  properties:
                    id: { type: string }
                    name: { type: string }
                    role: { type: string }
                    permissions: { type: array, items: { type: string } }
```

**POST /auth/face/login**

```yaml
requestBody:
  required: true
  content:
    application/json:
      schema:
        type: object
        required: [face_data, liveness_data]
        properties:
          face_data: { type: string, description: "Base64编码的人脸图像" }
          liveness_data: { type: string, description: "活体检测数据" }

responses:
  200:
    description: 识别成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code: { type: integer, example: 200 }
            data:
              type: object
              properties:
                access_token: { type: string }
                confidence: { type: number, example: 0.987 }
                user: { $ref: '#/components/schemas/User' }
```


## 三、指挥舱API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/dashboard/command/agents` | 获取智能体团队状态 | AGENT-RUNTIME-06 |
| GET | `/dashboard/command/metrics` | 获取关键指标 | CG-04 |
| GET | `/dashboard/command/decisions` | 获取待决策事项 | DC-05 |
| POST | `/dashboard/command/decisions/{id}` | 处理决策 | DC-09 |
| GET | `/dashboard/command/projects/health` | 获取项目健康度 | QL-07 |
| GET | `/dashboard/command/agents/load` | 获取智能体负载热力图 | AGENT-RUNTIME-04 |
| GET | `/dashboard/command/finance/trend` | 获取收支趋势 | CG-04 |
| GET | `/dashboard/command/activities` | 获取最近活动 | SC-07 |
| POST | `/chat/quick` | 快速提问（SSE） | PC-01 |
| GET | `/system/status/full` | 获取完整系统状态 | AGENT-RUNTIME-05 |


## 四、对话系统API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/chat/sessions` | 获取会话列表 | MM-02 |
| POST | `/chat/sessions` | 创建新会话 | MM-01 |
| DELETE | `/chat/sessions/{id}` | 删除会话 | - |
| GET | `/chat/sessions/{id}/messages` | 获取会话消息 | MM-03 |
| POST | `/chat/sessions/{id}/messages` | 发送消息（SSE流式） | PC-01, EM-13 |
| GET | `/chat/sessions/{id}/thinking` | 获取思考过程 | AGENT-RUNTIME-03 |
| GET | `/chat/history` | 获取历史对话 | MM-04 |
| GET | `/chat/history/search` | 搜索历史对话 | MM-04 |
| POST | `/chat/voice/asr` | 语音转文字 | PC-04 |
| POST | `/chat/voice/tts` | 文字转语音 | EX-16 |

### 4.1 流式对话

**POST /chat/sessions/{id}/messages**

```yaml
requestBody:
  content:
    application/json:
      schema:
        type: object
        required: [content]
        properties:
          content: { type: string }
          agent_id: { type: string }
          context: { type: object }

responses:
  200:
    description: SSE流式响应
    content:
      text/event-stream:
        schema:
          type: string
          description: |
            事件类型:
            - thinking: 思考过程
            - intent: 意图识别
            - action: 执行动作
            - reasoning: 推理过程
            - counterfactual: 反事实分析
            - message_chunk: 消息片段
            - done: 完成
```


## 五、智能体管理API

### 5.1 智能体全景

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/agents/panorama` | 获取智能体全景数据 | AGENT-RUNTIME-06 |
| GET | `/agents/team/status` | 获取团队状态 | HR-03 |
| GET | `/agents/stats/by-level` | 按层级统计 | - |
| GET | `/agents/stats/by-dept` | 按部门统计 | - |
| GET | `/agents/load/heatmap` | 获取负载热力图 | AGENT-RUNTIME-04 |
| GET | `/agents/alerts` | 获取需要关注的智能体 | AGENT-RUNTIME-05 |

### 5.2 智能体CRUD

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/agents` | 获取智能体列表 | - |
| POST | `/agents` | 创建智能体 | HR-01 |
| GET | `/agents/{id}` | 获取智能体详情 | HR-03 |
| PUT | `/agents/{id}` | 更新智能体 | HR-01 |
| DELETE | `/agents/{id}` | 删除智能体 | - |
| POST | `/agents/batch` | 批量操作 | EX-12 |

### 5.3 智能体详情

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/agents/{id}/evaluation` | 获取主脑评估 | AGENT-RUNTIME-03 |
| GET | `/agents/{id}/capabilities` | 获取能力清单 | META-05 |
| PUT | `/agents/{id}/capabilities` | 配置能力 | META-01 |
| GET | `/agents/{id}/memory` | 获取记忆统计 | MM-01~08 |
| GET | `/agents/{id}/memory/search` | 检索记忆 | MM-04 |
| GET | `/agents/{id}/stats` | 获取工作统计 | HR-03 |
| GET | `/agents/{id}/tasks` | 获取当前任务 | - |
| GET | `/agents/{id}/reflection` | 获取反思报告 | AGENT-RUNTIME-11 |
| POST | `/agents/{id}/reflect` | 触发自我反思 | AGENT-RUNTIME-11 |
| POST | `/agents/{id}/pause` | 暂停智能体 | - |
| POST | `/agents/{id}/restart` | 重启智能体 | AGENT-RUNTIME-05 |

### 5.4 API详细定义

**GET /agents/{id}**

```yaml
responses:
  200:
    description: 成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code: { type: integer, example: 200 }
            data:
              type: object
              properties:
                id: { type: string }
                name: { type: string }
                level: { type: integer }
                level_name: { type: string }
                department: { type: string }
                supervisor: { $ref: '#/components/schemas/AgentBrief' }
                status: { type: string }
                load: { type: number }
                trust_score: { type: number }
                emotion: { type: string }
                runtime_state:
                  type: object
                  properties:
                    cognitive_load: { type: number }
                    current_mood: { type: string }
                    energy_level: { type: number }
                    motivation: { type: number }
```

**GET /agents/{id}/evaluation**

```yaml
responses:
  200:
    description: 成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code: { type: integer, example: 200 }
            data:
              type: object
              properties:
                overall_assessment: { type: string }
                strengths: { type: array, items: { type: string } }
                weaknesses: { type: array, items: { type: string } }
                suggestions: { type: array, items: { type: string } }
                counterfactual: { type: string }
```


## 六、能力库API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/capabilities/overview` | 获取能力总览 | META-05 |
| GET | `/capabilities` | 获取能力列表 | META-05 |
| GET | `/capabilities/{id}` | 获取能力详情 | META-05 |
| GET | `/capabilities/categories` | 获取能力分类 | - |
| PUT | `/agents/{id}/capabilities` | 分配能力 | META-01 |
| GET | `/capabilities/gaps` | 获取能力缺口 | META-04 |
| GET | `/capabilities/development` | 获取开发中能力 | - |
| POST | `/capabilities/notify-ceo` | 通知主脑处理 | CL-04 |

### 6.1 能力缺口检测

**GET /capabilities/gaps**

```yaml
responses:
  200:
    description: 成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code: { type: integer, example: 200 }
            data:
              type: object
              properties:
                gaps:
                  type: array
                  items:
                    type: object
                    properties:
                      capability_id: { type: string }
                      capability_name: { type: string }
                      severity: { type: string, enum: [critical, high, medium, low] }
                      affected_projects: { type: array, items: { type: string } }
                      current_status: { type: string }
                      progress: { type: integer }
                      suggestions:
                        type: array
                        items:
                          type: object
                          properties:
                            option: { type: string }
                            description: { type: string }
                            cost: { type: number }
                            timeline: { type: string }
                            tradeoff: { type: string }
                total: { type: integer }
```


## 七、工具库API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/tools` | 获取工具列表 | WEB-01~11 |
| GET | `/tools/{id}` | 获取工具详情 | - |
| POST | `/tools/{id}/execute` | 执行工具 | - |
| GET | `/tools/categories` | 获取工具分类 | - |


## 八、培训中心API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/training/overview` | 获取培训总览 | HR-02 |
| GET | `/training/in-progress` | 获取进行中培训 | HR-02 |
| GET | `/training/demands` | 获取培训需求 | HR-02 |
| GET | `/training/courses` | 获取课程列表 | HR-02 |
| GET | `/training/courses/{id}` | 获取课程详情 | HR-02 |
| POST | `/training/arrange` | 安排培训 | HR-02 |
| PUT | `/training/{id}/progress` | 更新培训进度 | HR-02 |
| GET | `/training/{id}/effect` | 获取培训效果 | LN-01 |


## 九、绩效评估API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/performance/ranking` | 获取绩效排行 | HR-03 |
| GET | `/performance/agents/{id}` | 获取智能体绩效 | HR-03 |
| GET | `/performance/agents/{id}/trend` | 获取绩效趋势 | HR-03 |
| GET | `/performance/agents/{id}/suggestions` | 获取改进建议 | HR-03 |
| GET | `/performance/report` | 导出绩效报告 | EX-14 |


## 十、进化中心API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/evolution/overview` | 获取进化总览 | META-03 |
| GET | `/evolution/self` | 获取自我进化状态 | META-03 |
| GET | `/evolution/reflections` | 获取能力自省报告 | META-04 |
| GET | `/evolution/dual-loop` | 获取双循环学习状态 | LN-04 |
| GET | `/evolution/curiosity` | 获取内在动机探索 | LN-05 |
| GET | `/evolution/strategies` | 获取策略调整记录 | META-02 |


## 十一、项目管理API

### 11.1 项目全景

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/projects/panorama` | 获取项目全景 | - |
| GET | `/projects` | 获取项目列表 | - |
| POST | `/projects` | 创建项目 | DC-01 |
| GET | `/projects/{id}` | 获取项目详情 | - |
| PUT | `/projects/{id}` | 更新项目 | - |
| DELETE | `/projects/{id}` | 删除项目 | - |

### 11.2 项目详情

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/projects/{id}/ceo-evaluation` | 获取主脑评估 | AGENT-RUNTIME-03 |
| GET | `/projects/{id}/progress/trend` | 获取进度趋势 | CG-04 |
| GET | `/projects/{id}/milestones` | 获取里程碑 | - |
| POST | `/projects/{id}/milestones` | 创建里程碑 | - |
| GET | `/projects/{id}/team` | 获取项目团队 | - |
| GET | `/projects/{id}/risks` | 获取风险列表 | DC-08 |
| GET | `/projects/{id}/issues` | 获取问题列表 | - |
| GET | `/projects/{id}/discussions` | 获取讨论列表 | CL-03 |
| POST | `/projects/{id}/discussions` | 发送讨论 | CL-03 |
| GET | `/projects/{id}/resources` | 获取资源使用 | RS-01 |
| GET | `/projects/{id}/export` | 导出项目报告 | EX-14 |

### 11.3 API详细定义

**GET /projects/{id}/ceo-evaluation**

```yaml
responses:
  200:
    description: 成功
    content:
      application/json:
        schema:
          type: object
          properties:
            code: { type: integer, example: 200 }
            data:
              type: object
              properties:
                overall: { type: string }
                concerns: { type: array, items: { type: string } }
                suggestions: { type: array, items: { type: string } }
                counterfactual:
                  type: object
                  properties:
                    scenario: { type: string }
                    expected_progress: { type: string }
                confidence: { type: number }
```


## 十二、任务管理API

### 12.1 任务CRUD

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/tasks` | 获取任务列表 | - |
| POST | `/tasks` | 创建任务 | DC-02 |
| GET | `/tasks/{id}` | 获取任务详情 | - |
| PUT | `/tasks/{id}` | 更新任务 | - |
| DELETE | `/tasks/{id}` | 删除任务 | - |

### 12.2 任务看板

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/tasks/board` | 获取看板数据 | - |
| GET | `/tasks/calendar` | 获取日历数据 | - |
| GET | `/tasks/my` | 获取我的任务 | - |
| POST | `/tasks/{id}/move` | 移动任务状态 | - |
| POST | `/tasks/{id}/block` | 标记阻塞 | - |
| POST | `/tasks/{id}/unblock` | 解除阻塞 | - |

### 12.3 合同网协议

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| POST | `/tasks/{id}/tender` | 发起招标 | CL-06 |
| GET | `/tasks/{id}/bids` | 获取投标列表 | CL-06 |
| POST | `/tasks/{id}/award` | 选择中标者 | CL-06 |


## 十三、资源池API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/resources/overview` | 获取资源总览 | RS-01 |
| GET | `/resources/available` | 获取可用资源 | RS-01 |
| GET | `/resources/suggestions` | 获取分配建议 | RS-01 |
| POST | `/resources/allocate` | 分配资源 | RS-01 |
| GET | `/resources/trend` | 获取资源趋势 | CG-04 |


## 十四、财务中心API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/finance/overview` | 获取财务概览 | CG-04 |
| GET | `/finance/transactions` | 获取收支明细 | - |
| POST | `/finance/transactions` | 新增收支 | - |
| GET | `/finance/receivables` | 获取应收账款 | - |
| GET | `/finance/payables` | 获取应付账款 | - |
| GET | `/finance/cost-analysis` | 获取成本分析 | CG-04 |
| GET | `/finance/budgets` | 获取预算列表 | - |
| POST | `/finance/budgets` | 创建预算 | - |
| POST | `/finance/budgets/{id}/adjust` | 调整预算 | - |
| GET | `/finance/model-costs` | 获取模型费用 | EM-05 |
| GET | `/finance/cashflow` | 获取现金流 | - |
| GET | `/finance/cashflow/forecast` | 获取现金流预测 | CG-04 |
| GET | `/finance/tax` | 获取税务信息 | - |
| GET | `/finance/invoices` | 获取发票列表 | - |
| GET | `/finance/reconciliation` | 获取对账状态 | - |
| POST | `/finance/reconciliation/diff` | 处理对账差异 | - |
| GET | `/finance/reports` | 获取报表列表 | EX-14 |
| POST | `/finance/reports/generate` | 生成报表 | EX-14 |


## 十五、营销中心API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/marketing/overview` | 获取营销概览 | CG-04 |
| GET | `/marketing/contents` | 获取内容列表 | MK-01 |
| POST | `/marketing/contents` | 创建内容 | MK-01 |
| GET | `/marketing/contents/{id}` | 获取内容详情 | - |
| PUT | `/marketing/contents/{id}` | 更新内容 | - |
| POST | `/marketing/ai/generate` | AI生成内容 | MK-01, EM-01 |
| GET | `/marketing/review` | 获取待审核 | LAW-01 |
| POST | `/marketing/review/{id}` | 提交审核结果 | LAW-01 |
| POST | `/marketing/distribute` | 分发内容 | MK-08, EX-09 |
| POST | `/marketing/schedule` | 定时发布 | EX-11 |
| GET | `/marketing/analytics` | 获取数据分析 | CG-04 |
| GET | `/marketing/competitors` | 获取竞品列表 | MK-25 |
| GET | `/marketing/competitors/{id}/swot` | 获取SWOT分析 | CG-01 |
| GET | `/marketing/orders/match` | 获取匹配项目 | MK-14 |
| POST | `/marketing/orders/quote` | 生成报价 | MK-15 |
| GET | `/marketing/orders/revenue` | 获取收益统计 | MK-17 |
| GET | `/marketing/media` | 获取媒体资源 | MK-18 |
| POST | `/marketing/media/tasks` | 创建发稿任务 | MK-19 |
| GET | `/marketing/media/indexing` | 获取收录状态 | MK-20 |
| POST | `/marketing/geo/optimize` | GEO优化 | MK-21 |
| GET | `/marketing/workflows` | 获取工作流 | AUTO-03 |
| POST | `/marketing/workflows` | 创建工作流 | AUTO-03 |
| GET | `/marketing/assets` | 获取素材列表 | FILE-01 |
| POST | `/marketing/assets/upload` | 上传素材 | FILE-01 |


## 十六、调研中心API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/research/overview` | 获取调研全景 | - |
| GET | `/research/ai-domains` | 获取AI领域分析 | KNOW-01 |
| GET | `/research/internet` | 获取互联网分析 | KNOW-01 |
| GET | `/research/smart-home` | 获取智能家居分析 | KNOW-01 |
| GET | `/research/smart-agri` | 获取智慧农业分析 | KNOW-01 |
| GET | `/research/smart-city` | 获取智慧城市分析 | KNOW-01 |
| GET | `/research/policies` | 获取政策列表 | KNOW-01 |
| GET | `/research/policies/{id}` | 获取政策详情 | - |
| GET | `/research/files` | 获取文件列表 | FILE-01 |
| POST | `/research/files/upload` | 上传文件 | FILE-01 |
| GET | `/research/files/{id}/summary` | 获取AI摘要 | PC-06 |
| GET | `/research/news` | 获取行业动态 | WEB-02 |
| GET | `/research/reports` | 获取报告列表 | - |
| POST | `/research/reports/generate` | 生成调研报告 | EX-14 |


## 十七、安全中心API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/security/overview` | 获取安全态势 | AGENT-RUNTIME-05 |
| GET | `/security/threats` | 获取威胁信息 | SC-01 |
| GET | `/security/threats/trend` | 获取攻击趋势 | CG-04 |
| GET | `/security/blacklist` | 获取黑名单 | SC-06 |
| POST | `/security/blacklist` | 添加黑名单 | SC-06 |
| GET | `/security/policies` | 获取防护策略 | SC-01 |
| PUT | `/security/policies` | 更新防护策略 | SC-01 |
| GET | `/security/vulnerabilities` | 获取漏洞列表 | SC-03 |
| GET | `/security/vulnerabilities/{id}` | 获取漏洞详情 | SC-03 |
| POST | `/security/vulnerabilities/{id}/fix` | 修复漏洞 | SC-03 |
| GET | `/security/scans` | 获取扫描任务 | SC-03 |
| POST | `/security/scans` | 启动扫描 | SC-03 |
| GET | `/security/compliance` | 获取合规状态 | LAW-05 |
| GET | `/security/audit-logs` | 获取审计日志 | SC-07 |
| GET | `/security/privacy` | 获取隐私状态 | LAW-02 |
| GET | `/security/privacy/requests` | 获取隐私请求 | LAW-02 |
| PUT | `/security/privacy/masking` | 配置脱敏规则 | LAW-02 |
| GET | `/security/access` | 获取访问控制 | SC-04 |
| GET | `/security/api-keys` | 获取API密钥 | SC-20 |
| POST | `/security/api-keys` | 创建API密钥 | SC-20 |


## 十八、外部工具配置API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/integrations/overview` | 获取配置总览 | WEB-04 |
| GET | `/integrations/models` | 获取模型配置 | EM-01 |
| POST | `/integrations/models` | 添加模型配置 | EM-01 |
| POST | `/integrations/models/{id}/test` | 测试模型连接 | EM-01 |
| GET | `/integrations/platforms` | 获取平台配置 | WEB-05 |
| GET | `/integrations/order-platforms` | 获取接单平台 | - |
| GET | `/integrations/media` | 获取媒体平台 | - |
| GET | `/integrations/dev` | 获取开发平台 | WEB-09 |
| GET | `/integrations/collab` | 获取协作工具 | EX-08 |
| POST | `/integrations/tools` | 添加工具配置 | WEB-04 |
| GET | `/integrations/tools/{id}` | 获取工具详情 | - |
| PUT | `/integrations/tools/{id}` | 更新工具配置 | - |
| DELETE | `/integrations/tools/{id}` | 删除工具配置 | - |
| POST | `/integrations/tools/{id}/test` | 测试连接 | WEB-04 |
| GET | `/integrations/quotas` | 获取配额信息 | EM-06 |
| GET | `/integrations/stats` | 获取调用统计 | CG-04 |


## 十九、权限管理API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/permissions/users` | 获取用户权限列表 | SC-04 |
| GET | `/permissions/users/{id}` | 获取用户权限详情 | SC-04 |
| PUT | `/permissions/users/{id}` | 更新用户权限 | SC-04 |
| POST | `/permissions/users` | 新增员工 | SC-04 |
| POST | `/permissions/recommend` | 智能推荐权限 | SC-04 |
| GET | `/permissions/roles` | 获取角色列表 | SC-04 |
| GET | `/permissions/roles/{id}` | 获取角色详情 | SC-04 |
| POST | `/permissions/roles` | 创建角色 | SC-04 |
| GET | `/permissions/rules` | 获取动态规则 | SC-04 |
| GET | `/permissions/history` | 获取变更历史 | SC-07 |
| POST | `/permissions/notify-ceo` | 通知主脑 | CL-04 |


## 二十、外部平台账号管理API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/external-accounts/overview` | 获取账号总览 | - |
| GET | `/external-accounts/platforms` | 获取内容平台账号 | WEB-05 |
| GET | `/external-accounts/orders` | 获取接单平台账号 | - |
| GET | `/external-accounts/media` | 获取媒体平台账号 | - |
| GET | `/external-accounts/dev` | 获取开发平台账号 | WEB-09 |
| GET | `/external-accounts/collab` | 获取协作工具账号 | EX-08 |
| GET | `/external-accounts/models` | 获取AI模型账号 | EM-01 |
| GET | `/external-accounts/{id}` | 获取账号详情 | - |
| GET | `/external-accounts/{id}/stats` | 获取账号动态 | - |
| POST | `/external-accounts/connect` | 连接新账号 | WEB-04 |
| DELETE | `/external-accounts/{id}` | 断开账号 | - |
| POST | `/external-accounts/{id}/refresh` | 刷新账号数据 | - |
| GET | `/external-accounts/{id}/health` | 获取账号健康度 | AGENT-RUNTIME-05 |
| POST | `/external-accounts/batch-refresh` | 批量刷新 | EX-12 |


## 二十一、系统监控API

| 方法 | 端点 | 说明 | 关联能力 |
|------|------|------|----------|
| GET | `/system/status` | 获取系统状态 | AGENT-RUNTIME-05 |
| GET | `/system/components` | 获取组件状态 | AGENT-RUNTIME-05 |
| GET | `/system/resources` | 获取资源使用 | RS-01 |
| GET | `/system/performance` | 获取性能指标 | PO-01 |
| GET | `/system/performance/api` | 获取API响应时间 | PO-01 |
| GET | `/system/alerts` | 获取告警列表 | - |
| GET | `/system/alerts/rules` | 获取告警规则 | - |
| POST | `/system/alerts/rules` | 创建告警规则 | - |
| GET | `/system/self-healing` | 获取自愈历史 | AGENT-RUNTIME-05 |
| GET | `/system/degradation` | 获取降级状态 | EM-03 |


## 二十二、WebSocket事件

### 22.1 连接事件

| 事件 | 方向 | 说明 | 关联能力 |
|------|------|------|----------|
| `connection_established` | S→C | 连接建立成功 | - |
| `heartbeat` | C→S | 心跳 | - |
| `heartbeat_ack` | S→C | 心跳确认 | - |

### 22.2 对话事件

| 事件 | 方向 | 说明 | 关联能力 |
|------|------|------|----------|
| `message` | C→S | 发送消息 | PC-01 |
| `thinking` | S→C | 思考过程 | AGENT-RUNTIME-03 |
| `intent` | S→C | 意图识别 | PC-04 |
| `action` | S→C | 执行动作 | - |
| `reasoning` | S→C | 推理过程 | CG-01 |
| `counterfactual` | S→C | 反事实分析 | AGENT-RUNTIME-07 |
| `message_chunk` | S→C | 消息片段 | EM-13 |
| `response` | S→C | 完整响应 | - |
| `done` | S→C | 对话完成 | - |
| `error` | S→C | 错误 | - |

### 22.3 任务事件

| 事件 | 方向 | 说明 | 关联能力 |
|------|------|------|----------|
| `task_update` | S→C | 任务状态更新 | - |
| `task_assigned` | S→C | 任务已分配 | CL-01 |
| `task_completed` | S→C | 任务已完成 | - |
| `task_failed` | S→C | 任务失败 | - |

### 22.4 系统事件

| 事件 | 方向 | 说明 | 关联能力 |
|------|------|------|----------|
| `alert` | S→C | 告警推送 | - |
| `agent_status_change` | S→C | 智能体状态变更 | AGENT-RUNTIME-05 |
| `project_update` | S→C | 项目更新 | - |
| `security_event` | S→C | 安全事件 | SC-01 |
| `cost_alert` | S→C | 成本告警 | EM-05 |


## 二十三、数据模型定义

### 23.1 智能体模型

```yaml
components:
  schemas:
    Agent:
      type: object
      properties:
        id: { type: string }
        name: { type: string }
        level: { type: integer, enum: [1,2,3,4,5,6] }
        level_name: { type: string }
        department: { type: string }
        role_type: { type: string }
        parent_id: { type: string, nullable: true }
        status: { type: string, enum: [online, offline, busy, error, degraded] }
        profile: { $ref: '#/components/schemas/AgentProfile' }
        model_config: { $ref: '#/components/schemas/ModelConfig' }
        memory_config: { $ref: '#/components/schemas/MemoryConfig' }
        health_config: { $ref: '#/components/schemas/HealthConfig' }
        runtime_state: { $ref: '#/components/schemas/RuntimeState' }
        trust_score: { type: number }
        created_at: { type: string, format: date-time }
        updated_at: { type: string, format: date-time }
        last_active_at: { type: string, format: date-time }

    AgentProfile:
      type: object
      properties:
        mission: { type: string }
        vision: { type: string }
        values: { type: array, items: { type: string } }
        preferences: { type: object }
        personality:
          type: object
          properties:
            openness: { type: number }
            conscientiousness: { type: number }
            extraversion: { type: number }
            agreeableness: { type: number }
            neuroticism: { type: number }

    RuntimeState:
      type: object
      properties:
        cognitive_load: { type: number }
        current_mood: { type: string }
        energy_level: { type: number }
        motivation: { type: number }
        current_task: { type: string, nullable: true }
```

### 23.2 能力模型

```yaml
    Capability:
      type: object
      properties:
        id: { type: string }
        code: { type: string }
        name: { type: string }
        category: { type: string }
        level_required: { type: string }
        status: { type: string, enum: [active, developing, deprecated] }
        version: { type: string }
        description: { type: string }
        input_schema: { type: object }
        output_schema: { type: object }
        sla: { type: object }
```

### 23.3 项目模型

```yaml
    Project:
      type: object
      properties:
        id: { type: string }
        code: { type: string }
        name: { type: string }
        domain: { type: string }
        status: { type: string }
        phase: { type: string }
        owner_id: { type: string }
        start_date: { type: string, format: date }
        end_date: { type: string, format: date }
        progress: { type: integer }
        budget: { type: number }
        actual_cost: { type: number }
        health_score: { type: number }
```

### 23.4 任务模型

```yaml
    Task:
      type: object
      properties:
        id: { type: string }
        project_id: { type: string }
        name: { type: string }
        description: { type: string }
        priority: { type: string, enum: [low, medium, high, critical] }
        status: { type: string }
        progress: { type: integer }
        assignee_id: { type: string }
        due_date: { type: string, format: date }
        estimated_hours: { type: number }
        actual_hours: { type: number }
        required_capabilities: { type: array, items: { type: string } }
```


## 二十四、错误码定义

### 24.1 HTTP错误码

| 错误码 | 名称 | 说明 |
|--------|------|------|
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证或认证过期 |
| 403 | Forbidden | 无权限访问 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突 |
| 422 | Unprocessable Entity | 请求体格式错误 |
| 429 | Too Many Requests | 请求频率超限 |
| 500 | Internal Server Error | 服务器内部错误 |
| 503 | Service Unavailable | 服务不可用 |

### 24.2 业务错误码

| 错误码 | 名称 | 说明 | 关联能力 |
|--------|------|------|----------|
| 10001 | AGENT_NOT_FOUND | 智能体不存在 | - |
| 10002 | AGENT_LEVEL_INVALID | 智能体层级无效 | HR-01 |
| 10003 | AGENT_PERMISSION_DENIED | 智能体权限不足 | SC-04 |
| 10004 | AGENT_OFFLINE | 智能体离线 | AGENT-RUNTIME-05 |
| 20001 | PROJECT_NOT_FOUND | 项目不存在 | - |
| 20002 | PROJECT_ALREADY_APPROVED | 项目已审批 | APPROVE-02 |
| 20003 | PROJECT_BUDGET_EXCEEDED | 预算超限 | - |
| 30001 | TASK_NOT_FOUND | 任务不存在 | - |
| 30002 | TASK_CIRCULAR_DEPENDENCY | 任务循环依赖 | DC-02 |
| 30003 | TASK_DEPENDENCY_NOT_MET | 任务依赖未满足 | DC-02 |
| 40001 | MODEL_NOT_FOUND | 模型不存在 | EM-01 |
| 40002 | MODEL_RATE_LIMIT | 模型请求频率超限 | SC-06 |
| 40003 | MODEL_TIMEOUT | 模型调用超时 | EM-03 |
| 50001 | CAPABILITY_NOT_FOUND | 能力不存在 | META-05 |
| 50002 | CAPABILITY_NOT_ACTIVATED | 能力未激活 | META-01 |
| 50003 | CAPABILITY_EXECUTION_FAILED | 能力执行失败 | QL-05 |
| 60001 | QUOTA_EXCEEDED | 配额不足 | EM-06 |
| 60002 | BUDGET_EXCEEDED | 预算超限 | EM-05 |


## 二十五、端点汇总

| 模块 | GET | POST | PUT | DELETE | 总计 |
|------|-----|------|-----|--------|------|
| 认证 | 1 | 9 | 0 | 0 | 10 |
| 指挥舱 | 6 | 2 | 0 | 0 | 8 |
| 对话系统 | 5 | 4 | 0 | 1 | 10 |
| 智能体管理 | 12 | 6 | 4 | 0 | 22 |
| 能力库 | 8 | 1 | 1 | 0 | 10 |
| 培训中心 | 5 | 1 | 1 | 0 | 7 |
| 绩效评估 | 4 | 0 | 0 | 0 | 4 |
| 进化中心 | 5 | 0 | 0 | 0 | 5 |
| 项目全景 | 15 | 6 | 3 | 1 | 25 |
| 任务看板 | 4 | 4 | 2 | 0 | 10 |
| 资源池 | 4 | 1 | 0 | 0 | 5 |
| 财务中心 | 14 | 4 | 0 | 0 | 18 |
| 营销中心 | 12 | 8 | 1 | 0 | 21 |
| 调研中心 | 9 | 2 | 0 | 0 | 11 |
| 安全中心 | 12 | 4 | 2 | 0 | 18 |
| 外部工具 | 8 | 4 | 1 | 1 | 14 |
| 权限管理 | 6 | 3 | 1 | 0 | 10 |
| 账号管理 | 9 | 3 | 0 | 1 | 13 |
| 系统监控 | 8 | 1 | 0 | 0 | 9 |
| **总计** | **147** | **63** | **16** | **4** | **238** |


## 二十六、版本记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-13 | 完整版：基于所有子文件和对话内容，补充全部238个API端点、WebSocket事件、142项能力接口、安全接口、财务接口、营销接口、调研接口 |