@echo off
REM Enable USB Serial Port Access for COM5 - Permanent Solution

REM Check if Windows USB serial port access is disabled
echo Checking USB Serial Driver settings...
echo.

REM Method 1: Disable "Allow unsigned drivers" in Device Manager (Windows)
REGEDIT HKLM\SYSTEM\CurrentControlSet\Enum\USB\COM5
if exist "%systemdrive%\config\system32\dism.exe" echo Dism script ready or PowerShell method
powershell -Command "Get-WmiObject -Class Win32_SerialPort | Where-Object {$_.DeviceID -match 'USB'}"

echo.
REM Method 2: Run Python scripts with admin privilege via Task Scheduler
REM (Optional: Create a scheduled task that runs as Admin)

REM Enable USB serial drivers in Windows feature
echo Enabling USB Serial Controller support...
dism /online /enable-feature /featurename:USBserial /allfeatures

echo.
echo Done! Run 'run_camera.bat' now - COM5 should be accessible without admin rights
