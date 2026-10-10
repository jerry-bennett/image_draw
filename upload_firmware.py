"""
Upload esp32_camera.cpp to XIAO ESP32S3 Camera via PlatformIO
"""

import subprocess
import sys
import os

def erase_flash():
    """Erase all flash memory from ESP32"""
    print("🧹 Erasing ESP32 flash memory...")

    # Use PlatformIO's erase-flash command if available
    try:
        result = subprocess.run([
            'platformio', 'run', '--command', 'erase-flash'
        ], timeout=60, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Flash erased successfully")
            return True
        else:
            print("⚠ PlatformIO erase command returned:", result.returncode)
            print(result.stdout[:500] if result.stdout else "No output")
            return False

    except FileNotFoundError:
        print("⚠ PlatformIO not found - trying Arduino CLI...")

    # Fall back to arduino-cli if PlatformIO unavailable
    try:
        result = subprocess.run([
            'arduino-cli', 'upload', '--fqbn',
            'esp32:esp32s3:xiao-esp32-s3-cam-v1.0',
            '--port', '/dev/ttyUSB0',
            esp32_camera.cpp
        ], timeout=180, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Arduino CLI erase successful")
            return True
    except FileNotFoundError:
        pass

    return False

def upload_sketch():
    """Upload esp32_camera.cpp to the ESP32"""
    print("📤 Uploading esp32_camera.cpp...")

    try:
        result = subprocess.run([
            'platformio', 'run'
        ], timeout=180, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Upload successful via PlatformIO")
            return True
        else:
            print("⚠ PlatformIO upload returned:", result.returncode)
            print("Output:")
            print(result.stdout[:1000] if result.stdout else "No output")
            print(result.stderr[:500] if result.stderr else "")
            return False

    except FileNotFoundError:
        # Fall back to arduino-cli
        try:
            result = subprocess.run([
                'arduino-cli', 'upload', '--fqbn',
                'esp32:esp32s3:xiao-esp32-s3-cam-v1.0',
                '--port', '/dev/ttyUSB0'
            ], timeout=180, capture_output=True, text=True)

            if result.returncode == 0:
                print("✓ Arduino CLI upload successful")
                return True
            else:
                print("⚠ Arduino CLI returned:", result.returncode)

        except FileNotFoundError:
            pass

    return False

if __name__ == '__main__':
    # Get current working directory
    cwd = os.getcwd()

    # Ensure we're in the right project folder
    if not os.path.exists(os.path.join(cwd, 'esp32_camera.cpp')):
        print(f"Error: esp32_camera.cpp not found in {cwd}")
        print("Please open this directory in VS Code first")
        sys.exit(1)

    # Run upload via PlatformIO or Arduino CLI
    success = upload_sketch()

    if success:
        print("\nUPLOAD COMPLETE!")
        print("You should see:")
        print("  - 'Serial port opened successfully!' from ESP32")
        print("  - 'Camera initialized' message")
        print("  - 'Starting camera capture...' on XIAO ESP32S3")
    else:
        print("\n❌ Upload failed, trying manual VS Code PlatformIO upload...")
        print("\nTo try manually:")
        print("1. Open VS Code with this project folder")
        print("2. Install PlatformIO IDE extension if not already installed")
        print("3. Click the PlatformIO button in bottom-right corner")
        print("4. Run: platformio run --path .\\esp32_camera.cpp")
