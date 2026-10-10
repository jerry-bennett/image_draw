# How to Upload ESP32 Firmware Using VS Code (Without PlatformIO/Arduino CLI)

---

## The Problem

- Your XIAO ESP32S3 Camera module uses pins for OV7670/OV5640 camera sensor that aren't in PlatformIO's default board definitions
- `esp32_camera.cpp` is already written and configured correctly for your hardware

---

## Option 1: Use VS Code Arduino Extension (Recommended)

The VS Code "Arduino" extension can upload sketches without a platformio.ini file.

### Step 1: Install Arduino Extension

1. Open VS Code
2. Press `Ctrl + Shift + X` (Extensions panel)
3. Search for **"Arduino"** 
4. Install the Arduino IDE extension by Microsoft (not PlatformIO!)

### Step 2: Connect Your Board

Plug your XIAO ESP32S3 Camera via USB-C power cable, then connect to computer.

### Step 3: Upload in VS Code

1. In VS Code bottom-right, look for **Arduino** button (different from PlatformIO >)
2. Click it - Arduino extension opens its own terminal
3. Type: `platformio run` OR simply let Arduino handle the upload from your folder

**OR use this simpler command:**

```bash
arduino-cli upload --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 --port COM5 .\esp32_camera.cpp
```

---

## Option 2: Use VS Code's Terminal with Arduino CLI (Installed System-Wide)

If you have arduino-cli installed elsewhere on your system, use it directly:

**From Command Prompt:**
```cmd
arduino-cli.exe upload --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 --port COM5 C:\Users\Jerry Benenett\documents\Programming Stuff\image_draw\esp32_camera.cpp
```

---

## Option 3: PlatformIO - Create Custom Board Definition

I've created a custom board XML definition file (`.pio/packages/platformio-custom-boards/xiaoxiao-cam.xml`) for you.

### To Use PlatformIO Properly:

1. Install VS Code Extension: **"PlatformIO IDE" by Alexxico or PlatformIO**
2. Open this project folder in VS Code
3. In PlatformIO Console, run: `platformio run -C C:\Users\Jerry Benenett\documents\Programming Stuff\image_draw`
4. This should use your custom board definition

---

## Expected Output (After Upload)

Your ESP32 serial output should show:

```
Connecting to /dev/ttyUSB0 at 115200 baud... (or COM5)
Serial port opened successfully!       (from esp32_camera.cpp line 47-51)
Camera initialized                     (from esp32_camera.cpp line 64)
Starting camera capture...             (from esp32_camera.cpp line 68)
```

---

## Verify It Works - Run cam_preview_debug.py

After upload succeeds, run:

```batch
python3 cam_preview_debug.py COM5
```

You should see raw bytes from ESP32 starting with:

```
--- RAW DATA (first 100 bytes) ---
   0: 43616d6572612063617... 'Camera cap...'
    ^ START marker detected!
*** FOUND COMMUNICATION MARKER ***
```

---

## Key Configuration Files

| File | Purpose |
|------|---------|
| `esp32_camera.cpp` | Main firmware (already written for XIAO) |
| `platformio.ini` | PlatformIO config with custom board |
| `.pio/packages/.../xiaoxiao-cam.xml` | Custom board XML definition |
| `partitions_Bootloader.csv` | Flash partition scheme |

---

## If Upload Fails - Check baud rates

The ESP32 firmware uses **115200 baud** (line 40 in esp32_camera.cpp). Make sure your upload script and Python scripts use the correct rate.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
