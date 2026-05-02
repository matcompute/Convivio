$projectRoot = Split-Path -Parent $PSScriptRoot
$frontendPath = Join-Path $projectRoot "frontend"

Set-Location $frontendPath
npm.cmd run dev -- --host 127.0.0.1 --port 4203

