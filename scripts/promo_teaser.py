#!/usr/bin/env python3
"""Generate a ~30s TikTok/Reels teaser from this repo's README via dup-content-engine.

Fail-closed: prints ALLOW/REFUSE from the content gate.
ALLOW ≠ audience growth. Upload the exported mp4 manually.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_engine() -> Path | None:
    env = os.environ.get("DUP_CONTENT_ENGINE")
    candidates = []
    if env:
        candidates.append(Path(env))
    candidates.extend(
        [
            ROOT / "vendor" / "dup-content-engine",
            ROOT.parent / "dup-content-engine",
            Path.home() / "Desktop" / "dup-content-engine",
        ]
    )
    for c in candidates:
        if (c / "pyproject.toml").is_file() and (c / "src" / "content_engine").is_dir():
            return c.resolve()
    return None


def ensure_engine(engine: Path) -> None:
    # Editable install so `python -m content_engine` resolves
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-e", str(engine), "-q"],
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="dup-lab README → 30s promo teaser")
    p.add_argument(
        "--readme",
        type=Path,
        default=ROOT / "README.md",
        help="README to teaserize (default: repo README.md)",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=ROOT / "out" / "promo",
        help="Output directory for mp4 + verified pack",
    )
    p.add_argument("--target-sec", type=float, default=30.0)
    p.add_argument("--offline-tts", action="store_true")
    p.add_argument("--script-only", action="store_true")
    p.add_argument("--no-export", action="store_true", help="Skip export drop folder")
    p.add_argument(
        "--engine",
        type=Path,
        default=None,
        help="Path to dup-content-engine (else auto-detect sibling/vendor)",
    )
    args = p.parse_args(argv)

    engine = args.engine or find_engine()
    if engine is None:
        print(
            "dup-content-engine not found.\n"
            "  Clone https://github.com/Gruver87/dup-content-engine next to dup-lab\n"
            "  or set DUP_CONTENT_ENGINE=/path/to/dup-content-engine",
            file=sys.stderr,
        )
        return 2

    if not args.readme.is_file():
        print(f"README missing: {args.readme}", file=sys.stderr)
        return 2

    print(f"engine={engine}", file=sys.stderr)
    ensure_engine(engine)

    cmd = [
        sys.executable,
        "-m",
        "content_engine",
        "teaser",
        str(args.readme.resolve()),
        "--out",
        str(args.out.resolve()),
        "--target-sec",
        str(args.target_sec),
        "--name",
        "DUP Lab",
    ]
    if args.offline_tts:
        cmd.append("--offline-tts")
    if args.script_only:
        cmd.append("--script-only")
    elif not args.no_export:
        cmd.append("--export")

    print(" ".join(cmd), file=sys.stderr)
    proc = subprocess.run(cmd)
    if proc.returncode == 0 and not args.script_only:
        packs = sorted(args.out.glob("verified_pack_*.json"))
        summary = {
            "ok": True,
            "out": str(args.out),
            "pack": str(packs[-1]) if packs else None,
            "note": "ALLOW ≠ growth. Upload out/promo/export/*.mp4 manually to TikTok/Reels.",
            "docs": "docs/PROMO.md",
        }
        print(json.dumps(summary, indent=2))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
