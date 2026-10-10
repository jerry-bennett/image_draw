@echo off
REM Run Camera Preview Script - Starts both ESP32 data viewer and camera preview
REM This opens two WSL windows to monitor ESP32 serial output

echo ============================================
echo Testing XIAO ESP32S3 Camera via USB Serial
echo ============================================
echo.

REM Start ESP32 debug script (monitors raw bytes coming from ESP32)
echo Starting ESP32 data viewer...
python3 cam_preview_debug.py COM5

REM Wait for ESP32 to initialize and send camera frame
timeout /t 10 /nobreak >nul

REM Now run camera preview script with OpenCV display
echo.
echo ============================================
echo Starting Camera Preview in new window...
echo Press 'q' to exit
echo ============================================
python3 cam_preview.py COM5

REM Keep this terminal open so you can monitor both scripts
REM Close either window - the other will stay running
