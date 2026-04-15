import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import chat_service


client = TestClient(app)


def test_resolve_assistant_text_template_without_llm(monkeypatch):
    monkeypatch.delenv("LLM_ENABLED", raising=False)
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    text = asyncio.run(chat_service.resolve_assistant_text([{"role": "user", "content": "你好"}]))
    assert "主脑已收到" in text or "主脑：" in text


def test_resolve_assistant_text_uses_llm_when_enabled(monkeypatch):
    monkeypatch.setenv("LLM_ENABLED", "true")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test-not-real")

    async def fake_complete(**kwargs):
        return "【模型替身回复】"

    monkeypatch.setattr(
        "app.services.model_router.openai_compatible_chat_completion",
        fake_complete,
    )
    text = asyncio.run(chat_service.resolve_assistant_text([{"role": "user", "content": "问一句"}]))
    assert "【模型替身回复】" in text


def test_llm_status_endpoint():
    r = client.get("/api/v1/llm/status")
    assert r.status_code == 200
    body = r.json()
    assert "llm_enabled" in body
    assert "primary_model" in body
    assert "api_configured" in body


def test_history_to_chat_messages_filters_roles():
    rows = [
        {"role": "user", "content": "a"},
        {"role": "tool", "content": "x"},
        {"role": "assistant", "content": "b"},
    ]
    out = chat_service.history_to_chat_messages(rows)
    assert [m["role"] for m in out] == ["user", "assistant"]
