# Generate ~30s TikTok/Reels teaser from README via dup-content-engine.
# ALLOW ≠ audience growth. Manual upload only.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

$extra = @()
if ($args -contains "-Offline") { $extra += "--offline-tts" }
if ($args -contains "-ScriptOnly") { $extra += "--script-only" }

python scripts/promo_teaser.py @extra
exit $LASTEXITCODE
