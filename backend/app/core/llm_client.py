"""OpenAI 兼容 Chat Completions HTTP 客户端（DeepSeek / 自建网关等）。"""

from __future__ import annotations

from typing import Any, Dict, List

import httpx


class LLMClientError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


async def openai_compatible_chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 2048,
    temperature: float = 0.7,
    timeout: float = 90.0,
) -> str:
    """
    POST {base_url}/chat/completions
    base_url 须含版本前缀，例如 https://api.deepseek.com/v1
    """
    root = base_url.rstrip("/")
    url = f"{root}/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max(1, min(int(max_tokens), 8192)),
        "temperature": float(temperature),
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, headers=headers, json=body)
    except httpx.TimeoutException as e:
        raise LLMClientError(f"LLM timeout: {e}") from e
    except httpx.RequestError as e:
        raise LLMClientError(f"LLM request error: {e}") from e

    if resp.status_code >= 400:
        raise LLMClientError(
            f"LLM HTTP {resp.status_code}: {resp.text[:500]}",
            status_code=resp.status_code,
        )
    data = resp.json()
    choices = data.get("choices") or []
    if not choices:
        raise LLMClientError("LLM response missing choices")
    msg = choices[0].get("message") or {}
    content = msg.get("content")
    if not isinstance(content, str):
        raise LLMClientError("LLM response missing message.content")
    return content.strip()
