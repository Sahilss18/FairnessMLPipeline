# Start Flask API with virtual environment
$env:PYTHONDONTWRITEBYTECODE = "1"
Set-Location -Path $PSScriptRoot
& .\.venv\Scripts\python.exe api/app.py

