@echo off
REM Run Camera Preview Script - Starts both ESP32 data viewer and camera preview
REM This opens two WSL windows to monitor ESP32 serial output

echo ============================================
echo Testing XIAO ESP32S3 Camera via USB Serial
echo ============================================
echo.

REM Start ESP32 Camera Bootloader viewer
echo ============================================
echo Testing XIAO ESP32S3 Camera via USB Serial
echo Using baud rate: 115200 (matching ESP32 firmware)
echo ============================================
echo.
echo Starting ESP32 debug viewer (shows raw bytes)...
python3 cam_preview_debug.py COM5

REM Keep this terminal open so you can see ESP32 status messages
REM Press Ctrl+C to exit

REM Keep this terminal open so you can monitor both scripts
REM Close either window - the other will stay running
