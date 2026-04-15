from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def _default_backup_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "data" / "backups"


def _fmt_mtime(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")


def main() -> int:
    parser = argparse.ArgumentParser(description="List available state.json backup files.")
    parser.add_argument("--backup-dir", type=Path, default=_default_backup_dir(), help="Directory containing backup files")
    parser.add_argument("--limit", type=int, default=20, help="Max rows to print (newest first)")
    args = parser.parse_args()

    if not args.backup_dir.exists():
        print(f"backup dir not found: {args.backup_dir}")
        return 0

    files = sorted(
        (p for p in args.backup_dir.glob("state-*.json") if p.is_file()),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not files:
        print(f"no backups found in: {args.backup_dir}")
        return 0

    limit = max(1, int(args.limit))
    print(f"backup dir: {args.backup_dir}")
    print(f"showing: {min(limit, len(files))}/{len(files)}")
    print("-" * 88)
    print(f"{'mtime':19}  {'size':>10}  file")
    print("-" * 88)
    for p in files[:limit]:
        st = p.stat()
        print(f"{_fmt_mtime(st.st_mtime)}  {st.st_size:10d}  {p.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
