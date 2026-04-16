from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_ui_static_dashboard():
    r = client.get("/ui/")
    assert r.status_code == 200
    assert "老板工作台".encode("utf-8") in r.content
    assert "任务进度".encode("utf-8") in r.content
    assert "stat-cards".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "agents.html".encode("utf-8") in r.content
    assert "pendingBody".encode("utf-8") in r.content
    assert "pending-approvals".encode("utf-8") in r.content
    assert "审批链进度".encode("utf-8") in r.content
    assert "auditBody".encode("utf-8") in r.content
    assert "auditTrend".encode("utf-8") in r.content
    assert "auditTopReasons".encode("utf-8") in r.content
    assert "auditHealthSummary".encode("utf-8") in r.content
    assert "auditFilter".encode("utf-8") in r.content
    assert "auditPolicyFilter".encode("utf-8") in r.content
    assert "auditEnvFilter".encode("utf-8") in r.content
    assert "auditReasonCodeFilter".encode("utf-8") in r.content
    assert "btnAuditApply".encode("utf-8") in r.content
    assert "event_type_prefix".encode("utf-8") in r.content
    assert "policy_id".encode("utf-8") in r.content
    assert "environment".encode("utf-8") in r.content
    assert "/api/v1/audit/events".encode("utf-8") in r.content
    assert "/api/v1/audit/summary".encode("utf-8") in r.content
    assert "reason_code_prefix".encode("utf-8") in r.content
    assert "reason_code".encode("utf-8") in r.content
    assert "allowed_rate".encode("utf-8") in r.content
    assert "llm/status".encode("utf-8") in r.content
    assert "/docs".encode("utf-8") in r.content
    assert "login.html".encode("utf-8") in r.content
    assert "api-client.js".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content


def test_ui_memory_page():
    r = client.get("/ui/memory.html")
    assert r.status_code == 200
    assert "工作记忆".encode("utf-8") in r.content
    assert "memory/working".encode("utf-8") in r.content
    assert "jyisApiFetch".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content


def test_ui_tasks_page():
    r = client.get("/ui/tasks.html")
    assert r.status_code == 200
    assert "任务看板".encode("utf-8") in r.content
    assert "/tasks".encode("utf-8") in r.content
    assert "jyisApiFetch".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "proj-link".encode("utf-8") in r.content
    assert "project.html".encode("utf-8") in r.content
    assert "btnPutTask".encode("utf-8") in r.content
    assert "PUT".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content


def test_ui_chat_page():
    r = client.get("/ui/chat.html")
    assert r.status_code == 200
    assert "对话会话".encode("utf-8") in r.content
    assert "chat/sessions".encode("utf-8") in r.content
    assert "/messages".encode("utf-8") in r.content
    assert "jyisApiFetch".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content


def test_ui_api_client_js():
    r = client.get("/ui/api-client.js")
    assert r.status_code == 200
    assert b"jyisApiFetch" in r.content
    assert b"jyis_access_token" in r.content
    assert b"jyisInitUserBar" in r.content
    assert b"/auth/me" in r.content


def test_ui_login_page():
    r = client.get("/ui/login.html")
    assert r.status_code == 200
    assert "auth/login".encode("utf-8") in r.content
    assert "jyis_access_token".encode("utf-8") in r.content
    assert "dev@jyis.local".encode("utf-8") in r.content
    assert "agents.html".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content


def test_ui_skills_page():
    r = client.get("/ui/skills.html")
    assert r.status_code == 200
    assert "agents.html".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "技能库".encode("utf-8") in r.content
    assert "/api/v1/skills".encode("utf-8") in r.content
    assert "新建技能".encode("utf-8") in r.content
    assert "POST /api/v1/skills".encode("utf-8") in r.content
    assert "GET /api/v1/skills/{id}".encode("utf-8") in r.content
    assert "skillDetail".encode("utf-8") in r.content
    assert "btnSaveSkill".encode("utf-8") in r.content
    assert "btnDeleteSkill".encode("utf-8") in r.content
    assert "PUT".encode("utf-8") in r.content
    assert "DELETE /api/v1/skills/{id}".encode("utf-8") in r.content
    assert 'method: "DELETE"'.encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content


def test_ui_marketing_page():
    r = client.get("/ui/marketing.html")
    assert r.status_code == 200
    assert "agents.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "营销中心".encode("utf-8") in r.content
    assert "/api/v1/marketing/metrics".encode("utf-8") in r.content
    assert "marketing/dashboard".encode("utf-8") in r.content
    assert "recentPub".encode("utf-8") in r.content
    assert "/publish".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content


def test_ui_agents_page():
    r = client.get("/ui/agents.html")
    assert r.status_code == 200
    assert "智能体".encode("utf-8") in r.content
    assert "/api/v1/agents".encode("utf-8") in r.content
    assert "agents/org-tree".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "collab.html".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content


def test_ui_collab_page():
    r = client.get("/ui/collab.html")
    assert r.status_code == 200
    assert "agents.html".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content
    assert "协作委托".encode("utf-8") in r.content
    assert "/collaboration/delegations".encode("utf-8") in r.content
    assert '"/api/v1"'.encode("utf-8") in r.content
    assert "from_agent_id".encode("utf-8") in r.content
    assert "to_agent_id".encode("utf-8") in r.content
    assert "objective".encode("utf-8") in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisApiFetch".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "DELETE".encode("utf-8") in r.content
    assert "PATCH".encode("utf-8") in r.content
    assert "dlg-st".encode("utf-8") in r.content
    assert "dlg-del".encode("utf-8") in r.content
    assert "delegation.create".encode("utf-8") in r.content
    assert "audit/events".encode("utf-8") in r.content
    assert "dlgDetail".encode("utf-8") in r.content
    assert "dlg-id".encode("utf-8") in r.content


def test_ui_project_detail_page():
    pid = client.post(
        "/api/v1/projects",
        json={
            "name": "详情页测试",
            "domain": "D03",
            "project_type": "new_feature",
            "environment": "dev",
            "law": ["LAW-05"],
        },
    ).json()["id"]
    r = client.get(f"/ui/project.html?id={pid}")
    assert r.status_code == 200
    assert "主脑拆解".encode("utf-8") in r.content
    assert "项目讨论".encode("utf-8") in r.content
    assert "项目团队".encode("utf-8") in r.content
    assert "复盘报告".encode("utf-8") in r.content
    assert "立项审批".encode("utf-8") in r.content
    assert "sec-approval".encode("utf-8") in r.content
    assert "里程碑".encode("utf-8") in r.content
    assert "sec-milestones".encode("utf-8") in r.content
    assert "阶段生命周期".encode("utf-8") in r.content
    assert "sec-stages".encode("utf-8") in r.content
    assert "/projects/".encode("utf-8") in r.content
    assert "/stages".encode("utf-8") in r.content
    assert "stageDeliverablesJson".encode("utf-8") in r.content
    assert "stageDefBody".encode("utf-8") in r.content
    assert "stageApprovalPill".encode("utf-8") in r.content
    assert "btnCopyApproverJson".encode("utf-8") in r.content
    assert "stageEnvBudgetPill".encode("utf-8") in r.content
    assert "stageConditionPill".encode("utf-8") in r.content
    assert "stageApproverReqPill".encode("utf-8") in r.content
    assert "stageApprHistBody".encode("utf-8") in r.content
    assert "stagePartBody".encode("utf-8") in r.content
    assert "stageDeliverableName".encode("utf-8") in r.content
    assert "stageDeliverableOneJson".encode("utf-8") in r.content
    assert "btnStageUploadOne".encode("utf-8") in r.content
    assert "/deliverables/".encode("utf-8") in r.content
    assert "btnStageStartCurrent".encode("utf-8") in r.content
    assert "btnStageCompleteCurrent".encode("utf-8") in r.content
    assert "btnStageApproveCurrent".encode("utf-8") in r.content
    assert "btnStageRejectCurrent".encode("utf-8") in r.content
    assert "执行状态".encode("utf-8") in r.content
    assert "data-status-action".encode("utf-8") in r.content
    assert "milestonesJson".encode("utf-8") in r.content
    assert "btnSaveMilestones".encode("utf-8") in r.content
    assert "api-client.js".encode("utf-8") in r.content
    assert b"PROJECT_ID" in r.content
    assert "userBar".encode("utf-8") in r.content
    assert "jyisInitUserBar".encode("utf-8") in r.content
    assert "marketing.html".encode("utf-8") in r.content
    assert "skills.html".encode("utf-8") in r.content
    assert "memory.html".encode("utf-8") in r.content
    assert "tasks.html".encode("utf-8") in r.content
    assert "chat.html".encode("utf-8") in r.content
