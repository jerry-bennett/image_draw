# Upload ESP32 Firmware Script for XIAO ESP32S3 Camera
# Usage: .\upload_esp32.ps1

Write-Host "=" * 60
Write-Host "ESP32 Upload Script - XIAO ESP32S3 Camera"
Write-Host "=" * 60

$ProjectPath = Get-Location -ErrorAction SilentlyContinue
if ($ProjectPath -eq $null) {
    Write-Host "Error: Could not determine project path. Please run from project folder."
    exit 1
}

# Find esp32_camera.cpp in this folder
$CppFile = Join-Path $ProjectPath 'esp32_camera.cpp'
if (!(Test-Path $CppFile)) {
    Write-Host "Error: esp32_camera.cpp not found in $($ProjectPath.FullName)"
    exit 1
}

Write-Host "Project directory: $($ProjectPath.FullName)"
Write-Host "Target COM port: COM5"
Write-Host "Baud rate: 115200 (matching esp32_camera.cpp)"
Write-Host "=" * 60

# Try PlatformIO first
Write-Host "`nTrying to find PlatformIO...`n"

$PioPath = Get-ChildItem -Path "$env:LOCALAPPDATA\PlatformIO\platformio.exe", `
             "C:\Program Files\PlatformIO\platformio.exe" -ErrorAction SilentlyContinue | Where-Object { $_ } | Select-Object -First 1

if ($PioPath) {
    Write-Host "Found PlatformIO at: $($PioPath.FullName)`n"

    Write-Host "Attempting upload with PlatformIO...`n"

    $Output = & "$PioPath.FullName run" -C $ProjectPath.FullName 2>&1 | Out-String

    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Upload completed successfully!"
    } else {
        Write-Host "✗ PlatformIO upload failed."
        Write-Host $Output[:500]
    }
} else {
    Write-Host "PlatformIO not found on this system`n"
    Write-Host "Please install via VS Code Extensions or use arduino-cli next`n"
}

# Check for arduino-cli
$ArduCli = Get-Command arduino-cli -ErrorAction SilentlyContinue

if ($ArduCli) {
    Write-Host "arduino-cli found!"

    $Output = & "$ArduCli.exe upload" `
              --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 `
              --port COM5 `
              $CppFile 2>&1 | Out-String

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ arduino-cli upload successful!"
    } else {
        Write-Host "✗ arduino-cli upload failed:"
        Write-Host $Output[:500]
    }
} else {
    Write-Host "⚠ arduino-cli not found"
}

# Expected output from ESP32 after successful upload
Write-Host "`n=========================================================="
Write-Host "Expected ESP32 Serial Output (after upload):"
Write-Host "--------------------------------------------------------"
Write-Host "Connecting to /dev/ttyUSB0 at 115200 baud...        or COM5"
Write-Host "Serial port opened successfully!                     (from esp32_camera.cpp)"
Write-Host "Camera initialized                                    (from esp32_camera.cpp)"
Write-Host "Starting camera capture...                            (from esp32_camera.cpp)"
Write-Host "--------------------------------------------------------"
