# Production API startup (Waitress)
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path
$VENV_PYTHON = Join-Path $PROJECT_ROOT ".venv\Scripts\python.exe"

if (-Not (Test-Path $VENV_PYTHON)) {
    Write-Host "[ERROR] Python virtual environment not found at .venv" -ForegroundColor Red
    Write-Host "Create it with: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

Set-Location $PROJECT_ROOT
& $VENV_PYTHON -m waitress --listen=0.0.0.0:5000 api.wsgi:app
