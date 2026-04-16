from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from threading import Thread
from queue import Queue, Empty
from typing import Any


@dataclass
class StepResult:
    name: str
    command: str
    ok: bool
    exit_code: int
    output: str
    duration_seconds: float
    retries: int = 0


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _docs_dir() -> Path:
    return _repo_root().parent / "docs"


def _reports_dir() -> Path:
    return _repo_root() / "reports"


def _stream_reader(stream, source: str, q: Queue) -> None:
    try:
        for line in iter(stream.readline, ""):
            q.put((source, line))
    finally:
        stream.close()


def _run(name: str, cmd: list[str], cwd: Path, *, live_log_fp=None, live_echo: bool = False) -> StepResult:
    started_at = datetime.now()
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    q: Queue = Queue()
    t_out = Thread(target=_stream_reader, args=(proc.stdout, "stdout", q), daemon=True)
    t_err = Thread(target=_stream_reader, args=(proc.stderr, "stderr", q), daemon=True)
    t_out.start()
    t_err.start()

    collected: list[str] = []
    while t_out.is_alive() or t_err.is_alive() or not q.empty():
        try:
            source, line = q.get(timeout=0.1)
        except Empty:
            continue
        row = f"[{source}] {line.rstrip()}"
        collected.append(row)
        if live_log_fp is not None:
            live_log_fp.write(row + "\n")
            live_log_fp.flush()
        if live_echo:
            print(row)

    exit_code = int(proc.wait())
    duration_seconds = round((datetime.now() - started_at).total_seconds(), 3)
    text = "\n".join(collected).strip()
    return StepResult(
        name=name,
        command=" ".join(cmd),
        ok=exit_code == 0,
        exit_code=exit_code,
        output=text.strip(),
        duration_seconds=duration_seconds,
        retries=0,
    )


def _run_with_retry(
    name: str,
    cmd: list[str],
    cwd: Path,
    *,
    max_retries: int,
    retry_delay_seconds: float,
    retry_enabled: bool,
    live_log_fp=None,
    live_echo: bool = False,
) -> StepResult:
    if not retry_enabled:
        return _run(name, cmd, cwd=cwd, live_log_fp=live_log_fp, live_echo=live_echo)
    attempt = 0
    last: StepResult | None = None
    while attempt <= max_retries:
        if live_log_fp is not None:
            live_log_fp.write(f"[attempt-start] {name} attempt={attempt + 1}/{max_retries + 1}\n")
            live_log_fp.flush()
        res = _run(name, cmd, cwd=cwd, live_log_fp=live_log_fp, live_echo=live_echo)
        if res.ok:
            res.retries = attempt
            return res
        last = res
        if attempt < max_retries:
            delay = retry_delay_seconds * (2**attempt)
            if live_log_fp is not None:
                live_log_fp.write(f"[attempt-retry] {name} attempt={attempt + 1} failed; sleep={delay}s\n")
                live_log_fp.flush()
            if live_echo:
                print(f"[retry] {name} attempt={attempt + 1} failed, retry in {delay}s")
            import time

            time.sleep(delay)
        attempt += 1
    assert last is not None
    last.retries = max_retries
    return last


def _to_md(report: dict[str, Any]) -> str:
    lines = [
        "# Day5 Final Precheck Runner Report",
        "",
        f"- started_at: `{report['started_at']}`",
        f"- finished_at: `{report['finished_at']}`",
        f"- decision: **{report['decision']}**",
        "",
        "## Retry Policy",
        "",
        f"- max_retries: `{report.get('retry_policy', {}).get('max_retries', 0)}`",
        f"- retry_delay_seconds: `{report.get('retry_policy', {}).get('retry_delay_seconds', 0)}`",
        f"- whitelist: `{', '.join(report.get('retry_policy', {}).get('whitelist', []))}`",
        "",
        "## Steps",
        "",
        "| step | result | exit_code | duration_seconds | retries |",
        "|---|---|---:|---:|---:|",
    ]
    for s in report["steps"]:
        lines.append(
            f"| {s['name']} | {'PASS' if s['ok'] else 'FAIL'} | {s['exit_code']} | "
            f"{s.get('duration_seconds', 0)} | {s.get('retries', 0)} |"
        )
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    for s in report["steps"]:
        lines.append(f"### {s['name']}")
        lines.append("")
        lines.append(f"- command: `{s['command']}`")
        lines.append("```text")
        lines.append(s["output"] or "(empty)")
        lines.append("```")
        lines.append("")
    return "\n".join(lines)


def _checkpoint_text(step_name: str, res: StepResult, *, index: int, total: int, ts: datetime) -> str:
    status = "通过" if res.ok else "失败"
    return (
        f"【Day5预检进展】[{index}/{total}] {step_name} {status}；"
        f"exit_code={res.exit_code}；时间={ts.strftime('%Y-%m-%d %H:%M:%S')}"
    )


def _checkpoint_message(step_name: str, res: StepResult, *, index: int, total: int, ts: datetime, style: str) -> str:
    ok = bool(res.ok)
    icon = "🟢" if ok else "🔴"
    status_cn = "通过" if ok else "失败"
    time_str = ts.strftime("%Y-%m-%d %H:%M:%S")
    if style == "wechat":
        return (
            f"{icon}【Day5预检播报】\n"
            f"步骤：[{index}/{total}] {step_name}\n"
            f"结果：{status_cn}（exit_code={res.exit_code}）\n"
            f"时间：{time_str}"
        )
    # feishu default
    return (
        f"{icon} **Day5预检播报**\n"
        f"- 步骤：`[{index}/{total}] {step_name}`\n"
        f"- 结果：**{status_cn}**（`exit_code={res.exit_code}`）\n"
        f"- 时间：`{time_str}`"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Day5 final precheck in one shot and emit archive report.")
    parser.add_argument("--date", default=datetime.now().strftime("%Y%m%d"), help="Date tag, e.g. 20260417")
    parser.add_argument("--release-tag", required=True, help="Release tag, e.g. release-20260417-r1")
    parser.add_argument("--backend-digest", required=True, help="Backend image digest")
    parser.add_argument("--frontend-checksum", required=True, help="Frontend package checksum")
    parser.add_argument(
        "--duty-schedule",
        type=Path,
        default=_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_20260417_auto_filled.md",
        help="Duty schedule path to validate/use",
    )
    parser.add_argument("--docs-dir", type=Path, default=_docs_dir(), help="Docs output directory")
    parser.add_argument("--reports-dir", type=Path, default=_reports_dir(), help="Reports output directory")
    parser.add_argument("--live-log", action="store_true", help="Write step-by-step live timeline log.")
    parser.add_argument("--live-echo", action="store_true", help="Echo live step output to console.")
    parser.add_argument("--max-retries", type=int, default=1, help="Max retries per step when failed.")
    parser.add_argument(
        "--retry-delay-seconds",
        type=float,
        default=1.0,
        help="Base delay seconds before retry; exponential backoff is applied.",
    )
    parser.add_argument(
        "--retry-whitelist",
        default="day4_gate_runner,day5_release_prep,day5_management_summary",
        help="Comma-separated step names allowed for auto-retry.",
    )
    parser.add_argument("--checkpoint", action="store_true", help="Emit checkpoint broadcast lines after each step.")
    parser.add_argument(
        "--checkpoint-style",
        choices=["wechat", "feishu"],
        default="wechat",
        help="Checkpoint message style for broadcast copy.",
    )
    parser.add_argument(
        "--live-log-path",
        type=Path,
        default=None,
        help="Optional path for live timeline log file.",
    )
    args = parser.parse_args()

    py = sys.executable
    root = _repo_root()
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    args.docs_dir.mkdir(parents=True, exist_ok=True)

    started_at = datetime.now()
    ts_start = started_at.strftime("%Y%m%d-%H%M%S")
    live_log_path = args.live_log_path or (args.reports_dir / f"day5-final-precheck-live-{ts_start}.log")
    checkpoint_path = args.reports_dir / f"day5-final-precheck-checkpoints-{ts_start}.md"
    live_log_fp = None
    checkpoint_lines: list[str] = []
    if args.live_log:
        live_log_fp = live_log_path.open("w", encoding="utf-8")
        live_log_fp.write(f"[meta] started_at={started_at.isoformat()}\n")
        live_log_fp.flush()

    steps: list[StepResult] = []
    retry_whitelist = {x.strip() for x in args.retry_whitelist.split(",") if x.strip()}
    commands: list[tuple[str, list[str]]] = [
        ("pytest_day3_gate", [py, "-m", "pytest", "-m", "day3_gate", "-q", "--tb=short"]),
        ("day4_gate_runner", [py, "scripts/day4_gate_runner.py", "--reports-dir", str(args.reports_dir)]),
        (
            "day5_artifact_lock",
            [
                py,
                "scripts/day5_artifact_lock.py",
                "--release-tag",
                args.release_tag,
                "--backend-digest",
                args.backend_digest,
                "--frontend-checksum",
                args.frontend_checksum,
                "--output-dir",
                str(args.reports_dir),
            ],
        ),
        (
            "day5_release_prep",
            [
                py,
                "scripts/day5_release_prep.py",
                "--reports-dir",
                str(args.reports_dir),
                "--output-dir",
                str(args.docs_dir),
                "--duty-schedule",
                str(args.duty_schedule),
                "--emit-duty-todo",
            ],
        ),
        (
            "day5_release_finalize",
            [
                py,
                "scripts/day5_release_finalize.py",
                "--date",
                args.date,
                "--docs-dir",
                str(args.docs_dir),
                "--reports-dir",
                str(args.reports_dir),
                "--duty-schedule",
                str(args.duty_schedule),
            ],
        ),
    ]

    total = len(commands)
    for idx, (name, cmd) in enumerate(commands, start=1):
        if live_log_fp is not None:
            live_log_fp.write(f"[step-start] {name} :: {' '.join(cmd)}\n")
            live_log_fp.flush()
        res = _run_with_retry(
            name,
            cmd,
            cwd=root,
            max_retries=max(0, args.max_retries),
            retry_delay_seconds=max(0.1, args.retry_delay_seconds),
            retry_enabled=name in retry_whitelist,
            live_log_fp=live_log_fp,
            live_echo=args.live_echo,
        )
        steps.append(res)
        if live_log_fp is not None:
            live_log_fp.write(f"[step-end] {name} :: exit_code={res.exit_code}\n")
            live_log_fp.flush()
        if args.checkpoint:
            cp = _checkpoint_text(name, res, index=idx, total=total, ts=datetime.now())
            checkpoint_lines.append(cp)
            print(f"checkpoint: {cp}")
            rich = _checkpoint_message(
                name,
                res,
                index=idx,
                total=total,
                ts=datetime.now(),
                style=args.checkpoint_style,
            )
            checkpoint_lines.append(f"[{args.checkpoint_style}] {rich}")
            if live_log_fp is not None:
                live_log_fp.write(f"[checkpoint] {cp}\n")
                live_log_fp.write(f"[checkpoint-{args.checkpoint_style}] {rich}\n")
                live_log_fp.flush()
        if not res.ok:
            break

    finished_at = datetime.now()
    decision = "Go" if all(s.ok for s in steps) and len(steps) == len(commands) else "No-Go"
    ts = finished_at.strftime("%Y%m%d-%H%M%S")
    out_json = args.reports_dir / f"day5-final-precheck-runner-{ts}.json"
    out_md = args.reports_dir / f"day5-final-precheck-runner-{ts}.md"
    report = {
        "title": "Day5 Final Precheck Runner Report",
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "decision": decision,
        "retry_policy": {
            "max_retries": max(0, args.max_retries),
            "retry_delay_seconds": max(0.1, args.retry_delay_seconds),
            "whitelist": sorted(retry_whitelist),
        },
        "steps": [asdict(s) for s in steps],
    }
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_to_md(report), encoding="utf-8")

    mgmt_cmd = [
        py,
        "scripts/day5_management_summary.py",
        "--date",
        args.date,
        "--reports-dir",
        str(args.reports_dir),
        "--docs-dir",
        str(args.docs_dir),
        "--final-precheck-report",
        str(out_json),
    ]
    mgmt_res = _run_with_retry(
        "day5_management_summary",
        mgmt_cmd,
        cwd=root,
        max_retries=max(0, args.max_retries),
        retry_delay_seconds=max(0.1, args.retry_delay_seconds),
        retry_enabled="day5_management_summary" in retry_whitelist,
        live_log_fp=live_log_fp,
        live_echo=args.live_echo,
    )
    steps.append(mgmt_res)
    if args.checkpoint:
        cp = _checkpoint_text("day5_management_summary", mgmt_res, index=total + 1, total=total + 1, ts=datetime.now())
        checkpoint_lines.append(cp)
        print(f"checkpoint: {cp}")
        rich = _checkpoint_message(
            "day5_management_summary",
            mgmt_res,
            index=total + 1,
            total=total + 1,
            ts=datetime.now(),
            style=args.checkpoint_style,
        )
        checkpoint_lines.append(f"[{args.checkpoint_style}] {rich}")
        if live_log_fp is not None:
            live_log_fp.write(f"[checkpoint] {cp}\n")
            live_log_fp.write(f"[checkpoint-{args.checkpoint_style}] {rich}\n")
            live_log_fp.flush()
    if not mgmt_res.ok:
        decision = "No-Go"
    finished_at = datetime.now()
    report = {
        "title": "Day5 Final Precheck Runner Report",
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
        "decision": decision,
        "retry_policy": {
            "max_retries": max(0, args.max_retries),
            "retry_delay_seconds": max(0.1, args.retry_delay_seconds),
            "whitelist": sorted(retry_whitelist),
        },
        "steps": [asdict(s) for s in steps],
    }
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_to_md(report), encoding="utf-8")
    if args.checkpoint:
        checkpoint_md = [
            "# Day5 Checkpoint Broadcasts",
            "",
            f"- started_at: `{started_at.isoformat()}`",
            f"- finished_at: `{finished_at.isoformat()}`",
            f"- decision: **{decision}**",
            "",
            "## Lines",
            "",
        ]
        checkpoint_md.extend([f"- {line}" for line in checkpoint_lines] or ["- (none)"])
        checkpoint_path.write_text("\n".join(checkpoint_md) + "\n", encoding="utf-8")
        template_path = args.reports_dir / f"day5-final-precheck-checkpoint-template-{ts_start}.md"
        template_lines = [
            "# Day5 Checkpoint Message Template",
            "",
            f"- style: `{args.checkpoint_style}`",
            f"- started_at: `{started_at.isoformat()}`",
            "",
            "## Broadcast Messages",
            "",
        ]
        for line in checkpoint_lines:
            if not line.startswith(f"[{args.checkpoint_style}] "):
                continue
            template_lines.append("```text")
            template_lines.append(line.split("] ", 1)[1])
            template_lines.append("```")
            template_lines.append("")
        template_path.write_text("\n".join(template_lines), encoding="utf-8")
    if live_log_fp is not None:
        live_log_fp.write(f"[meta] finished_at={finished_at.isoformat()} decision={decision}\n")
        live_log_fp.close()

    print(f"Decision: {decision}")
    print(f"report_json: {out_json}")
    print(f"report_md: {out_md}")
    if args.checkpoint:
        print(f"checkpoint_md: {checkpoint_path}")
        print(f"checkpoint_template: {template_path}")
    if args.live_log:
        print(f"live_log: {live_log_path}")
    return 0 if decision == "Go" else 1


if __name__ == "__main__":
    raise SystemExit(main())
