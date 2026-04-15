from __future__ import annotations

from typing import Any, Dict, Optional

from app.services.planning_service import build_ceo_plan


def plan(instruction: str, project: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """主脑 CEO：意图解析 + 任务分解入口。"""
    return build_ceo_plan(instruction, project)
