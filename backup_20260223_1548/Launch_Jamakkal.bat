@echo off
echo Starting Jamakkal Prasna Application...

:: Kill existing processes on the ports just in case
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8999') do taskkill /f /pid %%a 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3999') do taskkill /f /pid %%a 2>nul

echo Starting Backend...
start /b cmd /c "cd /d backend && python main.py"

echo Starting Frontend...
start /b cmd /c "cd /d frontend && npm run dev"

echo Waiting for servers to initialize...
timeout /t 5 /nobreak > nul

echo Opening Jamakkal Prasna in browser...
start http://localhost:3999

echo Application is running!
pause
