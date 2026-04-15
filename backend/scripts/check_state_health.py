from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def _default_state_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "state.json"


def _default_backup_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "backups"


def _fmt_time(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def _load_json(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ValueError("state file is empty")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("state root must be object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local state.json and backup health.")
    parser.add_argument("--state", type=Path, default=_default_state_path(), help="Path to state.json")
    parser.add_argument("--backup-dir", type=Path, default=_default_backup_dir(), help="Path to backup directory")
    parser.add_argument(
        "--max-backup-age-hours",
        type=int,
        default=24,
        help="Warn if newest backup is older than this many hours",
    )
    args = parser.parse_args()

    ok = True
    state_path = args.state
    backup_dir = args.backup_dir

    print(f"state path: {state_path}")
    if not state_path.exists():
        print("ERROR: state.json not found")
        return 2

    try:
        data = _load_json(state_path)
        print("OK: state.json is valid JSON object")
        for key in ("projects", "agents", "tasks", "skills"):
            if key not in data:
                print(f"WARN: missing key `{key}`")
                ok = False
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: failed to parse state.json: {exc}")
        return 2

    print(f"backup dir: {backup_dir}")
    if not backup_dir.exists():
        print("WARN: backup directory not found")
        return 1

    files = sorted(
        (p for p in backup_dir.glob("state-*.json") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not files:
        print("WARN: no backup files found")
        return 1

    newest = files[0]
    newest_mtime = datetime.fromtimestamp(newest.stat().st_mtime)
    age = datetime.now() - newest_mtime
    print(f"OK: backups found = {len(files)}")
    print(f"newest backup: {newest.name} ({_fmt_time(newest.stat().st_mtime)})")

    max_age = timedelta(hours=max(1, int(args.max_backup_age_hours)))
    if age > max_age:
        print(f"WARN: newest backup is older than {args.max_backup_age_hours} hours")
        ok = False

    if ok:
        print("HEALTH: GOOD")
        return 0
    print("HEALTH: WARN")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
