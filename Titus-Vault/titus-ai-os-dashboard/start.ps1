# Titus AI OS Dashboard Startup Script
# Run this to start both API and frontend servers

Write-Host "Starting Titus AI OS Dashboard..." -ForegroundColor Cyan

# Check if Python is available
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Install API dependencies
Write-Host "Installing API dependencies..." -ForegroundColor Yellow
cd api
pip install -r requirements.txt -q

# Start API server in background
Write-Host "Starting API server on port 8000..." -ForegroundColor Green
Start-Process python -ArgumentList "-m", "uvicorn", "main:app", "--reload", "--port", "8000" -WindowStyle Minimized

# Wait for API to start
Start-Sleep -Seconds 3

# Start frontend server
Write-Host "Starting frontend server on port 3000..." -ForegroundColor Green
cd ../frontend
Start-Process python -ArgumentList "-m", "http.server", "3000" -WindowStyle Minimized

Write-Host ""
Write-Host "Dashboard is running!" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  API:      http://localhost:8000" -ForegroundColor White
Write-Host "  Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop servers" -ForegroundColor Yellow
