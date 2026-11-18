# Getting started — DUP Lab

## 60-second path

1. `git clone https://github.com/Gruver87/dup-lab.git && cd dup-lab`
2. `make bootstrap` (Windows: `.\scripts\bootstrap.ps1`)
3. Open the `dup-lab` folder in Cursor
4. Ask the agent a claim/honesty question — skills like `evidence-honesty` activate
5. MCP: `dup-policy-gate` works offline; domain MCP tools may need a live service

Works offline with local fixtures — no external API keys required.

## What is automatic

| Piece | Auto? | How |
|-------|-------|-----|
| Agent Skills | yes | copied to `.agents/skills` + user skills dirs |
| Python gates | yes | `pip install -e` from `vendor/` or Desktop siblings |
| Cursor MCP | yes | `.cursor/mcp.json` written by bootstrap |
| Fixture demos | yes | eval / graph / trust / news / security |
| External API keys | no | never required for bootstrap |
| Long soak claims | no | only with sealed packs elsewhere |

## After bootstrap

- Status file: `DUP_LAB_READY.json`
- MCP bundle copy: `mcp.bundle.json`
- Skills live under `.agents/skills/<name>/SKILL.md`
- Verify: `.\scripts\verify.ps1` / `make verify`

## Domain stands

Optional crypto market-ops stand: [`CRYPTO_STAND.md`](CRYPTO_STAND.md).

## Troubleshooting

- **MCP missing in Cursor** → reload window; confirm `.cursor/mcp.json` exists  
- **Skill not found** → re-run bootstrap; folder name must match `name` in SKILL.md  
- **Demo FAIL on trust-plane** → install siblings (bootstrap clones them); gates optional for partial demo  
- **Domain MCP refuses** → start the domain service or ignore (policy-gate still works)
