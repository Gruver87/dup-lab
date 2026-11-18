#!/usr/bin/env python3
"""DUP Lab bootstrap — one entrypoint for skills + gates + Cursor MCP.

Fail-closed honesty:
  - demos use fixtures (no KuCoin keys, no soak)
  - optional live radar is never required for bootstrap PASS
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
CONFIG = ROOT / "configs" / "ecosystem.json"
READY = ROOT / "DUP_LAB_READY.json"
AGENTS_SKILLS = ROOT / ".agents" / "skills"
CURSOR_MCP = ROOT / ".cursor" / "mcp.json"
BUNDLE_MCP = ROOT / "mcp.bundle.json"


def _run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> int:
    print(f"+ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    if check and proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return proc.returncode


def _load_config() -> dict[str, Any]:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def _python() -> str:
    return sys.executable


def _resolve_sibling(sib_id: str) -> Path | None:
    """Prefer vendor/, then Desktop/parent sibling, then None."""
    candidates = [
        VENDOR / sib_id,
        ROOT.parent / sib_id,
        Path.home() / "Desktop" / sib_id,
    ]
    for path in candidates:
        if (path / ".git").exists() or (path / "pyproject.toml").exists() or (
            path / "skills"
        ).is_dir():
            return path.resolve()
    return None


def ensure_sibling(sib: dict[str, Any], *, clone: bool) -> Path:
    existing = _resolve_sibling(sib["id"])
    if existing is not None:
        print(f"OK sibling {sib['id']} → {existing}")
        return existing
    if not clone:
        raise SystemExit(f"missing sibling {sib['id']} (pass --clone or place on Desktop)")
    VENDOR.mkdir(parents=True, exist_ok=True)
    dest = VENDOR / sib["id"]
    if dest.exists():
        return dest.resolve()
    url = sib["github"]
    _run(["git", "clone", "--depth", "1", url, str(dest)])
    return dest.resolve()


def install_pip(path: Path) -> None:
    # Prefer editable +[dev]; fall back to plain editable if extra missing
    rc = _run([_python(), "-m", "pip", "install", "-e", f"{path}[dev]"], check=False)
    if rc != 0:
        rc = _run([_python(), "-m", "pip", "install", "-e", str(path)], check=False)
    if rc != 0:
        raise SystemExit(f"pip install failed for {path}")


def _copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def install_skills(skills_root: Path, *, user_scope: bool) -> list[str]:
    src = skills_root / "skills"
    if not src.is_dir():
        raise SystemExit(f"skills/ missing under {skills_root}")
    installed: list[str] = []
    targets = [AGENTS_SKILLS]
    if user_scope:
        home = Path.home()
        targets.extend([home / ".agents" / "skills", home / ".cursor" / "skills"])
    for skill_dir in sorted(p for p in src.iterdir() if p.is_dir()):
        name = skill_dir.name
        for dst_root in targets:
            dst_root.mkdir(parents=True, exist_ok=True)
            legacy = dst_root / f"dup-{name}"
            if legacy.exists():
                shutil.rmtree(legacy)
            _copy_tree(skill_dir, dst_root / name)
        installed.append(name)
        print(f"installed skill {name}")
    return installed


def write_workspace(paths: dict[str, Path]) -> Path:
    """Multi-root workspace with resolved sibling paths (absolute)."""
    folders = [{"path": str(ROOT), "name": "dup-lab"}]
    order = [
        "dup-agent-skills",
        "dup-skill-trust-plane",
        "dup-skills-eval",
        "dup-evidence-graph",
        "dup-policy-gate",
        "dup-skill-security-scan",
        "dup-radar-news-mcp",
    ]
    for sib_id in order:
        path = paths.get(sib_id)
        if path is None:
            continue
        folders.append({"path": str(path), "name": sib_id.replace("dup-", "")})
    payload = {
        "folders": folders,
        "settings": {
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
            }
        },
    }
    out = ROOT / "dup-lab.code-workspace"
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.name} ({len(folders)} folders)")
    return out


def write_mcp(paths: dict[str, Path], cfg: dict[str, Any]) -> dict[str, Any]:
    """Project .cursor/mcp.json — Cursor loads this when the folder is open."""
    servers: dict[str, Any] = {}
    py = _python()

    # Always-on offline policy MCP
    if "dup-policy-gate" in paths:
        servers["dup-policy-gate"] = {
            "command": py,
            "args": ["-m", "policy_gate.mcp_server"],
            "env": {},
        }

    # Radar news — works when radar is up; tools refuse cleanly if not
    if "dup-radar-news-mcp" in paths:
        servers["dup-radar-news"] = {
            "command": py,
            "args": ["-m", "radar_news_mcp"],
            "env": {
                "RADAR_BASE_URL": os.environ.get("RADAR_BASE_URL", "http://127.0.0.1:8787"),
            },
        }

    # Radar-ops from agent-skills package if installed
    skills = paths.get("dup-agent-skills")
    if skills is not None:
        run_ps1 = skills / "scripts" / "run_radar_mcp.ps1"
        run_py = skills / "packages" / "radar_mcp"
        if run_ps1.is_file() and os.name == "nt":
            servers["radar-ops"] = {
                "command": "powershell",
                "args": [
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(run_ps1),
                ],
            }
        elif (skills / "packages").is_dir():
            # Cross-platform: module path after pip install -e packages/radar_mcp if present
            pkg = skills / "packages" / "radar_mcp"
            if (pkg / "pyproject.toml").is_file() or (pkg / "setup.py").is_file():
                _run([_python(), "-m", "pip", "install", "-e", str(pkg)], check=False)
                servers["radar-ops"] = {
                    "command": py,
                    "args": ["-m", "radar_mcp"],
                    "env": {
                        "RADAR_BASE_URL": os.environ.get(
                            "RADAR_BASE_URL", "http://127.0.0.1:8787"
                        ),
                    },
                }

    payload = {"mcpServers": servers}
    CURSOR_MCP.parent.mkdir(parents=True, exist_ok=True)
    CURSOR_MCP.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    # Portable template for git (no absolute python path)
    portable: dict[str, Any] = {"mcpServers": {}}
    for name, conf in servers.items():
        c = dict(conf)
        if c.get("command") == py:
            c["command"] = "python"
        portable["mcpServers"][name] = c
    BUNDLE_MCP.write_text(json.dumps(portable, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {CURSOR_MCP.relative_to(ROOT)} ({len(servers)} MCP servers)")
    return payload


def run_demos(paths: dict[str, Path], cfg: dict[str, Any]) -> dict[str, str]:
    results: dict[str, str] = {}
    for sib in cfg["siblings"]:
        demo = sib.get("demo")
        if not demo:
            continue
        path = paths.get(sib["id"])
        if path is None:
            results[sib["id"]] = "SKIP missing"
            continue
        print(f"\n== demo {sib['id']} ==")
        rc = _run(demo, cwd=path, check=False)
        results[sib["id"]] = "PASS" if rc == 0 else f"FAIL exit={rc}"
    return results


def doctor(paths: dict[str, Path], skills: list[str], mcp: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "skills_count": len(skills),
        "skills": skills,
        "siblings": {k: str(v) for k, v in paths.items()},
        "mcp_servers": list((mcp.get("mcpServers") or {}).keys()),
        "cursor_mcp": CURSOR_MCP.is_file(),
        "project_skills": AGENTS_SKILLS.is_dir(),
        "note": "demo≠soak; FUTURES_BLOCK; no live keys required for bootstrap",
    }
    # Import smoke
    imports = {}
    for mod in ("skills_eval", "skill_security", "policy_gate", "evidence_graph", "skill_trust"):
        try:
            __import__(mod)
            imports[mod] = "ok"
        except ImportError as exc:
            imports[mod] = f"missing: {exc}"
    checks["imports"] = imports
    return checks


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="dup-lab-bootstrap")
    p.add_argument("--clone", action="store_true", help="git clone missing siblings into vendor/")
    p.add_argument("--no-user-skills", action="store_true", help="Only project .agents/skills")
    p.add_argument("--skip-demos", action="store_true")
    p.add_argument("--skip-pip", action="store_true")
    p.add_argument("--doctor-only", action="store_true")
    args = p.parse_args(argv)

    cfg = _load_config()
    paths: dict[str, Path] = {}

    if args.doctor_only and READY.is_file():
        print(READY.read_text(encoding="utf-8"))
        return 0

    print("=== DUP Lab bootstrap ===")
    print(f"root={ROOT}")

    for sib in cfg["siblings"]:
        # Default: clone if missing (automatic for beginners)
        path = ensure_sibling(sib, clone=args.clone or True)
        paths[sib["id"]] = path
        if sib.get("pip") and not args.skip_pip:
            install_pip(path)

    skills_pack = paths.get("dup-agent-skills")
    if skills_pack is None:
        raise SystemExit("dup-agent-skills required")
    installed = install_skills(skills_pack, user_scope=not args.no_user_skills)

    mcp = write_mcp(paths, cfg)
    write_workspace(paths)

    demo_results: dict[str, str] = {}
    if not args.skip_demos:
        demo_results = run_demos(paths, cfg)

    report = doctor(paths, installed, mcp)
    report["demos"] = demo_results
    report["ok"] = all(v == "PASS" for v in demo_results.values()) if demo_results else True
    # Soft-ok: skills+mcp wired even if one optional demo fails
    report["bootstrap_wired"] = bool(installed) and CURSOR_MCP.is_file()
    READY.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"\n=== READY → {READY.name} bootstrap_wired={report['bootstrap_wired']} ===")
    print("Open this folder in Cursor — skills load from .agents/skills, MCP from .cursor/mcp.json")
    print("Restart Cursor MCP / reload window if servers do not appear yet.")
    return 0 if report["bootstrap_wired"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
