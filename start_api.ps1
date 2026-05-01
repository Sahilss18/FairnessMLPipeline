# Start Flask API with fresh Python environment
$env:PYTHONDONTWRITEBYTECODE = "1"
Set-Location -Path $PSScriptRoot
python api/app.py
