@echo off
title TTS Studio
cd /d "%~dp0"

echo.
echo  Installing dependencies (first run only)...
call npm install --silent

echo.
echo  Starting TTS Studio...
echo  Open your browser to: http://localhost:3737
echo.
start "" http://localhost:3737
node server.js
pause
