from __future__ import annotations

from typing import Literal, TypeAlias

TaskPriority: TypeAlias = Literal["P0", "P1", "P2", "P3"]
TaskStatus: TypeAlias = Literal["pending", "assigned", "in_progress", "blocked", "completed", "done", "failed", "cancelled"]
ProjectStatus: TypeAlias = Literal["draft", "pending_approval", "approved", "rejected", "in_progress", "completed", "cancelled"]
Environment: TypeAlias = Literal["dev", "staging", "prod"]
RuntimeMode: TypeAlias = Literal["normal", "degraded"]
ProjectType: TypeAlias = Literal["new_feature", "optimization", "bug_fix"]
DomainCode: TypeAlias = Literal["D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08"]
VALID_DOMAIN_CODES: frozenset[DomainCode] = frozenset({"D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08"})
PRIORITY_LEVELS: tuple[TaskPriority, TaskPriority, TaskPriority, TaskPriority] = ("P0", "P1", "P2", "P3")

TASK_STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "pending": frozenset({"assigned", "in_progress", "blocked", "cancelled"}),
    "assigned": frozenset({"in_progress", "blocked", "cancelled"}),
    "in_progress": frozenset({"blocked", "completed", "done", "cancelled"}),
    "blocked": frozenset({"in_progress", "cancelled"}),
    "done": frozenset({"completed"}),
    "failed": frozenset({"in_progress", "cancelled"}),
    "completed": frozenset(),
    "cancelled": frozenset(),
}

PROJECT_STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"pending_approval", "cancelled"}),
    "pending_approval": frozenset({"approved", "rejected"}),
    "approved": frozenset({"in_progress", "cancelled"}),
    "in_progress": frozenset({"completed", "cancelled"}),
    "rejected": frozenset(),
    "completed": frozenset(),
    "cancelled": frozenset(),
}


def empty_priority_counts() -> dict[str, int]:
    return {p: 0 for p in PRIORITY_LEVELS}
