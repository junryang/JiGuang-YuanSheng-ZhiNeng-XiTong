from __future__ import annotations

from typing import Any, Dict, List


def history_to_chat_messages(history: List[Dict[str, Any]], *, max_turns: int = 20) -> List[Dict[str, str]]:
    """将会话历史转为 OpenAI/DeepSeek chat messages（仅 user/assistant/system）。"""
    out: List[Dict[str, str]] = []
    tail = history[-max_turns:] if max_turns else history
    for m in tail:
        role = str(m.get("role", ""))
        if role not in ("user", "assistant", "system"):
            continue
        txt = str(m.get("content", ""))
        if len(txt) > 48000:
            txt = txt[:48000] + "\n[truncated]"
        out.append({"role": role, "content": txt})
    return out


def build_assistant_content(history: List[Dict[str, Any]], *, context_tail: int = 8) -> str:
    """
    根据会话历史生成助手回复文本；history 须包含末尾一条 role=user（刚发送的用户消息）。
    """
    if not history or history[-1].get("role") != "user":
        return "主脑："
    user_text = str(history[-1].get("content", ""))
    prior = history[:-1][-context_tail:] if len(history) > 1 else []
    if not prior:
        return f"主脑已收到：{user_text}"
    lines: list[str] = []
    for m in prior:
        role = m.get("role", "")
        prefix = "用户" if role == "user" else "主脑"
        lines.append(f"{prefix}: {m.get('content', '')}")
    return "[会话上下文]\n" + "\n".join(lines) + f"\n\n主脑已收到：{user_text}"


def chunk_text_for_sse(text: str, chunk_size: int = 12) -> List[str]:
    if not text:
        return [""]
    return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]


async def resolve_assistant_text(history: List[Dict[str, Any]]) -> str:
    """优先走大模型（若已配置），否则使用本地模板回复。"""
    from app.services.model_router import generate_chat_reply

    generated = await generate_chat_reply(history)
    if generated is not None:
        return generated
    return build_assistant_content(history)
