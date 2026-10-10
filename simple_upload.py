"""
Alternative Upload Method Using Arduino CLI (If PlatformIO Fails)
Usage: python3 simple_upload.py
Or run via: Run this file from VS Code or command prompt
"""

import subprocess
import sys
import os

# Get current working directory and ensure we're in the right folder
if len(sys.argv) > 1:
    project_path = sys.argv[1]
    cwd = os.path.abspath(project_path)
else:
    cwd = os.getcwd()

cpp_files = [f for f in os.listdir(cwd) if f.endswith('.cpp')]
if not any('esp32_camera' in f for f in cpp_files):
    print(f"Error: No esp32_camera.cpp file found in {cwd}")
    print("Files in folder:", cpp_files)
    sys.exit(1)

print("=" * 60)
print("ESP32 Upload Script - XIAO ESP32S3 Camera")
print("=" * 60)
print(f"Project directory: {cwd}")
print(f"Target COM port: COM5 (Windows)")
print(f"Baud rate: 115200 (matching esp32_camera.cpp)")
print("=" * 60)

# Try PlatformIO first if available
if sys.platform == 'win32':
    print("\nTrying to find PlatformIO...")

    pio_paths = [
        r"C:\Users\Jerry Benenett\AppData\Local\PlatformIO\platformio.exe",
        r"C:\Program Files\PlatformIO\platformio.exe",
    ]

    found_pio = False
    for path in pio_paths:
        try:
            f = open(path, 'rb')
            f.read(1024)
            f.close()
            print("Found PlatformIO at:", path)
            found_pio = True
            break
        except FileNotFoundError:
            continue

    if found_pio:
        print("\nAttempting upload with PlatformIO...")

        com_port = "COM5"

        result = subprocess.run([
            'platformio', 'run', '-C', os.path.abspath(cwd)
        ], timeout=300, capture_output=True, text=True)

        if result.returncode == 0:
            print("\nUpload completed successfully!")
            print("Expected output on ESP32:")
            print("  - 'Serial port opened successfully!'")
            print("  - 'Camera initialized'")
            print("  - 'Starting camera capture...'")
        else:
            print("\nPlatformIO upload failed:")
            print(result.stdout[:1000])

# If PlatformIO fails or not available, try arduino-cli
print("\nChecking for arduino-cli...")

try:
    import arduino_cli
    print("arduino-cli is installed\n")

    fqbn = "esp32:esp32s3:xiao-esp32-s3-cam-v1.0"

    result = subprocess.run([
        'arduino-cli', 'upload', '--fqbn', fqbn,
        '--port', com_port,
        os.path.join(cwd, 'esp32_camera.cpp')
    ], timeout=300, capture_output=True, text=True)

    if result.returncode == 0:
        print("Arduino CLI upload successful!")
    else:
        print("\nArduino CLI upload failed:")
        print(result.stdout[:1000])

except ImportError:
    print("arduino-cli not installed")
    print("Manual installation required from: https://arduino-cli.io")

# Manual instructions
print("\n" + "=" * 60)
print("If you need to upload manually:")
print("=" * 60)

upload_text = ("""
Via VS Code PlatformIO Extension:
1. Install PlatformIO IDE extension in VS Code
2. Connect XIAO ESP32S3 via USB-C (powered ON)
3. Open PlatformIO Console (>) button in bottom-right
4. Run: platformio run -C C:\\Users\\Jerry Benenett\\documents\\Programming Stuff\\image_draw

Via Arduino CLI command prompt:
arduino-cli upload --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 \\
  --port COM5 esp32_camera.cpp

---

Expected ESP32 Serial Output (after successful upload):
--------------------------------------------------------
Connecting to COM5 at 115200 baud...
Serial port opened successfully!
Camera initialized
Starting camera capture...

Your cam_preview_debug.py should then show:
--------------------------------------------------------
--- RAW DATA (first 100 bytes) ---
   0: 43616d6572612063617... 'Camera cap...'
    ^ START marker (5 bytes)

If you see "ERROR DETECTED" instead, check baud rates!
========================================================="""
)

print(upload_text)
