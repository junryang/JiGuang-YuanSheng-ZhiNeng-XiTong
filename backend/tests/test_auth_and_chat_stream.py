import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.services.chat_service import build_assistant_content


client = TestClient(app)


def test_build_assistant_content_uses_tail():
    hist = [
        {"role": "user", "content": "a"},
        {"role": "assistant", "content": "b"},
        {"role": "user", "content": "last"},
    ]
    t = build_assistant_content(hist)
    assert "last" in t
    assert "会话上下文" in t


def test_auth_login_me_refresh_admin():
    r = client.post("/api/v1/auth/login", json={"email": "dev@jyis.local", "password": "devpass"})
    assert r.status_code == 200
    body = r.json()
    assert "access_token" in body and "refresh_token" in body

    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {body['access_token']}"})
    assert me.status_code == 200
    assert me.json()["email"] == "dev@jyis.local"

    ref = client.post("/api/v1/auth/refresh", json={"refresh_token": body["refresh_token"]})
    assert ref.status_code == 200
    ref_body = ref.json()
    assert ref_body["access_token"] != body["access_token"]
    new_access = ref_body["access_token"]

    ping = client.get("/api/v1/authz/ping", headers={"Authorization": f"Bearer {new_access}"})
    assert ping.status_code == 200

    adm = client.get("/api/v1/authz/admin-summary", headers={"Authorization": f"Bearer {new_access}"})
    assert adm.status_code == 200


def test_authz_ping_requires_token():
    assert client.get("/api/v1/authz/ping").status_code == 401


def test_register_conflict():
    email = f"dup-stream-{uuid.uuid4().hex}@local.test"
    r1 = client.post("/api/v1/auth/register", json={"email": email, "password": "longpass1"})
    assert r1.status_code == 200
    r2 = client.post("/api/v1/auth/register", json={"email": email, "password": "longpass2"})
    assert r2.status_code == 409


def test_non_admin_blocked():
    email = f"plain-user-{uuid.uuid4().hex}@local.test"
    client.post("/api/v1/auth/register", json={"email": email, "password": "longpass1"})
    tok = client.post("/api/v1/auth/login", json={"email": email, "password": "longpass1"}).json()["access_token"]
    assert client.get("/api/v1/authz/admin-summary", headers={"Authorization": f"Bearer {tok}"}).status_code == 403


def test_chat_sse_stream():
    s = client.post("/api/v1/chat/sessions", json={"title": "sse"})
    sid = s.json()["id"]
    buf = b""
    with client.stream(
        "POST",
        f"/api/v1/chat/sessions/{sid}/messages/stream",
        json={"message": "流式", "environment": "dev", "law": ["LAW-05"]},
    ) as r:
        assert r.status_code == 200
        for chunk in r.iter_bytes():
            buf += chunk
            if b'"type": "done"' in buf:
                break
    assert b"thinking_steps" in buf
    assert b"delta" in buf
    assert b"done" in buf
    hist = client.get(f"/api/v1/chat/sessions/{sid}/messages")
    assert hist.status_code == 200
    msgs = hist.json()["messages"]
    assert any(m.get("role") == "assistant" for m in msgs)
