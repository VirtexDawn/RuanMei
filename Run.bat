@echo off
setlocal

:: Cek apakah uv tersedia
where uv >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: uv belum terinstall atau tidak ada di PATH.
    exit /b 1
)

:: Jalankan aplikasi PySide6
echo Memulai RuanMei Desktop App...
uv run python ./src/main.py