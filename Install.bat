@echo off
REM Runs the SparxxUI installer with a console window.
python "%~dp0install.py"
if errorlevel 1 pause
pause
