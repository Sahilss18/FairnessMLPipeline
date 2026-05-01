# Fairness & Bias Detection System - Startup Script
# This script starts both the Flask API backend and React frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fairness & Bias Detection System" -ForegroundColor Cyan
Write-Host "Multi-Phase ML Web Interface" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$PROJECT_ROOT = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if virtual environment exists
$VENV_PATH = Join-Path $PROJECT_ROOT ".venv"
if (-Not (Test-Path $VENV_PATH)) {
    Write-Host "[ERROR] Virtual environment not found at $VENV_PATH" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

# Check if models exist
$BASELINE_MODEL = Join-Path $PROJECT_ROOT "models\baseline_rf_model.pkl"
$EMBEDDING_MODEL = Join-Path $PROJECT_ROOT "models\embedding_rf_model.pkl"

if (-Not (Test-Path $BASELINE_MODEL) -or -Not (Test-Path $EMBEDDING_MODEL)) {
    Write-Host "[WARNING] Trained models not found!" -ForegroundColor Yellow
    Write-Host "Models should be located at:" -ForegroundColor Yellow
    Write-Host "  - $BASELINE_MODEL" -ForegroundColor Yellow
    Write-Host "  - $EMBEDDING_MODEL" -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Would you like to train the models now? (y/n)"
    if ($response -eq 'y') {
        Write-Host "[INFO] Starting model training..." -ForegroundColor Cyan
        & "$VENV_PATH\Scripts\python.exe" (Join-Path $PROJECT_ROOT "main.py") --mode all
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Model training failed!" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "[ERROR] Cannot start without trained models!" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[✓] Models found" -ForegroundColor Green
Write-Host ""

# Function to start Flask API in a new window
function Start-FlaskAPI {
    Write-Host "[INFO] Starting Flask API Backend..." -ForegroundColor Cyan
    $flaskScript = @"
Write-Host 'Activating virtual environment...' -ForegroundColor Yellow
& '$VENV_PATH\Scripts\Activate.ps1'

Write-Host 'Starting Flask API on http://localhost:5000' -ForegroundColor Green
Write-Host 'Press Ctrl+C to stop the server' -ForegroundColor Yellow
Write-Host ''

cd '$PROJECT_ROOT'
python api/app.py

Write-Host ''
Write-Host 'Flask API server stopped.' -ForegroundColor Red
pause
"@
    
    $flaskScript | Out-File -FilePath "${env:TEMP}\start_flask.ps1" -Encoding UTF8
    Start-Process powershell -ArgumentList "-NoExit", "-File", "${env:TEMP}\start_flask.ps1"
}

# Function to start React frontend in a new window
function Start-ReactFrontend {
    Write-Host "[INFO] Starting React Frontend..." -ForegroundColor Cyan
    $frontendPath = Join-Path $PROJECT_ROOT "frontend"
    
    # Check if node_modules exists
    $nodeModules = Join-Path $frontendPath "node_modules"
    if (-Not (Test-Path $nodeModules)) {
        Write-Host "[INFO] Installing frontend dependencies (first time only)..." -ForegroundColor Yellow
        $installScript = @"
Write-Host 'Installing Node.js dependencies...' -ForegroundColor Yellow
cd '$frontendPath'
npm install

if (`$LASTEXITCODE -eq 0) {
    Write-Host ''
    Write-Host 'Dependencies installed successfully!' -ForegroundColor Green
    Write-Host 'Starting React development server...' -ForegroundColor Green
    Write-Host 'The app will open at http://localhost:3000' -ForegroundColor Cyan
    Write-Host 'Press Ctrl+C to stop the server' -ForegroundColor Yellow
    Write-Host ''
    npm start
} else {
    Write-Host ''
    Write-Host 'Failed to install dependencies!' -ForegroundColor Red
    pause
}
"@
        $installScript | Out-File -FilePath "${env:TEMP}\start_react.ps1" -Encoding UTF8
        Start-Process powershell -ArgumentList "-NoExit", "-File", "${env:TEMP}\start_react.ps1"
    } else {
        $reactScript = @"
Write-Host 'Starting React development server...' -ForegroundColor Green
Write-Host 'The app will open at http://localhost:3000' -ForegroundColor Cyan
Write-Host 'Press Ctrl+C to stop the server' -ForegroundColor Yellow
Write-Host ''

cd '$frontendPath'
npm start

Write-Host ''
Write-Host 'React server stopped.' -ForegroundColor Red
pause
"@
        $reactScript | Out-File -FilePath "${env:TEMP}\start_react.ps1" -Encoding UTF8
        Start-Process powershell -ArgumentList "-NoExit", "-File", "${env:TEMP}\start_react.ps1"
    }
}

# Start both servers
Write-Host "[INFO] Launching servers in separate windows..." -ForegroundColor Cyan
Write-Host ""

Start-Sleep -Seconds 1
Start-FlaskAPI
Start-Sleep -Seconds 2
Start-ReactFrontend

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Servers Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Flask API:      http://localhost:5000" -ForegroundColor Cyan
Write-Host "React Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Two new PowerShell windows have opened." -ForegroundColor Yellow
Write-Host "Close those windows to stop the servers." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
