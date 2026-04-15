"""
多模型路由（PH4-T03）：DeepSeek / OpenAI 兼容端点、简易响应缓存、主备降级、并发配额。
无 LLM_ENABLED 或未配置密钥时，聊天仍走本地模板（chat_service.build_assistant_content）。
"""

from __future__ import annotations

import hashlib
import os
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import asyncio

from app.core.llm_client import LLMClientError, openai_compatible_chat_completion
from app.services.chat_service import history_to_chat_messages


def _truthy_env(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ("1", "true", "yes", "on")


def _api_key() -> str:
    return (os.environ.get("LLM_API_KEY") or os.environ.get("DEEPSEEK_API_KEY") or "").strip()


@dataclass(frozen=True)
class LLMSettings:
    enabled: bool
    api_key: str
    base_url: str
    primary_model: str
    fallback_model: Optional[str]
    max_tokens: int
    max_concurrent: int
    cache_ttl_seconds: float
    cache_max_entries: int
    max_input_chars: int
    system_prompt: str


def load_llm_settings() -> LLMSettings:
    fb = (os.environ.get("LLM_FALLBACK_MODEL") or "").strip() or None
    return LLMSettings(
        enabled=_truthy_env("LLM_ENABLED"),
        api_key=_api_key(),
        base_url=(os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com/v1").strip().rstrip("/"),
        primary_model=(os.environ.get("LLM_PRIMARY_MODEL") or "deepseek-chat").strip(),
        fallback_model=fb,
        max_tokens=int(os.environ.get("LLM_MAX_TOKENS", "2048")),
        max_concurrent=max(1, min(int(os.environ.get("LLM_MAX_CONCURRENT", "3")), 32)),
        cache_ttl_seconds=float(os.environ.get("LLM_CACHE_TTL_SECONDS", "300")),
        cache_max_entries=max(8, min(int(os.environ.get("LLM_CACHE_MAX_ENTRIES", "128")), 2000)),
        max_input_chars=max(2000, min(int(os.environ.get("LLM_MAX_INPUT_CHARS", "48000")), 200000)),
        system_prompt=(
            os.environ.get("LLM_SYSTEM_PROMPT")
            or "你是「纪光元生」主脑数字员工，用简体中文专业、简洁地回答。"
        ).strip(),
    )


_sem_pair: tuple[int, asyncio.Semaphore] | None = None
_cache: "OrderedDict[str, tuple[float, str]]" = OrderedDict()


def _get_semaphore(max_concurrent: int) -> asyncio.Semaphore:
    global _sem_pair
    if _sem_pair is None or _sem_pair[0] != max_concurrent:
        _sem_pair = (max_concurrent, asyncio.Semaphore(max_concurrent))
    return _sem_pair[1]


def _cache_key(messages: List[Dict[str, str]], model: str) -> str:
    h = hashlib.sha256()
    h.update(model.encode("utf-8"))
    for m in messages[-16:]:
        h.update(m["role"].encode("utf-8"))
        h.update(m["content"].encode("utf-8")[:4000])
    return h.hexdigest()[:48]


def _cache_get(key: str, settings: LLMSettings) -> Optional[str]:
    now = time.monotonic()
    if key not in _cache:
        return None
    exp_at, text = _cache[key]
    if exp_at <= now:
        del _cache[key]
        return None
    _cache.move_to_end(key)
    return text


def _cache_set(key: str, text: str, settings: LLMSettings) -> None:
    exp_at = time.monotonic() + settings.cache_ttl_seconds
    _cache[key] = (exp_at, text)
    _cache.move_to_end(key)
    while len(_cache) > settings.cache_max_entries:
        _cache.popitem(last=False)


def _trim_messages_to_budget(
    messages: List[Dict[str, str]], max_chars: int
) -> List[Dict[str, str]]:
    """保留末尾轮次，使总字符数不超过预算（尽量保留最后一条 user）。"""
    if not messages:
        return messages
    out = list(messages)
    while out:
        total = sum(len(m["content"]) for m in out)
        if total <= max_chars:
            return out
        if len(out) <= 2:
            # system + 一条 user：截断内容
            if len(out) == 2 and out[1]["role"] == "user":
                room = max_chars - len(out[0]["content"]) - 20
                out[1] = {**out[1], "content": out[1]["content"][: max(200, room)] + "\n[已截断]"}
            return out
        # 去掉最早一条非 system
        for i, m in enumerate(out):
            if m["role"] != "system":
                del out[i]
                break
        else:
            break
    return out


def _build_messages(history: List[Dict[str, Any]], settings: LLMSettings) -> List[Dict[str, str]]:
    hm = history_to_chat_messages(history)
    if hm and hm[0].get("role") == "system":
        core = hm
    else:
        core = [{"role": "system", "content": settings.system_prompt}, *hm]
    budget = max(4000, settings.max_input_chars - 4000)
    return _trim_messages_to_budget(core, budget)


async def _try_complete(settings: LLMSettings, model: str, messages: List[Dict[str, str]]) -> str:
    return await openai_compatible_chat_completion(
        base_url=settings.base_url,
        api_key=settings.api_key,
        model=model,
        messages=messages,
        max_tokens=settings.max_tokens,
    )


async def generate_chat_reply(history: List[Dict[str, Any]]) -> Optional[str]:
    """
    若 LLM 已启用且配置了密钥，则返回模型文本；否则返回 None（由上层回退到模板回复）。
    """
    settings = load_llm_settings()
    if not settings.enabled or not settings.api_key:
        return None

    messages = _build_messages(history, settings)
    cache_key = _cache_key(messages, settings.primary_model)
    hit = _cache_get(cache_key, settings)
    if hit is not None:
        return hit

    sem = _get_semaphore(settings.max_concurrent)
    async with sem:
        try:
            text = await _try_complete(settings, settings.primary_model, messages)
            _cache_set(cache_key, text, settings)
            return text
        except LLMClientError:
            pass
        except Exception:
            return None

    if settings.fallback_model and settings.fallback_model != settings.primary_model:
        fb_key = _cache_key(messages, settings.fallback_model)
        hit_fb = _cache_get(fb_key, settings)
        if hit_fb is not None:
            return hit_fb
        async with sem:
            try:
                text = await _try_complete(settings, settings.fallback_model, messages)
                _cache_set(fb_key, text, settings)
                return text
            except (LLMClientError, Exception):
                return None
    return None


def public_llm_status() -> Dict[str, Any]:
    s = load_llm_settings()
    return {
        "llm_enabled": s.enabled,
        "api_configured": bool(s.api_key),
        "base_url": s.base_url,
        "primary_model": s.primary_model,
        "fallback_model": s.fallback_model,
        "max_concurrent": s.max_concurrent,
        "cache_entries": len(_cache),
        "cache_max_entries": s.cache_max_entries,
        "cache_ttl_seconds": s.cache_ttl_seconds,
    }
