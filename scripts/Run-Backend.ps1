$projectRoot = Split-Path -Parent $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"

Set-Location $backendPath
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 5061

