# Promo — README → 30s TikTok / Reels teaser

Generate a vertical short from this repo’s `README.md` using
[`dup-content-engine`](https://github.com/Gruver87/dup-content-engine).

> **Honesty:** gate `ALLOW` means the file passed media/policy checks.  
> It is **not** an audience-growth or monetization claim.  
> TikTok / Reels / Shorts = **manual upload** of the exported mp4 (no cookie bots).

## Prerequisites

1. Python 3.11+
2. Sibling clone of the engine (recommended layout):

```text
Desktop/
  dup-lab/
  dup-content-engine/
```

Or set `DUP_CONTENT_ENGINE` to the engine path / put it under `vendor/dup-content-engine`.

## One command

```bash
# from dup-lab/
python scripts/promo_teaser.py
# Windows:
.\scripts\promo_teaser.ps1
# Offline TTS (no network):
python scripts/promo_teaser.py --offline-tts
# Script JSON only (no render):
python scripts/promo_teaser.py --script-only
```

Makefile:

```bash
make promo
make promo-offline
```

## Beyond the teaser (engine v0.1.5+)

From the sibling `dup-content-engine` checkout (still **no API keys** required):

```bash
cd ../dup-content-engine
python -m content_engine calendar topics.example.txt
python -m content_engine day topics.example.txt          # best A/B hook → offline render
python -m content_engine series topics.example.txt --limit 3
# Keys later: youtube / tiktok --dry-run / instagram --dry-run
```

Artifacts: `out/series/*/AB_REPORT.html`, `verified_pack_*.json`, `.srt`, `.thumb.jpg`.

## What you get

Under `out/promo/`:

| Artifact | Meaning |
|----------|---------|
| `teaser_script.json` | Scenes derived from README |
| `*.mp4` | ~30s 9:16 teaser (when gate allows) |
| `verified_pack_*.json` | SHA-256 + gate snapshot on ALLOW |
| `export/` | Drop folder ready for manual TikTok/Reels upload |

## Pipeline (under the hood)

```text
README.md → dup-content teaser → TTS → synthetic visuals → FFmpeg → policy gate → pack
```

Equivalent direct call:

```bash
cd ../dup-content-engine
pip install -e .
python -m content_engine teaser ../dup-lab/README.md --out ../dup-lab/out/promo --export --name "DUP Lab"
```

## Publish

1. Confirm `verified_pack_*.json` exists (ALLOW).
2. Open `out/promo/export/` and upload the mp4 in the official TikTok / Instagram / YouTube app.
3. Do **not** claim soak / production readiness from a promo clip — skill `evidence-honesty`.

## Tuning

| Flag | Effect |
|------|--------|
| `--target-sec 30` | Scene text budget (~default) |
| `--readme PATH` | Another markdown entrypoint |
| `--engine PATH` | Force content-engine location |
| `--no-export` | Skip copy into `export/` |

Edit scene copy by regenerating with `--script-only`, editing `teaser_script.json`, then:

```bash
python -m content_engine run out/promo/teaser_script.json --out out/promo
```
