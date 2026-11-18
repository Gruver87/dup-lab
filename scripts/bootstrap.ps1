#Requires -Version 5.1
# One-shot Windows entry: python bootstrap (clones + skills + MCP + demos)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { throw "python not found on PATH" }
python -m pip install -U pip -q
python scripts\bootstrap.py @args
exit $LASTEXITCODE
