# DUP Lab — start here

[![ci](https://github.com/Gruver87/dup-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Gruver87/dup-lab/actions/workflows/ci.yml)

**Org:** [DUP Labs](https://github.com/Gruver87) · **Author:** Uladzimir Dabranski  

One-command onboarding for the whole Agent Skills / MCP / trust stack.  
**Not** financial advice. **Not** a 48h soak. **Not** live trading.

```text
clone → bootstrap → open in Cursor → skills + MCP already wired
```

## Quick start (beginners)

```bash
git clone https://github.com/Gruver87/dup-lab.git
cd dup-lab
make bootstrap
# Windows: .\scripts\bootstrap.ps1
```

What bootstrap does automatically:

1. Finds or **clones** sibling repos into `vendor/`
2. `pip install -e` gates (eval, security-scan, policy-gate, evidence-graph, trust-plane, radar-news)
3. Copies all Agent Skills into:
   - `dup-lab/.agents/skills/` (this project — Cursor auto-loads)
   - `~/.agents/skills/` and `~/.cursor/skills/` (all your projects)
4. Writes `.cursor/mcp.json` (policy-gate + radar-news + radar-ops)
5. Runs fixture demos (no KuCoin keys)

Then: **File → Open Folder → `dup-lab`** in Cursor (or open `dup-lab.code-workspace`).  
Reload window once if MCP servers do not show up.

## Architecture (what you just wired)

```text
Execution     dup-agent-skills · radar-news-mcp
Guardrails    policy-gate · skill-security-scan
Trust         skills-eval · evidence-graph · skill-trust-plane
```

L1 (`dup-protocol`) stays a **separate** evidence tree — see skill `l1-boundary`.

## Commands

| Command | Purpose |
|---------|---------|
| `make bootstrap` / `.\scripts\bootstrap.ps1` | Full auto wiring |
| `make doctor` | Print last `DUP_LAB_READY.json` |
| `make demos` | Re-run fixture demos only |

## Honesty

- Bootstrap PASS ≠ soak PASS  
- Futures auto always refused (`FUTURES_BLOCK`)  
- Live radar / KuCoin keys are **optional** — demos use fixtures  

## Related

| Repo | Role |
|------|------|
| [`dup-agent-skills`](https://github.com/Gruver87/dup-agent-skills) | Skills pack source |
| [`dup-skill-trust-plane`](https://github.com/Gruver87/dup-skill-trust-plane) | Control plane |
| [`dup-skills-eval`](https://github.com/Gruver87/dup-skills-eval) | Eval gate |
| Profile | [github.com/Gruver87](https://github.com/Gruver87) |

## License

MIT — [`LICENSE`](LICENSE).
