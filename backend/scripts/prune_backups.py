from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from pathlib import Path


def _default_backup_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "backups"


def _collect_backups(backup_dir: Path) -> list[Path]:
    return sorted(
        (p for p in backup_dir.glob("state-*.json") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune old state.json backups by retention rules.")
    parser.add_argument("--backup-dir", type=Path, default=_default_backup_dir(), help="Directory containing backup files")
    parser.add_argument("--keep-last", type=int, default=30, help="Always keep newest N backups")
    parser.add_argument("--keep-days", type=int, default=14, help="Keep backups newer than N days")
    parser.add_argument("--dry-run", action="store_true", help="Print files to delete without deleting")
    args = parser.parse_args()

    if not args.backup_dir.exists():
        print(f"backup dir not found: {args.backup_dir}")
        return 0

    backups = _collect_backups(args.backup_dir)
    if not backups:
        print(f"no backups found in: {args.backup_dir}")
        return 0

    keep_last = max(0, int(args.keep_last))
    keep_days = max(0, int(args.keep_days))
    threshold = datetime.now() - timedelta(days=keep_days)

    to_delete: list[Path] = []
    for idx, path in enumerate(backups):
        if idx < keep_last:
            continue
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        if mtime < threshold:
            to_delete.append(path)

    print(f"backup dir: {args.backup_dir}")
    print(f"total backups: {len(backups)}")
    print(f"delete candidates: {len(to_delete)}")
    if not to_delete:
        return 0

    for p in to_delete:
        print(p.name)
        if not args.dry_run:
            p.unlink(missing_ok=True)

    if args.dry_run:
        print("dry-run mode, no files deleted.")
    else:
        print("prune complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
