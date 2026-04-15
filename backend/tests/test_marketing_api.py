from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_marketing_dashboard():
    r = client.get("/api/v1/marketing/dashboard")
    assert r.status_code == 200
    b = r.json()
    assert "metrics" in b
    assert "fans_growth_7d" in b["metrics"]
    assert "contents_total" in b


def test_marketing_metrics_patch():
    r = client.patch("/api/v1/marketing/metrics", json={"fans_growth_7d": 200})
    assert r.status_code == 200
    assert r.json()["fans_growth_7d"] == 200


def test_marketing_content_crud_and_ai_draft():
    c = client.post(
        "/api/v1/marketing/contents",
        json={"title": "春季上新", "body": "预告文案", "platforms": ["wechat", "xhs"], "status": "draft"},
    )
    assert c.status_code == 201
    cid = c.json()["id"]

    g = client.get(f"/api/v1/marketing/contents/{cid}")
    assert g.status_code == 200
    assert g.json()["title"] == "春季上新"

    u = client.put(f"/api/v1/marketing/contents/{cid}", json={"status": "published"})
    assert u.status_code == 200
    assert u.json()["status"] == "published"

    ai = client.post(f"/api/v1/marketing/contents/{cid}/ai-draft", json={"hint": "突出限时"})
    assert ai.status_code == 200
    assert "draft" in ai.json()
    assert len(ai.json()["draft"]) > 0

    lst = client.get("/api/v1/marketing/contents")
    assert lst.status_code == 200
    assert lst.json()["total"] >= 1


def test_marketing_content_404():
    r = client.get("/api/v1/marketing/contents/mc-nonexistent")
    assert r.status_code == 404


def test_marketing_publish_dev_records_event():
    c = client.post(
        "/api/v1/marketing/contents",
        json={"title": "外发测试", "body": "正文", "platforms": ["wechat"], "status": "draft"},
    )
    assert c.status_code == 201
    cid = c.json()["id"]
    p = client.post(
        f"/api/v1/marketing/contents/{cid}/publish",
        json={"environment": "dev"},
    )
    assert p.status_code == 200
    assert p.json().get("content_id") == cid
    dash = client.get("/api/v1/marketing/dashboard").json()
    assert any(x.get("content_id") == cid for x in dash.get("recent_publishes", []))


def test_marketing_publish_prod_requires_approval():
    c = client.post(
        "/api/v1/marketing/contents",
        json={"title": "prod门控", "body": "x", "platforms": [], "status": "draft"},
    )
    assert c.status_code == 201
    cid = c.json()["id"]
    r = client.post(
        f"/api/v1/marketing/contents/{cid}/publish",
        json={
            "environment": "prod",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"],
            "approved": False,
        },
    )
    assert r.status_code == 403
    assert r.json()["detail"]["error_code"] == "PROD_APPROVAL_REQUIRED"


def test_marketing_publish_staging_requires_approval():
    c = client.post(
        "/api/v1/marketing/contents",
        json={"title": "staging门控", "body": "x", "platforms": [], "status": "draft"},
    )
    assert c.status_code == 201
    cid = c.json()["id"]
    r = client.post(
        f"/api/v1/marketing/contents/{cid}/publish",
        json={
            "environment": "staging",
            "law": ["LAW-01", "LAW-02", "LAW-03", "LAW-04", "LAW-05"],
            "approved": False,
        },
    )
    assert r.status_code == 403
    assert r.json()["detail"]["error_code"] == "STAGING_APPROVAL_REQUIRED"


def test_marketing_publish_404():
    r = client.post("/api/v1/marketing/contents/mc-missing/publish", json={"environment": "dev"})
    assert r.status_code == 404
