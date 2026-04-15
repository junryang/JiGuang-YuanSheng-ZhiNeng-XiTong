# 数据库设计文档 - 纪光元生智能系统

| 文档版本 | 修改日期 | 修改人 | 修改内容 |
|---------|---------|--------|---------|
| v1.0 | 2026-01-13 | AI助手 | 完整版：基于所有子文件和对话内容，补充智能体完整数据模型、能力库、记忆系统、安全审计、财务数据、营销数据、调研数据等全部表结构 |


## 一、概述

### 1.1 数据库选型

| 数据库类型 | 产品 | 版本 | 用途 | 关联能力 |
|-----------|------|------|------|----------|
| 关系型数据库 | PostgreSQL | 16+ | 业务数据：用户、智能体、任务、项目等 | EX-04 数据库操作 |
| 向量数据库 | Chroma / Qdrant | 最新 | 智能体记忆、知识检索、语义搜索 | MM-01~08 记忆能力 |
| 缓存数据库 | Redis | 7+ | 会话缓存、任务队列、实时状态、限流 | - |
| 消息队列 | RabbitMQ | 3.12+ | 智能体间异步通信、任务分发 | EX-10 异步执行 |
| 时序数据库 | TimescaleDB | 2.13+ | 系统指标、性能监控、成本记录 | CG-04 数值推理 |
| 图数据库 | Neo4j | 5+ | 知识图谱、智能体关系网络 | KNOW-03 知识图谱 |

### 1.2 命名规范

| 对象类型 | 命名规则 | 示例 |
|---------|---------|------|
| 数据库 | `jyis_{env}` | `jyis_dev`, `jyis_prod` |
| 表名 | 小写+下划线，复数 | `users`, `agent_tasks` |
| 字段名 | 小写+下划线 | `created_at`, `agent_name` |
| 主键 | `id` (UUID格式) | `550e8400-e29b-41d4-a716-446655440000` |
| 外键 | `{关联表}_id` | `project_id`, `agent_id` |
| 索引 | `idx_{表名}_{字段}` | `idx_users_email` |
| 唯一约束 | `uk_{表名}_{字段}` | `uk_users_email` |
| 检查约束 | `ck_{表名}_{字段}` | `ck_agents_level` |


## 二、ER图（实体关系图）- 完整版

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    纪光元生智能系统 ER 图                                        │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐           │
│  │    users     │      │    roles     │      │  user_roles  │      │  user_sessions│           │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤      ├──────────────┤           │
│  │ id (PK)      │─────▶│ id (PK)      │◀─────│ user_id (FK) │      │ id (PK)      │           │
│  │ username     │      │ name         │      │ role_id (FK) │◀─────│ user_id (FK) │           │
│  │ email        │      │ level        │      └──────────────┘      │ token        │           │
│  │ password_hash│      │ permissions  │                            │ expires_at   │           │
│  │ biometric    │      └──────────────┘                            └──────────────┘           │
│  │ status       │                                                                             │
│  └──────────────┘                                                                             │
│         │                                                                                     │
│         │ 1                                                                                   │
│         │                                                                                     │
│         ▼ N                                                                                   │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐         │
│  │   agents     │      │ agent_skills │      │    skills    │      │capabilities  │         │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤      ├──────────────┤         │
│  │ id (PK)      │─────▶│ agent_id(FK) │      │ id (PK)      │      │ id (PK)      │         │
│  │ name         │      │ skill_id(FK) │─────▶│ code         │      │ code         │         │
│  │ level        │      │ level        │      │ name         │      │ name         │         │
│  │ parent_id(FK)│      │ enabled      │      │ category     │      │ category     │         │
│  │ department   │      └──────────────┘      │ description  │      │ status       │         │
│  │ role_type    │                            │ input_schema │      │ version      │         │
│  │ status       │                            │ output_schema│      └──────────────┘         │
│  │ profile      │                            │ dependencies │                                │
│  │ model_config │                            └──────────────┘                                │
│  │ memory_config│                                                                             │
│  │ health_config│      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐         │
│  │ runtime_state│      │agent_capabilities│  │agent_memories│      │  knowledge   │         │
│  │ trust_score  │      ├──────────────┤      ├──────────────┤      ├──────────────┤         │
│  │ created_at   │─────▶│ agent_id(FK) │◀─────│ agent_id(FK) │      │ id (PK)      │         │
│  └──────────────┘      │ capability_id│      │ memory_type  │─────▶│ title        │         │
│         │              │ level        │      │ content      │      │ content      │         │
│         │              │ activated_at │      │ embedding    │      │ embedding    │         │
│         │              └──────────────┘      │ importance   │      │ source       │         │
│         │                                    │ access_level │      │ created_by   │         │
│         │                                    │ created_at   │      └──────────────┘         │
│         │                                    │ expires_at   │                                │
│         │                                    └──────────────┘                                │
│         │                                                                                   │
│         │ 1                                                                                 │
│         │                                                                                   │
│         ▼ N                                                                                 │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐       │
│  │   projects   │      │   tasks      │      │task_assignees│      │task_dependencies│    │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤      ├──────────────┤       │
│  │ id (PK)      │─────▶│ id (PK)      │      │ task_id(FK)  │      │ task_id(FK)  │       │
│  │ name         │      │ project_id   │─────▶│ agent_id(FK) │◀─────│ depends_on   │       │
│  │ domain       │      │ name         │      │ role         │      │ type         │       │
│  │ status       │      │ description  │      └──────────────┘      └──────────────┘       │
│  │ owner_id(FK) │      │ priority     │                                                    │
│  │ start_date   │      │ status       │                                                    │
│  │ end_date     │      │ progress     │      ┌──────────────┐      ┌──────────────┐       │
│  │ budget       │      │ due_date     │      │task_contract │      │task_bids     │       │
│  │ actual_cost  │      │ parent_id(FK)│      ├──────────────┤      ├──────────────┤       │
│  │ plan_document│      │ estimated_hrs│─────▶│ task_id(FK)  │◀─────│ contract_id  │       │
│  └──────────────┘      │ actual_hrs   │      │ status       │      │ agent_id(FK) │       │
│         │              └──────────────┘      │ deadline     │      │ bid_amount   │       │
│         │                                    │ awarded_to   │      │ bid_score    │       │
│         │                                    └──────────────┘      └──────────────┘       │
│         │                                                                                 │
│         │ 1                                                                               │
│         │                                                                                 │
│         ▼ N                                                                               │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐     │
│  │  milestones  │      │   messages   │      │   sessions   │      │  approvals   │     │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤      ├──────────────┤     │
│  │ id (PK)      │      │ id (PK)      │      │ id (PK)      │      │ id (PK)      │     │
│  │ project_id   │─────▶│ session_id   │─────▶│ agent_id(FK) │      │ type         │     │
│  │ name         │      │ sender_type  │      │ user_id(FK)  │      │ requester_id │     │
│  │ planned_date │      │ sender_id    │      │ title        │      │ target_id    │     │
│  │ actual_date  │      │ content      │      │ context      │      │ details      │     │
│  │ status       │      │ role         │      │ created_at   │      │ status       │     │
│  │ deliverable  │      │ metadata     │      │ updated_at   │      │ approved_by  │     │
│  └──────────────┘      └──────────────┘      └──────────────┘      │ comment      │     │
│                                                                     └──────────────┘     │
│                                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              财务与营销模块                                          │ │
│  ├──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │ │
│  │ transactions │      │   budgets    │      │marketing_    │      │ media_tasks  │    │ │
│  ├──────────────┤      ├──────────────┤      │  contents    │      ├──────────────┤    │ │
│  │ id (PK)      │      │ id (PK)      │      ├──────────────┤      │ id (PK)      │    │ │
│  │ type         │─────▶│ name         │      │ id (PK)      │─────▶│ content_id   │    │ │
│  │ amount       │      │ amount       │      │ platform     │      │ media_id     │    │ │
│  │ category     │      │ period       │      │ title        │      │ status       │    │ │
│  │ project_id   │      │ used         │      │ content      │      │ cost         │    │ │
│  │ description  │      │ status       │      │ status       │      │ published_at │    │ │
│  │ created_by   │      └──────────────┘      │ engagement   │      │ indexing     │    │ │
│  └──────────────┘                            │ created_by   │      └──────────────┘    │ │
│                                              └──────────────┘                          │ │
│                                                                                           │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │ │
│  │ competitor   │      │research_files│      │   orders     │      │  invoices    │    │ │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤      ├──────────────┤    │ │
│  │ id (PK)      │      │ id (PK)      │      │ id (PK)      │      │ id (PK)      │    │ │
│  │ name         │      │ name         │      │ platform     │      │ order_id     │    │ │
│  │ domain       │      │ type         │      │ project_name │─────▶│ amount       │    │ │
│  │ metrics      │      │ url          │      │ amount       │      │ status       │    │ │
│  │ swot         │      │ summary      │      │ status       │      │ due_date     │    │ │
│  │ updated_at   │      │ uploaded_by  │      │ created_by   │      └──────────────┘    │ │
│  └──────────────┘      └──────────────┘      └──────────────┘                          │ │
│                                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              安全与监控模块                                          │ │
│  ├──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │ │
│  │ audit_logs   │      │ security_    │      │ system_      │      │ api_keys     │    │ │
│  ├──────────────┤      │   events     │      │   metrics    │      ├──────────────┤    │ │
│  │ id (PK)      │      ├──────────────┤      ├──────────────┤      │ id (PK)      │    │ │
│  │ user_id      │      │ id (PK)      │      │ id (PK)      │      │ name         │    │ │
│  │ agent_id     │      │ event_type   │      │ metric_type  │      │ key_hash     │    │ │
│  │ action       │      │ severity     │      │ value        │      │ user_id      │    │ │
│  │ resource     │      │ source       │      │ unit         │      │ permissions  │    │ │
│  │ details      │      │ description  │      │ agent_id     │      │ last_used    │    │ │
│  │ ip_address   │      │ status       │      │ tags         │      │ expires_at   │    │ │
│  └──────────────┘      └──────────────┘      │ timestamp    │      └──────────────┘    │ │
│                                              └──────────────┘                          │ │
│                                                                                           │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐                            │ │
│  │ integrations │      │  webhooks    │      │ model_calls  │                            │ │
│  ├──────────────┤      ├──────────────┤      ├──────────────┤                            │ │
│  │ id (PK)      │      │ id (PK)      │      │ id (PK)      │                            │ │
│  │ name         │      │ name         │      │ model        │                            │ │
│  │ type         │      │ url          │      │ agent_id     │                            │ │
│  │ config       │      │ events       │      │ tokens_in    │                            │ │
│  │ enabled      │      │ secret       │      │ tokens_out   │                            │ │
│  │ status       │      │ enabled      │      │ cost         │                            │ │
│  └──────────────┘      └──────────────┘      │ duration_ms  │                            │ │
│                                              │ created_at   │                            │ │
│                                              └──────────────┘                            │ │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```


## 三、核心表结构设计

### 3.1 用户与权限模块

#### 表1：users（用户表）

| 字段名 | 类型 | 约束 | 说明 | 关联能力 |
|-------|------|------|------|----------|
| id | UUID | PRIMARY KEY | 用户唯一标识 | - |
| username | VARCHAR(50) | NOT NULL, UNIQUE | 用户名 | - |
| email | VARCHAR(100) | NOT NULL, UNIQUE | 邮箱 | - |
| phone | VARCHAR(20) | | 手机号 | - |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt加密密码 | SC-19 数据加密 |
| avatar_url | TEXT | | 头像URL | - |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'viewer' | 角色 | SC-04 权限检查 |
| biometric_enabled | BOOLEAN | DEFAULT FALSE | 是否启用生物识别 | SC-03 敏感信息检测 |
| face_data | BYTEA | | 人脸特征数据（加密） | SC-03 |
| voice_data | BYTEA | | 声纹特征数据（加密） | SC-03 |
| webauthn_credentials | JSONB | | WebAuthn凭证 | SC-20 访问令牌 |
| mfa_enabled | BOOLEAN | DEFAULT FALSE | 是否启用MFA | SC-04 |
| mfa_secret | VARCHAR(100) | | MFA密钥 | SC-04 |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'active' | active/inactive/locked | - |
| last_login_at | TIMESTAMP | | 最后登录时间 | - |
| last_login_ip | INET | | 最后登录IP | SC-07 操作审计 |
| login_attempts | INTEGER | DEFAULT 0 | 登录失败次数 | SC-06 速率限制 |
| locked_until | TIMESTAMP | | 锁定到期时间 | SC-06 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 | - |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 | - |
| deleted_at | TIMESTAMP | | 软删除时间 | - |

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    role VARCHAR(20) NOT NULL DEFAULT 'viewer',
    biometric_enabled BOOLEAN DEFAULT FALSE,
    face_data BYTEA,
    voice_data BYTEA,
    webauthn_credentials JSONB,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    last_login_at TIMESTAMP,
    last_login_ip INET,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_deleted ON users(deleted_at);

-- 密码强度检查
ALTER TABLE users ADD CONSTRAINT ck_users_password CHECK (length(password_hash) >= 60);
```

#### 表2：roles（角色表）

| 字段名 | 类型 | 约束 | 说明 |
|-------|------|------|------|
| id | UUID | PRIMARY KEY | 角色ID |
| name | VARCHAR(50) | NOT NULL, UNIQUE | 角色名称 |
| level | INTEGER | NOT NULL | 层级: 0-6 |
| permissions | JSONB | NOT NULL | 权限列表 |
| description | TEXT | | 角色描述 |
| is_system | BOOLEAN | DEFAULT FALSE | 是否系统预设 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 |

```sql
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    level INTEGER NOT NULL,
    permissions JSONB NOT NULL DEFAULT '[]',
    description TEXT,
    is_system BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_roles_level ON roles(level);
```

#### 表3：user_roles（用户角色关联表）

```sql
CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    assigned_by UUID REFERENCES users(id),
    expires_at TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);
```

#### 表4：user_sessions（用户会话表）

```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) NOT NULL,
    refresh_token VARCHAR(500),
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    revoked_at TIMESTAMP
);

CREATE INDEX idx_user_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(token);
```


### 3.2 智能体模块

#### 表5：agents（智能体表）

| 字段名 | 类型 | 约束 | 说明 | 关联能力 |
|-------|------|------|------|----------|
| id | UUID | PRIMARY KEY | 智能体ID | - |
| name | VARCHAR(100) | NOT NULL | 智能体名称 | - |
| level | INTEGER | NOT NULL | 层级: 1-6 | AGENT-RUNTIME-01 |
| parent_id | UUID | FOREIGN KEY | 父级智能体ID | - |
| department | VARCHAR(50) | | 所属部门 | - |
| role_type | VARCHAR(50) | NOT NULL | ceo/gm/pm/lead/employee/intern | - |
| role_name | VARCHAR(100) | | 具体岗位名称 | - |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'offline' | online/offline/busy/error/degraded | AGENT-RUNTIME-05 |
| profile | JSONB | | 使命、愿景、价值观、偏好 | AGENT-RUNTIME-02 |
| model_config | JSONB | | 模型配置 | EM-01 |
| memory_config | JSONB | | 记忆配置 | MM-01~08 |
| health_config | JSONB | | 健康检查配置 | AGENT-RUNTIME-05 |
| runtime_state | JSONB | | 认知负载、情绪状态 | AGENT-RUNTIME-04 |
| trust_score | FLOAT | DEFAULT 50.0 | 信任评分 0-100 | AGENT-RUNTIME-06 |
| total_tasks | INTEGER | DEFAULT 0 | 总任务数 | HR-03 |
| completed_tasks | INTEGER | DEFAULT 0 | 完成任务数 | HR-03 |
| success_rate | FLOAT | DEFAULT 0.0 | 成功率 | HR-03 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 | - |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 | - |
| last_active_at | TIMESTAMP | | 最后活跃时间 | - |
| deleted_at | TIMESTAMP | | 软删除时间 | - |

```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    level INTEGER NOT NULL,
    parent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    department VARCHAR(50),
    role_type VARCHAR(50) NOT NULL,
    role_name VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'offline',
    profile JSONB,
    model_config JSONB,
    memory_config JSONB,
    health_config JSONB,
    runtime_state JSONB,
    trust_score FLOAT DEFAULT 50.0,
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    success_rate FLOAT DEFAULT 0.0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_active_at TIMESTAMP,
    deleted_at TIMESTAMP
);

CREATE INDEX idx_agents_parent ON agents(parent_id);
CREATE INDEX idx_agents_level ON agents(level);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_department ON agents(department);
CREATE INDEX idx_agents_role_type ON agents(role_type);
CREATE INDEX idx_agents_trust_score ON agents(trust_score DESC);

ALTER TABLE agents ADD CONSTRAINT ck_agents_level CHECK (level BETWEEN 1 AND 6);
ALTER TABLE agents ADD CONSTRAINT ck_agents_trust_score CHECK (trust_score BETWEEN 0 AND 100);
```

#### 表6：skills（技能表）

| 字段名 | 类型 | 约束 | 说明 | 关联能力 |
|-------|------|------|------|----------|
| id | UUID | PRIMARY KEY | 技能ID | - |
| code | VARCHAR(50) | NOT NULL, UNIQUE | 技能编码 | META-05 |
| name | VARCHAR(100) | NOT NULL | 技能名称 | - |
| name_en | VARCHAR(100) | | 英文名称 | - |
| version | VARCHAR(20) | DEFAULT '1.0.0' | 版本号 | - |
| category | VARCHAR(50) | NOT NULL | 分类 | - |
| description | TEXT | | 技能描述 | - |
| input_schema | JSONB | | 输入参数定义 | - |
| output_schema | JSONB | | 输出结果定义 | - |
| dependencies | UUID[] | | 依赖的技能ID列表 | - |
| examples | JSONB | | 示例用法 | - |
| tags | VARCHAR(50)[] | | 标签 | - |
| execution_config | JSONB | | 执行配置（超时、重试） | - |
| resources | JSONB | | 资源需求 | - |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 | - |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 | - |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 | - |

```sql
CREATE TABLE skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    name_en VARCHAR(100),
    version VARCHAR(20) DEFAULT '1.0.0',
    category VARCHAR(50) NOT NULL,
    description TEXT,
    input_schema JSONB,
    output_schema JSONB,
    dependencies UUID[],
    examples JSONB,
    tags VARCHAR(50)[],
    execution_config JSONB,
    resources JSONB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_skills_category ON skills(category);
CREATE INDEX idx_skills_tags ON skills USING GIN(tags);
CREATE INDEX idx_skills_active ON skills(is_active);
```

#### 表7：capabilities（能力表）- 142项能力

| 字段名 | 类型 | 约束 | 说明 | 关联能力 |
|-------|------|------|------|----------|
| id | UUID | PRIMARY KEY | 能力ID | - |
| code | VARCHAR(50) | NOT NULL, UNIQUE | 能力编码 | META-05 |
| name | VARCHAR(100) | NOT NULL | 能力名称 | - |
| category | VARCHAR(50) | NOT NULL | 分类（AGENT-RUNTIME/WEB/KNOW等） | - |
| level_required | VARCHAR(20) | | 所需智能体层级 | - |
| status | VARCHAR(20) | DEFAULT 'active' | active/developing/deprecated | - |
| version | VARCHAR(20) | DEFAULT '1.0.0' | 版本 | - |
| description | TEXT | | 描述 | - |
| implementation | TEXT | | 实现方式 | - |
| dependencies | UUID[] | | 依赖能力 | - |
| sla | JSONB | | SLA配置 | - |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 | - |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 | - |

```sql
CREATE TABLE capabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    level_required VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    version VARCHAR(20) DEFAULT '1.0.0',
    description TEXT,
    implementation TEXT,
    dependencies UUID[],
    sla JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_capabilities_category ON capabilities(category);
CREATE INDEX idx_capabilities_status ON capabilities(status);
```

#### 表8：agent_capabilities（智能体能力关联表）

```sql
CREATE TABLE agent_capabilities (
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    capability_id UUID REFERENCES capabilities(id) ON DELETE CASCADE,
    level VARCHAR(20) NOT NULL DEFAULT 'B',
    activated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    activated_by UUID REFERENCES agents(id),
    PRIMARY KEY (agent_id, capability_id)
);
```

#### 表9：agent_skills（智能体技能关联表）

```sql
CREATE TABLE agent_skills (
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    skill_id UUID REFERENCES skills(id) ON DELETE CASCADE,
    level VARCHAR(20) NOT NULL DEFAULT 'junior',
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    assigned_by UUID REFERENCES agents(id),
    PRIMARY KEY (agent_id, skill_id)
);
```


### 3.3 项目管理模块

#### 表10：projects（项目表）

| 字段名 | 类型 | 约束 | 说明 | 关联能力 |
|-------|------|------|------|----------|
| id | UUID | PRIMARY KEY | 项目ID | - |
| code | VARCHAR(50) | UNIQUE | 项目编号 | - |
| name | VARCHAR(200) | NOT NULL | 项目名称 | - |
| domain | VARCHAR(20) | NOT NULL | 领域: D01-D08 | - |
| type | VARCHAR(50) | | 项目类型 | - |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | draft/pending/approved/in_progress/completed/cancelled | - |
| phase | VARCHAR(20) | | 当前阶段 | PROJECT_LIFECYCLE |
| owner_id | UUID | FOREIGN KEY | 项目负责人ID | - |
| start_date | DATE | | 开始日期 | - |
| end_date | DATE | | 预计完成日期 | - |
| actual_end_date | DATE | | 实际完成日期 | - |
| progress | INTEGER | DEFAULT 0 | 进度百分比 | CG-04 |
| budget | DECIMAL(15,2) | | 预算 | - |
| actual_cost | DECIMAL(15,2) | | 实际成本 | - |
| plan_document | TEXT | | 项目计划书 | DC-01 |
| goals | JSONB | | 项目目标 | - |
| scope | JSONB | | 项目范围 | - |
| risks | JSONB | | 风险评估 | DC-08 |
| health_score | FLOAT | | 健康度评分 0-100 | QL-07 |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 | - |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 | - |
| deleted_at | TIMESTAMP | | 软删除时间 | - |

```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE,
    name VARCHAR(200) NOT NULL,
    domain VARCHAR(20) NOT NULL,
    type VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    phase VARCHAR(20),
    owner_id UUID REFERENCES agents(id),
    start_date DATE,
    end_date DATE,
    actual_end_date DATE,
    progress INTEGER DEFAULT 0,
    budget DECIMAL(15,2),
    actual_cost DECIMAL(15,2),
    plan_document TEXT,
    goals JSONB,
    scope JSONB,
    risks JSONB,
    health_score FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_domain ON projects(domain);
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_health ON projects(health_score);
```

#### 表11：milestones（里程碑表）

```sql
CREATE TABLE milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    planned_date DATE NOT NULL,
    actual_date DATE,
    status VARCHAR(20) DEFAULT 'pending',
    deliverable TEXT,
    acceptance_criteria TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_milestones_project ON milestones(project_id);
```

#### 表12：tasks（任务表）

| 字段名 | 类型 | 约束 | 说明 | 关联能力 |
|-------|------|------|------|----------|
| id | UUID | PRIMARY KEY | 任务ID | - |
| project_id | UUID | FOREIGN KEY | 所属项目ID | - |
| milestone_id | UUID | FOREIGN KEY | 所属里程碑ID | - |
| name | VARCHAR(200) | NOT NULL | 任务名称 | - |
| description | TEXT | | 任务描述 | - |
| priority | VARCHAR(20) | NOT NULL, DEFAULT 'medium' | low/medium/high/critical | DC-05 |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' | pending/assigned/in_progress/blocked/completed/failed | - |
| progress | INTEGER | DEFAULT 0 | 进度百分比 | - |
| parent_id | UUID | FOREIGN KEY | 父任务ID | DC-02 |
| due_date | DATE | | 截止日期 | - |
| completed_at | TIMESTAMP | | 完成时间 | - |
| estimated_hours | DECIMAL(8,2) | | 预估工时 | - |
| actual_hours | DECIMAL(8,2) | | 实际工时 | - |
| required_capabilities | UUID[] | | 所需能力 | - |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 创建时间 | - |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | 更新时间 | - |

```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    milestone_id UUID REFERENCES milestones(id) ON DELETE SET NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    progress INTEGER DEFAULT 0,
    parent_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    due_date DATE,
    completed_at TIMESTAMP,
    estimated_hours DECIMAL(8,2),
    actual_hours DECIMAL(8,2),
    required_capabilities UUID[],
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_parent ON tasks(parent_id);
CREATE INDEX idx_tasks_priority ON tasks(priority);
```

#### 表13：task_assignees（任务指派表）

```sql
CREATE TABLE task_assignees (
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'assignee',
    assigned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    assigned_by UUID REFERENCES agents(id),
    PRIMARY KEY (task_id, agent_id)
);
```

#### 表14：task_dependencies（任务依赖表）

```sql
CREATE TABLE task_dependencies (
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    depends_on_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    type VARCHAR(20) DEFAULT 'finish_to_start',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY (task_id, depends_on_id)
);
```

#### 表15：task_contracts（合同网协议表）

```sql
CREATE TABLE task_contracts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'tendering',
    deadline TIMESTAMP,
    awarded_to UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMP
);

CREATE INDEX idx_contracts_task ON task_contracts(task_id);
```

#### 表16：task_bids（任务投标表）

```sql
CREATE TABLE task_bids (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contract_id UUID REFERENCES task_contracts(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    bid_amount DECIMAL(10,2),
    bid_score FLOAT,
    estimated_hours INTEGER,
    proposal TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_bids_contract ON task_bids(contract_id);
CREATE INDEX idx_bids_agent ON task_bids(agent_id);
```


### 3.4 对话与记忆模块

#### 表17：sessions（对话会话表）

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200),
    context JSONB,
    importance_score FLOAT DEFAULT 0.5,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    closed_at TIMESTAMP
);

CREATE INDEX idx_sessions_agent ON sessions(agent_id);
CREATE INDEX idx_sessions_user ON sessions(user_id);
```

#### 表18：messages（消息表）

```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES sessions(id) ON DELETE CASCADE,
    sender_type VARCHAR(20) NOT NULL,
    sender_id UUID NOT NULL,
    content TEXT NOT NULL,
    role VARCHAR(20),
    metadata JSONB,
    tokens_used INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_messages_session ON messages(session_id);
CREATE INDEX idx_messages_sender ON messages(sender_type, sender_id);
```

#### 表19：agent_memories（智能体记忆表）

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE agent_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    memory_type VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    importance FLOAT DEFAULT 0.5,
    access_level VARCHAR(20) NOT NULL DEFAULT 'private',
    access_count INTEGER DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_accessed TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX idx_memories_agent ON agent_memories(agent_id);
CREATE INDEX idx_memories_type ON agent_memories(memory_type);
CREATE INDEX idx_memories_access ON agent_memories(access_level);
CREATE INDEX idx_memories_embedding ON agent_memories USING ivfflat (embedding vector_cosine_ops);
```

#### 表20：knowledge_base（知识库表）

```sql
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    source VARCHAR(200),
    source_url TEXT,
    category VARCHAR(50),
    tags VARCHAR(50)[],
    credibility FLOAT DEFAULT 0.5,
    created_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_knowledge_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_knowledge_category ON knowledge_base(category);
```


### 3.5 审批模块

#### 表21：approvals（审批表）

```sql
CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) NOT NULL,
    requester_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    target_id UUID,
    details JSONB NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    current_level INTEGER DEFAULT 1,
    approval_chain JSONB,
    approved_by UUID REFERENCES agents(id),
    comment TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMP
);

CREATE INDEX idx_approvals_status ON approvals(status);
CREATE INDEX idx_approvals_requester ON approvals(requester_id);
CREATE INDEX idx_approvals_type ON approvals(type);
```


### 3.6 财务模块

#### 表22：transactions（收支记录表）

```sql
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(20) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'CNY',
    category VARCHAR(50),
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    transaction_date DATE NOT NULL,
    created_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transactions_type ON transactions(type);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_project ON transactions(project_id);
```

#### 表23：budgets（预算表）

```sql
CREATE TABLE budgets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    period VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    used DECIMAL(15,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_budgets_period ON budgets(period);
```

#### 表24：model_calls（模型调用记录表）

```sql
CREATE TABLE model_calls (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    model VARCHAR(50) NOT NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    tokens_in INTEGER,
    tokens_out INTEGER,
    cost DECIMAL(10,4),
    duration_ms INTEGER,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_model_calls_model ON model_calls(model);
CREATE INDEX idx_model_calls_agent ON model_calls(agent_id);
CREATE INDEX idx_model_calls_created ON model_calls(created_at);
```


### 3.7 营销模块

#### 表25：marketing_contents（营销内容表）

```sql
CREATE TABLE marketing_contents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    content_type VARCHAR(50),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',
    scheduled_at TIMESTAMP,
    published_at TIMESTAMP,
    engagement JSONB,
    ai_review JSONB,
    risk_score FLOAT,
    created_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_contents_status ON marketing_contents(status);
CREATE INDEX idx_contents_platform ON marketing_contents(platform);
```

#### 表26：media_tasks（媒体发稿任务表）

```sql
CREATE TABLE media_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_id UUID REFERENCES marketing_contents(id) ON DELETE CASCADE,
    media_id VARCHAR(100),
    media_name VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    cost DECIMAL(10,2),
    published_at TIMESTAMP,
    indexing JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_media_tasks_content ON media_tasks(content_id);
```

#### 表27：competitors（竞品表）

```sql
CREATE TABLE competitors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    domain VARCHAR(50),
    metrics JSONB,
    swot JSONB,
    last_updated TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### 表28：orders（接单表）

```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,
    external_id VARCHAR(200),
    project_name VARCHAR(500),
    amount DECIMAL(15,2),
    currency VARCHAR(3) DEFAULT 'CNY',
    status VARCHAR(20) DEFAULT 'pending',
    match_score FLOAT,
    quote_amount DECIMAL(15,2),
    created_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP
);

CREATE INDEX idx_orders_platform ON orders(platform);
CREATE INDEX idx_orders_status ON orders(status);
```


### 3.8 调研模块

#### 表29：research_files（调研文件表）

```sql
CREATE TABLE research_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50),
    category VARCHAR(50),
    url TEXT,
    summary TEXT,
    embedding VECTOR(1536),
    uploaded_by UUID REFERENCES agents(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_research_files_category ON research_files(category);
```


### 3.9 安全与监控模块

#### 表30：audit_logs（审计日志表）

```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    status VARCHAR(20),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_agent ON audit_logs(agent_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_created ON audit_logs(created_at);
```

#### 表31：security_events（安全事件表）

```sql
CREATE TABLE security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    source_ip INET,
    details JSONB,
    status VARCHAR(20) DEFAULT 'open',
    resolved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_security_events_type ON security_events(event_type);
CREATE INDEX idx_security_events_severity ON security_events(severity);
```

#### 表32：system_metrics（系统指标表）- TimescaleDB

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE system_metrics (
    time TIMESTAMPTZ NOT NULL,
    metric_type VARCHAR(50) NOT NULL,
    value FLOAT NOT NULL,
    unit VARCHAR(20),
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    tags JSONB
);

SELECT create_hypertable('system_metrics', 'time');
CREATE INDEX idx_metrics_type_time ON system_metrics(metric_type, time DESC);
```

#### 表33：api_keys（API密钥表）

```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    permissions JSONB,
    last_used TIMESTAMP,
    expires_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    revoked_at TIMESTAMP
);

CREATE INDEX idx_api_keys_user ON api_keys(user_id);
```

#### 表34：integrations（集成配置表）

```sql
CREATE TABLE integrations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,
    type VARCHAR(20) NOT NULL,
    config JSONB NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    status VARCHAR(20) DEFAULT 'disconnected',
    last_sync TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

#### 表35：webhooks（Webhook表）

```sql
CREATE TABLE webhooks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    events VARCHAR(50)[] NOT NULL,
    secret VARCHAR(200),
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```


## 四、Redis数据结构设计

### 4.1 会话缓存

| Key格式 | 类型 | 说明 | TTL |
|---------|------|------|-----|
| `session:{session_id}` | Hash | 会话信息 | 24h |
| `session:{session_id}:messages` | List | 会话消息列表 | 24h |
| `user:{user_id}:session` | String | 用户当前会话ID | 24h |

### 4.2 任务队列

| Key格式 | 类型 | 说明 |
|---------|------|------|
| `queue:tasks:critical` | List | 紧急任务队列 |
| `queue:tasks:high` | List | 高优先级任务队列 |
| `queue:tasks:medium` | List | 中优先级任务队列 |
| `queue:tasks:low` | List | 低优先级任务队列 |

### 4.3 智能体状态

| Key格式 | 类型 | 说明 | TTL |
|---------|------|------|-----|
| `agent:{agent_id}:status` | String | 智能体在线状态 | 30s |
| `agent:{agent_id}:heartbeat` | String | 心跳时间戳 | 30s |
| `agent:{agent_id}:load` | String | 当前负载 | 10s |
| `agent:{agent_id}:current_task` | String | 当前执行任务 | 任务结束 |

### 4.4 限流计数器

| Key格式 | 类型 | 说明 | TTL |
|---------|------|------|-----|
| `ratelimit:user:{user_id}:{api}` | String | 用户API调用计数 | 1min |
| `ratelimit:agent:{agent_id}:{api}` | String | 智能体API调用计数 | 1min |
| `ratelimit:ip:{ip}` | String | IP限流计数 | 1min |

### 4.5 能力缓存

| Key格式 | 类型 | 说明 | TTL |
|---------|------|------|-----|
| `capability:{code}` | Hash | 能力配置缓存 | 1h |
| `agent:{agent_id}:capabilities` | Set | 智能体能力列表 | 5min |

### 4.6 记忆缓存

| Key格式 | 类型 | 说明 | TTL |
|---------|------|------|-----|
| `memory:working:{agent_id}` | Hash | 工作记忆 | 任务结束 |
| `memory:short_term:{agent_id}` | List | 短期记忆 | 7天 |


## 五、初始化数据

### 5.1 角色初始化

```sql
INSERT INTO roles (id, name, level, permissions, is_system) VALUES
    ('role_boss', '创始人', 0, '["*"]', TRUE),
    ('role_partner', '合伙人', 0, '["finance.*", "project.*", "agent.read", "report.*"]', TRUE),
    ('role_ceo', 'CEO', 1, '["approve.*", "project.*", "agent.*", "resource.*", "report.*"]', TRUE),
    ('role_cfo', 'CFO', 2, '["finance.*", "budget.*", "report.read"]', TRUE),
    ('role_cto', 'CTO', 2, '["agent.*", "capability.*", "security.read", "system.*"]', TRUE),
    ('role_gm', '总经理', 2, '["project.*", "agent.list", "resource.request"]', TRUE),
    ('role_pm', '项目经理', 3, '["task.*", "project.view", "team.manage"]', TRUE),
    ('role_lead', '主管', 4, '["task.assign", "code.review", "team.view"]', TRUE),
    ('role_employee', '员工', 5, '["task.execute", "code.write", "doc.write"]', TRUE),
    ('role_intern', '实习', 6, '["task.view", "code.read", "doc.read"]', TRUE),
    ('role_analyst', '分析师', 5, '["report.read", "data.read"]', TRUE),
    ('role_auditor', '审计员', 5, '["audit.read", "finance.read"]', TRUE);
```

### 5.2 初始智能体（主脑）

```sql
INSERT INTO agents (id, name, level, role_type, status, profile, model_config) VALUES
    ('agent_ceo', '主脑', 1, 'ceo', 'online', 
     '{"mission": "理解老板意图，拆解为可执行目标，协调全系统资源达成战略目标", "values": ["诚信", "卓越", "协作"]}',
     '{"model": "deepseek-v3", "temperature": 0.7, "max_tokens": 4096}');
```

### 5.3 初始用户

```sql
INSERT INTO users (id, username, email, password_hash, role) VALUES
    ('user_boss', 'boss', 'boss@jyis.com', '$2b$12$...', 'boss');
```

### 5.4 能力初始化

```sql
INSERT INTO capabilities (code, name, category, status) VALUES
    ('AGENT-RUNTIME-01', '智能体主循环', 'AGENT-RUNTIME', 'active'),
    ('AGENT-RUNTIME-02', '长期目标与个人偏好', 'AGENT-RUNTIME', 'active'),
    ('WEB-01', '浏览器自动化', 'WEB', 'active'),
    ('WEB-02', '搜索引擎查询', 'WEB', 'active'),
    ('EX-01', '代码生成', 'EXECUTION', 'active'),
    ('EX-03', 'API调用', 'EXECUTION', 'active');
```


## 六、备份策略

| 备份类型 | 频率 | 保留时间 | 工具 |
|---------|------|---------|------|
| 全量备份 | 每日02:00 | 30天 | pg_dump |
| 增量备份 | 每小时 | 7天 | WAL归档 |
| 向量数据备份 | 每周日 | 90天 | Chroma备份 |
| Redis备份 | 每小时 | 7天 | RDB + AOF |
| 配置备份 | 每日 | 30天 | kubectl |


## 七、版本记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-13 | 完整版：基于所有子文件和对话内容，新增智能体完整数据模型、能力表、合同网协议表、财务表、营销表、调研表、安全审计表、模型调用表、TimescaleDB指标表等35张表 |