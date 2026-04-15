from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _scripts_dir() -> Path:
    return Path(__file__).resolve().parent


def _run_step(name: str, args: list[str]) -> int:
    print(f"\n=== {name} ===")
    print(" ".join(args))
    result = subprocess.run(args, check=False)
    print(f"{name} exit_code={result.returncode}")
    return int(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run daily local maintenance for state.json.")
    parser.add_argument("--label", type=str, default="daily", help="Backup label")
    parser.add_argument("--max-backup-age-hours", type=int, default=24, help="Health check max backup age")
    parser.add_argument("--keep-last", type=int, default=30, help="Keep newest N backups")
    parser.add_argument("--keep-days", type=int, default=14, help="Keep backups newer than N days")
    parser.add_argument("--prune-dry-run", action="store_true", help="Run prune in dry-run mode")
    args = parser.parse_args()

    py = sys.executable
    scripts = _scripts_dir()

    health_cmd = [
        py,
        str(scripts / "check_state_health.py"),
        "--max-backup-age-hours",
        str(max(1, int(args.max_backup_age_hours))),
    ]
    backup_cmd = [py, str(scripts / "backup_state.py"), "--label", args.label]
    prune_cmd = [
        py,
        str(scripts / "prune_backups.py"),
        "--keep-last",
        str(max(0, int(args.keep_last))),
        "--keep-days",
        str(max(0, int(args.keep_days))),
    ]
    if args.prune_dry_run:
        prune_cmd.append("--dry-run")

    health_code = _run_step("health-check", health_cmd)
    backup_code = _run_step("backup", backup_cmd)
    prune_code = _run_step("prune", prune_cmd)

    if backup_code != 0:
        return backup_code
    if prune_code != 0:
        return prune_code
    return 0 if health_code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
