@echo off
echo Starting Social Insight Engine...

:: Check if backend directory exists
if not exist "backend" (
    echo Error: backend directory not found!
    pause
    exit /b 1
)

:: Check if frontend directory exists
if not exist "Frontend" (
    echo Error: Frontend directory not found!
    pause
    exit /b 1
)

:: Start Backend
echo Starting Backend...
cd backend
start cmd /k "cd /d %cd% && venv\Scripts\python -m uvicorn main:app --reload"

:: Start Frontend
echo Starting Frontend...
cd ..\Frontend
start cmd /k "cd /d %cd% && npm run dev"

:: Return to root
cd ..

echo Process started in new windows.
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Opening browser...
timeout /t 2 >nul
start chrome "http://localhost:5173"

pause
