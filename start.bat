@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo       SearchTrust ML Startup Script       
echo ==========================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python first.
    pause
    exit /b 1
)

:: 2. Setup Python Environment
echo [1/5] Checking Python Virtual Environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing backend dependencies...
    .\venv\Scripts\pip.exe install -r requirements.txt
) else (
    echo Virtual environment already exists.
)

:: 3. Check pnpm
echo [2/5] Checking Frontend Package Manager (pnpm)...
call pnpm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pnpm is not installed. Installing pnpm globally via npm...
    call npm install -g pnpm
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install pnpm. Please ensure Node.js and npm are installed.
        pause
        exit /b 1
    )
)

:: 4. Setup Frontend Environment
echo [3/5] Checking Frontend Dependencies...
cd frontend
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call pnpm install
) else (
    echo Frontend dependencies already installed.
)
cd ..

:: 5. Run Backend Tests
echo [4/5] Running Backend Tests...
.\venv\Scripts\python.exe -m pytest backend/tests/
if %errorlevel% neq 0 (
    echo [WARNING] Some backend tests failed!
    echo Press any key to continue launching anyway, or Ctrl+C to cancel.
    pause
) else (
    echo All tests passed!
)
echo.

:: 6. Launch Services
echo [5/5] Launching Services...
echo.
echo Starting FastAPI Backend on Port 8000...
start "SearchTrust ML - Backend" cmd /k ".\venv\Scripts\activate.bat && set PYTHONPATH=. && uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload"

echo Starting React Frontend on Port 5173...
start "SearchTrust ML - Frontend" cmd /k "cd frontend && pnpm run dev"

echo.
echo ==========================================
echo Services are starting up in separate windows.
echo - Backend API: http://127.0.0.1:8000/docs
echo - Frontend UI: http://localhost:5173/
echo ==========================================
echo.
echo Opening browser...
timeout /t 3 /nobreak >nul
start http://localhost:5173/

pause
