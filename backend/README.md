# Backend Day1 Snapshot

## What is implemented

- FastAPI app entry: `app/main.py`
- Core routes:
  - `GET /healthz`
  - `GET /api/v1/agents`
  - `GET /api/v1/projects`
  - `POST /api/v1/chat/sessions`
  - `GET /api/v1/chat/sessions`
  - `GET /api/v1/chat/sessions/{session_id}/messages`
  - `POST /api/v1/chat/sessions/{session_id}/messages`
  - `POST /api/v1/policy/evaluate`
  - `POST /api/v1/runtime/mode`
  - `GET /api/v1/runtime/mode`
  - `GET /api/v1/audit/events`
  - `POST /api/v1/contents/publish` (high-risk gate demo)
- Policy engine:
  - Loads `docs/ceo_policy.engine.yaml`
  - Evaluates deny rules for `CEO-POLICY-09~14` baseline conditions
  - Exposes `policy_version` in decision payloads
  - Exposes `error_code` for standardized deny reason handling
- Audit:
  - Stores decision trail with `policy_id / policy_version / environment / reason / endpoint`
- Persistence:
  - Minimal JSON state store under `app/data/state.json` for agents/projects/chat sessions
- Tests:
  - `tests/test_policy_engine.py`
  - `tests/test_api_smoke.py`

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir .
pytest tests -q
```
