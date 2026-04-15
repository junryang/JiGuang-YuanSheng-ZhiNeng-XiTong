from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.audit import AuditStore
from app.core.policy_engine import PolicyEngine
from app.core.security import decode_token
from app.core.store import JsonStore


_policy_engine: PolicyEngine | None = None
_audit_store: AuditStore | None = None
_json_store: JsonStore | None = None


def set_policy_engine(engine: PolicyEngine) -> None:
    global _policy_engine
    _policy_engine = engine


def set_audit_store(audit_store: AuditStore) -> None:
    global _audit_store
    _audit_store = audit_store


def set_json_store(store: JsonStore) -> None:
    global _json_store
    _json_store = store


def get_policy_engine() -> PolicyEngine:
    if _policy_engine is None:
        raise RuntimeError("Policy engine is not initialized")
    return _policy_engine


def get_audit_store() -> AuditStore:
    if _audit_store is None:
        raise RuntimeError("Audit store is not initialized")
    return _audit_store


def get_json_store() -> JsonStore:
    if _json_store is None:
        raise RuntimeError("Json store is not initialized")
    return _json_store


_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    store: JsonStore = Depends(get_json_store),
) -> dict:
    if creds is None or creds.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="not authenticated")
    try:
        payload = decode_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    if payload.get("typ") != "access":
        raise HTTPException(status_code=401, detail="invalid token type")
    email = str(payload.get("sub", ""))
    try:
        return store.get_user_by_email(email)
    except KeyError as e:
        raise HTTPException(status_code=401, detail="user not found") from e


def require_admin(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if "admin" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="admin role required")
    return user
