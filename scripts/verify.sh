#!/usr/bin/env bash
# DUP Lab self-check — run after bootstrap.
# Usage: bash scripts/verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0
ok()  { echo "PASS  $*"; }
bad() { echo "FAIL  $*"; fail=$((fail+1)); }
info(){ echo "INFO  $*"; }

echo "=== DUP Lab verify ==="
echo "root=$ROOT"

if [[ -f DUP_LAB_READY.json ]]; then
  ok "DUP_LAB_READY.json present"
  python - <<'PY' || bad "READY parse/assertions"
import json
from pathlib import Path
r=json.loads(Path("DUP_LAB_READY.json").read_text())
assert r.get("bootstrap_wired") is True
assert int(r.get("skills_count") or 0) >= 8
print("PASS  bootstrap_wired + skills_count")
demos=r.get("demos") or {}
for k,v in demos.items():
    print(("PASS" if v=="PASS" else "FAIL")+f"  demo {k}={v}")
    if v!="PASS":
        raise SystemExit(1)
PY
else
  bad "DUP_LAB_READY.json missing — run: make bootstrap"
fi

[[ -d .agents/skills ]] && ok ".agents/skills present" || bad ".agents/skills missing"
[[ -f .cursor/mcp.json ]] && ok ".cursor/mcp.json present" || bad ".cursor/mcp.json missing"

for m in skills_eval skill_security policy_gate evidence_graph skill_trust radar_news_mcp; do
  if python -c "import $m" 2>/dev/null; then ok "import $m"; else bad "import $m"; fi
done

echo
echo "--- live demos ---"
python -m skills_eval --demo && ok "skills_eval --demo" || bad "skills_eval --demo"
python -m evidence_graph demo && ok "evidence_graph demo" || bad "evidence_graph demo"
python -m skill_trust demo && ok "skill_trust demo" || bad "skill_trust demo"
python -m radar_news_mcp.demo && ok "radar_news_mcp.demo" || bad "radar_news_mcp.demo"

echo
if [[ "$fail" -eq 0 ]]; then
  echo "RESULT: PASS — lab wired (demo≠soak; no live keys required)"
  exit 0
fi
echo "RESULT: FAIL ($fail checks) — re-run: make bootstrap"
exit 1
