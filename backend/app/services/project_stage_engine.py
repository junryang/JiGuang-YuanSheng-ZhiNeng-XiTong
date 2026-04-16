from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from app.core.store import JsonStore
from app.models.project_stage import (
    Approval,
    Deliverable,
    ProjectStage,
    Participant,
    StagePhase,
    StageStatus,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class StageDefinition:
    id: str
    name: str
    phase: StagePhase
    order: int
    timeout_days: int

    owner_role: str
    owner_level: str
    owner_department: str

    participants: List[Participant]
    deliverables: List[Deliverable]
    approval: Approval


def _stage_definitions() -> List[StageDefinition]:
    """
    Minimal definitions derived from PROJECT_LIFECYCLE_SPEC_v1.0.md.
    Note: Only required deliverable names are guaranteed; schema/templates are optional.
    """

    def A(
        *,
        required: bool,
        approver_role: str,
        approver_level: str,
        timeout_hours: int = 48,
        auto_approve_if_no_response: bool = False,
        condition: str | None = None,
        default_approver_role: str | None = None,
        default_approver_level: str | None = None,
    ) -> Approval:
        return Approval(
            required=required,
            approver_role=approver_role,
            approver_level=approver_level,
            timeout_hours=timeout_hours,
            auto_approve_if_no_response=auto_approve_if_no_response,
            condition=condition,
            default_approver_role=default_approver_role,
            default_approver_level=default_approver_level,
        )

    return [
        StageDefinition(
            id="P01",
            name="市场调研",
            phase=StagePhase.PLANNING,
            order=1,
            timeout_days=5,
            owner_role="营销主管",
            owner_level="L4",
            owner_department="营销部",
            participants=[
                Participant(role="营销主管", level="L4", responsibility="组织调研，审核报告"),
                Participant(role="资深内容运营", level="L5", responsibility="执行调研，收集数据"),
                Participant(role="实习运营助理", level="L6", responsibility="整理数据，协助分析"),
            ],
            deliverables=[
                Deliverable(
                    name="市场分析报告",
                    type="document",
                    template="market_analysis_report_template.md",
                    required=True,
                    schema_def={
                        "title": "string",
                        "date": "date",
                        "author": "string",
                        "executive_summary": "string",
                        "market_size": "object",
                        "competition_analysis": "array",
                        "target_audience": "array",
                        "swot_analysis": "object",
                        "recommendations": "array",
                    },
                )
            ],
            approval=A(required=True, approver_role="总经理", approver_level="L2", timeout_hours=48),
        ),
        StageDefinition(
            id="P02",
            name="需求分析",
            phase=StagePhase.PLANNING,
            order=2,
            timeout_days=5,
            owner_role="产品主管",
            owner_level="L4",
            owner_department="产品部",
            participants=[
                Participant(role="产品主管", level="L4", responsibility="组织需求分析，审核需求文档"),
                Participant(role="资深产品经理", level="L5", responsibility="执行需求分析，编写需求文档"),
                Participant(role="实习产品助理", level="L6", responsibility="整理需求，协助编写文档"),
            ],
            deliverables=[
                Deliverable(
                    name="需求规格说明书",
                    type="document",
                    template="prd_template.md",
                    required=True,
                    schema_def={
                        "title": "string",
                        "version": "string",
                        "creation_date": "date",
                        "authors": "array",
                        "stakeholders": "array",
                        "background": "string",
                        "goals": "array",
                        "functional_requirements": "array",
                        "non_functional_requirements": "array",
                        "user_stories": "array",
                        "acceptance_criteria": "array",
                    },
                )
            ],
            approval=A(required=True, approver_role="总经理", approver_level="L2", timeout_hours=48),
        ),
        StageDefinition(
            id="P03",
            name="项目计划书",
            phase=StagePhase.PLANNING,
            order=3,
            timeout_days=3,
            owner_role="经理",
            owner_level="L3",
            owner_department="项目管理部",
            participants=[
                Participant(role="经理", level="L3", responsibility="制定项目计划"),
                Participant(role="各主管", level="L4", responsibility="提供部门资源估算"),
                Participant(role="各员工", level="L5", responsibility="提供任务时间估算"),
            ],
            deliverables=[
                Deliverable(
                    name="项目计划书",
                    type="document",
                    template="project_plan_template.md",
                    required=True,
                    schema_def={
                        "project_name": "string",
                        "project_id": "string",
                        "version": "string",
                        "creation_date": "date",
                        "project_manager": "string",
                        "executive_summary": "string",
                        "scope": "object",
                        "schedule": "object",
                        "resources": "object",
                        "budget": "object",
                        "risk_management": "object",
                        "communication_plan": "object",
                        "quality_plan": "object",
                    },
                )
            ],
            approval=A(required=True, approver_role="CEO", approver_level="L1", timeout_hours=72),
        ),
        StageDefinition(
            id="P04",
            name="立项审批",
            phase=StagePhase.APPROVAL,
            order=4,
            timeout_days=2,
            owner_role="CEO",
            owner_level="L1",
            owner_department="决策层",
            participants=[
                Participant(role="CEO", level="L1", responsibility="审批立项"),
                Participant(role="老板", level="L0", responsibility="最终审批（预算超限时）"),
            ],
            deliverables=[
                Deliverable(
                    name="立项决议",
                    type="document",
                    template="approval_decision_template.md",
                    required=True,
                    schema_def={
                        "decision": "string",
                        "approver": "string",
                        "date": "date",
                        "conditions": "array",
                        "notes": "string",
                    },
                )
            ],
            approval=A(
                required=True,
                approver_role="老板",
                approver_level="L0",
                condition="budget > 100000",
                default_approver_role="CEO",
                default_approver_level="L1",
                timeout_hours=48,
            ),
        ),
        StageDefinition(
            id="P05",
            name="技术方案",
            phase=StagePhase.DESIGN,
            order=5,
            timeout_days=7,
            owner_role="架构师/主管",
            owner_level="L4",
            owner_department="相关技术部门",
            participants=[
                Participant(role="架构师", level="L4", responsibility="设计整体技术架构"),
                Participant(role="各主管", level="L4", responsibility="设计子模块技术方案"),
                Participant(role="资深工程师", level="L5", responsibility="技术调研和验证"),
            ],
            deliverables=[
                Deliverable(
                    name="技术架构设计文档",
                    type="document",
                    template="tech_architecture_template.md",
                    required=True,
                    schema_def={
                        "overview": "string",
                        "architecture_diagram": "string",
                        "components": "array",
                        "data_flow": "object",
                        "interfaces": "array",
                        "security": "object",
                        "risk_analysis": "object",
                    },
                )
            ],
            approval=A(required=True, approver_role="总经理", approver_level="L2", timeout_hours=48),
        ),
        StageDefinition(
            id="P06",
            name="开发执行",
            phase=StagePhase.EXECUTION,
            order=6,
            timeout_days=7,
            owner_role="各员工",
            owner_level="L5",
            owner_department="各技术部门",
            participants=[
                Participant(role="员工", level="L5", responsibility="执行开发任务"),
                Participant(role="实习", level="L6", responsibility="辅助开发"),
                Participant(role="主管", level="L4", responsibility="任务分配和质量把控"),
                Participant(role="经理", level="L3", responsibility="进度跟踪"),
            ],
            deliverables=[
                Deliverable(name="代码", type="code", required=True, schema_def={"repo": "string", "branch": "string"}),
                Deliverable(
                    name="技术文档",
                    type="document",
                    required=True,
                    schema_def={"title": "string", "modules": "array", "decisions": "array"},
                ),
                Deliverable(
                    name="单元测试",
                    type="test",
                    required=True,
                    schema_def={"framework": "string", "coverage_report": "string"},
                ),
            ],
            approval=A(required=False, approver_role="无", approver_level="L0"),
        ),
        StageDefinition(
            id="P07",
            name="测试验收",
            phase=StagePhase.TESTING,
            order=7,
            timeout_days=5,
            owner_role="测试主管",
            owner_level="L4",
            owner_department="测试部",
            participants=[
                Participant(role="测试主管", level="L4", responsibility="组织测试，审核测试报告"),
                Participant(role="资深测试工程师", level="L5", responsibility="执行测试"),
                Participant(role="实习测试助理", level="L6", responsibility="辅助测试"),
            ],
            deliverables=[
                Deliverable(
                    name="测试报告",
                    type="document",
                    template="test_report_template.md",
                    required=True,
                    schema_def={
                        "summary": "string",
                        "test_scope": "array",
                        "results": "object",
                        "bugs": "array",
                        "risk": "object",
                    },
                )
            ],
            approval=A(required=True, approver_role="经理", approver_level="L3", timeout_hours=24),
        ),
        StageDefinition(
            id="P08",
            name="部署上线",
            phase=StagePhase.DEPLOYMENT,
            order=8,
            timeout_days=2,
            owner_role="运维主管",
            owner_level="L4",
            owner_department="运维部",
            participants=[
                Participant(role="运维主管", level="L4", responsibility="组织部署上线"),
                Participant(role="运维工程师", level="L5", responsibility="执行部署与巡检"),
                Participant(role="开发代表", level="L5", responsibility="协助验证与回滚支持"),
            ],
            deliverables=[
                Deliverable(
                    name="部署文档",
                    type="document",
                    template="deployment_guide_template.md",
                    required=True,
                    schema_def={"steps": "array", "rollback": "object", "checks": "array"},
                ),
                Deliverable(
                    name="上线确认单",
                    type="document",
                    template="deployment_confirmation_template.md",
                    required=True,
                    schema_def={
                        "approver": "string",
                        "window": "string",
                        "canary_check": "object",
                        "final_check": "object",
                    },
                ),
            ],
            approval=A(required=True, approver_role="总经理", approver_level="L2"),
        ),
        StageDefinition(
            id="P09",
            name="项目复盘",
            phase=StagePhase.REVIEW,
            order=9,
            timeout_days=3,
            owner_role="经理",
            owner_level="L3",
            owner_department="项目管理部",
            participants=[
                Participant(role="经理", level="L3", responsibility="组织复盘会议，输出复盘报告"),
                Participant(role="各主管", level="L4", responsibility="提供部门视角问题与改进项"),
                Participant(role="各员工", level="L5", responsibility="提供经验教训与行动项"),
            ],
            deliverables=[
                Deliverable(
                    name="复盘报告",
                    type="document",
                    template="retrospective_report_template.md",
                    required=True,
                    schema_def={
                        "milestones": "array",
                        "wins": "array",
                        "issues": "array",
                        "root_causes": "array",
                        "actions": "array",
                    },
                )
            ],
            approval=A(required=True, approver_role="CEO", approver_level="L1"),
        ),
    ]


class ProjectStageEngine:
    def __init__(self, store: JsonStore):
        self.store = store
        self.defs = {d.id: d for d in _stage_definitions()}
        self.ordered = sorted(self.defs.values(), key=lambda d: d.order)

    def ensure_project_stages(self, project_id: str) -> List[dict]:
        project = self.store.get_project(project_id)
        stages = project.get("stages")
        if isinstance(stages, list) and stages:
            # best-effort: re-evaluate condition approver when project budget changes
            budget = project.get("budget", 0)

            def _safe_int(value: object, default: int = 0) -> int:
                try:
                    return int(value)  # type: ignore[arg-type]
                except Exception:
                    return default

            def _eval_budget_condition(cond: str | None) -> bool:
                if not cond:
                    return True
                c = str(cond).strip().lower()
                if not c.startswith("budget"):
                    return True
                b = _safe_int(budget, 0)
                rest = c[len("budget") :].strip()
                for op in (">=", "<=", ">", "<"):
                    if rest.startswith(op):
                        raw = rest[len(op) :].strip()
                        th = _safe_int(raw, 0)
                        if op == ">=":
                            return b >= th
                        if op == "<=":
                            return b <= th
                        if op == ">":
                            return b > th
                        if op == "<":
                            return b < th
                return True

            changed = False
            patched: List[dict] = []
            for s in stages:
                row = dict(s)
                ap = dict(row.get("approval") or {})
                cond = ap.get("condition")
                if cond:
                    ok = _eval_budget_condition(str(cond))
                    if not ok:
                        default_role = str(ap.get("default_approver_role") or "").strip()
                        default_level = str(ap.get("default_approver_level") or "").strip()
                        if default_role and ap.get("approver_role") != default_role:
                            ap["approver_role"] = default_role
                            changed = True
                        if default_level and ap.get("approver_level") != default_level:
                            ap["approver_level"] = default_level
                            changed = True
                    # if condition becomes true, keep the original approver_role/level from definition (do not override)
                    # we only restore when we can map by stage id from definitions
                    if ok and str(row.get("id")) in self.defs:
                        d = self.defs[str(row.get("id"))]
                        if ap.get("approver_role") != d.approval.approver_role:
                            ap["approver_role"] = d.approval.approver_role
                            changed = True
                        if ap.get("approver_level") != d.approval.approver_level:
                            ap["approver_level"] = d.approval.approver_level
                            changed = True
                row["approval"] = ap
                patched.append(row)
            if changed:
                self.store.update_project(project_id, {"stages": patched})
                return patched
            return stages

        def _safe_int(value: object, default: int = 0) -> int:
            try:
                return int(value)  # type: ignore[arg-type]
            except Exception:
                return default

        def _eval_condition(cond: str | None) -> bool:
            if not cond:
                return True
            c = str(cond).strip().lower()
            # minimal parser: support "budget > N" / "budget >= N" / "<" / "<="
            if not c.startswith("budget"):
                return True
            budget = _safe_int(project.get("budget", 0), 0)
            rest = c[len("budget") :].strip()
            for op in (">=", "<=", ">", "<"):
                if rest.startswith(op):
                    raw = rest[len(op) :].strip()
                    th = _safe_int(raw, 0)
                    if op == ">=":
                        return budget >= th
                    if op == "<=":
                        return budget <= th
                    if op == ">":
                        return budget > th
                    if op == "<":
                        return budget < th
            return True

        stage_items: List[dict] = []
        for d in self.ordered:
            approval_dict = d.approval.model_dump(mode="json")
            # condition-based approver override (e.g. budget > 100000)
            if not _eval_condition(approval_dict.get("condition")):
                default_role = str(approval_dict.get("default_approver_role") or "").strip()
                default_level = str(approval_dict.get("default_approver_level") or "").strip()
                if default_role:
                    approval_dict["approver_role"] = default_role
                if default_level:
                    approval_dict["approver_level"] = default_level
            stage_items.append(
                {
                    "id": d.id,
                    "name": d.name,
                    "phase": d.phase.value,
                    "order": d.order,
                    "owner_role": d.owner_role,
                    "owner_level": d.owner_level,
                    "owner_department": d.owner_department,
                    "participants": [p.model_dump(mode="json") for p in d.participants],
                    "deliverables": [x.model_dump(mode="json", by_alias=True) for x in d.deliverables],
                    "approval": approval_dict,
                    "timeout_days": d.timeout_days,
                    "status": StageStatus.PENDING.value,
                    "project_id": project_id,
                    "start_date": None,
                    "end_date": None,
                    "actual_deliverables": [],
                    "comments": None,
                    "approval_history": [],
                }
            )

        self.store.update_project(project_id, {"stages": stage_items})
        return stage_items

    def _find_stage_index(self, stages: List[dict], stage_id: str) -> int:
        for i, s in enumerate(stages):
            if str(s.get("id")) == stage_id:
                return i
        raise ValueError(f"stage not found: {stage_id}")

    def list_stages(self, project_id: str) -> List[dict]:
        return self.ensure_project_stages(project_id)

    def get_stage(self, project_id: str, stage_id: str) -> dict:
        stages = self.ensure_project_stages(project_id)
        idx = self._find_stage_index(stages, stage_id)
        return stages[idx]

    def start_stage(self, project_id: str, stage_id: str) -> ProjectStage:
        stages = self.ensure_project_stages(project_id)
        idx = self._find_stage_index(stages, stage_id)
        stage = dict(stages[idx])
        if stage.get("status") != StageStatus.PENDING.value:
            raise ValueError("stage must be in pending state to start")

        # Order gating: only allow start when previous stage has finished (best-effort).
        if stage.get("order", 0) > 1:
            prev_order = int(stage["order"]) - 1
            prev = next((s for s in stages if int(s.get("order", 0)) == prev_order), None)
            if not prev or prev.get("status") not in {StageStatus.COMPLETED.value, StageStatus.APPROVED.value}:
                raise ValueError("previous stage not completed/approved")

        stage["status"] = StageStatus.IN_PROGRESS.value
        stage["start_date"] = _utc_now().isoformat()
        stages[idx] = stage
        self.store.update_project(project_id, {"stages": stages})
        return ProjectStage.model_validate(stage)

    def complete_stage(
        self, project_id: str, stage_id: str, deliverables: List[Deliverable], comments: Optional[str] = None
    ) -> ProjectStage:
        stages = self.ensure_project_stages(project_id)
        idx = self._find_stage_index(stages, stage_id)
        stage = dict(stages[idx])

        if stage.get("status") != StageStatus.IN_PROGRESS.value:
            raise ValueError("stage must be in_progress state to complete")

        required_names = {d.name for d in (Deliverable.model_validate(x) for x in stage.get("deliverables") or []) if d.required}
        provided_names = {d.name for d in deliverables}
        missing = sorted(required_names - provided_names)
        if missing:
            raise ValueError(f"missing required deliverables: {missing}")

        approval_required = bool((stage.get("approval") or {}).get("required", True))
        stage["status"] = StageStatus.REVIEW.value if approval_required else StageStatus.COMPLETED.value
        stage["end_date"] = _utc_now().isoformat()
        stage["comments"] = comments
        stage["actual_deliverables"] = [d.model_dump(mode="json", by_alias=True) for d in deliverables]
        stages[idx] = stage

        # Auto start next stage only when approval is not required.
        if not approval_required:
            stage_order = int(stage.get("order", 0))
            next_stage = next((s for s in stages if int(s.get("order", 0)) == stage_order + 1), None)
            if next_stage and next_stage.get("status") == StageStatus.PENDING.value:
                nidx = self._find_stage_index(stages, str(next_stage.get("id")))
                stages[nidx]["status"] = StageStatus.IN_PROGRESS.value
                stages[nidx]["start_date"] = _utc_now().isoformat()

        self.store.update_project(project_id, {"stages": stages})
        return ProjectStage.model_validate(stage)

    def approve_stage(
        self,
        project_id: str,
        stage_id: str,
        approved: bool,
        comments: Optional[str] = None,
        *,
        approver_role: str | None = None,
        approver_level: str | None = None,
    ) -> ProjectStage:
        stages = self.ensure_project_stages(project_id)
        idx = self._find_stage_index(stages, stage_id)
        stage = dict(stages[idx])

        if stage.get("status") not in {StageStatus.REVIEW.value, StageStatus.COMPLETED.value, StageStatus.IN_PROGRESS.value}:
            raise ValueError("stage must be review/completed or in_progress to approve")

        stage["status"] = StageStatus.APPROVED.value if approved else StageStatus.REJECTED.value
        stage["end_date"] = stage.get("end_date") or _utc_now().isoformat()
        stage["comments"] = comments
        history = list(stage.get("approval_history") or [])
        history.append(
            {
                "timestamp": _utc_now().isoformat(),
                "approved": bool(approved),
                "approver_role": approver_role,
                "approver_level": approver_level,
                "comments": comments,
            }
        )
        stage["approval_history"] = history[-50:]
        stages[idx] = stage

        # Auto start next stage when approved OR when approval not required and stage is completed.
        if approved:
            stage_order = int(stage.get("order", 0))
            next_stage = next((s for s in stages if int(s.get("order", 0)) == stage_order + 1), None)
            if next_stage and next_stage.get("status") == StageStatus.PENDING.value:
                nidx = self._find_stage_index(stages, str(next_stage.get("id")))
                stages[nidx]["status"] = StageStatus.IN_PROGRESS.value
                stages[nidx]["start_date"] = _utc_now().isoformat()

        self.store.update_project(project_id, {"stages": stages})
        return ProjectStage.model_validate(stage)

    def list_stage_deliverables(self, project_id: str, stage_id: str) -> List[Deliverable]:
        stage = self.get_stage(project_id, stage_id)
        raw = stage.get("actual_deliverables") or []
        return [Deliverable.model_validate(x) for x in raw]

