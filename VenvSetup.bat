@echo off
setlocal

where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: uv is not installed or not in PATH.
    exit /b 1
)

uv venv

:WAIT_LOOP
if not exist ".venv\Scripts\activate.bat" (
    timeout /t 1 /nobreak >nul
    goto WAIT_LOOP
)

call .venv\Scripts\activate.bat