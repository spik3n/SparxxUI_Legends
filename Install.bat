@echo off
REM Runs the SparxxUI installer. Uses Windows PowerShell (built in) - no Python needed.
powershell -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0install.ps1"
if errorlevel 1 pause
pause
