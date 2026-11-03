@echo off
setlocal

set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: uv belum terinstall atau tidak ada di PATH.
    exit /b 1
)

echo Memulai RuanMei App di port 80...
uv run streamlit run ./src/main.py --server.port 80