@echo off
REM Camera Feed for ESP32 via USB Serial
REM Run this script as Administrator once, or enable admin access permanently below

REM Option 1: Quick run with Admin (run this file from PowerShell/Command Prompt as Admin)
REM option 2: Enable permanent admin access in Windows
REM    1. Run Device Manager → Universal Serial Bus controllers → right-click XIAO ESP32S3 COM5
REM       Properties → Access tab → "Allow administrator to access" ✓

echo ============================================
echo Camera Feed for ESP32 via USB Serial (COM5)
echo ============================================
echo.
echo Running Python scripts with admin access...
echo.

REM Launch both camera preview windows
python3 cam_preview_debug.py COM5 & python3 cam_preview.py COM5

echo.
echo === Camera feed windows opened! ===
echo ESP32's built-in OLED should show live video
echo Press 'q' in each terminal to exit
echo ============================================
