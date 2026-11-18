# Crypto combat stand (optional)

DUP Lab is a **generic** Agent Skills / MCP / trust onboarding entry.  
Crypto Market Radar is the **first combat stand**, not the product identity of `dup-lab`.

## What stays crypto-specific

| Piece | Role |
|-------|------|
| [`dup-agent-skills`](https://github.com/Gruver87/dup-agent-skills) | Market-ops skills (`radar-*`, `no-futures-auto`, …) |
| [`dup-radar-news-mcp`](https://github.com/Gruver87/dup-radar-news-mcp) | Read-only digests |
| [`dup-market-radar`](https://github.com/Gruver87/dup-market-radar) | Live spot ops (optional; not required for bootstrap) |
| [`dup-policy-gate`](https://github.com/Gruver87/dup-policy-gate) | Spot-only intents · `FUTURES_BLOCK` |

## Honesty (crypto stand)

- Bootstrap / fixture demos ≠ 48h soak PASS  
- Ops-ready ≠ live money  
- Futures auto always refused  
- Never invent exchange API keys — use sealed packs / env ceremony only  

## Live radar (optional)

```bash
# only if you already run Market Radar locally
# RADAR_BASE_URL=http://127.0.0.1:8787
# RADAR_API_KEY=…   # from radar .env — never commit
```

Without radar, policy-gate MCP and fixture demos still work. Radar MCP tools refuse cleanly when the API is down.

## Universal layers (reuse elsewhere)

Trust + guardrails (`skills-eval`, `security-scan`, `evidence-graph`, `trust-plane`, `policy-gate`) apply to any high-stakes Agent Skills / MCP install — fintech, DevOps, regulated ops — not only crypto.
