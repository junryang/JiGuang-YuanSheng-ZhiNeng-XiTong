from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _docs_dir() -> Path:
    return _repo_root().parent / "docs"


def _reports_dir() -> Path:
    return _repo_root() / "reports"


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")


def _ensure_exists(path: Path, kind: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{kind} not found: {path}")


def _latest(path_dir: Path, pattern: str) -> Path | None:
    files = sorted(path_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0] if files else None


def _checklist_markdown(*, date_tag: str, go_memo: Path, release_memo: Path, duty_schedule: Path, artifact_lock: Path) -> str:
    return f"""# Day5 发布前最终检查清单（{date_tag}）

## 文档定版结果

- Go/No-Go 评审纪要：`{go_memo}`
- 发布纪要：`{release_memo}`
- 值班排班表：`{duty_schedule}`
- 工件锁定清单：`{artifact_lock}`

## 一键执行顺序

1. `python -m pytest -m day3_gate -q --tb=short`
2. `python scripts/day4_gate_runner.py --reports-dir "d:/BaiduSyncdisk/JiGuang/backend/reports"`
3. `python scripts/day5_release_prep.py --reports-dir "d:/BaiduSyncdisk/JiGuang/backend/reports" --output-dir "d:/BaiduSyncdisk/JiGuang/docs" --duty-schedule "{duty_schedule.as_posix()}" --emit-duty-todo`
4. `python scripts/day5_artifact_lock.py --release-tag "release-{date_tag}-r1" --backend-digest "<真实digest>" --frontend-checksum "<真实checksum>" --output-dir "d:/BaiduSyncdisk/JiGuang/backend/reports"`

## 窗口前人工确认

- [ ] 主备联系方式实名校验
- [ ] 升级链路与响应 SLA 已确认
- [ ] 回滚入口可用并已演练
- [ ] Go/No-Go 评审签字完成
- [ ] 发布纪要签字完成
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize Day5 auto drafts into r1 release-ready docs.")
    parser.add_argument("--date", default=datetime.now().strftime("%Y%m%d"), help="Date tag, e.g. 20260417")
    parser.add_argument("--docs-dir", type=Path, default=_docs_dir(), help="Docs directory")
    parser.add_argument("--reports-dir", type=Path, default=_reports_dir(), help="Reports directory")
    parser.add_argument(
        "--go-auto",
        type=Path,
        default=None,
        help="Optional explicit Go/No-Go auto memo path",
    )
    parser.add_argument(
        "--release-auto",
        type=Path,
        default=None,
        help="Optional explicit release memo auto path",
    )
    parser.add_argument(
        "--duty-schedule",
        type=Path,
        default=_docs_dir() / "D5_RELEASE_DUTY_SCHEDULE_20260417_auto_filled.md",
        help="Duty schedule path used for release window",
    )
    args = parser.parse_args()

    go_auto = args.go_auto or (args.docs_dir / f"D5_GO_NO_GO_REVIEW_MEMO_{args.date}_auto.md")
    release_auto = args.release_auto or (args.docs_dir / f"D3_RELEASE_MEMO_{args.date}_auto.md")
    artifact_lock = _latest(args.reports_dir, "day5-artifact-lock-*.json")

    _ensure_exists(go_auto, "go/no-go auto memo")
    _ensure_exists(release_auto, "release auto memo")
    _ensure_exists(args.duty_schedule, "duty schedule")
    if artifact_lock is None:
        raise FileNotFoundError(f"artifact lock not found in: {args.reports_dir}")

    go_r1 = args.docs_dir / f"D5_GO_NO_GO_REVIEW_MEMO_{args.date}_r1.md"
    rel_r1 = args.docs_dir / f"D3_RELEASE_MEMO_{args.date}_r1.md"
    checklist = args.docs_dir / f"D5_FINAL_PRECHECK_{args.date}_r1.md"

    _copy_file(go_auto, go_r1)
    _copy_file(release_auto, rel_r1)
    checklist.write_text(
        _checklist_markdown(
            date_tag=args.date,
            go_memo=go_r1,
            release_memo=rel_r1,
            duty_schedule=args.duty_schedule,
            artifact_lock=artifact_lock,
        ),
        encoding="utf-8",
    )

    print(f"go_memo_r1: {go_r1}")
    print(f"release_memo_r1: {rel_r1}")
    print(f"final_precheck: {checklist}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
