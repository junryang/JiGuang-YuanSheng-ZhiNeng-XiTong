from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path


def _default_state_path() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "state.json"


def _default_backup_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "backups"


def _pick_latest_backup(backup_dir: Path) -> Path:
    items = sorted((p for p in backup_dir.glob("state-*.json") if p.is_file()), key=lambda p: p.stat().st_mtime)
    if not items:
        raise FileNotFoundError(f"no backup files found in: {backup_dir}")
    return items[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Restore backend/data/state.json from backup file.")
    parser.add_argument("--state", type=Path, default=_default_state_path(), help="Path to destination state.json")
    parser.add_argument("--backup", type=Path, default=None, help="Backup file path; if omitted uses latest in --backup-dir")
    parser.add_argument("--backup-dir", type=Path, default=_default_backup_dir(), help="Directory containing backup files")
    parser.add_argument(
        "--preserve-current",
        action="store_true",
        help="Preserve current state.json to backups before restoring",
    )
    args = parser.parse_args()

    state_path = args.state
    state_path.parent.mkdir(parents=True, exist_ok=True)
    args.backup_dir.mkdir(parents=True, exist_ok=True)

    backup_file = args.backup if args.backup else _pick_latest_backup(args.backup_dir)
    if not backup_file.exists():
        raise FileNotFoundError(f"backup file not found: {backup_file}")

    if args.preserve_current and state_path.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        preserve_path = args.backup_dir / f"state-{ts}-pre-restore.json"
        shutil.copy2(state_path, preserve_path)
        print(f"preserved current state to: {preserve_path}")

    shutil.copy2(backup_file, state_path)
    print(f"restored from: {backup_file}")
    print(f"state path: {state_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
