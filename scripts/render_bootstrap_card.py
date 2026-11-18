#!/usr/bin/env python3
"""Render docs/assets/bootstrap-ready-*.png from DUP_LAB_READY.json + mcp.bundle.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READY = ROOT / "DUP_LAB_READY.json"
MCP = ROOT / "mcp.bundle.json"
OUT_DIR = ROOT / "docs" / "assets"


def main() -> int:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("pip install pillow", file=sys.stderr)
        return 2

    if not READY.is_file():
        print("missing DUP_LAB_READY.json — run bootstrap first", file=sys.stderr)
        return 2
    ready = json.loads(READY.read_text(encoding="utf-8"))
    mcp = {}
    if MCP.is_file():
        mcp = json.loads(MCP.read_text(encoding="utf-8")).get("mcpServers") or {}

    w, h = 1280, 720
    img = Image.new("RGB", (w, h), "#0f1419")
    draw = ImageDraw.Draw(img)
    try:
        font_lg = ImageFont.truetype("arial.ttf", 36)
        font_md = ImageFont.truetype("arial.ttf", 22)
        font_sm = ImageFont.truetype("consola.ttf", 18)
    except OSError:
        font_lg = ImageFont.load_default()
        font_md = font_lg
        font_sm = font_lg

    # Header
    draw.rectangle((0, 0, w, 88), fill="#161b22")
    draw.text((40, 24), "DUP Lab  ·  bootstrap ready", fill="#e6edf3", font=font_lg)
    wired = bool(ready.get("bootstrap_wired"))
    badge = "PASS" if wired else "FAIL"
    badge_color = "#3fb950" if wired else "#f85149"
    draw.rounded_rectangle((1040, 22, 1240, 66), radius=8, fill=badge_color)
    draw.text((1085, 30), badge, fill="#0d1117", font=font_md)

    # Left card — READY
    draw.rounded_rectangle((40, 120, 620, 660), radius=12, fill="#161b22", outline="#30363d")
    draw.text((64, 140), "DUP_LAB_READY.json", fill="#58a6ff", font=font_md)
    lines = [
        f'bootstrap_wired: {ready.get("bootstrap_wired")}',
        f'skills_count:    {ready.get("skills_count")}',
        f'project_skills:  {ready.get("project_skills")}',
        f'cursor_mcp:      {ready.get("cursor_mcp")}',
        "",
        "imports:",
    ]
    for k, v in (ready.get("imports") or {}).items():
        lines.append(f"  {k}: {v}")
    demos = ready.get("demos") or {}
    if demos:
        lines.append("")
        lines.append("demos:")
        for k, v in demos.items():
            lines.append(f"  {k}: {v}")
    y = 190
    for line in lines:
        draw.text((64, y), line, fill="#c9d1d9", font=font_sm)
        y += 26

    # Right card — MCP
    draw.rounded_rectangle((660, 120, 1240, 660), radius=12, fill="#161b22", outline="#30363d")
    draw.text((684, 140), "Cursor MCP (.cursor/mcp.json)", fill="#58a6ff", font=font_md)
    servers = list(ready.get("mcp_servers") or mcp.keys())
    y = 200
    for name in servers:
        draw.rounded_rectangle((684, y, 1200, y + 56), radius=8, fill="#21262d", outline="#3fb950")
        draw.ellipse((704, y + 18, 724, y + 38), fill="#3fb950")
        draw.text((744, y + 14), name, fill="#e6edf3", font=font_md)
        draw.text((1000, y + 16), "connected", fill="#3fb950", font=font_sm)
        y += 72
    draw.text(
        (684, 600),
        "Works offline with local fixtures — no external API keys required",
        fill="#8b949e",
        font=font_sm,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "bootstrap-ready-v0.1.0.png"
    img.save(out, "PNG")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
