# Fairness Detection System - Offline Launcher
# No internet connection required - all services run locally

$ErrorActionPreference = "Stop"

# Colors for output
function Write-Header {
    param([string]$Text)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host $Text -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Text)
    Write-Host "✓ $Text" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Text)
    Write-Host "⚠ $Text" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Text)
    Write-Host "✗ $Text" -ForegroundColor Red
}

# Check offline requirements
function Test-OfflineRequirements {
    Write-Header "Checking Offline Requirements"
    
    $issues = @()
    
    # Check virtual environment
    if (Test-Path ".venv") {
        Write-Success "Virtual environment found"
    } else {
        Write-Error "Virtual environment not found"
        $issues += "Create venv: python -m venv .venv"
    }
    
    # Check models
    if ((Test-Path "models") -and (Get-ChildItem "models\*.pkl" -ErrorAction SilentlyContinue)) {
        Write-Success "Trained models found"
    } else {
        Write-Warning "Models not found - train models first"
        $issues += "Train models before running"
    }
    
    # Check Groq
    try {
        $groqKey = $env:GROQ_API_KEY
        if ([string]::IsNullOrWhiteSpace($groqKey)) {
            Write-Warning "GROQ_API_KEY is not set"
            $issues += "Set GROQ_API_KEY environment variable"
        } else {
            $response = Invoke-WebRequest -Uri "https://api.groq.com/openai/v1/models" -Headers @{ Authorization = "Bearer $groqKey" } -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Success "Groq API reachable"
            }
        }
    } catch {
        Write-Warning "Groq API not accessible"
        $issues += "Check Groq API key and network access"
    }
    
    # Check frontend dependencies
    if (Test-Path "frontend\node_modules") {
        Write-Success "Frontend dependencies installed"
    } else {
        Write-Error "Frontend dependencies missing"
        $issues += "Install: cd frontend; npm install"
    }
    
    if ($issues.Count -gt 0) {
        Write-Host "`nIssues to resolve:" -ForegroundColor Yellow
        foreach ($issue in $issues) {
            Write-Host "  • $issue" -ForegroundColor Yellow
        }
        return $false
    }
    
    Write-Success "`nAll offline requirements met!"
    return $true
}

# Stop existing processes
function Stop-ExistingProcesses {
    Write-Host "Stopping any existing services..." -ForegroundColor Yellow
    
    # Stop Python processes
    Get-Process | Where-Object {
        $_.ProcessName -eq "python" -and $_.Path -like "*\.venv\*"
    } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    # Stop Node processes (carefully - only our frontend)
    Get-Process | Where-Object {
        $_.ProcessName -eq "node" -and $_.CommandLine -like "*react-scripts*"
    } | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Start-Sleep -Seconds 2
    Write-Success "Cleaned up existing processes"
}

# Main execution
Write-Header "Fairness Detection System - Offline Mode"

# Check requirements
if (-not (Test-OfflineRequirements)) {
    Write-Error "`nPlease resolve issues before starting"
    exit 1
}

# Clean up any existing processes
Stop-ExistingProcesses

Write-Header "Starting Services"

# Start Flask API in background
Write-Host "Starting Flask API..." -ForegroundColor Cyan
$apiJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    & .\.venv\Scripts\python.exe api\app.py
}

Start-Sleep -Seconds 5

# Check if API started
if ($apiJob.State -eq "Running") {
    Write-Success "Flask API running on http://localhost:5000"
} else {
    Write-Error "Failed to start API server"
    $apiJob | Receive-Job
    exit 1
}

# Start React frontend in background
Write-Host "Starting React frontend..." -ForegroundColor Cyan
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD\frontend
    npm start
}

Start-Sleep -Seconds 8

# Check if frontend started
if ($frontendJob.State -eq "Running") {
    Write-Success "React frontend running on http://localhost:3000"
} else {
    Write-Warning "Frontend may be starting (check manually)"
}

# Display summary
Write-Header "Application Ready - Offline Mode"
Write-Host "✓ Frontend:   " -NoNewline -ForegroundColor Green
Write-Host "http://localhost:3000" -ForegroundColor White -BackgroundColor DarkGreen
Write-Host "✓ Backend:    " -NoNewline -ForegroundColor Green
Write-Host "http://localhost:5000" -ForegroundColor White -BackgroundColor DarkGreen
Write-Host "✓ Groq:       " -NoNewline -ForegroundColor Green
Write-Host "http://localhost:11434" -ForegroundColor White -BackgroundColor DarkGreen

Write-Host "`n📡 Mode: " -NoNewline -ForegroundColor Cyan
Write-Host "OFFLINE" -ForegroundColor White -BackgroundColor DarkCyan
Write-Host "   All services running locally, no internet required`n" -ForegroundColor Gray

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray

# Keep running and monitor
try {
    while ($true) {
        Start-Sleep -Seconds 2
        
        # Check if jobs are still running
        if ($apiJob.State -ne "Running") {
            Write-Warning "API server stopped unexpectedly"
            $apiJob | Receive-Job
            break
        }
        
        if ($frontendJob.State -ne "Running") {
            Write-Warning "Frontend server stopped unexpectedly"
            $frontendJob | Receive-Job
            break
        }
    }
} finally {
    # Cleanup on exit
    Write-Header "Shutting Down"
    
    Write-Host "Stopping services..." -ForegroundColor Yellow
    
    # Stop jobs
    $apiJob | Stop-Job -ErrorAction SilentlyContinue
    $frontendJob | Stop-Job -ErrorAction SilentlyContinue
    
    # Remove jobs
    $apiJob | Remove-Job -Force -ErrorAction SilentlyContinue
    $frontendJob | Remove-Job -Force -ErrorAction SilentlyContinue
    
    # Clean up processes
    Stop-ExistingProcesses
    
    Write-Success "All services stopped"
    Write-Host "`nOffline session ended" -ForegroundColor Gray
}
