from __future__ import annotations

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.core.deps import get_current_user, get_json_store, require_admin
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.core.store import JsonStore

router = APIRouter(tags=["auth"])


class RegisterRequest(BaseModel):
    email: str = Field(..., min_length=3, max_length=120)
    password: str = Field(..., min_length=6)
    roles: List[str] = Field(default_factory=lambda: ["user"])

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        s = v.strip().lower()
        if "@" not in s:
            raise ValueError("invalid email")
        return s


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    id: str
    email: str
    roles: List[str]


def _issue_tokens(user: dict) -> TokenResponse:
    email = str(user["email"])
    roles = list(user.get("roles", []))
    return TokenResponse(
        access_token=create_access_token(subject=email, roles=roles),
        refresh_token=create_refresh_token(subject=email, roles=roles),
    )


@router.post("/auth/register", response_model=UserPublic)
def register(payload: RegisterRequest, store: JsonStore = Depends(get_json_store)):
    try:
        user = store.create_user(
            email=str(payload.email),
            password_hash=hash_password(payload.password),
            roles=payload.roles or ["user"],
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return UserPublic(id=user["id"], email=user["email"], roles=user["roles"])


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, store: JsonStore = Depends(get_json_store)):
    try:
        user = store.get_user_by_email(str(payload.email))
    except KeyError:
        raise HTTPException(status_code=401, detail="invalid credentials")
    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="invalid credentials")
    return _issue_tokens(user)


@router.post("/auth/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, store: JsonStore = Depends(get_json_store)):
    try:
        data = decode_token(payload.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="invalid refresh token")
    if data.get("typ") != "refresh":
        raise HTTPException(status_code=401, detail="invalid token type")
    email = str(data.get("sub", ""))
    try:
        user = store.get_user_by_email(email)
    except KeyError:
        raise HTTPException(status_code=401, detail="user no longer valid")
    return _issue_tokens(user)


@router.post("/auth/logout")
def logout():
    return {"status": "ok", "hint": "客户端丢弃令牌即可；服务端为无状态 JWT。"}


@router.get("/auth/me", response_model=UserPublic)
def me(user: Annotated[dict, Depends(get_current_user)]):
    return UserPublic(id=user["id"], email=user["email"], roles=user["roles"])


@router.get("/authz/admin-summary")
def admin_summary(_: Annotated[dict, Depends(require_admin)]):
    return {"scope": "admin", "message": "RBAC 示例：仅 admin 角色可访问"}


@router.get("/authz/ping")
def authz_ping(user: Annotated[dict, Depends(get_current_user)]):
    return {"authenticated": True, "email": user["email"]}
