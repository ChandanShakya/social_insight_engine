@echo off
echo Starting Social Insight Engine...

:: Start Backend
echo Starting Backend...
start cmd /k "cd backend && python -m uvicorn main:app --reload"

:: Start Frontend
echo Starting Frontend...
start cmd /k "cd Frontend && npm run dev"

echo Process started in new windows.

:: Open Chrome
echo Opening Chrome...
start chrome "http://localhost:5173"

echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
pause
