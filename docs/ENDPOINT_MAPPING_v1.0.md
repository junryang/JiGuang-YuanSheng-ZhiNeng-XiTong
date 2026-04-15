# 端点映射文档 - 纪光元生智能系统

| 文档版本 | 修改日期 | 修改人 | 修改内容 |
|---------|---------|--------|---------|
| v1.0 | 2026-01-12 | AI助手 | 完整版：基于所有子文件和对话内容，补充智能体管理、能力库、安全中心、财务中心、营销中心、调研中心、外部工具配置、权限管理等全部端点 |


## 一、概述

本文档定义了前端页面与后端API端点之间的完整映射关系，确保前后端开发人员有一致的接口理解。所有端点均与 `AGENT_ABILITY_SPEC_v1.0.md` 中定义的通用能力对齐。

### 1.1 基础URL

| 环境 | API基础URL | 说明 |
|------|-----------|------|
| 开发环境 | `http://localhost:8000/api/v1` | 本地开发 |
| 测试环境 | `https://test.jyis.com/api/v1` | 内部测试 |
| 生产环境 | `https://api.jyis.com/api/v1` | 正式环境 |

> 规范说明：基础URL固定包含 `/api/v1`，本文件端点映射表默认使用相对路径（如`/auth/login`），仅在跨系统引用时写绝对路径，避免前缀重复。

### 1.2 通用请求头

| Header | 值 | 说明 | 关联能力 |
|--------|-----|------|----------|
| `Content-Type` | `application/json` | 请求体格式 | - |
| `Authorization` | `Bearer {token}` | 认证令牌 | SC-20 访问令牌管理 |
| `X-Request-ID` | `{uuid}` | 请求追踪ID | SC-07 操作审计 |
| `X-2FA-Code` | `{code}` | 双因素认证码（敏感操作） | SC-04 权限检查 |

### 1.3 通用响应格式

```json
{
  "code": 200,
  "message": "success",
  "data": {},
  "timestamp": "2026-01-12T10:30:00Z",
  "request_id": "uuid"
}
```

**状态码说明**：

| code | 含义 | 关联能力 |
|------|------|----------|
| 200 | 成功 | - |
| 400 | 请求参数错误 | QL-04 质量自检 |
| 401 | 未认证 | SC-04 权限检查 |
| 403 | 无权限 | SC-04 权限检查 |
| 404 | 资源不存在 | - |
| 429 | 请求过于频繁 | SC-06 速率限制 |
| 500 | 服务器内部错误 | - |
| 503 | 服务降级中 | EM-03 模型降级 |


## 二、认证模块

| 前端页面 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|---------|------|---------|------|------|----------|
| 登录页 | `/login` | `/auth/login` | POST | 用户名/密码登录 | SC-04 权限检查 |
| 登录页 | `/login` | `/auth/face/login` | POST | 人脸识别登录 | SC-03 敏感信息检测 |
| 登录页 | `/login` | `/auth/voice/login` | POST | 声纹识别登录 | SC-03 敏感信息检测 |
| 登录页 | `/login` | `/auth/webauthn/login` | POST | 硬件密钥登录 | SC-20 访问令牌管理 |
| 登录页 | `/login` | `/auth/wechat/login` | POST | 微信登录 | WEB-05 社交媒体交互 |
| 登录页 | `/login` | `/auth/feishu/login` | POST | 飞书登录 | EX-08 消息发送 |
| 登录页 | `/login` | `/auth/register` | POST | 用户注册（需邀请码） | SC-04 权限检查 |
| 登录页 | `/login` | `/auth/refresh` | POST | 刷新令牌 | SC-20 访问令牌管理 |
| 登录页 | `/login` | `/auth/logout` | POST | 退出登录 | SC-20 访问令牌管理 |
| 登录页 | `/login` | `/auth/me` | GET | 获取当前用户信息 | SC-04 权限检查 |
| 忘记密码 | `/forgot-password` | `/auth/password/reset` | POST | 发送重置邮件 | EX-08 消息发送 |
| 忘记密码 | `/forgot-password` | `/auth/password/verify` | POST | 验证重置令牌 | SC-04 权限检查 |
| 忘记密码 | `/forgot-password` | `/auth/password/update` | POST | 更新密码 | SC-19 数据加密 |

### 2.1 API详细定义

**POST /auth/login**

请求体：
```json
{
  "username": "boss@jyis.com",
  "password": "encrypted_password"
}
```

响应：
```json
{
  "code": 200,
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "expires_in": 7200,
    "user": {
      "id": "user_001",
      "name": "张总",
      "role": "boss",
      "avatar": "https://...",
      "permissions": ["*"]
    }
  }
}
```

**POST /auth/face/login**

请求体：
```json
{
  "face_data": "base64_encoded_face_image",
  "liveness_data": "base64_encoded_liveness"
}
```

响应：
```json
{
  "code": 200,
  "data": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "expires_in": 7200,
    "confidence": 0.987,
    "user": {
      "id": "user_001",
      "name": "张总",
      "role": "boss"
    }
  }
}
```


## 三、指挥舱（老板/高管视角）

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 智能体团队状态 | `/command` | `/dashboard/command/agents` | GET | 获取智能体团队状态 | AGENT-RUNTIME-06 |
| 关键指标卡片 | `/command` | `/dashboard/command/metrics` | GET | 获取关键指标 | CG-04 数值推理 |
| 待决策事项 | `/command` | `/dashboard/command/decisions` | GET | 获取待决策事项 | DC-05 优先级排序 |
| 待决策事项 | `/command` | `/dashboard/command/decisions/{id}` | POST | 处理决策 | DC-09 自主决策 |
| 项目健康度一览 | `/command` | `/dashboard/command/projects/health` | GET | 获取项目健康度 | QL-07 质量趋势分析 |
| 智能体负载热力图 | `/command` | `/dashboard/command/agents/load` | GET | 获取智能体负载 | AGENT-RUNTIME-04 |
| 收支趋势 | `/command` | `/dashboard/command/finance/trend` | GET | 获取收支趋势 | CG-04 数值推理 |
| 最近活动 | `/command` | `/dashboard/command/activities` | GET | 获取最近活动 | SC-07 操作审计 |
| 快速提问 | `/command` | `/chat/quick` | POST | 快速提问（SSE） | PC-01 自然语言理解 |
| 系统态势 | `/command` | `/system/status/full` | GET | 获取完整系统状态 | AGENT-RUNTIME-05 |

### 3.1 API详细定义

**GET /dashboard/command/metrics**

响应：
```json
{
  "code": 200,
  "data": {
    "agents": {
      "total": 47,
      "online": 46,
      "busy": 3,
      "offline": 1,
      "error": 0
    },
    "projects": {
      "total": 12,
      "in_progress": 8,
      "completed": 3,
      "planned": 2,
      "at_risk": 1
    },
    "decisions": {
      "pending": 2,
      "urgent": 1,
      "today_completed": 3
    },
    "system_health": {
      "score": 98,
      "status": "healthy",
      "trend": "↑1%"
    },
    "today_cost": {
      "total": 1234,
      "trend": "↓5%"
    }
  }
}
```

**GET /dashboard/command/decisions**

响应：
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "dec_001",
        "type": "project_approval",
        "title": "光速计划二期立项",
        "priority": "critical",
        "submitted_by": "多智能体总经理",
        "submitted_at": "2026-01-10T09:00:00Z",
        "timeout_at": "2026-01-12T09:00:00Z",
        "is_timeout": true,
        "options": [
          {
            "id": "opt_a",
            "name": "批准",
            "description": "周期4周，成本¥120,000",
            "impact": "视频产能+300%"
          },
          {
            "id": "opt_b",
            "name": "暂缓",
            "description": "不影响现有进度",
            "impact": "推迟至少4周"
          }
        ],
        "counterfactual": {
          "alternative": "如果选择自研方案，预计延期4周但长期成本更低"
        }
      }
    ],
    "total": 2
  }
}
```

**POST /dashboard/command/decisions/{id}**

请求体：
```json
{
  "decision": "opt_a",
  "comment": "批准，尽快启动"
}
```

响应：
```json
{
  "code": 200,
  "data": {
    "decision_id": "dec_001",
    "status": "approved",
    "next_steps": ["创建项目", "分配资源", "启动开发"]
  }
}
```


## 四、对话系统

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 对话界面 | `/chat` | `/chat/sessions` | GET | 获取会话列表 | MM-02 短期记忆 |
| 对话界面 | `/chat` | `/chat/sessions` | POST | 创建新会话 | MM-01 工作记忆 |
| 对话界面 | `/chat` | `/chat/sessions/{id}` | DELETE | 删除会话 | - |
| 对话界面 | `/chat` | `/chat/sessions/{id}/messages` | GET | 获取会话消息 | MM-03 长期记忆 |
| 对话界面 | `/chat` | `/chat/sessions/{id}/messages` | POST | 发送消息（SSE流式） | PC-01, EM-13 |
| 对话界面 | `/chat` | `/chat/sessions/{id}/thinking` | GET | 获取思考过程 | AGENT-RUNTIME-03 |
| 对话历史 | `/chat/history` | `/chat/history` | GET | 获取历史对话 | MM-04 记忆检索 |
| 对话历史 | `/chat/history` | `/chat/history/search` | GET | 搜索历史对话 | MM-04 记忆检索 |
| 语音输入 | `/chat` | `/chat/voice/asr` | POST | 语音转文字 | PC-04 语音理解 |
| 语音输出 | `/chat` | `/chat/voice/tts` | POST | 文字转语音 | EX-16 音频生成 |

### 4.1 API详细定义

**POST /chat/sessions/{id}/messages (SSE流式)**

请求体：
```json
{
  "content": "光速计划二期现在什么进度？",
  "agent_id": "agent_ceo",
  "context": {
    "session_id": "sess_001",
    "parent_message_id": "msg_001"
  }
}
```

SSE响应流：
```
event: thinking
data: {"step": 1, "content": "正在分析查询意图...", "confidence": 0.95}

event: intent
data: {"intent": "query_progress", "entities": {"project": "光速计划二期"}}

event: action
data: {"action": "querying_project", "project_id": "proj_light_speed_2"}

event: reasoning
data: {"step": 2, "content": "查询到项目进度：45%，预计完成：02-15"}

event: counterfactual
data: {"analysis": "如果上周批准了增加人力，当前进度预计为52%"}

event: message_chunk
data: {"content": "光速计划二期"}

event: message_chunk
data: {"content": "当前进度45%"}

event: message_chunk
data: {"content": "，预计2月15日完成。"}

event: done
data: {"message_id": "msg_002", "tokens_used": 234}
```

**GET /chat/sessions/{id}/thinking**

响应：
```json
{
  "code": 200,
  "data": {
    "message_id": "msg_002",
    "thinking_steps": [
      {
        "step": 1,
        "reasoning": "分析查询意图",
        "confidence": 0.95,
        "evidence": "关键词匹配: 进度"
      },
      {
        "step": 2,
        "reasoning": "查询项目数据",
        "result": "项目进度45%"
      }
    ],
    "reasoning_chain": "首先识别用户意图为查询进度，然后从项目数据库查询光速计划二期的状态，发现进度为45%...",
    "confidence": 0.92
  }
}
```


## 五、智能体管理中心

### 5.1 智能体全景

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 智能体全景 | `/agents` | `/agents/panorama` | GET | 获取智能体全景数据 | AGENT-RUNTIME-06 |
| 智能体团队状态 | `/agents` | `/agents/team/status` | GET | 获取团队状态 | HR-03 绩效评估 |
| 按层级分布 | `/agents` | `/agents/stats/by-level` | GET | 按层级统计 | - |
| 按部门分布 | `/agents` | `/agents/stats/by-dept` | GET | 按部门统计 | - |
| 负载热力图 | `/agents` | `/agents/load/heatmap` | GET | 获取负载热力图 | AGENT-RUNTIME-04 |
| 需要关注 | `/agents` | `/agents/alerts` | GET | 获取需要关注的智能体 | AGENT-RUNTIME-05 |

### 5.2 智能体列表

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 智能体列表 | `/agents/list` | `/agents` | GET | 获取智能体列表 | - |
| 智能体列表 | `/agents/list` | `/agents` | POST | 创建智能体 | HR-01 |
| 智能体筛选 | `/agents/list` | `/agents?{filters}` | GET | 筛选智能体 | - |
| 批量操作 | `/agents/list` | `/agents/batch` | POST | 批量操作 | EX-12 批量执行 |

### 5.3 智能体详情

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 基本信息 | `/agent/:id` | `/agents/{id}` | GET | 获取智能体详情 | HR-03 |
| 基本信息 | `/agent/:id` | `/agents/{id}` | PUT | 更新智能体 | HR-01 |
| 主脑评估 | `/agent/:id` | `/agents/{id}/evaluation` | GET | 获取主脑评估 | AGENT-RUNTIME-03 |
| 能力清单 | `/agent/:id` | `/agents/{id}/capabilities` | GET | 获取能力清单 | META-05 |
| 能力配置 | `/agent/:id` | `/agents/{id}/capabilities` | PUT | 配置能力 | META-01 |
| 记忆系统 | `/agent/:id` | `/agents/{id}/memory` | GET | 获取记忆统计 | MM-01~08 |
| 记忆检索 | `/agent/:id` | `/agents/{id}/memory/search` | GET | 检索记忆 | MM-04 |
| 工作统计 | `/agent/:id` | `/agents/{id}/stats` | GET | 获取工作统计 | HR-03 |
| 当前任务 | `/agent/:id` | `/agents/{id}/tasks` | GET | 获取当前任务 | - |
| 自我反思 | `/agent/:id` | `/agents/{id}/reflection` | GET | 获取反思报告 | AGENT-RUNTIME-11 |
| 触发反思 | `/agent/:id` | `/agents/{id}/reflect` | POST | 触发自我反思 | AGENT-RUNTIME-11 |
| 对话 | `/agent/:id` | `/chat/sessions` | POST | 创建对话 | PC-01 |
| 暂停/恢复 | `/agent/:id` | `/agents/{id}/pause` | POST | 暂停智能体 | - |
| 重启 | `/agent/:id` | `/agents/{id}/restart` | POST | 重启智能体 | AGENT-RUNTIME-05 |

### 5.4 API详细定义

**GET /agents/{id}**

响应：
```json
{
  "code": 200,
  "data": {
    "id": "agent_senior_backend_a",
    "name": "资深后端工程师A",
    "level": 5,
    "level_name": "L5 员工",
    "department": "后端部",
    "supervisor": {
      "id": "agent_backend_lead",
      "name": "后端主管"
    },
    "status": "busy",
    "load": 78,
    "trust_score": 85,
    "emotion": "focused",
    "created_at": "2025-12-01T00:00:00Z",
    "last_active": "2026-01-12T10:30:00Z",
    "runtime_state": {
      "cognitive_load": 0.78,
      "current_mood": "focused",
      "energy_level": 0.65,
      "motivation": 0.82
    }
  }
}
```

**GET /agents/{id}/evaluation**

响应：
```json
{
  "code": 200,
  "data": {
    "overall_assessment": "表现良好，但当前负载偏高",
    "strengths": [
      "API开发能力S级，代码质量高",
      "任务完成率94.8%，高于部门平均",
      "主动学习能力强"
    ],
    "weaknesses": [
      "当前负载78%，建议分担部分任务",
      "微服务架构能力仅B级"
    ],
    "suggestions": [
      "将数据清洗任务分配给爬虫工程师",
      "安排微服务架构培训课程"
    ],
    "counterfactual": "如果上周批准了增加人力的申请，当前负载预计为62%"
  }
}
```

**GET /agents/{id}/reflection**

响应：
```json
{
  "code": 200,
  "data": {
    "last_reflection": "2026-01-12T02:00:00Z",
    "insights": [
      {
        "type": "issue",
        "description": "API性能优化任务因等待索引方案而阻塞"
      },
      {
        "type": "improvement",
        "description": "近3天代码审查反馈有2次需要重新修改"
      }
    ],
    "improvement_plan": {
      "actions": [
        "提前沟通依赖，避免阻塞",
        "加强代码自测，减少审查返工"
      ],
      "status": "in_progress"
    },
    "overall_score": 88.5
  }
}
```


## 六、能力库中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 能力总览 | `/capabilities` | `/capabilities/overview` | GET | 获取能力总览 | META-05 |
| 能力列表 | `/capabilities` | `/capabilities` | GET | 获取能力列表 | META-05 |
| 能力详情 | `/capabilities` | `/capabilities/{id}` | GET | 获取能力详情 | META-05 |
| 能力分类 | `/capabilities` | `/capabilities/categories` | GET | 获取能力分类 | - |
| 能力分配 | `/capabilities` | `/agents/{id}/capabilities` | PUT | 分配能力 | META-01 |
| 能力缺口 | `/capabilities` | `/capabilities/gaps` | GET | 获取能力缺口 | META-04 |
| 开发中能力 | `/capabilities` | `/capabilities/development` | GET | 获取开发中能力 | - |
| 工具库 | `/capabilities/tools` | `/tools` | GET | 获取工具列表 | WEB-01~11 |
| 技能库 | `/capabilities/skills` | `/skills` | GET | 获取技能列表 | - |
| 记忆库 | `/capabilities/memory` | `/memory/global` | GET | 获取全局记忆 | MM-05 |
| 知识库 | `/capabilities/knowledge` | `/knowledge` | GET | 获取知识库 | KNOW-03 |
| 模型库 | `/capabilities/models` | `/models` | GET | 获取模型列表 | EM-01 |
| 一键通知主脑 | `/capabilities` | `/capabilities/notify-ceo` | POST | 通知主脑处理 | CL-04 求助请求 |

### 6.1 API详细定义

**GET /capabilities**

响应：
```json
{
  "code": 200,
  "data": {
    "items": [
      {
        "id": "AGENT-RUNTIME-01",
        "name": "智能体主循环",
        "category": "运行时",
        "level_required": "L0-L6",
        "status": "active",
        "activated_agents": 47,
        "activation_rate": 100
      },
      {
        "id": "WEB-01",
        "name": "浏览器自动化",
        "category": "WEB",
        "level_required": "L0-L6",
        "status": "active",
        "activated_agents": 12,
        "activation_rate": 26
      },
      {
        "id": "VIDEO-01",
        "name": "视频生成能力",
        "category": "领域扩展",
        "level_required": "L4-L5",
        "status": "developing",
        "progress": 45,
        "estimated_completion": "2026-02-15"
      }
    ],
    "total": 142,
    "categories": {
      "AGENT-RUNTIME": 12,
      "WEB": 11,
      "KNOW": 6,
      "LAW": 5,
      "AUTO": 6,
      "HR": 5,
      "RD": 4,
      "FILE": 4,
      "APPROVE": 6,
      "PC": 10,
      "CG": 12,
      "DC": 15,
      "EX": 14,
      "MM": 8,
      "EM": 11,
      "SC": 6,
      "CL": 6,
      "LN": 6,
      "META": 5,
      "DOMAIN": 8
    }
  }
}
```

**GET /capabilities/gaps**

响应：
```json
{
  "code": 200,
  "data": {
    "gaps": [
      {
        "capability_id": "VIDEO-01",
        "capability_name": "视频生成能力",
        "severity": "critical",
        "affected_projects": ["光速计划二期"],
        "current_status": "developing",
        "progress": 45,
        "suggestions": [
          {
            "option": "A",
            "description": "加速商务谈判",
            "cost": 5000,
            "timeline": "1周"
          },
          {
            "option": "B",
            "description": "切换Runway API",
            "cost": 0,
            "timeline": "立即",
            "tradeoff": "成本高30%"
          }
        ]
      }
    ],
    "total": 8
  }
}
```

**POST /capabilities/notify-ceo**

请求体：
```json
{
  "gaps": ["VIDEO-01", "IOT-01"],
  "priority": "high",
  "message": "视频生成能力缺失，阻塞光速计划二期"
}
```

响应：
```json
{
  "code": 200,
  "data": {
    "notification_id": "notif_001",
    "status": "sent",
    "ceo_response": "pending"
  }
}
```


## 七、培训中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 培训总览 | `/training` | `/training/overview` | GET | 获取培训总览 | HR-02 |
| 进行中培训 | `/training` | `/training/in-progress` | GET | 获取进行中培训 | HR-02 |
| 培训需求 | `/training` | `/training/demands` | GET | 获取培训需求 | HR-02 |
| 课程库 | `/training` | `/training/courses` | GET | 获取课程列表 | HR-02 |
| 课程详情 | `/training` | `/training/courses/{id}` | GET | 获取课程详情 | HR-02 |
| 安排培训 | `/training` | `/training/arrange` | POST | 安排培训 | HR-02 |
| 培训进度 | `/training` | `/training/{id}/progress` | PUT | 更新培训进度 | HR-02 |
| 培训效果 | `/training` | `/training/{id}/effect` | GET | 获取培训效果 | LN-01 |


## 八、绩效评估中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 绩效排行 | `/performance` | `/performance/ranking` | GET | 获取绩效排行 | HR-03 |
| 绩效详情 | `/performance` | `/performance/agents/{id}` | GET | 获取智能体绩效 | HR-03 |
| 绩效趋势 | `/performance` | `/performance/agents/{id}/trend` | GET | 获取绩效趋势 | HR-03 |
| 改进建议 | `/performance` | `/performance/agents/{id}/suggestions` | GET | 获取改进建议 | HR-03 |
| 导出报告 | `/performance` | `/performance/report` | GET | 导出绩效报告 | EX-14 文档生成 |


## 九、进化中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 进化总览 | `/evolution` | `/evolution/overview` | GET | 获取进化总览 | META-03 |
| 自我进化 | `/evolution` | `/evolution/self` | GET | 获取自我进化状态 | META-03 |
| 能力自省 | `/evolution` | `/evolution/reflections` | GET | 获取能力自省报告 | META-04 |
| 双循环学习 | `/evolution` | `/evolution/dual-loop` | GET | 获取双循环学习状态 | LN-04 |
| 内在动机 | `/evolution` | `/evolution/curiosity` | GET | 获取内在动机探索 | LN-05 |
| 策略调整 | `/evolution` | `/evolution/strategies` | GET | 获取策略调整记录 | META-02 |


## 十、项目全景

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 项目全景 | `/projects` | `/projects/panorama` | GET | 获取项目全景 | - |
| 项目列表 | `/projects` | `/projects` | GET | 获取项目列表 | - |
| 项目列表 | `/projects` | `/projects` | POST | 创建项目 | DC-01 |
| 智能筛选 | `/projects` | `/projects?{filters}` | GET | 筛选项目 | - |
| 项目详情 | `/project/:id` | `/projects/{id}` | GET | 获取项目详情 | - |
| 项目详情 | `/project/:id` | `/projects/{id}` | PUT | 更新项目 | - |
| 项目详情 | `/project/:id` | `/projects/{id}` | DELETE | 删除项目 | - |
| 主脑评估 | `/project/:id` | `/projects/{id}/ceo-evaluation` | GET | 获取主脑评估 | AGENT-RUNTIME-03 |
| 进度趋势 | `/project/:id` | `/projects/{id}/progress/trend` | GET | 获取进度趋势 | CG-04 |
| 里程碑 | `/project/:id` | `/projects/{id}/milestones` | GET | 获取里程碑 | - |
| 里程碑 | `/project/:id` | `/projects/{id}/milestones` | POST | 创建里程碑 | - |
| 项目团队 | `/project/:id` | `/projects/{id}/team` | GET | 获取项目团队 | - |
| 任务看板 | `/project/:id` | `/projects/{id}/tasks/board` | GET | 获取任务看板 | - |
| 任务列表 | `/project/:id` | `/projects/{id}/tasks` | GET | 获取任务列表 | - |
| 任务详情 | `/project/:id` | `/tasks/{id}` | GET | 获取任务详情 | - |
| 任务详情 | `/project/:id` | `/tasks/{id}` | PUT | 更新任务 | - |
| 任务分配 | `/project/:id` | `/tasks/{id}/assign` | POST | 分配任务 | CL-01 |
| 风险中心 | `/project/:id` | `/projects/{id}/risks` | GET | 获取风险列表 | DC-08 |
| 问题追踪 | `/project/:id` | `/projects/{id}/issues` | GET | 获取问题列表 | - |
| 项目讨论 | `/project/:id` | `/projects/{id}/discussions` | GET | 获取讨论列表 | CL-03 |
| 项目讨论 | `/project/:id` | `/projects/{id}/discussions` | POST | 发送讨论 | CL-03 |
| 资源使用 | `/project/:id` | `/projects/{id}/resources` | GET | 获取资源使用 | RS-01 |
| 导出报告 | `/project/:id` | `/projects/{id}/export` | GET | 导出项目报告 | EX-14 |
| 快速操作 | `/project/:id` | `/projects/{id}/quick-actions` | POST | 快速操作 | - |

### 10.1 API详细定义

**GET /projects/{id}/ceo-evaluation**

响应：
```json
{
  "code": 200,
  "data": {
    "overall": "项目进展正常，预计可按时交付",
    "concerns": [
      "后端API开发进度55%，略低于计划(60%)",
      "测试验证尚未开始"
    ],
    "suggestions": [
      "建议增加后端资源",
      "提前准备测试用例"
    ],
    "counterfactual": {
      "scenario": "如果上周批准了增加人力的申请",
      "expected_progress": "82% (+7%)"
    },
    "confidence": 0.85
  }
}
```

**GET /projects/{id}/risks**

响应：
```json
{
  "code": 200,
  "data": {
    "risks": [
      {
        "id": "risk_001",
        "name": "后端资源不足",
        "probability": "medium",
        "impact": "medium",
        "level": "medium",
        "status": "mitigating",
        "owner": "项目经理",
        "mitigation": "调整任务分配，考虑增加人手"
      }
    ],
    "matrix": {
      "high": 0,
      "medium": 2,
      "low": 6
    }
  }
}
```


## 十一、任务看板

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 看板视图 | `/project/:id/board` | `/tasks/board` | GET | 获取看板数据 | - |
| 列表视图 | `/project/:id/board` | `/tasks` | GET | 获取任务列表 | - |
| 日历视图 | `/project/:id/board` | `/tasks/calendar` | GET | 获取日历数据 | - |
| 我的任务 | `/project/:id/board` | `/tasks/my` | GET | 获取我的任务 | - |
| 创建任务 | `/project/:id/board` | `/tasks` | POST | 创建任务 | DC-02 |
| 更新任务 | `/project/:id/board` | `/tasks/{id}` | PUT | 更新任务 | - |
| 移动任务 | `/project/:id/board` | `/tasks/{id}/move` | POST | 移动任务状态 | - |
| 阻塞任务 | `/project/:id/board` | `/tasks/{id}/block` | POST | 标记阻塞 | - |
| 解除阻塞 | `/project/:id/board` | `/tasks/{id}/unblock` | POST | 解除阻塞 | - |


## 十二、资源池管理

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 资源总览 | `/resources` | `/resources/overview` | GET | 获取资源总览 | RS-01 |
| 可用资源 | `/resources` | `/resources/available` | GET | 获取可用资源 | RS-01 |
| 资源分配建议 | `/resources` | `/resources/suggestions` | GET | 获取分配建议 | RS-01 |
| 资源分配 | `/resources` | `/resources/allocate` | POST | 分配资源 | RS-01 |
| 资源趋势 | `/resources` | `/resources/trend` | GET | 获取资源趋势 | CG-04 |


## 十三、财务中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 财务概览 | `/finance` | `/finance/overview` | GET | 获取财务概览 | CG-04 |
| 收支明细 | `/finance` | `/finance/transactions` | GET | 获取收支明细 | - |
| 收支明细 | `/finance` | `/finance/transactions` | POST | 新增收支 | - |
| 应收账款 | `/finance` | `/finance/receivables` | GET | 获取应收账款 | - |
| 应付账款 | `/finance` | `/finance/payables` | GET | 获取应付账款 | - |
| 成本分析 | `/finance` | `/finance/cost-analysis` | GET | 获取成本分析 | CG-04 |
| 预算管理 | `/finance` | `/finance/budgets` | GET | 获取预算列表 | - |
| 预算管理 | `/finance` | `/finance/budgets` | POST | 创建预算 | - |
| 预算调整 | `/finance` | `/finance/budgets/{id}/adjust` | POST | 调整预算 | - |
| 模型费用 | `/finance` | `/finance/model-costs` | GET | 获取模型费用 | EM-05 |
| 现金流 | `/finance` | `/finance/cashflow` | GET | 获取现金流 | - |
| 现金流预测 | `/finance` | `/finance/cashflow/forecast` | GET | 获取现金流预测 | CG-04 |
| 税务管理 | `/finance` | `/finance/tax` | GET | 获取税务信息 | - |
| 发票管理 | `/finance` | `/finance/invoices` | GET | 获取发票列表 | - |
| 对账管理 | `/finance` | `/finance/reconciliation` | GET | 获取对账状态 | - |
| 对账差异 | `/finance` | `/finance/reconciliation/diff` | POST | 处理对账差异 | - |
| 财务报表 | `/finance` | `/finance/reports` | GET | 获取报表列表 | EX-14 |
| 生成报表 | `/finance` | `/finance/reports/generate` | POST | 生成报表 | EX-14 |
| 财务团队 | `/finance` | `/finance/team` | GET | 获取财务团队 | - |


## 十四、营销中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 营销概览 | `/marketing` | `/marketing/overview` | GET | 获取营销概览 | CG-04 |
| 内容管理 | `/marketing` | `/marketing/contents` | GET | 获取内容列表 | MK-01 |
| 内容管理 | `/marketing` | `/marketing/contents` | POST | 创建内容 | MK-01 |
| 内容详情 | `/marketing` | `/marketing/contents/{id}` | GET | 获取内容详情 | - |
| 内容更新 | `/marketing` | `/marketing/contents/{id}` | PUT | 更新内容 | - |
| AI生成 | `/marketing` | `/marketing/ai/generate` | POST | AI生成内容 | MK-01, EM-01 |
| 内容审核 | `/marketing` | `/marketing/review` | GET | 获取待审核 | LAW-01 |
| 内容审核 | `/marketing` | `/marketing/review/{id}` | POST | 提交审核结果 | LAW-01 |
| 多平台分发 | `/marketing` | `/marketing/distribute` | POST | 分发内容 | MK-08, EX-09 |
| 定时发布 | `/marketing` | `/marketing/schedule` | POST | 定时发布 | EX-11 |
| 数据分析 | `/marketing` | `/marketing/analytics` | GET | 获取数据分析 | CG-04 |
| 竞品监控 | `/marketing` | `/marketing/competitors` | GET | 获取竞品列表 | MK-25 |
| 竞品详情 | `/marketing` | `/marketing/competitors/{id}` | GET | 获取竞品详情 | MK-25 |
| SWOT分析 | `/marketing` | `/marketing/competitors/{id}/swot` | GET | 获取SWOT分析 | CG-01 |
| 接单匹配 | `/marketing` | `/marketing/orders/match` | GET | 获取匹配项目 | MK-14 |
| 报价生成 | `/marketing` | `/marketing/orders/quote` | POST | 生成报价 | MK-15 |
| 收益统计 | `/marketing` | `/marketing/orders/revenue` | GET | 获取收益统计 | MK-17 |
| 媒体资源 | `/marketing` | `/marketing/media` | GET | 获取媒体资源 | MK-18 |
| 发稿任务 | `/marketing` | `/marketing/media/tasks` | POST | 创建发稿任务 | MK-19 |
| 收录跟踪 | `/marketing` | `/marketing/media/indexing` | GET | 获取收录状态 | MK-20 |
| GEO优化 | `/marketing` | `/marketing/geo/optimize` | POST | GEO优化 | MK-21 |
| 自动化工作流 | `/marketing` | `/marketing/workflows` | GET | 获取工作流 | AUTO-03 |
| 自动化工作流 | `/marketing` | `/marketing/workflows` | POST | 创建工作流 | AUTO-03 |
| 素材管理 | `/marketing` | `/marketing/assets` | GET | 获取素材列表 | FILE-01 |
| 素材上传 | `/marketing` | `/marketing/assets/upload` | POST | 上传素材 | FILE-01 |


## 十五、调研中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 调研全景 | `/research` | `/research/overview` | GET | 获取调研全景 | - |
| AI领域 | `/research` | `/research/ai-domains` | GET | 获取AI领域分析 | KNOW-01 |
| 互联网领域 | `/research` | `/research/internet` | GET | 获取互联网分析 | KNOW-01 |
| 智能家居 | `/research` | `/research/smart-home` | GET | 获取智能家居分析 | KNOW-01 |
| 智慧农业 | `/research` | `/research/smart-agri` | GET | 获取智慧农业分析 | KNOW-01 |
| 智慧城市 | `/research` | `/research/smart-city` | GET | 获取智慧城市分析 | KNOW-01 |
| 政策研究 | `/research` | `/research/policies` | GET | 获取政策列表 | KNOW-01 |
| 政策详情 | `/research` | `/research/policies/{id}` | GET | 获取政策详情 | - |
| 文件管理 | `/research` | `/research/files` | GET | 获取文件列表 | FILE-01 |
| 文件上传 | `/research` | `/research/files/upload` | POST | 上传文件 | FILE-01 |
| AI摘要 | `/research` | `/research/files/{id}/summary` | GET | 获取AI摘要 | PC-06 |
| 行业动态 | `/research` | `/research/news` | GET | 获取行业动态 | WEB-02 |
| 调研报告 | `/research` | `/research/reports` | GET | 获取报告列表 | - |
| 生成报告 | `/research` | `/research/reports/generate` | POST | 生成调研报告 | EX-14 |


## 十六、安全中心

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 安全态势 | `/security` | `/security/overview` | GET | 获取安全态势 | AGENT-RUNTIME-05 |
| 威胁防护 | `/security` | `/security/threats` | GET | 获取威胁信息 | SC-01 |
| 攻击趋势 | `/security` | `/security/threats/trend` | GET | 获取攻击趋势 | CG-04 |
| IP黑名单 | `/security` | `/security/blacklist` | GET | 获取黑名单 | SC-06 |
| IP黑名单 | `/security` | `/security/blacklist` | POST | 添加黑名单 | SC-06 |
| 防护策略 | `/security` | `/security/policies` | GET | 获取防护策略 | SC-01 |
| 防护策略 | `/security` | `/security/policies` | PUT | 更新防护策略 | SC-01 |
| 漏洞管理 | `/security` | `/security/vulnerabilities` | GET | 获取漏洞列表 | SC-03 |
| 漏洞详情 | `/security` | `/security/vulnerabilities/{id}` | GET | 获取漏洞详情 | SC-03 |
| 漏洞修复 | `/security` | `/security/vulnerabilities/{id}/fix` | POST | 修复漏洞 | SC-03 |
| 扫描任务 | `/security` | `/security/scans` | GET | 获取扫描任务 | SC-03 |
| 启动扫描 | `/security` | `/security/scans` | POST | 启动扫描 | SC-03 |
| 合规审计 | `/security` | `/security/compliance` | GET | 获取合规状态 | LAW-05 |
| 审计日志 | `/security` | `/security/audit-logs` | GET | 获取审计日志 | SC-07 |
| 隐私保护 | `/security` | `/security/privacy` | GET | 获取隐私状态 | LAW-02 |
| 隐私请求 | `/security` | `/security/privacy/requests` | GET | 获取隐私请求 | LAW-02 |
| 数据脱敏 | `/security` | `/security/privacy/masking` | PUT | 配置脱敏规则 | LAW-02 |
| 访问控制 | `/security` | `/security/access` | GET | 获取访问控制 | SC-04 |
| API密钥 | `/security` | `/security/api-keys` | GET | 获取API密钥 | SC-20 |
| API密钥 | `/security` | `/security/api-keys` | POST | 创建API密钥 | SC-20 |
| 安全团队 | `/security` | `/security/team` | GET | 获取安全团队 | - |


## 十七、外部工具配置

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 工具配置总览 | `/integrations` | `/integrations/overview` | GET | 获取配置总览 | WEB-04 |
| AI模型配置 | `/integrations` | `/integrations/models` | GET | 获取模型配置 | EM-01 |
| AI模型配置 | `/integrations` | `/integrations/models` | POST | 添加模型配置 | EM-01 |
| 模型测试 | `/integrations` | `/integrations/models/{id}/test` | POST | 测试模型连接 | EM-01 |
| 内容平台配置 | `/integrations` | `/integrations/platforms` | GET | 获取平台配置 | WEB-05 |
| 接单平台配置 | `/integrations` | `/integrations/order-platforms` | GET | 获取接单平台 | - |
| 媒体平台配置 | `/integrations` | `/integrations/media` | GET | 获取媒体平台 | - |
| 开发平台配置 | `/integrations` | `/integrations/dev` | GET | 获取开发平台 | WEB-09 |
| 协作工具配置 | `/integrations` | `/integrations/collab` | GET | 获取协作工具 | EX-08 |
| 添加工具 | `/integrations` | `/integrations/tools` | POST | 添加工具配置 | WEB-04 |
| 工具详情 | `/integrations` | `/integrations/tools/{id}` | GET | 获取工具详情 | - |
| 工具更新 | `/integrations` | `/integrations/tools/{id}` | PUT | 更新工具配置 | - |
| 工具删除 | `/integrations` | `/integrations/tools/{id}` | DELETE | 删除工具配置 | - |
| 测试连接 | `/integrations` | `/integrations/tools/{id}/test` | POST | 测试连接 | WEB-04 |
| 配额管理 | `/integrations` | `/integrations/quotas` | GET | 获取配额信息 | EM-06 |
| 调用统计 | `/integrations` | `/integrations/stats` | GET | 获取调用统计 | CG-04 |


## 十八、权限管理

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 员工权限列表 | `/permissions` | `/permissions/users` | GET | 获取用户权限列表 | SC-04 |
| 权限详情 | `/permissions` | `/permissions/users/{id}` | GET | 获取用户权限详情 | SC-04 |
| 权限配置 | `/permissions` | `/permissions/users/{id}` | PUT | 更新用户权限 | SC-04 |
| 新增员工 | `/permissions` | `/permissions/users` | POST | 新增员工 | SC-04 |
| 智能推荐 | `/permissions` | `/permissions/recommend` | POST | 智能推荐权限 | SC-04 |
| 角色管理 | `/permissions` | `/permissions/roles` | GET | 获取角色列表 | SC-04 |
| 角色详情 | `/permissions` | `/permissions/roles/{id}` | GET | 获取角色详情 | SC-04 |
| 创建角色 | `/permissions` | `/permissions/roles` | POST | 创建角色 | SC-04 |
| 动态权限规则 | `/permissions` | `/permissions/rules` | GET | 获取动态规则 | SC-04 |
| 权限变更历史 | `/permissions` | `/permissions/history` | GET | 获取变更历史 | SC-07 |
| 一键通知主脑 | `/permissions` | `/permissions/notify-ceo` | POST | 通知主脑 | CL-04 |


## 十九、外部平台账号管理

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 账号总览 | `/accounts` | `/external-accounts/overview` | GET | 获取账号总览 | - |
| 内容平台账号 | `/accounts` | `/external-accounts/platforms` | GET | 获取内容平台账号 | WEB-05 |
| 接单平台账号 | `/accounts` | `/external-accounts/orders` | GET | 获取接单平台账号 | - |
| 媒体平台账号 | `/accounts` | `/external-accounts/media` | GET | 获取媒体平台账号 | - |
| 开发平台账号 | `/accounts` | `/external-accounts/dev` | GET | 获取开发平台账号 | WEB-09 |
| 协作工具账号 | `/accounts` | `/external-accounts/collab` | GET | 获取协作工具账号 | EX-08 |
| AI模型账号 | `/accounts` | `/external-accounts/models` | GET | 获取AI模型账号 | EM-01 |
| 账号详情 | `/accounts` | `/external-accounts/{id}` | GET | 获取账号详情 | - |
| 账号动态 | `/accounts` | `/external-accounts/{id}/stats` | GET | 获取账号动态 | - |
| 连接账号 | `/accounts` | `/external-accounts/connect` | POST | 连接新账号 | WEB-04 |
| 断开账号 | `/accounts` | `/external-accounts/{id}` | DELETE | 断开账号 | - |
| 刷新账号 | `/accounts` | `/external-accounts/{id}/refresh` | POST | 刷新账号数据 | - |
| 账号健康度 | `/accounts` | `/external-accounts/{id}/health` | GET | 获取账号健康度 | AGENT-RUNTIME-05 |
| 批量刷新 | `/accounts` | `/external-accounts/batch-refresh` | POST | 批量刷新 | EX-12 |
| 快捷跳转 | `/accounts` | `/external-accounts/quick-links` | GET | 获取快捷跳转 | - |


## 二十、系统监控

| 前端组件/区域 | 路由 | 后端API | 方法 | 说明 | 关联能力 |
|-------------|------|---------|------|------|----------|
| 系统状态 | `/monitor` | `/system/status` | GET | 获取系统状态 | AGENT-RUNTIME-05 |
| 组件状态 | `/monitor` | `/system/components` | GET | 获取组件状态 | AGENT-RUNTIME-05 |
| 资源使用 | `/monitor` | `/system/resources` | GET | 获取资源使用 | RS-01 |
| 性能指标 | `/monitor` | `/system/performance` | GET | 获取性能指标 | PO-01 |
| API响应时间 | `/monitor` | `/system/performance/api` | GET | 获取API响应时间 | PO-01 |
| 告警列表 | `/monitor` | `/system/alerts` | GET | 获取告警列表 | - |
| 告警规则 | `/monitor` | `/system/alerts/rules` | GET | 获取告警规则 | - |
| 告警规则 | `/monitor` | `/system/alerts/rules` | POST | 创建告警规则 | - |
| 自愈历史 | `/monitor` | `/system/self-healing` | GET | 获取自愈历史 | AGENT-RUNTIME-05 |
| 降级状态 | `/monitor` | `/system/degradation` | GET | 获取降级状态 | EM-03 |


## 二十一、WebSocket/SSE端点

| 用途 | 端点 | 协议 | 说明 | 关联能力 |
|------|------|------|------|----------|
| 实时对话 | `/ws/chat/{session_id}` | WebSocket | 双向实时对话 | PC-01 |
| 流式响应 | `/chat/stream` | SSE | AI响应流式输出 | EM-13 |
| 任务进度 | `/ws/tasks/{task_id}/progress` | WebSocket | 实时任务进度推送 | - |
| 系统告警 | `/ws/alerts` | WebSocket | 实时告警推送 | - |
| 智能体状态 | `/ws/agents/{id}/status` | WebSocket | 智能体状态实时更新 | AGENT-RUNTIME-04 |
| 项目更新 | `/ws/projects/{id}` | WebSocket | 项目实时更新 | - |
| 讨论消息 | `/ws/discussions/{channel}` | WebSocket | 实时讨论消息 | CL-03 |
| 安全事件 | `/ws/security` | WebSocket | 实时安全事件 | SC-01 |
| 成本监控 | `/ws/finance/cost` | WebSocket | 实时成本监控 | EM-05 |


## 二十二、端点汇总表

| 模块 | GET | POST | PUT | DELETE | 总计 | 关联能力数 |
|------|-----|------|-----|--------|------|-----------|
| 认证 | 1 | 9 | 0 | 0 | 10 | SC-04, SC-20 |
| 指挥舱 | 6 | 2 | 0 | 0 | 8 | AGENT-RUNTIME, CG-04 |
| 对话系统 | 5 | 4 | 0 | 1 | 10 | PC-01, EM-13 |
| 智能体管理 | 12 | 6 | 4 | 0 | 22 | HR-01/03, META-01/05 |
| 能力库 | 8 | 1 | 1 | 0 | 10 | META-01/04/05 |
| 培训中心 | 5 | 1 | 1 | 0 | 7 | HR-02, LN-01 |
| 绩效评估 | 4 | 0 | 0 | 0 | 4 | HR-03 |
| 进化中心 | 5 | 0 | 0 | 0 | 5 | META-02/03/04, LN-04/05 |
| 项目全景 | 15 | 6 | 3 | 1 | 25 | DC-01/02/08, CL-01/03 |
| 任务看板 | 4 | 4 | 2 | 0 | 10 | DC-02 |
| 资源池 | 4 | 1 | 0 | 0 | 5 | RS-01 |
| 财务中心 | 14 | 4 | 0 | 0 | 18 | CG-04, EM-05 |
| 营销中心 | 12 | 8 | 1 | 0 | 21 | MK-01~30 |
| 调研中心 | 9 | 2 | 0 | 0 | 11 | KNOW-01, FILE-01 |
| 安全中心 | 12 | 4 | 2 | 0 | 18 | SC-01~20 |
| 外部工具配置 | 8 | 4 | 1 | 1 | 14 | WEB-04/05/09 |
| 权限管理 | 6 | 3 | 1 | 0 | 10 | SC-04 |
| 账号管理 | 9 | 3 | 0 | 1 | 13 | WEB-05, EM-01 |
| 系统监控 | 8 | 1 | 0 | 0 | 9 | AGENT-RUNTIME-05 |
| WebSocket | - | - | - | - | 8 | - |
| **总计** | **147** | **63** | **16** | **4** | **238** | - |


## 二十三、错误码对照表

| 错误码 | 说明 | 处理建议 | 关联能力 |
|--------|------|---------|----------|
| 10001 | 参数验证失败 | 检查请求参数格式 | QL-04 |
| 10002 | 资源不存在 | 检查资源ID是否正确 | - |
| 10003 | 权限不足 | 确认用户角色权限 | SC-04 |
| 10004 | 认证失败 | 重新登录获取token | SC-04 |
| 10005 | Token过期 | 使用refresh_token刷新 | SC-20 |
| 10006 | 请求过于频繁 | 稍后重试 | SC-06 |
| 20001 | 智能体不存在 | 检查agent_id | - |
| 20002 | 智能体离线 | 等待智能体上线或重新启动 | AGENT-RUNTIME-05 |
| 20003 | 能力不存在 | 检查capability_id | META-05 |
| 20004 | 能力未激活 | 先激活能力再调用 | META-01 |
| 20005 | 能力调用失败 | 检查能力配置或降级 | EM-03 |
| 30001 | 项目不存在 | 检查project_id | - |
| 30002 | 任务不存在 | 检查task_id | - |
| 30003 | 任务依赖未满足 | 等待依赖任务完成 | DC-02 |
| 40001 | 模型调用失败 | 检查模型配置或网络 | EM-03 |
| 40002 | 记忆检索失败 | 检查向量数据库连接 | MM-04 |
| 40003 | 外部API调用失败 | 检查API配置或降级 | WEB-04 |
| 50001 | 数据库错误 | 联系运维 | - |
| 50002 | 内部服务错误 | 联系运维 | - |
| 60001 | 配额不足 | 申请扩容或等待重置 | EM-06 |
| 60002 | 预算超限 | 申请追加预算 | EM-05 |


## 二十四、版本记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-12 | 完整版：基于所有子文件和对话内容，补充智能体管理、能力库、培训中心、绩效评估、进化中心、安全中心、财务中心、营销中心、调研中心、外部工具配置、权限管理、账号管理等全部238个端点 |