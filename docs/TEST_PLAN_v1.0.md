# 测试计划文档 - 纪光元生智能系统

| 文档版本 | 修改日期 | 修改人 | 修改内容 |
|---------|---------|--------|---------|
| v1.0 | 2026-01-12 | AI助手 | 完整版：基于所有子文件和对话内容，补充智能体团队测试、能力测试、动态测试、安全团队测试 |


## 一、概述

> 裁决说明：若性能阈值与其他文档存在冲突，以 `docs/PERFORMANCE_METRICS_v1.0.md` 为基线。

### 1.1 测试目标

| 目标类型 | 具体目标 | 衡量指标 | 关联能力 |
|---------|---------|---------|----------|
| 功能正确性 | 所有核心功能正常工作 | 通过率 100% | QL-05 质量验证 |
| 智能体能力验证 | 142项能力全部可用 | 能力激活率 100% | META-05 能力注册 |
| 性能 | 系统响应时间符合要求（MK-01口径） | P95 ≤ 180秒，单次 ≤ 300秒 | PO-01 响应时间优化 |
| 稳定性 | 长时间运行无异常 | 7x24小时无重启 | AGENT-RUNTIME-05 健康自检 |
| 安全性 | 无高危漏洞 | 安全扫描无高危 | SC-01~20 安全能力 |
| 兼容性 | 主流浏览器可用 | Chrome/Firefox/Edge | COMPAT-01 浏览器兼容 |
| 智能体协作 | 多智能体协同正常 | 合同网协议成功率>95% | CL-06 合同网协议 |
| 学习能力 | 智能体持续进化 | 学习效率>10%/月 | LN-01~06 学习能力 |

### 1.2 测试范围

| 模块 | 测试范围 | 优先级 | 关联智能体团队 |
|------|---------|--------|---------------|
| 用户认证 | 登录、注册、权限、生物识别 | P0 | 安全团队 |
| 智能体管理 | 创建、配置、监控、能力库 | P0 | 智能体部 |
| 项目管理 | 创建、立项、进度跟踪、资源池 | P0 | 项目部 |
| 任务调度 | 创建、执行、通知、依赖 | P0 | 项目部 |
| 代码生成 | 生成、修改、验证、沙箱 | P1 | 后端部 |
| 对话系统 | 对话、历史、语音、意图识别 | P1 | 主脑 |
| 营销中心 | 内容管理、分发、分析、竞品 | P1 | 营销部 |
| 接单变现 | 项目匹配、报价、收益 | P1 | 营销部 |
| 媒体发稿 | 媒体资源、发稿、收录、GEO | P2 | 营销部 |
| 主脑策略引擎 | CEO-POLICY-09~14、环境门禁、降级与审批链 | P0 | 主脑/安全团队 |
| 财务中心 | 收支、成本、预算、税务、对账 | P1 | 财务部 |
| 系统监控 | 监控、告警、自愈 | P1 | 运维部 |
| 安全中心 | 威胁防护、漏洞管理、合规 | P0 | 安全团队 |
| 能力库 | 142项能力、工具库、技能库 | P0 | 智能体部 |
| 智能体进化 | 自我反思、双循环学习、内在动机 | P1 | 智能体部 |

### 1.3 测试环境

| 环境 | 用途 | 配置 | 智能体配置 |
|------|------|------|-----------|
| 开发环境 | 单元测试、集成测试 | 2核4G | 10个测试智能体 |
| 测试环境 | 功能测试、回归测试 | 4核8G | 全部47个智能体 |
| 预发布环境 | 验收测试、性能测试 | 4核8G | 全部47个智能体 |
| 生产环境 | 烟雾测试 | 8核16G | 全部47个智能体 |


## 二、测试策略

### 2.1 测试金字塔

```
                    ┌─────────────────────────────────────────────────────────┐
                    │              端到端测试 (E2E)                            │
                    │                 约 5%                                    │
                    │    关键用户路径验证、智能体协作链路验证                   │
                    ├─────────────────────────────────────────────────────────┤
                    │            集成测试 (Integration)                        │
                    │                 约 15%                                   │
                    │    API接口、服务间调用、智能体间通信、合同网协议          │
                    ├─────────────────────────────────────────────────────────┤
                    │              单元测试 (Unit)                             │
                    │                 约 80%                                   │
                    │      函数、类、模块级测试、能力单元测试                   │
                    └─────────────────────────────────────────────────────────┘
```

### 2.2 测试类型

| 测试类型 | 执行频率 | 负责智能体 | 工具 | 关联能力 |
|---------|---------|-----------|------|----------|
| 单元测试 | 每次提交 | 开发者/智能体自测 | pytest | EX-07 测试执行 |
| 集成测试 | 每日 | 测试主管 | pytest + requests | EX-07 测试执行 |
| 功能测试 | 每轮迭代 | 测试工程师 | Playwright | AUTO-06 自动化测试 |
| 回归测试 | 发版前 | 测试工程师 | Playwright | AUTO-06 自动化测试 |
| 性能测试 | 每周 | 测试工程师 | Locust | PO-01 响应时间优化 |
| 安全测试 | 每日 | 安全工程师 | OWASP ZAP | SC-01~20 安全能力 |
| 兼容性测试 | 每季度 | 测试工程师 | BrowserStack | COMPAT-01 浏览器兼容 |
| 烟雾测试 | 每次部署 | 自动/运维主管 | curl + pytest | AGENT-RUNTIME-05 健康自检 |
| 能力测试 | 能力变更时 | 智能体工程师 | pytest | META-05 能力注册 |
| 策略测试 | 每次策略变更 | 安全工程师/主脑联调 | policy-sim + pytest | CEO-POLICY-09~14 / LAW-01~05 |
| 协作测试 | 每周 | 项目协调员 | 自定义 | CL-06 合同网协议 |
| 学习效果测试 | 每月 | 智能体培训师 | 自定义 | LN-01~06 学习能力 |

> 策略测试样例与预期结果详见：`docs/STRATEGY_TEST_CASES_v1.0.md`。

### 2.3 通过标准

| 指标 | 标准 | 关联能力 |
|------|------|----------|
| 单元测试覆盖率 | 全局≥80%，核心模块按quality_standards更高门槛执行 | QL-05 质量验证 |
| 集成测试通过率 | 100% | QL-05 质量验证 |
| 功能测试通过率 | 100% | QL-05 质量验证 |
| 核心API成功率 | ≥ 99.5% | PO-01 响应时间优化 |
| 无P0/P1级别Bug | 必须为0 | QL-01 代码质量感知 |
| 性能指标 | P95 ≤ 180秒，单次 ≤ 300秒 | PO-01 响应时间优化 |
| 安全扫描 | 无高危漏洞 | SC-01~20 安全能力 |
| 能力激活率 | 100% | META-05 能力注册 |
| 智能体协作成功率 | ≥ 95% | CL-06 合同网协议 |


## 三、智能体团队测试

### 3.1 智能体测试团队配置

| 智能体 | 岗位 | 测试职责 | 关联能力 |
|--------|------|---------|----------|
| 测试主管 | L4 测试负责人 | 统筹测试工作，审核测试报告 | QL-05 质量验证 |
| 测试工程师A | L5 功能测试 | 功能测试、回归测试 | AUTO-06 自动化测试 |
| 测试工程师B | L5 性能测试 | 性能测试、压力测试 | PO-01 响应时间优化 |
| 安全工程师A | L5 安全测试 | 安全扫描、渗透测试 | SC-01~20 安全能力 |
| 智能体工程师A | L5 能力测试 | 能力验证、能力开发测试 | META-05 能力注册 |
| 实习测试助理 | L6 测试助理 | 测试用例执行、Bug记录 | EX-07 测试执行 |

### 3.2 测试任务分配

| 测试任务 | 负责智能体 | 频率 | 报告对象 |
|---------|-----------|------|---------|
| 单元测试执行 | 各开发智能体 | 每次提交 | 测试主管 |
| 集成测试执行 | 测试工程师A | 每日 | 测试主管 |
| 功能测试执行 | 测试工程师A | 每轮迭代 | 测试主管 |
| 性能测试执行 | 测试工程师B | 每周 | 测试主管 |
| 安全测试执行 | 安全工程师A | 每日 | 安全主管 |
| 能力验证测试 | 智能体工程师A | 能力变更时 | 智能体主管 |
| 协作测试 | 项目协调员 | 每周 | 项目经理 |
| 测试报告汇总 | 测试主管 | 每周 | 主脑 |


## 四、单元测试

### 4.1 测试框架配置

**`tests/conftest.py`**

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from core.database import Base, get_db

# 测试数据库
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client_with_auth(client):
    """已认证的客户端"""
    response = client.post("/api/v1/auth/login", json={
        "username": "test_boss@jyis.com",
        "password": "Test123!@#"
    })
    token = response.json()["data"]["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
def mock_agent_response():
    """模拟智能体响应"""
    return {
        "id": "test_agent_001",
        "name": "测试智能体",
        "level": 5,
        "status": "online",
        "cognitive_load": 0.45,
        "trust_score": 95
    }

@pytest.fixture
def mock_contract_net():
    """模拟合同网协议"""
    return {
        "task_id": "task_001",
        "bids": [
            {"agent_id": "agent_001", "bid_score": 95, "price": 1000},
            {"agent_id": "agent_002", "bid_score": 88, "price": 900}
        ],
        "winner": "agent_001"
    }
```

### 4.2 用户认证单元测试

**`tests/test_auth.py`**

```python
import pytest
from fastapi.testclient import TestClient

class TestAuth:
    
    def test_login_success(self, client: TestClient):
        """TC-AUTH-01：正确登录"""
        response = client.post("/api/v1/auth/login", json={
            "username": "boss@jyis.com",
            "password": "correct_password"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()["data"]
    
    def test_login_wrong_password(self, client: TestClient):
        """TC-AUTH-02：错误密码"""
        response = client.post("/api/v1/auth/login", json={
            "username": "boss@jyis.com",
            "password": "wrong_password"
        })
        assert response.status_code == 401
        assert "密码错误" in response.json()["message"]
    
    def test_login_missing_fields(self, client: TestClient):
        """TC-AUTH-04：空表单"""
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422
    
    def test_biometric_login(self, client: TestClient, mocker):
        """测试生物识别登录"""
        mocker.patch("core.auth.biometric.verify_face", return_value=True)
        response = client.post("/api/v1/auth/biometric", json={
            "face_data": "base64_encoded_face_data"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()["data"]
    
    def test_biometric_login_failed(self, client: TestClient, mocker):
        """生物识别失败"""
        mocker.patch("core.auth.biometric.verify_face", return_value=False)
        response = client.post("/api/v1/auth/biometric", json={
            "face_data": "invalid_face_data"
        })
        assert response.status_code == 401
    
    def test_get_current_user(self, client_with_auth):
        """TC-AUTH-05：获取当前用户"""
        response = client_with_auth.get("/api/v1/auth/me")
        assert response.status_code == 200
        assert response.json()["data"]["username"] == "boss@jyis.com"
    
    def test_access_without_token(self, client: TestClient):
        """TC-AUTH-06：无token访问"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_token_refresh(self, client_with_auth):
        """刷新token"""
        response = client_with_auth.post("/api/v1/auth/refresh")
        assert response.status_code == 200
        assert "access_token" in response.json()["data"]
```

### 4.3 智能体管理单元测试

**`tests/test_agents.py`**

```python
import pytest

class TestAgents:
    
    def test_list_agents(self, client_with_auth):
        """TC-AGENT-01：查看智能体列表"""
        response = client_with_auth.get("/api/v1/agents")
        assert response.status_code == 200
        assert "items" in response.json()["data"]
        assert isinstance(response.json()["data"]["items"], list)
    
    def test_filter_agents_by_level(self, client_with_auth):
        """按层级筛选智能体"""
        response = client_with_auth.get("/api/v1/agents?level=L5")
        assert response.status_code == 200
        items = response.json()["data"]["items"]
        for item in items:
            assert item["level"] == "L5"
    
    def test_filter_agents_by_department(self, client_with_auth):
        """按部门筛选智能体"""
        response = client_with_auth.get("/api/v1/agents?department=后端部")
        assert response.status_code == 200
        items = response.json()["data"]["items"]
        for item in items:
            assert item["department"] == "后端部"
    
    def test_search_agents(self, client_with_auth):
        """TC-AGENT-02：搜索智能体"""
        response = client_with_auth.get("/api/v1/agents?keyword=主脑")
        assert response.status_code == 200
    
    def test_get_agent_by_id(self, client_with_auth):
        """TC-AGENT-04：查看智能体详情"""
        list_resp = client_with_auth.get("/api/v1/agents")
        agent_id = list_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.get(f"/api/v1/agents/{agent_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == agent_id
        assert "cognitive_state" in response.json()["data"]
        assert "health_status" in response.json()["data"]
    
    def test_get_nonexistent_agent(self, client_with_auth):
        """获取不存在的智能体"""
        response = client_with_auth.get("/api/v1/agents/nonexistent-id")
        assert response.status_code == 404
    
    def test_create_agent(self, client_with_auth):
        """创建智能体"""
        response = client_with_auth.post("/api/v1/agents", json={
            "name": "测试智能体",
            "level": "L5",
            "role_type": "employee",
            "department": "测试部",
            "capabilities": ["EX-01", "EX-03", "EX-04"]
        })
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "测试智能体"
    
    def test_update_agent_config(self, client_with_auth):
        """TC-AGENT-05：配置智能体"""
        create_resp = client_with_auth.post("/api/v1/agents", json={
            "name": "待配置智能体",
            "level": "L5",
            "role_type": "employee"
        })
        agent_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.put(f"/api/v1/agents/{agent_id}/config", json={
            "model_config": {"model": "deepseek-v3", "temperature": 0.7},
            "memory_config": {"working_memory_mb": 10}
        })
        assert response.status_code == 200
    
    def test_get_agent_skills(self, client_with_auth):
        """TC-AGENT-06：查看智能体技能"""
        list_resp = client_with_auth.get("/api/v1/agents")
        agent_id = list_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.get(f"/api/v1/agents/{agent_id}/skills")
        assert response.status_code == 200
        assert "skills" in response.json()["data"]
    
    def test_enable_disable_skill(self, client_with_auth):
        """TC-AGENT-07：启用/禁用技能"""
        list_resp = client_with_auth.get("/api/v1/agents")
        agent_id = list_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.put(f"/api/v1/agents/{agent_id}/skills", json={
            "skills": [{"skill_id": "EX-01", "enabled": True}]
        })
        assert response.status_code == 200
    
    def test_get_agent_memory(self, client_with_auth):
        """TC-AGENT-08：查看智能体记忆"""
        list_resp = client_with_auth.get("/api/v1/agents")
        agent_id = list_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.get(f"/api/v1/agents/{agent_id}/memory")
        assert response.status_code == 200
        assert "working_memory" in response.json()["data"]
        assert "long_term_memory" in response.json()["data"]
    
    def test_search_agent_memory(self, client_with_auth):
        """TC-AGENT-09：搜索智能体记忆"""
        list_resp = client_with_auth.get("/api/v1/agents")
        agent_id = list_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.get(f"/api/v1/agents/{agent_id}/memory?query=API")
        assert response.status_code == 200
    
    def test_get_agent_stats(self, client_with_auth):
        """获取智能体统计"""
        list_resp = client_with_auth.get("/api/v1/agents")
        agent_id = list_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.get(f"/api/v1/agents/{agent_id}/stats")
        assert response.status_code == 200
        assert "performance" in response.json()["data"]
        assert "efficiency" in response.json()["data"]
```

### 4.4 项目管理单元测试

**`tests/test_projects.py`**

```python
import pytest

class TestProjects:
    
    def test_create_project(self, client_with_auth):
        """TC-PROJ-01：创建项目"""
        response = client_with_auth.post("/api/v1/projects", json={
            "name": "测试项目",
            "domain": "D03",
            "budget": 50000,
            "description": "测试项目描述"
        })
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "测试项目"
        assert response.json()["data"]["status"] == "draft"
    
    def test_list_projects(self, client_with_auth):
        """TC-PROJ-03：查看项目列表"""
        response = client_with_auth.get("/api/v1/projects")
        assert response.status_code == 200
        assert "items" in response.json()["data"]
    
    def test_filter_projects_by_status(self, client_with_auth):
        """按状态筛选项目"""
        response = client_with_auth.get("/api/v1/projects?status=in_progress")
        assert response.status_code == 200
    
    def test_filter_projects_by_domain(self, client_with_auth):
        """按领域筛选项目"""
        response = client_with_auth.get("/api/v1/projects?domain=D03")
        assert response.status_code == 200
    
    def test_get_project_detail(self, client_with_auth):
        """TC-PROJ-04：查看项目详情"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "详情测试项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == project_id
    
    def test_update_project(self, client_with_auth):
        """TC-PROJ-05：编辑项目信息"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "待更新项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.put(f"/api/v1/projects/{project_id}", json={
            "name": "已更新项目名称",
            "budget": 100000
        })
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "已更新项目名称"
    
    def test_delete_project(self, client_with_auth):
        """TC-PROJ-06：删除项目"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "待删除项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        
        # 验证已删除
        get_resp = client_with_auth.get(f"/api/v1/projects/{project_id}")
        assert get_resp.status_code == 404
    
    def test_submit_project_for_approval(self, client_with_auth):
        """TC-PROJ-02：项目立项审批"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "待审批项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.post(f"/api/v1/projects/{project_id}/submit")
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "pending_approval"
    
    def test_approve_project(self, client_with_auth):
        """批准项目"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "待批准项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        client_with_auth.post(f"/api/v1/projects/{project_id}/submit")
        
        response = client_with_auth.post(f"/api/v1/projects/{project_id}/approve", json={
            "comment": "批准立项"
        })
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "approved"
    
    def test_reject_project(self, client_with_auth):
        """驳回项目"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "待驳回项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        client_with_auth.post(f"/api/v1/projects/{project_id}/submit")
        
        response = client_with_auth.post(f"/api/v1/projects/{project_id}/reject", json={
            "comment": "预算过高，请调整"
        })
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "rejected"
    
    def test_get_project_progress(self, client_with_auth):
        """TC-PROJ-07：查看项目进度"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "进度测试项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.get(f"/api/v1/projects/{project_id}/progress")
        assert response.status_code == 200
        assert "overall_progress" in response.json()["data"]
    
    def test_get_project_tasks(self, client_with_auth):
        """获取项目任务列表"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "带任务的项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.get(f"/api/v1/projects/{project_id}/tasks")
        assert response.status_code == 200
    
    def test_get_project_team(self, client_with_auth):
        """获取项目团队"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "团队测试项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.get(f"/api/v1/projects/{project_id}/team")
        assert response.status_code == 200
    
    def test_export_project_report(self, client_with_auth):
        """TC-PROJ-08：导出项目报告"""
        create_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "导出测试项目",
            "domain": "D03"
        })
        project_id = create_resp.json()["data"]["id"]
        
        response = client_with_auth.post(f"/api/v1/projects/{project_id}/export", json={
            "format": "pdf"
        })
        assert response.status_code == 200
```

### 4.5 任务管理单元测试

**`tests/test_tasks.py`**

```python
import pytest

class TestTasks:
    
    def test_create_task(self, client_with_auth):
        """TC-TASK-01：创建任务"""
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "测试项目",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        response = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "测试任务",
            "priority": "high",
            "estimated_hours": 8,
            "description": "测试任务描述"
        })
        assert response.status_code == 200
        assert response.json()["data"]["name"] == "测试任务"
    
    def test_list_tasks(self, client_with_auth):
        """TC-TASK-03：查看任务列表"""
        response = client_with_auth.get("/api/v1/tasks")
        assert response.status_code == 200
    
    def test_filter_tasks_by_status(self, client_with_auth):
        """按状态筛选任务"""
        response = client_with_auth.get("/api/v1/tasks?status=pending")
        assert response.status_code == 200
    
    def test_filter_tasks_by_assignee(self, client_with_auth):
        """按负责人筛选任务"""
        response = client_with_auth.get("/api/v1/tasks?assignee_id=agent_001")
        assert response.status_code == 200
    
    def test_assign_task(self, client_with_auth):
        """TC-TASK-02：分配任务"""
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "分配测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        task_resp = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "待分配任务"
        })
        task_id = task_resp.json()["data"]["id"]
        
        agents_resp = client_with_auth.get("/api/v1/agents")
        agent_id = agents_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.post(f"/api/v1/tasks/{task_id}/assign", json={
            "agent_id": agent_id,
            "role": "负责人"
        })
        assert response.status_code == 200
    
    def test_update_task_status(self, client_with_auth):
        """TC-TASK-04：更新任务状态"""
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "状态测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        task_resp = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "待更新任务"
        })
        task_id = task_resp.json()["data"]["id"]
        
        response = client_with_auth.put(f"/api/v1/tasks/{task_id}", json={
            "status": "in_progress"
        })
        assert response.status_code == 200
        assert response.json()["data"]["status"] == "in_progress"
    
    def test_update_task_progress(self, client_with_auth):
        """TC-TASK-05：更新任务进度"""
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "进度测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        task_resp = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "进度更新任务"
        })
        task_id = task_resp.json()["data"]["id"]
        
        response = client_with_auth.put(f"/api/v1/tasks/{task_id}", json={
            "progress": 50
        })
        assert response.status_code == 200
        assert response.json()["data"]["progress"] == 50
    
    def test_create_scheduled_task(self, client_with_auth):
        """TC-TASK-06：定时任务"""
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "定时任务测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        response = client_with_auth.post("/api/v1/tasks/schedule", json={
            "project_id": project_id,
            "name": "定时任务",
            "cron": "0 9 * * *"
        })
        assert response.status_code == 200
    
    def test_task_dependency(self, client_with_auth):
        """TC-TASK-07：任务依赖"""
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "依赖测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        task_a = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "任务A"
        })
        task_a_id = task_a.json()["data"]["id"]
        
        response = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "任务B",
            "dependencies": [task_a_id]
        })
        assert response.status_code == 200
    
    def test_task_retry(self, client_with_auth, mocker):
        """TC-TASK-08：任务重试"""
        mocker.patch("core.tasks.execute_task", side_effect=Exception("模拟失败"))
        
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "重试测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        response = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "重试任务",
            "retry_count": 3
        })
        assert response.status_code == 200
```

### 4.6 能力库单元测试

**`tests/test_capabilities.py`**

```python
import pytest

class TestCapabilities:
    
    def test_list_capabilities(self, client_with_auth):
        """查看能力列表"""
        response = client_with_auth.get("/api/v1/capabilities")
        assert response.status_code == 200
        assert "items" in response.json()["data"]
    
    def test_get_capability_by_id(self, client_with_auth):
        """查看能力详情"""
        response = client_with_auth.get("/api/v1/capabilities/AGENT-RUNTIME-01")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == "AGENT-RUNTIME-01"
    
    def test_filter_capabilities_by_category(self, client_with_auth):
        """按类别筛选能力"""
        response = client_with_auth.get("/api/v1/capabilities?category=WEB")
        assert response.status_code == 200
        items = response.json()["data"]["items"]
        for item in items:
            assert item["category"] == "WEB"
    
    def test_activate_capability_for_agent(self, client_with_auth):
        """为智能体激活能力"""
        agents_resp = client_with_auth.get("/api/v1/agents")
        agent_id = agents_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.post(f"/api/v1/agents/{agent_id}/capabilities", json={
            "capability_id": "WEB-01",
            "level": "A"
        })
        assert response.status_code == 200
    
    def test_get_agent_capability_gaps(self, client_with_auth):
        """获取智能体能力缺口"""
        agents_resp = client_with_auth.get("/api/v1/agents")
        agent_id = agents_resp.json()["data"]["items"][0]["id"]
        
        response = client_with_auth.get(f"/api/v1/agents/{agent_id}/capabilities/gaps")
        assert response.status_code == 200
    
    def test_get_capability_development_status(self, client_with_auth):
        """获取能力开发状态"""
        response = client_with_auth.get("/api/v1/capabilities/development")
        assert response.status_code == 200
        assert "in_development" in response.json()["data"]
        assert "pending" in response.json()["data"]
```


## 五、集成测试

### 5.1 API集成测试

**`tests/integration/test_api_flow.py`**

```python
import pytest

class TestAPIFlow:
    """完整的用户操作流程测试"""
    
    def test_full_project_lifecycle(self, client_with_auth):
        """测试完整项目生命周期"""
        # 1. 创建项目
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "完整流程测试项目",
            "domain": "D03",
            "budget": 100000
        })
        assert project_resp.status_code == 200
        project_id = project_resp.json()["data"]["id"]
        
        # 2. 提交审批
        submit_resp = client_with_auth.post(f"/api/v1/projects/{project_id}/submit")
        assert submit_resp.status_code == 200
        
        # 3. 批准项目
        approve_resp = client_with_auth.post(f"/api/v1/projects/{project_id}/approve", json={
            "comment": "批准"
        })
        assert approve_resp.status_code == 200
        
        # 4. 创建任务
        task_resp = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "需求分析",
            "priority": "high"
        })
        assert task_resp.status_code == 200
        task_id = task_resp.json()["data"]["id"]
        
        # 5. 指派智能体
        agents_resp = client_with_auth.get("/api/v1/agents")
        agent_id = agents_resp.json()["data"]["items"][0]["id"]
        
        assign_resp = client_with_auth.post(f"/api/v1/tasks/{task_id}/assign", json={
            "agent_id": agent_id
        })
        assert assign_resp.status_code == 200
        
        # 6. 更新任务进度
        update_resp = client_with_auth.put(f"/api/v1/tasks/{task_id}", json={
            "status": "in_progress",
            "progress": 50
        })
        assert update_resp.status_code == 200
        
        # 7. 完成任务
        complete_resp = client_with_auth.put(f"/api/v1/tasks/{task_id}", json={
            "status": "completed",
            "progress": 100
        })
        assert complete_resp.status_code == 200
        
        # 8. 完成项目
        complete_proj = client_with_auth.put(f"/api/v1/projects/{project_id}", json={
            "status": "completed"
        })
        assert complete_proj.status_code == 200
    
    def test_contract_net_protocol(self, client_with_auth):
        """测试合同网协议（CL-06）"""
        # 创建任务
        project_resp = client_with_auth.post("/api/v1/projects", json={
            "name": "合同网测试",
            "domain": "D03"
        })
        project_id = project_resp.json()["data"]["id"]
        
        task_resp = client_with_auth.post("/api/v1/tasks", json={
            "project_id": project_id,
            "name": "合同网任务"
        })
        task_id = task_resp.json()["data"]["id"]
        
        # 发起招标
        tender_resp = client_with_auth.post(f"/api/v1/tasks/{task_id}/tender")
        assert tender_resp.status_code == 200
        
        # 获取投标
        bids_resp = client_with_auth.get(f"/api/v1/tasks/{task_id}/bids")
        assert bids_resp.status_code == 200
        bids = bids_resp.json()["data"]["bids"]
        
        if bids:
            # 选择中标者
            award_resp = client_with_auth.post(f"/api/v1/tasks/{task_id}/award", json={
                "bid_id": bids[0]["id"]
            })
            assert award_resp.status_code == 200
    
    def test_agent_to_agent_communication(self, client_with_auth):
        """测试智能体间通信（CL-03）"""
        agents_resp = client_with_auth.get("/api/v1/agents")
        agents = agents_resp.json()["data"]["items"]
        ceo = next(a for a in agents if a["level"] == "L1")
        employee = next(a for a in agents if a["level"] == "L5")
        
        # CEO发送消息给员工
        msg_resp = client_with_auth.post("/api/v1/agents/message", json={
            "from_agent_id": ceo["id"],
            "to_agent_id": employee["id"],
            "content": "请汇报当前任务进度"
        })
        assert msg_resp.status_code == 200
        
        # 员工回复
        reply_resp = client_with_auth.post("/api/v1/agents/message", json={
            "from_agent_id": employee["id"],
            "to_agent_id": ceo["id"],
            "content": "当前任务进度60%，预计今日完成"
        })
        assert reply_resp.status_code == 200
    
    def test_learning_feedback_loop(self, client_with_auth):
        """测试学习反馈循环（LN-01）"""
        agents_resp = client_with_auth.get("/api/v1/agents")
        agent_id = agents_resp.json()["data"]["items"][0]["id"]
        
        # 记录反馈
        feedback_resp = client_with_auth.post(f"/api/v1/agents/{agent_id}/feedback", json={
            "task_id": "task_001",
            "rating": 5,
            "comment": "表现优秀"
        })
        assert feedback_resp.status_code == 200
        
        # 获取学习状态
        learning_resp = client_with_auth.get(f"/api/v1/agents/{agent_id}/learning")
        assert learning_resp.status_code == 200
        assert "feedback_count" in learning_resp.json()["data"]
    
    def test_self_reflection(self, client_with_auth):
        """测试自我反思（AGENT-RUNTIME-11）"""
        agents_resp = client_with_auth.get("/api/v1/agents")
        agent_id = agents_resp.json()["data"]["items"][0]["id"]
        
        # 触发自我反思
        reflect_resp = client_with_auth.post(f"/api/v1/agents/{agent_id}/reflect")
        assert reflect_resp.status_code == 200
        
        # 获取反思报告
        report_resp = client_with_auth.get(f"/api/v1/agents/{agent_id}/reflection")
        assert report_resp.status_code == 200
        assert "insights" in report_resp.json()["data"]
```

### 5.2 数据库集成测试

**`tests/integration/test_database.py`**

```python
import pytest
from sqlalchemy import text

class TestDatabase:
    
    def test_database_connection(self, db_session):
        """测试数据库连接"""
        result = db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    
    def test_create_user(self, db_session):
        """测试创建用户"""
        from core.models import User
        
        user = User(
            username="test_user",
            email="test@jyis.com",
            password_hash="hashed_password",
            role="boss"
        )
        db_session.add(user)
        db_session.commit()
        
        saved_user = db_session.query(User).filter_by(username="test_user").first()
        assert saved_user is not None
        assert saved_user.email == "test@jyis.com"
    
    def test_create_agent_hierarchy(self, db_session):
        """测试智能体层级关系"""
        from core.models import Agent
        
        # 创建CEO
        ceo = Agent(
            name="测试主脑",
            level=1,
            role_type="ceo"
        )
        db_session.add(ceo)
        db_session.flush()
        
        # 创建总经理
        gm = Agent(
            name="测试总经理",
            level=2,
            role_type="gm",
            parent_id=ceo.id
        )
        db_session.add(gm)
        db_session.flush()
        
        # 创建员工
        employee = Agent(
            name="测试员工",
            level=5,
            role_type="employee",
            parent_id=gm.id
        )
        db_session.add(employee)
        db_session.commit()
        
        # 验证层级关系
        saved_employee = db_session.query(Agent).filter_by(name="测试员工").first()
        saved_gm = db_session.query(Agent).filter_by(id=saved_employee.parent_id).first()
        assert saved_gm.parent_id == ceo.id
    
    def test_create_project_with_team(self, db_session):
        """测试创建项目及团队"""
        from core.models import Project, Agent, ProjectTeam
        
        # 创建项目经理
        pm = Agent(
            name="测试项目经理",
            level=3,
            role_type="pm"
        )
        db_session.add(pm)
        db_session.flush()
        
        # 创建项目
        project = Project(
            name="测试项目",
            domain="D03",
            owner_id=pm.id,
            status="draft"
        )
        db_session.add(project)
        db_session.flush()
        
        # 添加团队成员
        team_member = ProjectTeam(
            project_id=project.id,
            agent_id=pm.id,
            role="负责人"
        )
        db_session.add(team_member)
        db_session.commit()
        
        saved_project = db_session.query(Project).filter_by(name="测试项目").first()
        assert saved_project is not None
        assert len(saved_project.team_members) == 1
    
    def test_create_memory_system(self, db_session):
        """测试记忆系统（MM-01~08）"""
        from core.models import Agent, Memory
        
        agent = Agent(
            name="记忆测试智能体",
            level=5,
            role_type="employee"
        )
        db_session.add(agent)
        db_session.flush()
        
        # 创建工作记忆
        working_memory = Memory(
            agent_id=agent.id,
            type="working",
            content="当前任务上下文",
            ttl=3600
        )
        db_session.add(working_memory)
        
        # 创建长期记忆
        long_term_memory = Memory(
            agent_id=agent.id,
            type="long_term",
            content="重要的经验知识",
            importance=0.85
        )
        db_session.add(long_term_memory)
        db_session.commit()
        
        memories = db_session.query(Memory).filter_by(agent_id=agent.id).all()
        assert len(memories) == 2
```


## 六、功能测试用例

### 6.1 用户认证模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-AUTH-01 | 正确登录 | 账号已注册 | 输入正确账号密码，点击登录 | 登录成功，跳转主页 | P0 | 测试工程师A |
| TC-AUTH-02 | 错误密码 | 账号已注册 | 输入正确账号、错误密码 | 提示"密码错误" | P0 | 测试工程师A |
| TC-AUTH-03 | 账号不存在 | - | 输入不存在的账号 | 提示"账号不存在" | P1 | 测试工程师A |
| TC-AUTH-04 | 空表单 | - | 不输入任何内容直接登录 | 提示"请输入账号/密码" | P1 | 测试工程师A |
| TC-AUTH-05 | Token过期 | 已登录 | 等待token过期后访问API | 返回401，要求重新登录 | P0 | 测试工程师A |
| TC-AUTH-06 | 人脸识别登录 | 人脸已注册 | 进行人脸扫描 | 登录成功 | P0 | 安全工程师A |
| TC-AUTH-07 | 人脸识别失败 | 人脸未注册 | 使用未注册人脸扫描 | 提示识别失败，切换到密码 | P1 | 安全工程师A |
| TC-AUTH-08 | 声纹识别登录 | 声纹已注册 | 说出验证短语 | 登录成功 | P1 | 安全工程师A |
| TC-AUTH-09 | 硬件密钥登录 | 密钥已绑定 | 插入硬件密钥 | 登录成功 | P1 | 安全工程师A |
| TC-AUTH-10 | 退出登录 | 已登录 | 点击退出登录 | 返回登录页，token失效 | P0 | 测试工程师A |
| TC-AUTH-11 | 密码找回 | 有绑定邮箱 | 点击忘记密码，邮箱重置 | 收到重置邮件，可重置密码 | P1 | 测试工程师A |

### 6.2 智能体管理模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-AGENT-01 | 查看智能体列表 | 已登录 | 进入智能体管理页面 | 显示所有智能体 | P0 | 测试工程师A |
| TC-AGENT-02 | 搜索智能体 | 有多个智能体 | 输入智能体名称搜索 | 显示匹配结果 | P1 | 测试工程师A |
| TC-AGENT-03 | 按层级筛选 | 有多个智能体 | 选择L5层级 | 只显示L5智能体 | P1 | 测试工程师A |
| TC-AGENT-04 | 按部门筛选 | 有多个智能体 | 选择后端部 | 只显示后端部智能体 | P1 | 测试工程师A |
| TC-AGENT-05 | 查看智能体详情 | 智能体存在 | 点击智能体名称 | 显示详细信息 | P0 | 测试工程师A |
| TC-AGENT-06 | 配置智能体模型 | 有配置权限 | 修改模型参数并保存 | 配置保存成功 | P0 | 智能体工程师A |
| TC-AGENT-07 | 查看智能体技能 | 智能体存在 | 进入技能库标签页 | 显示技能列表 | P1 | 测试工程师A |
| TC-AGENT-08 | 启用/禁用技能 | 智能体存在 | 切换技能开关 | 状态变更成功 | P1 | 智能体工程师A |
| TC-AGENT-09 | 查看智能体记忆 | 智能体有记忆 | 进入记忆系统标签页 | 显示记忆列表 | P1 | 测试工程师A |
| TC-AGENT-10 | 搜索智能体记忆 | 智能体有记忆 | 输入关键词搜索 | 显示匹配记忆 | P2 | 测试工程师A |
| TC-AGENT-11 | 创建新智能体 | 有创建权限 | 填写信息，点击创建 | 智能体创建成功 | P0 | 智能体工程师B |
| TC-AGENT-12 | 智能体自愈 | 智能体异常 | 触发自愈机制 | 智能体自动恢复 | P0 | 智能体主管 |
| TC-AGENT-13 | 智能体负载均衡 | 多个智能体 | 任务自动分配 | 负载均衡 | P1 | 项目协调员 |

### 6.3 项目管理模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-PROJ-01 | 创建项目 | 已登录 | 填写项目信息，点击创建 | 项目创建成功 | P0 | 测试工程师A |
| TC-PROJ-02 | 项目立项审批 | 项目为draft状态 | 提交审批→CEO审批通过 | 项目状态变为approved | P0 | 测试工程师A |
| TC-PROJ-03 | 项目立项驳回 | 项目为draft状态 | 提交审批→CEO驳回 | 项目状态变为rejected | P1 | 测试工程师A |
| TC-PROJ-04 | 查看项目列表 | 有多个项目 | 进入项目管理页面 | 显示所有项目 | P0 | 测试工程师A |
| TC-PROJ-05 | 查看项目详情 | 项目存在 | 点击项目名称 | 显示项目详情 | P0 | 测试工程师A |
| TC-PROJ-06 | 编辑项目信息 | 项目存在 | 修改信息并保存 | 信息更新成功 | P1 | 测试工程师A |
| TC-PROJ-07 | 删除项目 | 项目存在 | 点击删除并确认 | 项目被删除 | P1 | 测试工程师A |
| TC-PROJ-08 | 查看项目进度 | 项目有任务 | 查看进度条 | 显示正确百分比 | P0 | 测试工程师A |
| TC-PROJ-09 | 导出项目报告 | 项目存在 | 点击导出 | 下载报告文件 | P1 | 测试工程师A |
| TC-PROJ-10 | 项目讨论 | 项目存在 | 发送讨论消息 | 消息显示在讨论区 | P1 | 测试工程师A |
| TC-PROJ-11 | 资源池调配 | 有可用资源 | 调整项目人力 | 资源分配更新 | P1 | 项目协调员 |
| TC-PROJ-12 | 风险识别与处理 | 项目存在风险 | 识别风险，制定应对 | 风险被记录和处理 | P0 | 项目经理 |

### 6.4 任务调度模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-TASK-01 | 创建任务 | 项目存在 | 填写任务信息，点击创建 | 任务创建成功 | P0 | 测试工程师A |
| TC-TASK-02 | 分配任务 | 任务存在 | 选择智能体，点击分配 | 任务已分配 | P0 | 测试工程师A |
| TC-TASK-03 | 查看任务列表 | 有多个任务 | 进入任务管理页面 | 显示所有任务 | P0 | 测试工程师A |
| TC-TASK-04 | 更新任务状态 | 任务存在 | 修改状态为进行中 | 状态更新成功 | P0 | 测试工程师A |
| TC-TASK-05 | 更新任务进度 | 任务进行中 | 修改进度百分比 | 进度更新成功 | P0 | 测试工程师A |
| TC-TASK-06 | 定时任务 | - | 创建定时任务，设置Cron | 按计划执行 | P1 | 测试工程师A |
| TC-TASK-07 | 任务依赖 | 有多个任务 | 设置任务A依赖任务B | 任务B完成后任务A自动开始 | P1 | 测试工程师A |
| TC-TASK-08 | 任务重试 | 任务失败 | 配置重试策略 | 自动重试 | P1 | 测试工程师A |
| TC-TASK-09 | 任务通知 | 任务状态变更 | 完成任务 | 收到通知 | P1 | 测试工程师A |
| TC-TASK-10 | 合同网招标 | 任务未分配 | 发起招标 | 智能体投标 | P0 | 项目协调员 |
| TC-TASK-11 | 合同网评标 | 有多个投标 | 系统自动评标 | 选择最优智能体 | P0 | 项目经理 |

### 6.5 对话系统模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-CHAT-01 | 发送消息 | 已登录 | 输入消息，点击发送 | 收到主脑回复 | P0 | 测试工程师A |
| TC-CHAT-02 | 流式响应 | 已登录 | 发送长消息 | 逐字显示回复 | P0 | 测试工程师A |
| TC-CHAT-03 | 多轮对话 | 已登录 | 连续发送多条消息 | 保持上下文 | P0 | 测试工程师A |
| TC-CHAT-04 | 创建项目对话 | 已登录 | 发送"创建一个XX项目" | 自动创建项目 | P0 | 测试工程师A |
| TC-CHAT-05 | 查询进度对话 | 项目存在 | 发送"查看XX项目进度" | 返回进度信息 | P0 | 测试工程师A |
| TC-CHAT-06 | 分配任务对话 | 智能体存在 | 发送"把XX任务分配给YY" | 任务分配成功 | P1 | 测试工程师A |
| TC-CHAT-07 | 查看对话历史 | 有历史消息 | 进入历史页面 | 显示历史记录 | P1 | 测试工程师A |
| TC-CHAT-08 | 搜索对话 | 有历史消息 | 输入关键词搜索 | 显示匹配对话 | P1 | 测试工程师A |
| TC-CHAT-09 | 思考过程展示 | 已登录 | 发送复杂问题 | 显示主脑思考步骤 | P1 | 测试工程师A |
| TC-CHAT-10 | 反事实分析 | 已登录 | 问"如果选方案B会怎样" | 显示反事实分析 | P2 | 测试工程师A |

### 6.6 能力库模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-CAP-01 | 查看能力列表 | 已登录 | 进入能力库页面 | 显示142项能力 | P0 | 测试工程师A |
| TC-CAP-02 | 按类别筛选 | 已登录 | 选择WEB类别 | 只显示WEB能力 | P1 | 测试工程师A |
| TC-CAP-03 | 查看能力详情 | 能力存在 | 点击能力名称 | 显示能力详细信息 | P0 | 测试工程师A |
| TC-CAP-04 | 为智能体配置能力 | 有权限 | 勾选能力，点击保存 | 智能体获得能力 | P0 | 智能体工程师A |
| TC-CAP-05 | 查看能力缺口 | 智能体存在 | 进入能力缺口页面 | 显示缺失能力 | P1 | 智能体工程师A |
| TC-CAP-06 | 能力开发追踪 | 有开发中能力 | 查看开发进度 | 显示进度和负责人 | P1 | 智能体工程师A |
| TC-CAP-07 | 一键通知主脑 | 有能力缺口 | 点击通知主脑 | 主脑收到通知 | P1 | 测试工程师A |

### 6.7 安全中心模块

| 用例ID | 测试场景 | 前置条件 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 |
|--------|---------|---------|---------|---------|--------|-----------|
| TC-SEC-01 | SQL注入防护 | 已登录 | 在输入框输入注入语句 | 被过滤或转义 | P0 | 安全工程师A |
| TC-SEC-02 | XSS攻击防护 | 已登录 | 输入脚本语句 | 被转义，不执行 | P0 | 安全工程师A |
| TC-SEC-03 | 越权访问 | 普通用户 | 访问管理员API | 返回403 | P0 | 安全工程师A |
| TC-SEC-04 | 密码强度检查 | 已登录 | 设置弱密码 | 提示密码强度不足 | P1 | 安全工程师A |
| TC-SEC-05 | 暴力破解防护 | 已登录 | 连续多次错误登录 | 触发锁定或验证码 | P1 | 安全工程师A |
| TC-SEC-06 | API限流 | 已登录 | 短时间内大量请求 | 返回429 | P1 | 安全工程师A |
| TC-SEC-07 | 漏洞扫描 | 已部署 | 执行安全扫描 | 发现并报告漏洞 | P0 | 安全工程师A |
| TC-SEC-08 | 威胁监控 | 已部署 | 模拟攻击 | 检测并告警 | P0 | 安全工程师A |
| TC-SEC-09 | 合规检查 | 已部署 | 执行GDPR检查 | 显示合规状态 | P1 | 合规审计师 |


## 七、性能测试

### 7.1 Locust测试脚本

**`tests/performance/locustfile.py`**

```python
from locust import HttpUser, task, between
import random

class JYISUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """登录获取token"""
        response = self.client.post("/api/v1/auth/login", json={
            "username": "test_boss@jyis.com",
            "password": "Test123!@#"
        })
        if response.status_code == 200:
            self.token = response.json()["data"]["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}
    
    @task(5)
    def list_agents(self):
        """查看智能体列表（高频）"""
        if self.token:
            self.client.get("/api/v1/agents", headers=self.headers)
    
    @task(4)
    def list_projects(self):
        """查看项目列表"""
        if self.token:
            self.client.get("/api/v1/projects", headers=self.headers)
    
    @task(4)
    def list_tasks(self):
        """查看任务列表"""
        if self.token:
            self.client.get("/api/v1/tasks", headers=self.headers)
    
    @task(2)
    def get_agent_detail(self):
        """查看智能体详情"""
        if self.token:
            agent_id = f"agent_{random.randint(1, 47):03d}"
            self.client.get(f"/api/v1/agents/{agent_id}", headers=self.headers)
    
    @task(2)
    def get_project_detail(self):
        """查看项目详情"""
        if self.token:
            project_id = f"project_{random.randint(1, 12):03d}"
            self.client.get(f"/api/v1/projects/{project_id}", headers=self.headers)
    
    @task(1)
    def create_project(self):
        """创建项目（低频）"""
        if self.token:
            self.client.post("/api/v1/projects", headers=self.headers, json={
                "name": f"性能测试项目_{random.randint(1000, 9999)}",
                "domain": "D03"
            })
    
    @task(1)
    def chat_message(self):
        """发送对话消息"""
        if self.token:
            self.client.post("/api/v1/chat/sessions/test/messages", 
                             headers=self.headers,
                             json={"content": "测试消息"})
    
    @task(1)
    def get_capabilities(self):
        """查看能力库"""
        if self.token:
            self.client.get("/api/v1/capabilities", headers=self.headers)
    
    @task(1)
    def get_dashboard(self):
        """查看指挥舱"""
        if self.token:
            self.client.get("/api/v1/dashboard/command", headers=self.headers)
```

### 7.2 性能测试场景

| 场景 | 并发用户 | 运行时间 | 目标QPS | 目标响应时间 | 负责智能体 |
|------|---------|---------|---------|-------------|-----------|
| 轻负载 | 10 | 5分钟 | 100 | P95 < 200ms | 测试工程师B |
| 中负载 | 50 | 10分钟 | 500 | P95 < 300ms | 测试工程师B |
| 重负载 | 100 | 15分钟 | 1000 | P95 ≤ 180秒，单次 ≤ 300秒 | 测试工程师B |
| 峰值测试 | 200 | 5分钟 | 2000 | P95 ≤ 180秒，单次 ≤ 300秒 | 测试工程师B |
| 稳定性测试 | 50 | 2小时 | 500 | P95 ≤ 180秒，单次 ≤ 300秒 | 测试工程师B |
| 智能体协作压测 | 30 | 10分钟 | - | 合同网成功率>95% | 测试工程师B |
| 能力调用压测 | 50 | 10分钟 | - | 能力响应P95 ≤ 180秒，单次 ≤ 300秒 | 测试工程师B |

### 7.3 性能基准

| API端点 | 目标P95 | 目标P99 | QPS目标 | 关联能力 |
|--------|---------|---------|---------|----------|
| GET /agents | P95 ≤ 180秒 | 单次 ≤ 300秒 | 500 | AGENT-RUNTIME-06 |
| GET /projects | P95 ≤ 180秒 | 单次 ≤ 300秒 | 500 | - |
| GET /tasks | P95 ≤ 180秒 | 单次 ≤ 300秒 | 500 | - |
| GET /agents/{id} | P95 ≤ 180秒 | 单次 ≤ 300秒 | 200 | AGENT-RUNTIME-06 |
| POST /projects | < 300ms | < 800ms | 200 | DC-01 |
| POST /tasks | < 300ms | < 800ms | 200 | DC-02 |
| POST /chat/messages | P95 ≤ 180秒 | 单次 ≤ 300秒 | 100 | PC-01, EM-13 |
| GET /capabilities | P95 ≤ 180秒 | 单次 ≤ 300秒 | 300 | META-05 |
| POST /agents/{id}/capabilities | < 300ms | < 800ms | 100 | META-01 |
| POST /tasks/{id}/tender | P95 ≤ 180秒 | 单次 ≤ 300秒 | 50 | CL-06 |
| GET /dashboard/command | P95 ≤ 180秒 | 单次 ≤ 300秒 | 50 | - |


## 八、安全测试

### 8.1 安全测试用例

| 用例ID | 测试场景 | 测试步骤 | 预期结果 | 优先级 | 负责智能体 | 关联能力 |
|--------|---------|---------|---------|--------|-----------|----------|
| TC-SEC-01 | SQL注入 | 输入 `' OR '1'='1` | 被过滤或转义 | P0 | 安全工程师A | SC-01 |
| TC-SEC-02 | XSS攻击 | 输入 `<script>alert(1)</script>` | 被转义，不执行 | P0 | 安全工程师A | SC-01 |
| TC-SEC-03 | CSRF攻击 | 跨站请求伪造 | Token验证生效 | P1 | 安全工程师A | SC-04 |
| TC-SEC-04 | 越权访问 | 普通用户访问管理员API | 返回403 | P0 | 安全工程师A | SC-04 |
| TC-SEC-05 | 密码强度 | 设置弱密码"123456" | 提示密码强度不足 | P1 | 安全工程师A | SC-03 |
| TC-SEC-06 | Token泄露 | 使用过期token访问 | 返回401 | P0 | 安全工程师A | SC-20 |
| TC-SEC-07 | 敏感信息泄露 | 错误响应检查 | 不包含密码/密钥 | P0 | 安全工程师A | SC-03 |
| TC-SEC-08 | 暴力破解 | 连续多次错误登录 | 触发验证码或锁定 | P1 | 安全工程师A | SC-06 |
| TC-SEC-09 | API限流 | 短时间内大量请求 | 返回429 | P1 | 安全工程师A | SC-06 |
| TC-SEC-10 | 文件上传漏洞 | 上传恶意文件 | 被检测并拒绝 | P0 | 安全工程师A | SC-01 |
| TC-SEC-11 | 命令注入 | 输入 `; rm -rf /` | 被过滤或沙箱隔离 | P0 | 安全工程师A | SC-02 |
| TC-SEC-12 | 数据加密 | 检查敏感数据存储 | 已加密存储 | P0 | 安全工程师A | SC-19 |
| TC-SEC-13 | 人脸识别安全 | 使用照片/视频攻击 | 活体检测拦截 | P0 | 安全工程师A | SC-03 |
| TC-SEC-14 | 审计日志 | 检查操作记录 | 完整记录敏感操作 | P1 | 合规审计师 | SC-07 |

### 8.2 安全扫描配置

**`tests/security/zap_scan.py`**

```python
import time
from zapv2 import ZAPv2

def run_security_scan(target_url: str):
    """使用OWASP ZAP进行安全扫描"""
    zap = ZAPv2(apikey='your_api_key')
    
    # 开始扫描
    scan_id = zap.ascan.scan(target_url)
    
    # 等待扫描完成
    while int(zap.ascan.status(scan_id)) < 100:
        time.sleep(5)
    
    # 获取结果
    alerts = zap.core.alerts(baseurl=target_url)
    
    # 分类统计
    high_risk = [a for a in alerts if a['risk'] == 'High']
    medium_risk = [a for a in alerts if a['risk'] == 'Medium']
    low_risk = [a for a in alerts if a['risk'] == 'Low']
    
    return {
        'total': len(alerts),
        'high': len(high_risk),
        'medium': len(medium_risk),
        'low': len(low_risk),
        'alerts': alerts
    }
```


## 九、兼容性测试

### 9.1 浏览器兼容性

| 浏览器 | 最低版本 | 功能测试 | UI测试 | 性能测试 | 关联能力 |
|--------|---------|---------|--------|---------|----------|
| Chrome | 120+ | ✅ | ✅ | ✅ | COMPAT-01 |
| Firefox | 115+ | ✅ | ✅ | ✅ | COMPAT-01 |
| Edge | 120+ | ✅ | ✅ | ✅ | COMPAT-01 |
| Safari | 16+ | ✅ | ✅ | ✅ | COMPAT-01 |
| 移动端Chrome | 120+ | ✅ | ✅ | 部分 | COMPAT-01 |
| 移动端Safari | 16+ | ✅ | ✅ | 部分 | COMPAT-01 |

### 9.2 分辨率兼容性

| 分辨率 | 布局 | 功能 | 说明 | 关联能力 |
|--------|------|------|------|----------|
| 3840x2160 (4K) | 完整 | ✅ | 高分辨率适配 | COMPAT-02 |
| 2560x1440 (2K) | 完整 | ✅ | 高分辨率适配 | COMPAT-02 |
| 1920x1080 | 完整 | ✅ | 标准桌面 | COMPAT-02 |
| 1366x768 | 完整 | ✅ | 笔记本 | COMPAT-02 |
| 1024x768 | 折叠侧边栏 | ✅ | 小屏幕 | COMPAT-02 |
| 768x1024 | 单栏 | ✅ | 平板 | COMPAT-02 |
| 375x667 | 单栏+底部导航 | ✅ | 手机 | COMPAT-02 |


## 十、智能体能力测试

### 10.1 能力验证测试

| 能力类别 | 测试项 | 验证方法 | 通过标准 | 负责智能体 |
|---------|--------|---------|---------|-----------|
| AGENT-RUNTIME | 主循环 | 持续运行24小时 | 无中断 | 智能体工程师A |
| AGENT-RUNTIME | 决策可解释性 | 查询决策理由 | 返回推理链 | 智能体工程师A |
| AGENT-RUNTIME | 健康自检 | 模拟故障 | 自动自愈 | 智能体工程师A |
| WEB能力 | 浏览器自动化 | 访问测试网页 | 成功提取内容 | 智能体工程师A |
| WEB能力 | 搜索引擎查询 | 搜索关键词 | 返回搜索结果 | 智能体工程师A |
| 执行能力 | 代码生成 | 生成排序算法 | 代码可运行 | 智能体工程师A |
| 执行能力 | 命令执行 | 执行shell命令 | 返回正确结果 | 智能体工程师A |
| 记忆能力 | 记忆存储检索 | 存储后检索 | 准确召回 | 智能体工程师A |
| 学习能力 | 反馈学习 | 给予反馈 | 行为改善 | 智能体培训师 |
| 协作能力 | 合同网协议 | 发起招标 | 正常投标评标 | 项目协调员 |
| 元能力 | 能力自省 | 触发自省 | 返回能力报告 | 智能体工程师A |

### 10.2 能力开发测试

| 能力名称 | 开发状态 | 测试用例 | 验收标准 | 负责智能体 |
|---------|---------|---------|---------|-----------|
| 视频生成能力 | 开发中(45%) | 生成短视频 | 生成10-60秒视频 | 智能体工程师A |
| 语音识别集成 | 开发中(30%) | 语音转文字 | 准确率>95% | 智能体工程师A |
| 多模态理解 | 开发中(60%) | 图片内容理解 | 准确描述图片 | 智能体工程师A |
| 智能家居协议适配 | 待开发 | 设备发现控制 | 控制智能设备 | 智能体工程师B |
| 智慧农业数据解析 | 待开发 | 传感器数据解析 | 准确解析数据 | 智能体工程师B |


## 十一、测试报告模板

### 11.1 测试报告格式

```markdown
# 测试报告 - [版本号]

## 一、测试概况
- 测试开始时间：
- 测试结束时间：
- 测试环境：
- 测试智能体团队：
  - 测试主管：[名称]
  - 测试工程师：[名称]
  - 安全工程师：[名称]
- 测试范围：

## 二、测试统计
| 类型 | 总数 | 通过 | 失败 | 阻塞 | 通过率 | 负责智能体 |
|------|------|------|------|------|--------|-----------|
| 单元测试 | | | | | | 各开发智能体 |
| 集成测试 | | | | | | 测试工程师A |
| 功能测试 | | | | | | 测试工程师A |
| 性能测试 | | | | | | 测试工程师B |
| 安全测试 | | | | | | 安全工程师A |
| 能力测试 | | | | | | 智能体工程师A |

## 三、Bug统计
| 优先级 | 新增 | 已修复 | 未修复 | 负责人 |
|--------|------|--------|--------|--------|
| P0 | | | | |
| P1 | | | | |
| P2 | | | | |
| P3 | | | | |

## 四、性能测试结果
| API | P95目标 | P95实际 | 结果 | 备注 |
|-----|---------|---------|------|------|
| | | | | |

## 五、安全测试结果
| 风险等级 | 数量 | 已修复 | 未修复 | 备注 |
|---------|------|--------|--------|------|
| 高危 | | | | |
| 中危 | | | | |
| 低危 | | | | |

## 六、能力测试结果
| 能力类别 | 已激活 | 开发中 | 待开发 | 完成率 |
|---------|--------|--------|--------|--------|
| 智能体运行时 | 12 | 0 | 0 | 100% |
| WEB能力 | 8 | 2 | 1 | 73% |
| ... | | | | |

## 七、遗留问题
- [问题描述] [优先级] [计划修复版本] [负责人]

## 八、测试结论
- [ ] 通过，可发布
- [ ] 有条件通过，需修复P0问题
- [ ] 不通过，需重新测试

## 九、主脑评估意见
[主脑对测试结果的评估和建议]

## 十、签字
- 测试主管：__________ 日期：__________
- 安全主管：__________ 日期：__________
- 智能体主管：__________ 日期：__________
- 主脑：__________ 日期：__________
```


## 十二、测试自动化CI/CD集成

### 12.1 GitHub Actions配置

**`.github/workflows/test.yml`**

```yaml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements-dev.txt
      - name: Run unit tests
        run: pytest tests/ -m "not integration" --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
  
  integration-test:
    runs-on: ubuntu-latest
    needs: unit-test
    steps:
      - uses: actions/checkout@v3
      - name: Set up services
        run: docker-compose -f docker-compose.test.yml up -d
      - name: Run integration tests
        run: pytest tests/integration -v
      - name: Tear down
        run: docker-compose -f docker-compose.test.yml down
  
  security-scan:
    runs-on: ubuntu-latest
    needs: integration-test
    steps:
      - uses: actions/checkout@v3
      - name: Run Bandit
        run: bandit -r . -f json -o bandit-report.json
      - name: Run Safety
        run: safety check -r requirements.txt --json > safety-report.json
      - name: Upload reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: "*-report.json"
  
  performance-test:
    runs-on: ubuntu-latest
    needs: integration-test
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Run Locust
        run: |
          locust -f tests/performance/locustfile.py \
            --headless -u 50 -r 5 -t 5m \
            --host https://test.jyis.com \
            --csv=performance-report
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: performance-report
          path: performance-report_*.csv
```


## 十三、测试数据准备

### 13.1 测试数据脚本

**`scripts/prepare_test_data.py`**

```python
"""准备测试数据"""
import random
from datetime import datetime, timedelta

def create_test_users():
    """创建测试用户"""
    return [
        {"username": "test_boss", "role": "boss", "password": "Test123!@#"},
        {"username": "test_partner", "role": "partner", "password": "Test123!@#"},
        {"username": "test_cfo", "role": "cfo", "password": "Test123!@#"},
        {"username": "test_cto", "role": "cto", "password": "Test123!@#"},
        {"username": "test_pm", "role": "pm", "password": "Test123!@#"},
    ]

def create_test_agents():
    """创建测试智能体"""
    agents = []
    departments = ["产品部", "设计部", "前端部", "后端部", "智能体部", "测试部", "运维部", "营销部", "安全部", "财务部"]
    levels = ["L1", "L2", "L3", "L4", "L5", "L6"]
    
    for i in range(50):
        agents.append({
            "name": f"测试智能体_{i:03d}",
            "level": random.choice(levels),
            "department": random.choice(departments),
            "status": "online",
            "capabilities": random.sample(["EX-01", "EX-03", "EX-04", "WEB-01", "WEB-02"], 3)
        })
    return agents

def create_test_projects():
    """创建测试项目"""
    domains = ["D01", "D02", "D03", "D05"]
    statuses = ["draft", "pending_approval", "approved", "in_progress", "completed"]
    
    projects = []
    for i in range(20):
        start_date = datetime.now() - timedelta(days=random.randint(1, 60))
        projects.append({
            "name": f"测试项目_{i:03d}",
            "domain": random.choice(domains),
            "status": random.choice(statuses),
            "budget": random.randint(10000, 100000),
            "progress": random.randint(0, 100),
            "start_date": start_date,
            "end_date": start_date + timedelta(days=random.randint(14, 90))
        })
    return projects

def create_test_tasks(project_ids):
    """创建测试任务"""
    priorities = ["low", "medium", "high", "critical"]
    statuses = ["pending", "in_progress", "completed", "blocked"]
    
    tasks = []
    for project_id in project_ids:
        for i in range(random.randint(3, 10)):
            tasks.append({
                "project_id": project_id,
                "name": f"测试任务_{i:03d}",
                "priority": random.choice(priorities),
                "status": random.choice(statuses),
                "progress": random.randint(0, 100),
                "estimated_hours": random.randint(1, 40)
            })
    return tasks

def create_test_memories(agent_ids):
    """创建测试记忆"""
    memories = []
    for agent_id in agent_ids:
        for i in range(random.randint(5, 20)):
            memories.append({
                "agent_id": agent_id,
                "type": random.choice(["working", "short_term", "long_term"]),
                "content": f"测试记忆内容_{i:03d}",
                "importance": random.random()
            })
    return memories
```


## 十四、版本记录

| 版本 | 日期 | 修改内容 |
|------|------|---------|
| v1.0 | 2026-01-12 | 完整版：基于所有子文件和对话内容，新增智能体团队测试、能力测试、安全团队测试、CI/CD集成、测试数据准备 |