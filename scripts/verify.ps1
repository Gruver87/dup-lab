#Requires -Version 5.1
# DUP Lab self-check — run after bootstrap (or anytime).
# Usage: .\scripts\verify.ps1
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

Write-Host "=== DUP Lab verify ===" -ForegroundColor Cyan
Write-Host "root=$Root"

$fail = 0

function Ok($msg)  { Write-Host "PASS  $msg" -ForegroundColor Green }
function Bad($msg) { Write-Host "FAIL  $msg" -ForegroundColor Red; $script:fail++ }
function Info($msg){ Write-Host "INFO  $msg" -ForegroundColor Yellow }

# 1) Ready report
$readyPath = Join-Path $Root "DUP_LAB_READY.json"
if (Test-Path $readyPath) {
  Ok "DUP_LAB_READY.json present"
  $ready = Get-Content $readyPath -Raw | ConvertFrom-Json
  if ($ready.bootstrap_wired -eq $true) { Ok "bootstrap_wired=true" } else { Bad "bootstrap_wired!=true" }
  $n = [int]$ready.skills_count
  if ($n -ge 8) { Ok "skills_count=$n" } else { Bad "skills_count=$n (want >=8)" }
  $mcp = @($ready.mcp_servers)
  if ($mcp.Count -ge 1) { Ok ("mcp_servers=" + ($mcp -join ",")) } else { Bad "no mcp_servers in READY" }
  if ($ready.demos) {
    foreach ($p in $ready.demos.PSObject.Properties) {
      if ($p.Value -eq "PASS") { Ok "demo $($p.Name)=PASS" } else { Bad "demo $($p.Name)=$($p.Value)" }
    }
  } else {
    Info "no demos in READY (re-run bootstrap without --skip-demos)"
  }
} else {
  Bad "DUP_LAB_READY.json missing — run: .\scripts\bootstrap.ps1"
}

# 2) On-disk wiring
if (Test-Path (Join-Path $Root ".agents\skills")) {
  $skills = @(Get-ChildItem (Join-Path $Root ".agents\skills") -Directory)
  if ($skills.Count -ge 8) { Ok ".agents/skills count=$($skills.Count)" } else { Bad ".agents/skills count=$($skills.Count)" }
} else { Bad ".agents/skills missing" }

$mcpFile = Join-Path $Root ".cursor\mcp.json"
if (Test-Path $mcpFile) { Ok ".cursor/mcp.json present" } else { Bad ".cursor/mcp.json missing" }

$userSkills = Join-Path $env:USERPROFILE ".agents\skills"
if (Test-Path $userSkills) {
  $us = @(Get-ChildItem $userSkills -Directory -ErrorAction SilentlyContinue)
  Ok "user skills ~/.agents/skills count=$($us.Count)"
} else {
  Info "user skills dir missing (bootstrap without --no-user-skills)"
}

# 3) Import smoke
$mods = @("skills_eval","skill_security","policy_gate","evidence_graph","skill_trust","radar_news_mcp")
foreach ($m in $mods) {
  python -c "import $m" 2>$null
  if ($LASTEXITCODE -eq 0) { Ok "import $m" } else { Bad "import $m" }
}

# 4) Live fixture demos (fast)
Write-Host "`n--- live demos ---" -ForegroundColor Cyan
python -m skills_eval --demo
if ($LASTEXITCODE -eq 0) { Ok "skills_eval --demo" } else { Bad "skills_eval --demo" }

python -m evidence_graph demo
if ($LASTEXITCODE -eq 0) { Ok "evidence_graph demo" } else { Bad "evidence_graph demo" }

python -m skill_trust demo
if ($LASTEXITCODE -eq 0) { Ok "skill_trust demo" } else { Bad "skill_trust demo" }

python -m radar_news_mcp.demo
if ($LASTEXITCODE -eq 0) { Ok "radar_news_mcp.demo" } else { Bad "radar_news_mcp.demo" }

Write-Host ""
if ($fail -eq 0) {
  Write-Host "RESULT: PASS — lab wired (demo≠soak; no live keys required)" -ForegroundColor Green
  exit 0
} else {
  Write-Host "RESULT: FAIL ($fail checks) — re-run .\scripts\bootstrap.ps1" -ForegroundColor Red
  exit 1
}
