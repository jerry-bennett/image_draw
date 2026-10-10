@echo off
REM Test ESP32 Camera Connection - Start ESP32 Debug Script (runs in new window)
REM This script starts the ESP32 serial data viewer in a fresh WSL window

REM Start ESP32 debug script with admin access
wsl python3 cam_preview_debug.py COM5
REM Wait for ESP32 to settle and show camera frame
timeout /t 10 /nobreak >nul

REM Now run camera preview script (separate window)
echo.
echo ================================
echo Starting Camera Preview in new WSL window...
echo Press 'q' to exit both windows
echo ================================
wsl python3 cam_preview.py COM5

REM Keep the command prompt open
echo.
pause >nul
