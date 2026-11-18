# Getting started — DUP Lab

## 60-second path

1. `git clone https://github.com/Gruver87/dup-lab.git && cd dup-lab`
2. `make bootstrap` (Windows: `.\scripts\bootstrap.ps1`)
3. Open the `dup-lab` folder in Cursor
4. Ask the agent something that needs a skill, e.g. “Can we claim 48h soak?” → `evidence-honesty` / `radar-ops-status`
5. MCP: `dup-policy-gate` works offline; radar MCP tools need a running Market Radar

## What is automatic

| Piece | Auto? | How |
|-------|-------|-----|
| Agent Skills | yes | copied to `.agents/skills` + user skills dirs |
| Python gates | yes | `pip install -e` from `vendor/` or Desktop siblings |
| Cursor MCP | yes | `.cursor/mcp.json` written by bootstrap |
| Fixture demos | yes | eval / graph / trust / news / security |
| Live KuCoin | no | never invented; optional `.env` |
| 48h soak | no | only with sealed packs |

## After bootstrap

- Status file: `DUP_LAB_READY.json`
- MCP bundle copy: `mcp.bundle.json`
- Skills live under `.agents/skills/<name>/SKILL.md`

## Troubleshooting

- **MCP missing in Cursor** → reload window; confirm `.cursor/mcp.json` exists  
- **Skill not found** → re-run bootstrap; folder name must match `name` in SKILL.md  
- **Demo FAIL on trust-plane** → install siblings (bootstrap clones them); gates optional for partial demo  
- **Radar tools refuse** → start `dup-market-radar` or ignore (policy-gate still works)
