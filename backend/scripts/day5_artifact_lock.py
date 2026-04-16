from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_output_dir() -> Path:
    return _repo_root() / "reports"


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _collect_config_snapshot(config_paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in config_paths:
        item: dict[str, Any] = {
            "path": str(p),
            "exists": p.exists(),
        }
        if p.exists() and p.is_file():
            item["sha256"] = _sha256_file(p)
            item["size"] = p.stat().st_size
            item["mtime"] = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()
        rows.append(item)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lock Day5 release artifacts (tag/digest/config snapshot) into a manifest."
    )
    parser.add_argument("--release-tag", required=True, help="Release tag, e.g. release-2026-04-16-r1")
    parser.add_argument("--backend-digest", default="", help="Backend image digest, e.g. sha256:...")
    parser.add_argument("--frontend-checksum", default="", help="Frontend package checksum, e.g. sha256:...")
    parser.add_argument(
        "--config",
        action="append",
        default=[],
        help="Config file path for snapshot (can be used multiple times).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_default_output_dir(),
        help="Output directory for lock manifest.",
    )
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    ts = now.strftime("%Y%m%d-%H%M%S")

    default_configs = [
        _repo_root().parent / "docs" / "ceo_policy.engine.yaml",
        _repo_root() / "data" / "state.json",
    ]
    extra_configs = [Path(p).resolve() for p in args.config]
    config_snapshot = _collect_config_snapshot(default_configs + extra_configs)

    manifest = {
        "title": "Day5 Release Artifact Lock",
        "generated_at": now.isoformat(),
        "release_tag": args.release_tag,
        "backend_image_digest": args.backend_digest or None,
        "frontend_package_checksum": args.frontend_checksum or None,
        "config_snapshot": config_snapshot,
        "rollback_hint": {
            "release_tag": args.release_tag,
            "notes": "Use previous release tag/digest from earlier lock manifest if rollback is needed.",
        },
    }

    out_json = output_dir / f"day5-artifact-lock-{ts}.json"
    out_md = output_dir / f"day5-artifact-lock-{ts}.md"
    out_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    md_lines = [
        "# Day5 Artifact Lock",
        "",
        f"- 生成时间: `{manifest['generated_at']}`",
        f"- 发布标签: `{manifest['release_tag']}`",
        f"- Backend digest: `{manifest['backend_image_digest']}`",
        f"- Frontend checksum: `{manifest['frontend_package_checksum']}`",
        "",
        "## Config Snapshot",
        "",
        "| path | exists | sha256 | size | mtime |",
        "|---|---:|---|---:|---|",
    ]
    for row in config_snapshot:
        md_lines.append(
            f"| `{row.get('path')}` | {row.get('exists')} | "
            f"`{row.get('sha256', '')}` | {row.get('size', '')} | {row.get('mtime', '')} |"
        )
    out_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"manifest_json: {out_json}")
    print(f"manifest_md: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
