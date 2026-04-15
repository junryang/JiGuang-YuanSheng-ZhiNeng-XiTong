from __future__ import annotations

import json
import os
import re
import tempfile
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.schemas.common_enums import PROJECT_STATUS_TRANSITIONS, TASK_STATUS_TRANSITIONS


DEFAULT_APPROVAL_CHAIN: List[str] = ["L3", "L2", "L1"]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class JsonStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(self._default_data())

    @staticmethod
    def _default_data() -> Dict[str, Any]:
        return {
            "agents": [],
            "projects": [],
            "chat_sessions": [],
            "users": [],
            "tasks": [],
            "skills": [],
            "delegations": [],
            "working_memories": [],
            "project_discussions": [],
            "marketing_metrics": {
                "fans_growth_7d": 128,
                "engagement_rate_pct": 4.2,
                "reach_7d": 5600,
                "posts_published_7d": 3,
            },
            "marketing_contents": [],
            "marketing_publish_events": [],
            "webhooks": [],
        }

    def _read(self) -> Dict[str, Any]:
        raw = self.path.read_text(encoding="utf-8")
        if not raw.strip():
            # 避免并发/异常中断导致空文件后读取崩溃，自动回填默认结构。
            data = self._default_data()
            self._write(data)
            return data
        data = json.loads(raw)
        changed = False
        if "users" not in data:
            data["users"] = []
            changed = True
        if "tasks" not in data:
            data["tasks"] = []
            changed = True
        if "skills" not in data:
            data["skills"] = []
            changed = True
        if "delegations" not in data:
            data["delegations"] = []
            changed = True
        if "working_memories" not in data:
            data["working_memories"] = []
            changed = True
        if "project_discussions" not in data:
            data["project_discussions"] = []
            changed = True
        if "marketing_metrics" not in data or not isinstance(data.get("marketing_metrics"), dict):
            data["marketing_metrics"] = {
                "fans_growth_7d": 128,
                "engagement_rate_pct": 4.2,
                "reach_7d": 5600,
                "posts_published_7d": 3,
            }
            changed = True
        if "marketing_contents" not in data:
            data["marketing_contents"] = []
            changed = True
        if "marketing_publish_events" not in data:
            data["marketing_publish_events"] = []
            changed = True
        if "webhooks" not in data:
            data["webhooks"] = []
            changed = True
        if changed:
            self._write(data)
        return data

    def _write(self, data: Dict[str, Any]) -> None:
        payload = json.dumps(data, ensure_ascii=False, indent=2)
        fd, tmp_name = tempfile.mkstemp(
            prefix=f"{self.path.name}.",
            suffix=".tmp",
            dir=str(self.path.parent),
            text=True,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())
            for attempt in range(6):
                try:
                    os.replace(tmp_name, self.path)
                    break
                except PermissionError:
                    if attempt == 5:
                        raise
                    # Windows 下文件可能被同步器短暂占用，做轻量重试。
                    time.sleep(0.02 * (attempt + 1))
        finally:
            if os.path.exists(tmp_name):
                os.remove(tmp_name)

    def _touch_project_last_activity(self, data: Dict[str, Any], project_id: str) -> None:
        for i, p in enumerate(data.get("projects") or []):
            if str(p.get("id")) != str(project_id):
                continue
            merged = dict(p)
            merged["last_activity"] = _utc_now_iso()
            data["projects"][i] = merged
            return

    def seed_if_empty(self) -> None:
        data = self._read()
        if not data["agents"]:
            data["agents"] = [
                {
                    "id": "agent-ceo",
                    "name": "主脑",
                    "level": "L1",
                    "role": "CEO",
                    "status": "online",
                    "parent_id": None,
                    "domain": "D03",
                    "profile": {"mission": "统筹纪光元生系统", "long_term_goals": ["v2.0 交付"]},
                    "model_config": {"model_id": "gpt-thinking", "temperature": 0.2},
                    "skill_config": {"skill_ids": ["CEO-09", "CEO-11"]},
                    "memory_config": {"working_memory_slots": 12, "long_term_enabled": True},
                    "health": {"error_streak": 0},
                },
                {
                    "id": "agent-gm-d02",
                    "name": "研发总经理",
                    "level": "L2",
                    "role": "GM",
                    "status": "online",
                    "parent_id": "agent-ceo",
                    "domain": "D02",
                },
                {
                    "id": "agent-pm-d02",
                    "name": "项目经理",
                    "level": "L3",
                    "role": "PM",
                    "status": "busy",
                    "parent_id": "agent-gm-d02",
                    "domain": "D02",
                },
            ]
        if not data["projects"]:
            data["projects"] = [
                {
                    "id": "JYIS-2026-001",
                    "name": "纪光元生核心系统 v2.0",
                    "domain": "D03",
                    "project_type": "new_feature",
                    "environment": "dev",
                    "status": "draft",
                    "milestones": [
                        {
                            "id": "ms-mvp",
                            "name": "MVP 里程碑",
                            "target_date": "2026-06-30",
                            "done": False,
                        },
                    ],
                }
            ]
        if not data["users"]:
            from app.core.security import hash_password

            data["users"] = [
                {
                    "id": "usr-dev-admin",
                    "email": "dev@jyis.local",
                    "password_hash": hash_password("devpass"),
                    "roles": ["admin", "user"],
                }
            ]
        self._write(data)

    def list_agents(
        self,
        *,
        level: Optional[str] = None,
        status: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[Dict[str, Any]], int]:
        rows = list(self._read()["agents"])
        if level:
            rows = [a for a in rows if str(a.get("level")) == level]
        if status:
            rows = [a for a in rows if str(a.get("status", "online")) == status]
        if q:
            ql = q.lower()
            rows = [a for a in rows if ql in str(a.get("name", "")).lower() or ql in str(a.get("id", "")).lower()]
        total = len(rows)
        page = rows[offset : offset + max(1, min(limit, 200))]
        return page, total

    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        for a in self._read()["agents"]:
            if a.get("id") == agent_id:
                return a
        raise KeyError(f"agent not found: {agent_id}")

    def create_agent(self, record: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        parent_id = record.get("parent_id")
        if parent_id:
            # 校验父节点存在，避免孤儿引用。
            _ = next((a for a in data["agents"] if str(a.get("id")) == str(parent_id)), None)
            if _ is None:
                raise ValueError(f"parent agent not found: {parent_id}")
        row = {
            "id": f"agent-{uuid4().hex[:10]}",
            "name": str(record.get("name") or "").strip()[:120] or "unnamed-agent",
            "level": str(record.get("level") or "L5"),
            "role": str(record.get("role") or "EMPLOYEE"),
            "status": str(record.get("status") or "online"),
            "parent_id": parent_id,
            "domain": record.get("domain"),
        }
        data["agents"].append(row)
        self._write(data)
        return row

    def create_agents_batch(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        created: List[Dict[str, Any]] = []
        # 顺序创建，允许后续记录引用本批次前序新建节点。
        for row in rows:
            created.append(self.create_agent(row))
        return created

    def get_org_tree(self) -> List[Dict[str, Any]]:
        agents = self._read()["agents"]
        ids = {str(a["id"]) for a in agents if a.get("id")}
        by_parent: Dict[Any, List[Dict[str, Any]]] = {}
        for a in agents:
            p = a.get("parent_id")
            if p is not None and str(p) not in ids:
                p = None
            by_parent.setdefault(p, []).append(a)

        def build(agent: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "id": agent.get("id"),
                "name": agent.get("name"),
                "level": agent.get("level"),
                "role": agent.get("role"),
                "status": agent.get("status", "online"),
                "domain": agent.get("domain"),
                "children": [build(c) for c in by_parent.get(agent.get("id"), [])],
            }

        return [build(r) for r in by_parent.get(None, [])]

    def list_projects(self) -> List[Dict[str, Any]]:
        return self._read()["projects"]

    def _next_project_id(self, data: Dict[str, Any]) -> str:
        year = datetime.now().year
        prefix = f"JYIS-{year}-"
        max_n = 0
        # 兼容序号从 3 位增长到 4 位及以上（如 1000、1001...）
        pat = re.compile(rf"^{re.escape(prefix)}(\d{{3,}})$")
        for p in data["projects"]:
            m = pat.match(str(p.get("id", "")))
            if m:
                max_n = max(max_n, int(m.group(1)))
        return f"{prefix}{max_n + 1:03d}"

    def get_project(self, project_id: str) -> Dict[str, Any]:
        data = self._read()
        for p in data["projects"]:
            if p.get("id") == project_id:
                return p
        raise KeyError(f"project not found: {project_id}")

    def create_project(self, record: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        pid = self._next_project_id(data)
        project = {"id": pid, **record}
        if "tags" not in project:
            project["tags"] = []
        if not isinstance(project.get("tags"), list):
            project["tags"] = []
        project["last_activity"] = _utc_now_iso()
        data["projects"].append(project)
        self._write(data)
        return project

    def update_project(self, project_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        for i, p in enumerate(data["projects"]):
            if p.get("id") == project_id:
                merged = {**p, **{k: v for k, v in patch.items() if v is not None and k != "id"}}
                merged["id"] = project_id
                merged["last_activity"] = _utc_now_iso()
                data["projects"][i] = merged
                self._write(data)
                return merged
        raise KeyError(f"project not found: {project_id}")

    def delete_project(self, project_id: str) -> None:
        data = self._read()
        before = len(data["projects"])
        data["projects"] = [p for p in data["projects"] if p.get("id") != project_id]
        if len(data["projects"]) == before:
            raise KeyError(f"project not found: {project_id}")
        self._write(data)

    def transition_project_status(self, project_id: str, new_status: str) -> Dict[str, Any]:
        proj = self.get_project(project_id)
        current = str(proj.get("status", "draft"))
        allowed = PROJECT_STATUS_TRANSITIONS.get(current, frozenset())
        if new_status not in allowed:
            raise ValueError(f"invalid status transition: {current} -> {new_status}")
        return self.update_project(project_id, {"status": new_status})

    def list_projects_pending_approval(self) -> List[Dict[str, Any]]:
        return [p for p in self._read()["projects"] if str(p.get("status")) == "pending_approval"]

    def submit_for_approval(self, project_id: str, chain: Optional[List[str]] = None) -> Dict[str, Any]:
        proj = self.get_project(project_id)
        if str(proj.get("status", "draft")) != "draft":
            raise ValueError("only draft projects can be submitted for approval")
        ch = list(chain) if chain else list(DEFAULT_APPROVAL_CHAIN)
        if not ch:
            raise ValueError("approval_chain must not be empty")
        self.transition_project_status(project_id, "pending_approval")
        approval: Dict[str, Any] = {
            "chain": ch,
            "step": 0,
            "submitted_at": _utc_now_iso(),
            "history": [{"action": "submit", "at": _utc_now_iso()}],
        }
        return self.update_project(project_id, {"approval": approval})

    def approve_project_step(self, project_id: str, approver_level: str) -> Dict[str, Any]:
        proj = self.get_project(project_id)
        if str(proj.get("status")) != "pending_approval":
            raise ValueError("project is not pending approval")
        ap = proj.get("approval") or {}
        chain = list(ap.get("chain") or DEFAULT_APPROVAL_CHAIN)
        step = int(ap.get("step", 0))
        if step >= len(chain):
            raise ValueError("approval chain has no pending step")
        expected = chain[step]
        if approver_level != expected:
            raise ValueError(f"current approver level must be {expected}, got {approver_level}")
        history = list(ap.get("history", []))
        history.append({"action": "approve", "level": approver_level, "at": _utc_now_iso()})
        if step == len(chain) - 1:
            self.transition_project_status(project_id, "approved")
            new_ap = {**ap, "chain": chain, "step": step + 1, "history": history, "resolved_at": _utc_now_iso()}
            return self.update_project(project_id, {"approval": new_ap})
        new_ap = {**ap, "chain": chain, "step": step + 1, "history": history}
        return self.update_project(project_id, {"approval": new_ap})

    def reject_project_approval(self, project_id: str, approver_level: str, reason: str) -> Dict[str, Any]:
        proj = self.get_project(project_id)
        if str(proj.get("status")) != "pending_approval":
            raise ValueError("project is not pending approval")
        ap = proj.get("approval") or {}
        chain = list(ap.get("chain") or DEFAULT_APPROVAL_CHAIN)
        step = int(ap.get("step", 0))
        if step < len(chain):
            expected = chain[step]
            if approver_level != expected:
                raise ValueError(f"current approver level must be {expected}, got {approver_level}")
        history = list(ap.get("history", []))
        history.append(
            {
                "action": "reject",
                "level": approver_level,
                "reason": reason,
                "at": _utc_now_iso(),
            }
        )
        self.transition_project_status(project_id, "rejected")
        new_ap = {**ap, "chain": chain, "history": history, "rejected_at": _utc_now_iso(), "reject_reason": reason}
        return self.update_project(project_id, {"approval": new_ap})

    def create_session(self, title: str) -> Dict[str, Any]:
        data = self._read()
        session = {"id": f"sess-{uuid4().hex[:10]}", "title": title, "messages": []}
        data["chat_sessions"].append(session)
        self._write(data)
        return session

    def list_sessions(self) -> List[Dict[str, Any]]:
        return [{"id": s["id"], "title": s["title"]} for s in self._read()["chat_sessions"]]

    def add_message(self, session_id: str, role: str, content: str) -> Dict[str, Any]:
        data = self._read()
        for session in data["chat_sessions"]:
            if session["id"] == session_id:
                msg = {"id": f"msg-{uuid4().hex[:10]}", "role": role, "content": content}
                session["messages"].append(msg)
                self._write(data)
                return msg
        raise KeyError(f"session not found: {session_id}")

    def get_messages(self, session_id: str) -> List[Dict[str, Any]]:
        data = self._read()
        for session in data["chat_sessions"]:
            if session["id"] == session_id:
                return session["messages"]
        raise KeyError(f"session not found: {session_id}")

    def get_session(self, session_id: str) -> Dict[str, Any]:
        data = self._read()
        for session in data["chat_sessions"]:
            if session["id"] == session_id:
                return session
        raise KeyError(f"session not found: {session_id}")

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        el = email.strip().lower()
        for u in self._read()["users"]:
            if str(u.get("email", "")).lower() == el:
                return u
        raise KeyError(f"user not found: {email}")

    def create_user(self, email: str, password_hash: str, roles: List[str]) -> Dict[str, Any]:
        data = self._read()
        el = email.strip().lower()
        for u in data["users"]:
            if str(u.get("email", "")).lower() == el:
                raise ValueError("email already registered")
        user = {
            "id": f"usr-{uuid4().hex[:12]}",
            "email": el,
            "password_hash": password_hash,
            "roles": list(roles),
        }
        data["users"].append(user)
        self._write(data)
        return user

    # --- tasks (PH2-T02) ---

    def _task_index(self, data: Dict[str, Any], task_id: str) -> int:
        for i, t in enumerate(data["tasks"]):
            if t.get("id") == task_id:
                return i
        raise KeyError(f"task not found: {task_id}")

    def _strip_dependency_refs(self, data: Dict[str, Any], removed_id: str) -> None:
        for t in data["tasks"]:
            deps = list(t.get("dependencies") or [])
            if removed_id in deps:
                t["dependencies"] = [d for d in deps if d != removed_id]

    def _validate_task_integrity(self, task: Dict[str, Any], data: Dict[str, Any], *, is_new: bool) -> None:
        proj_id = task["project_id"]
        self.get_project(proj_id)
        tid = task.get("id")
        if pid := task.get("parent_id"):
            parent = data["tasks"][self._task_index(data, pid)]
            if parent.get("project_id") != proj_id:
                raise ValueError("parent task must belong to the same project")
        for dep_id in task.get("dependencies") or []:
            if tid and dep_id == tid:
                raise ValueError("task cannot depend on itself")
            dep = data["tasks"][self._task_index(data, dep_id)]
            if dep.get("project_id") != proj_id:
                raise ValueError("dependency must belong to the same project")
            if tid and tid in (dep.get("dependencies") or []):
                raise ValueError("circular dependency")

    def create_task(self, record: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        task: Dict[str, Any] = {
            "id": f"task-{uuid4().hex[:10]}",
            "project_id": record["project_id"],
            "name": record["name"],
            "description": str(record.get("description", "")),
            "priority": str(record.get("priority", "P2")),
            "status": str(record.get("status", "pending")),
            "progress": max(0, min(100, int(record.get("progress", 0)))),
            "parent_id": record.get("parent_id"),
            "assignee_level": record.get("assignee_level"),
            "assignee_role": record.get("assignee_role"),
            "assignee_id": record.get("assignee_id"),
            "estimated_hours": record.get("estimated_hours"),
            "actual_hours": record.get("actual_hours"),
            "dependencies": list(record.get("dependencies") or []),
            "start_date": record.get("start_date"),
            "end_date": record.get("end_date"),
            "completed_at": record.get("completed_at"),
        }
        self._validate_task_integrity(task, data, is_new=True)
        data["tasks"].append(task)
        self._touch_project_last_activity(data, task["project_id"])
        self._write(data)
        return task

    def list_tasks(
        self,
        *,
        project_id: Optional[str] = None,
        assignee_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        root_only: bool = False,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[Dict[str, Any]], int]:
        rows = list(self._read()["tasks"])
        if project_id:
            rows = [t for t in rows if str(t.get("project_id")) == project_id]
        if assignee_id:
            rows = [t for t in rows if str(t.get("assignee_id") or "") == str(assignee_id)]
        if root_only:
            rows = [t for t in rows if not t.get("parent_id")]
        elif parent_id is not None:
            rows = [t for t in rows if str(t.get("parent_id")) == parent_id]
        if status:
            rows = [t for t in rows if str(t.get("status")) == status]
        total = len(rows)
        lim = max(1, min(int(limit), 500))
        off = max(0, int(offset))
        return rows[off : off + lim], total

    def get_task(self, task_id: str) -> Dict[str, Any]:
        data = self._read()
        return data["tasks"][self._task_index(data, task_id)]

    def update_task(self, task_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        idx = self._task_index(data, task_id)
        merged = dict(data["tasks"][idx])
        old_status = str(merged.get("status", "pending"))
        for k, v in patch.items():
            if k == "id":
                continue
            merged[k] = v
        merged["id"] = task_id
        if "status" in patch:
            new_status = str(merged.get("status", "")).strip()
            if new_status not in TASK_STATUS_TRANSITIONS:
                raise ValueError(f"invalid task status: {new_status}")
            if new_status != old_status and new_status not in TASK_STATUS_TRANSITIONS.get(old_status, frozenset()):
                raise ValueError(f"invalid task status transition: {old_status} -> {new_status}")
        if "progress" in patch:
            merged["progress"] = max(0, min(100, int(merged["progress"])))
        if "dependencies" in patch:
            merged["dependencies"] = list(patch.get("dependencies") or [])
        self._validate_task_integrity(merged, data, is_new=False)
        data["tasks"][idx] = merged
        self._touch_project_last_activity(data, str(merged.get("project_id", "")))
        self._write(data)
        return merged

    def delete_task(self, task_id: str) -> None:
        data = self._read()
        children = [t for t in data["tasks"] if t.get("parent_id") == task_id]
        if children:
            raise ValueError("cannot delete task with child tasks")
        self._task_index(data, task_id)
        removed = next((t for t in data["tasks"] if t.get("id") == task_id), None)
        data["tasks"] = [t for t in data["tasks"] if t.get("id") != task_id]
        self._strip_dependency_refs(data, task_id)
        if removed and removed.get("project_id"):
            self._touch_project_last_activity(data, str(removed.get("project_id")))
        self._write(data)

    # --- skills (PH3-T02) ---

    SKILL_CATEGORIES = frozenset({"common", "backend", "frontend", "agent", "testing", "marketing"})
    SKILL_LEVELS = frozenset({"senior", "middle", "junior"})

    def create_skill(self, record: Dict[str, Any]) -> Dict[str, Any]:
        cat = str(record.get("category", "common"))
        if cat not in self.SKILL_CATEGORIES:
            raise ValueError(f"invalid category: {cat}")
        lvl = str(record.get("level", "middle"))
        if lvl not in self.SKILL_LEVELS:
            raise ValueError(f"invalid level: {lvl}")
        data = self._read()
        skill: Dict[str, Any] = {
            "id": f"skl-{uuid4().hex[:10]}",
            "name": record["name"],
            "description": str(record.get("description", "")),
            "category": cat,
            "level": lvl,
            "linked_agent_ids": list(record.get("linked_agent_ids") or []),
        }
        for aid in skill["linked_agent_ids"]:
            self.get_agent(str(aid))
        data["skills"].append(skill)
        self._write(data)
        return skill

    def list_skills(
        self,
        *,
        category: Optional[str] = None,
        level: Optional[str] = None,
        q: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[Dict[str, Any]], int]:
        rows = list(self._read()["skills"])
        if category:
            rows = [s for s in rows if str(s.get("category")) == category]
        if level:
            rows = [s for s in rows if str(s.get("level")) == level]
        if q:
            ql = q.lower()
            rows = [s for s in rows if ql in str(s.get("name", "")).lower()]
        total = len(rows)
        lim = max(1, min(int(limit), 500))
        off = max(0, int(offset))
        return rows[off : off + lim], total

    def get_skill(self, skill_id: str) -> Dict[str, Any]:
        for s in self._read()["skills"]:
            if s.get("id") == skill_id:
                return s
        raise KeyError(f"skill not found: {skill_id}")

    def update_skill(self, skill_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        for i, s in enumerate(data["skills"]):
            if s.get("id") == skill_id:
                merged = dict(s)
                for k, v in patch.items():
                    if k == "id":
                        continue
                    merged[k] = v
                merged["id"] = skill_id
                if "category" in patch and str(merged.get("category")) not in self.SKILL_CATEGORIES:
                    raise ValueError("invalid category")
                if "level" in patch and str(merged.get("level")) not in self.SKILL_LEVELS:
                    raise ValueError("invalid level")
                if "linked_agent_ids" in patch:
                    merged["linked_agent_ids"] = list(patch.get("linked_agent_ids") or [])
                    for aid in merged["linked_agent_ids"]:
                        self.get_agent(str(aid))
                data["skills"][i] = merged
                self._write(data)
                return merged
        raise KeyError(f"skill not found: {skill_id}")

    def delete_skill(self, skill_id: str) -> None:
        data = self._read()
        before = len(data["skills"])
        data["skills"] = [s for s in data["skills"] if s.get("id") != skill_id]
        if len(data["skills"]) == before:
            raise KeyError(f"skill not found: {skill_id}")
        self._write(data)

    def list_agent_skills(self, agent_id: str) -> List[Dict[str, Any]]:
        self.get_agent(agent_id)
        rows = []
        for s in self._read()["skills"]:
            linked = [str(x) for x in (s.get("linked_agent_ids") or [])]
            if str(agent_id) in linked:
                rows.append(dict(s))
        return rows

    def replace_agent_skills(self, agent_id: str, skill_ids: List[str]) -> List[Dict[str, Any]]:
        self.get_agent(agent_id)
        wanted = [str(x) for x in (skill_ids or [])]
        data = self._read()
        existing_ids = {str(s.get("id")) for s in data["skills"]}
        missing = [sid for sid in wanted if sid not in existing_ids]
        if missing:
            raise KeyError(f"skills not found: {', '.join(missing)}")

        wanted_set = set(wanted)
        for i, s in enumerate(data["skills"]):
            linked = [str(x) for x in (s.get("linked_agent_ids") or [])]
            linked_set = set(linked)
            sid = str(s.get("id"))
            if sid in wanted_set and str(agent_id) not in linked_set:
                linked.append(str(agent_id))
            if sid not in wanted_set and str(agent_id) in linked_set:
                linked = [x for x in linked if str(x) != str(agent_id)]
            data["skills"][i] = {**s, "linked_agent_ids": linked}
        self._write(data)
        return self.list_agent_skills(agent_id)

    # --- delegations (PH3-T04 雏形) ---

    def create_delegation(self, record: Dict[str, Any]) -> Dict[str, Any]:
        self.get_agent(str(record["from_agent_id"]))
        self.get_agent(str(record["to_agent_id"]))
        raw_contract = record.get("contract")
        if not isinstance(raw_contract, dict):
            raise ValueError("delegation contract is required")
        acceptance = str(raw_contract.get("acceptance_criteria", "")).strip()
        if not acceptance:
            raise ValueError("delegation contract.acceptance_criteria is required")
        raw_deliverables = raw_contract.get("deliverables")
        if not isinstance(raw_deliverables, list) or not raw_deliverables:
            raise ValueError("delegation contract.deliverables must be a non-empty list")
        deliverables = [str(x).strip() for x in raw_deliverables if str(x).strip()]
        if not deliverables:
            raise ValueError("delegation contract.deliverables must contain non-empty items")
        due_date = raw_contract.get("due_date")
        contract = {
            "acceptance_criteria": acceptance,
            "deliverables": deliverables,
            "due_date": str(due_date).strip() if due_date is not None and str(due_date).strip() else None,
        }
        data = self._read()
        row = {
            "id": f"dlg-{uuid4().hex[:10]}",
            "from_agent_id": str(record["from_agent_id"]),
            "to_agent_id": str(record["to_agent_id"]),
            "objective": str(record["objective"]),
            "contract": contract,
            "project_id": record.get("project_id"),
            "status": str(record.get("status", "open")),
            "created_at": _utc_now_iso(),
        }
        if row["project_id"]:
            self.get_project(str(row["project_id"]))
        data["delegations"].append(row)
        self._write(data)
        return row

    def get_delegation(self, delegation_id: str) -> Dict[str, Any]:
        for row in self._read()["delegations"]:
            if str(row.get("id")) == str(delegation_id):
                return dict(row)
        raise KeyError(f"delegation not found: {delegation_id}")

    def list_delegations(
        self,
        *,
        from_agent_id: Optional[str] = None,
        to_agent_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> tuple[List[Dict[str, Any]], int]:
        rows = list(self._read()["delegations"])
        if from_agent_id:
            rows = [r for r in rows if str(r.get("from_agent_id")) == from_agent_id]
        if to_agent_id:
            rows = [r for r in rows if str(r.get("to_agent_id")) == to_agent_id]
        total = len(rows)
        lim = max(1, min(int(limit), 500))
        off = max(0, int(offset))
        return rows[off : off + lim], total

    def update_delegation_status(self, delegation_id: str, status: str) -> Dict[str, Any]:
        if status not in ("open", "accepted", "done"):
            raise ValueError(f"invalid delegation status: {status}")
        data = self._read()
        for i, row in enumerate(data["delegations"]):
            if str(row.get("id")) == str(delegation_id):
                merged = {**row, "status": status}
                data["delegations"][i] = merged
                self._write(data)
                return merged
        raise KeyError(f"delegation not found: {delegation_id}")

    def delete_delegation(self, delegation_id: str) -> None:
        data = self._read()
        before = len(data["delegations"])
        data["delegations"] = [r for r in data["delegations"] if str(r.get("id")) != str(delegation_id)]
        if len(data["delegations"]) == before:
            raise KeyError(f"delegation not found: {delegation_id}")
        self._write(data)

    # --- working memory JSON 占位 (PH3-T03) ---

    def append_working_memory(self, agent_id: str, content: str) -> Dict[str, Any]:
        self.get_agent(agent_id)
        data = self._read()
        row = {
            "id": f"wm-{uuid4().hex[:10]}",
            "agent_id": agent_id,
            "content": content,
            "created_at": _utc_now_iso(),
        }
        data["working_memories"].append(row)
        self._write(data)
        return row

    def list_working_memories(self, agent_id: str, *, limit: int = 50) -> List[Dict[str, Any]]:
        self.get_agent(agent_id)
        rows = [m for m in self._read()["working_memories"] if m.get("agent_id") == agent_id]
        rows.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        return rows[: max(1, min(limit, 200))]

    # --- 项目讨论区 (PH4 项目详情) ---

    def add_project_discussion(self, project_id: str, author: str, body: str) -> Dict[str, Any]:
        self.get_project(project_id)
        data = self._read()
        row = {
            "id": f"pdc-{uuid4().hex[:10]}",
            "project_id": project_id,
            "author": (author or "anonymous").strip()[:80] or "anonymous",
            "body": body.strip()[:8000],
            "created_at": _utc_now_iso(),
        }
        data["project_discussions"].append(row)
        self._touch_project_last_activity(data, project_id)
        self._write(data)
        return row

    def list_project_discussions(
        self, project_id: str, *, limit: int = 100, offset: int = 0
    ) -> tuple[List[Dict[str, Any]], int]:
        self.get_project(project_id)
        rows = [d for d in self._read()["project_discussions"] if str(d.get("project_id")) == project_id]
        rows.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        total = len(rows)
        lim = max(1, min(int(limit), 500))
        off = max(0, int(offset))
        return rows[off : off + lim], total

    def project_team_from_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """按任务 assignee_level/assignee_role 汇总项目团队（PH4 项目详情）。"""
        self.get_project(project_id)
        tasks, _ = self.list_tasks(project_id=project_id, limit=500, offset=0)
        counts: Dict[tuple[str, str], int] = defaultdict(int)
        for t in tasks:
            lr = t.get("assignee_level")
            rr = t.get("assignee_role")
            lvl = str(lr).strip() if lr is not None else ""
            role = str(rr).strip() if rr is not None else ""
            if not lvl and not role:
                continue
            counts[(lvl, role)] += 1

        agents = self._read()["agents"]

        def names_for(lvl: str, role: str) -> List[str]:
            names: List[str] = []
            for a in agents:
                al = str(a.get("level") or "").strip()
                ar = str(a.get("role") or "").strip()
                if lvl and al != lvl:
                    continue
                if role and ar != role:
                    continue
                n = a.get("name")
                if n:
                    names.append(str(n))
            return sorted(set(names))[:8]

        items: List[Dict[str, Any]] = []
        for (lvl, role), n in sorted(counts.items(), key=lambda x: (-x[1], x[0][0], x[0][1])):
            items.append(
                {
                    "assignee_level": lvl or None,
                    "assignee_role": role or None,
                    "task_count": n,
                    "matched_agent_names": names_for(lvl, role),
                }
            )
        return items

    # --- 营销中心 (PH4-T04) ---

    def get_marketing_metrics(self) -> Dict[str, Any]:
        return dict(self._read()["marketing_metrics"])

    def patch_marketing_metrics(self, patch: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        cur = dict(data["marketing_metrics"])
        if "fans_growth_7d" in patch and patch["fans_growth_7d"] is not None:
            cur["fans_growth_7d"] = int(patch["fans_growth_7d"])
        if "reach_7d" in patch and patch["reach_7d"] is not None:
            cur["reach_7d"] = int(patch["reach_7d"])
        if "posts_published_7d" in patch and patch["posts_published_7d"] is not None:
            cur["posts_published_7d"] = int(patch["posts_published_7d"])
        if "engagement_rate_pct" in patch and patch["engagement_rate_pct"] is not None:
            cur["engagement_rate_pct"] = float(patch["engagement_rate_pct"])
        data["marketing_metrics"] = cur
        self._write(data)
        return cur

    def list_marketing_publish_events(self, *, limit: int = 30) -> List[Dict[str, Any]]:
        rows = list(self._read().get("marketing_publish_events") or [])
        rows.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        lim = max(1, min(int(limit), 200))
        return rows[:lim]

    def append_marketing_publish_event(
        self,
        *,
        content_id: str,
        title: str,
        platforms: List[str],
        environment: str,
    ) -> Dict[str, Any]:
        data = self._read()
        if "marketing_publish_events" not in data:
            data["marketing_publish_events"] = []
        ev: Dict[str, Any] = {
            "id": f"mpe-{uuid4().hex[:10]}",
            "content_id": content_id,
            "title": (title or "")[:500],
            "platforms": [str(p)[:32] for p in (platforms or [])][:16],
            "environment": str(environment),
            "created_at": _utc_now_iso(),
        }
        data["marketing_publish_events"].append(ev)
        self._write(data)
        return ev

    def marketing_dashboard(self) -> Dict[str, Any]:
        data = self._read()
        allc: List[Dict[str, Any]] = list(data.get("marketing_contents") or [])
        m = self.get_marketing_metrics()
        return {
            "metrics": m,
            "contents_total": len(allc),
            "contents_published": sum(1 for c in allc if str(c.get("status")) == "published"),
            "contents_draft": sum(1 for c in allc if str(c.get("status")) == "draft"),
            "contents_scheduled": sum(1 for c in allc if str(c.get("status")) == "scheduled"),
            "recent_publishes": self.list_marketing_publish_events(limit=8),
        }

    def list_marketing_contents(self, *, limit: int = 50, offset: int = 0) -> tuple[List[Dict[str, Any]], int]:
        rows = list(self._read().get("marketing_contents") or [])
        rows.sort(key=lambda x: str(x.get("updated_at", "")), reverse=True)
        total = len(rows)
        lim = max(1, min(int(limit), 200))
        off = max(0, int(offset))
        return rows[off : off + lim], total

    def get_marketing_content(self, content_id: str) -> Dict[str, Any]:
        for c in self._read().get("marketing_contents") or []:
            if str(c.get("id")) == content_id:
                return c
        raise KeyError(f"marketing content not found: {content_id}")

    def create_marketing_content(
        self,
        title: str,
        body: str,
        platforms: List[str],
        *,
        status: str = "draft",
    ) -> Dict[str, Any]:
        st = str(status)
        if st not in ("draft", "published", "scheduled"):
            st = "draft"
        data = self._read()
        row: Dict[str, Any] = {
            "id": f"mc-{uuid4().hex[:10]}",
            "title": title.strip()[:500] or "未命名",
            "body": str(body)[:50000],
            "status": st,
            "platforms": [str(p)[:32] for p in (platforms or [])][:16],
            "created_at": _utc_now_iso(),
            "updated_at": _utc_now_iso(),
        }
        data["marketing_contents"].append(row)
        self._write(data)
        return row

    def update_marketing_content(self, content_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        for i, c in enumerate(data.get("marketing_contents") or []):
            if str(c.get("id")) != content_id:
                continue
            merged = dict(c)
            if patch.get("title") is not None:
                t = str(patch["title"]).strip()[:500]
                merged["title"] = t or merged.get("title", "未命名")
            if patch.get("body") is not None:
                merged["body"] = str(patch["body"])[:50000]
            if patch.get("status") is not None:
                st = str(patch["status"])
                if st in ("draft", "published", "scheduled"):
                    merged["status"] = st
            if patch.get("platforms") is not None:
                merged["platforms"] = [str(p)[:32] for p in patch["platforms"]][:16]
            merged["updated_at"] = _utc_now_iso()
            data["marketing_contents"][i] = merged
            self._write(data)
            return merged
        raise KeyError(f"marketing content not found: {content_id}")

    # --- webhooks (v1.1.0 planned) ---

    def create_webhook(self, record: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        if "webhooks" not in data:
            data["webhooks"] = []
        row: Dict[str, Any] = {
            "id": f"wh-{uuid4().hex[:10]}",
            "name": str(record.get("name", "")).strip()[:120] or "default-webhook",
            "url": str(record.get("url", "")).strip(),
            "events": [str(x)[:80] for x in (record.get("events") or [])][:32],
            "enabled": bool(record.get("enabled", True)),
            "secret": str(record.get("secret", "")).strip()[:256],
            "created_at": _utc_now_iso(),
            "updated_at": _utc_now_iso(),
        }
        data["webhooks"].append(row)
        self._write(data)
        return row

    def list_webhooks(self, *, enabled: Optional[bool] = None, limit: int = 100, offset: int = 0) -> tuple[List[Dict[str, Any]], int]:
        rows = list(self._read().get("webhooks") or [])
        rows.sort(key=lambda x: str(x.get("created_at", "")), reverse=True)
        if enabled is not None:
            rows = [x for x in rows if bool(x.get("enabled", True)) is bool(enabled)]
        total = len(rows)
        lim = max(1, min(int(limit), 500))
        off = max(0, int(offset))
        return rows[off : off + lim], total

    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        for row in self._read().get("webhooks") or []:
            if str(row.get("id")) == str(webhook_id):
                return dict(row)
        raise KeyError(f"webhook not found: {webhook_id}")

    def update_webhook(self, webhook_id: str, patch: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        rows = list(data.get("webhooks") or [])
        for i, row in enumerate(rows):
            if str(row.get("id")) != str(webhook_id):
                continue
            merged = dict(row)
            if "name" in patch and patch.get("name") is not None:
                merged["name"] = str(patch.get("name")).strip()[:120] or merged.get("name", "default-webhook")
            if "url" in patch and patch.get("url") is not None:
                merged["url"] = str(patch.get("url")).strip()
            if "events" in patch and patch.get("events") is not None:
                merged["events"] = [str(x)[:80] for x in (patch.get("events") or [])][:32]
            if "enabled" in patch and patch.get("enabled") is not None:
                merged["enabled"] = bool(patch.get("enabled"))
            if "secret" in patch and patch.get("secret") is not None:
                merged["secret"] = str(patch.get("secret")).strip()[:256]
            merged["updated_at"] = _utc_now_iso()
            rows[i] = merged
            data["webhooks"] = rows
            self._write(data)
            return merged
        raise KeyError(f"webhook not found: {webhook_id}")

    def delete_webhook(self, webhook_id: str) -> None:
        data = self._read()
        rows = list(data.get("webhooks") or [])
        kept = [x for x in rows if str(x.get("id")) != str(webhook_id)]
        if len(kept) == len(rows):
            raise KeyError(f"webhook not found: {webhook_id}")
        data["webhooks"] = kept
        self._write(data)
