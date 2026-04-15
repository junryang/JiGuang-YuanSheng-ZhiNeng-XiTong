from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.ceo_router import router as ceo_router
from app.api.collab_router import router as collab_router
from app.api.marketing_router import router as marketing_router
from app.api.memory_router import router as memory_router
from app.api.routes import router
from app.api.skills_router import router as skills_router
from app.api.tasks_router import router as tasks_router
from app.core.audit import AuditStore
from app.core.deps import set_audit_store, set_json_store, set_policy_engine
from app.core.policy_engine import PolicyEngine
from app.core.store import JsonStore


def create_app() -> FastAPI:
    app = FastAPI(title="JYIS Backend", version="0.1.0")

    policy_path = Path(__file__).resolve().parents[2] / "docs" / "ceo_policy.engine.yaml"
    engine = PolicyEngine(policy_path=policy_path)
    set_policy_engine(engine)
    set_audit_store(AuditStore())
    store = JsonStore(path=Path(__file__).resolve().parents[1] / "data" / "state.json")
    store.seed_if_empty()
    set_json_store(store)

    app.state.runtime_mode = "normal"

    app.include_router(router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(tasks_router, prefix="/api/v1")
    app.include_router(ceo_router, prefix="/api/v1")
    app.include_router(skills_router, prefix="/api/v1")
    app.include_router(collab_router, prefix="/api/v1")
    app.include_router(memory_router, prefix="/api/v1")
    app.include_router(marketing_router, prefix="/api/v1")

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "runtime_mode": app.state.runtime_mode, "policy_engine": engine.health()}

    web_dir = Path(__file__).resolve().parents[1] / "web"
    if web_dir.is_dir():
        app.mount("/ui", StaticFiles(directory=str(web_dir), html=True), name="ui")

    return app


app = create_app()
