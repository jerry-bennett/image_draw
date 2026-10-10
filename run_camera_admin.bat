@echo off
REM Run Camera Preview Script with Admin Access - Required for USB Serial (COM5)

REM Start ESP32 debug script with admin privileges
echo ============================================
echo Testing XIAO ESP32S3 Camera via USB Serial
echo (Run with Admin Access Required)
echo ============================================
echo.

REM Launch Python scripts as Administrator
python3 --version & python3 cam_preview_debug.py COM5 & python3 cam_preview.py COM5

REM Keep windows open until you press Ctrl+C in each terminal
pause
