from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def _default_state_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "state.json"


def _default_backup_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "backups"


def main() -> int:
    parser = argparse.ArgumentParser(description="Backup backend/data/state.json with timestamp.")
    parser.add_argument("--state", type=Path, default=_default_state_path(), help="Path to source state.json")
    parser.add_argument("--out-dir", type=Path, default=_default_backup_dir(), help="Directory for backup files")
    parser.add_argument("--label", type=str, default="", help="Optional label suffix (letters/digits/_/-)")
    args = parser.parse_args()

    state_path = args.state
    if not state_path.exists():
        raise FileNotFoundError(f"state file not found: {state_path}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_label = "".join(ch for ch in args.label.strip() if ch.isalnum() or ch in ("_", "-"))
    name = f"state-{ts}.json" if not safe_label else f"state-{ts}-{safe_label}.json"
    dest = args.out_dir / name

    shutil.copy2(state_path, dest)
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
