from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


@dataclass
class CheckResult:
    name: str
    ok: bool
    command: str
    exit_code: int
    output: str


def _repo_root() -> Path:
    return ROOT


def _reports_dir() -> Path:
    return _repo_root() / "reports"


def _run_command(name: str, cmd: list[str], cwd: Path) -> CheckResult:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return CheckResult(
        name=name,
        ok=proc.returncode == 0,
        command=" ".join(cmd),
        exit_code=int(proc.returncode),
        output=output.strip(),
    )


def _http_health_check() -> CheckResult:
    with TestClient(app) as client:
        resp = client.get("/healthz")
    ok = resp.status_code == 200
    body = resp.text
    return CheckResult(
        name="healthz",
        ok=ok,
        command="GET /healthz",
        exit_code=0 if ok else 1,
        output=body[:4000],
    )


def _http_audit_summary_check() -> CheckResult:
    with TestClient(app) as client:
        resp = client.get("/api/v1/audit/summary")
    ok = resp.status_code == 200
    body = resp.text
    return CheckResult(
        name="audit_summary",
        ok=ok,
        command="GET /api/v1/audit/summary",
        exit_code=0 if ok else 1,
        output=body[:4000],
    )


def _build_report(checks: list[CheckResult], started_at: datetime, finished_at: datetime) -> dict[str, Any]:
    failures = [c.name for c in checks if not c.ok]
    return {
        "title": "Day4 Gate Runner Report",
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_seconds": round((finished_at - started_at).total_seconds(), 2),
        "checks_total": len(checks),
        "checks_passed": len(checks) - len(failures),
        "checks_failed": len(failures),
        "go_no_go": "Go" if not failures else "No-Go",
        "failed_checks": failures,
        "checks": [asdict(c) for c in checks],
    }


def _to_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Day4 Gate Runner Report")
    lines.append("")
    lines.append(f"- 开始时间: `{report['started_at']}`")
    lines.append(f"- 结束时间: `{report['finished_at']}`")
    lines.append(f"- 耗时: `{report['duration_seconds']}s`")
    lines.append(f"- 结论: **{report['go_no_go']}**")
    lines.append("")
    lines.append("## 检查结果")
    lines.append("")
    lines.append("| 检查项 | 结果 | 退出码 |")
    lines.append("|---|---|---|")
    for c in report["checks"]:
        mark = "通过" if c["ok"] else "失败"
        lines.append(f"| {c['name']} | {mark} | {c['exit_code']} |")
    lines.append("")
    lines.append("## 详情")
    lines.append("")
    for c in report["checks"]:
        lines.append(f"### {c['name']}")
        lines.append("")
        lines.append(f"- 命令: `{c['command']}`")
        lines.append(f"- 结果: `{'PASS' if c['ok'] else 'FAIL'}`")
        lines.append("")
        lines.append("```text")
        lines.append((c["output"] or "").strip() or "(empty output)")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Day4 gate checks (tests + day3_gate + health + audit summary)."
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip pytest checks and run only HTTP checks.",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=_reports_dir(),
        help="Directory to write report files.",
    )
    args = parser.parse_args()

    started_at = datetime.now()
    checks: list[CheckResult] = []
    root = _repo_root()
    py = sys.executable

    if not args.skip_tests:
        checks.append(
            _run_command(
                "pytest_all",
                [py, "-m", "pytest", "tests/", "-q", "--tb=short"],
                cwd=root,
            )
        )
        checks.append(
            _run_command(
                "pytest_day3_gate",
                [py, "-m", "pytest", "-m", "day3_gate", "-q", "--tb=short"],
                cwd=root,
            )
        )

    checks.append(_http_health_check())
    checks.append(_http_audit_summary_check())
    finished_at = datetime.now()

    report = _build_report(checks, started_at=started_at, finished_at=finished_at)
    ts = finished_at.strftime("%Y%m%d-%H%M%S")
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.reports_dir / f"day4-gate-report-{ts}.json"
    md_path = args.reports_dir / f"day4-gate-report-{ts}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(_to_markdown(report), encoding="utf-8")

    print(f"Go/No-Go: {report['go_no_go']}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    return 0 if report["go_no_go"] == "Go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
