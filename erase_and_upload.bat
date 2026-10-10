@echo off
REM Script to Erase ESP32 Flash and Upload esp32_camera.cpp
REM This clears all files from the XIAO ESP32S3 board

echo ============================================
echo Erasing ESP32 Flash Memory...
echo Board: XIAO ESP32S3 Camera (COM5)
echo Using PlatformIO to erase + upload
echo ============================================
echo.

REM Wait for user confirmation
set /p CONFIRM="Continue? (Y/N): "
if not "%CONFIRM%"==*"GOTO SKIP"
GOTO SKIP

REM Erase flash memory completely
echo.
echo Running PlatformIO command: platformio run --command erase-flash
platformio run --command erase-flash > C:\Users\Jerry Benenett\documents\Programming Stuff\image_draw\erase_output.log 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Flash erased successfully!
) else (
    echo.
    echo PlatformIO command failed, checking log...
    type C:\Users\Jerry Benenett\documents\Programming Stuff\image_draw\erase_output.log
)

GOTO DONE

:SKIP
echo.
echo Cancelled by user

:DONE
REM Exit
exit
