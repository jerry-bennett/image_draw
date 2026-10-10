# image_draw

A simple e-Paper (e-ink) display control system for Raspberry Pi with touch button interface and camera streaming support.

## 🎯 Purpose

Control an e-paper display from a **Raspberry Pi** using a **touch button controller** on a **XIAO ESP32S3** board. The system supports:
- Single image display (long press > 3s)
- Clear screen (double tap within 0.4s)
- Live camera preview via USB serial (ESP32 sends MJPEG frames to Pi)

---

## 📋 Hardware Setup

### Raspberry Pi Side
| Component | Description |
|-----------|-------------|
| e-Paper Display | 4" (400×600), 7-color dithering |
| Waveshare EPD Driver | Python SDK in `lib/waveshare_epd/` |

### Controller Side (XIAO ESP32S3)
| Component | Description |
|-----------|-------------|
| XIAO ESP32S3 CAM Board | Arduino-compatible, USB serial over WSL |
| Touch Button | BCM pin 26 (physical pin 37) |
| Built-in OLED | 0.96" (128x64), camera preview display |

### Connection
- Connect XIAO ESP32S3 to Pi via **USB-C cable**
- Ensure XIAO is powered on before connecting

---

## 📂 Project Structure

```
image_draw/
├── lib/waveshare_epd/              # e-Paper driver library
│   ├── epd4in0e.py                 # 4" display class (400×600)
│   ├── epdconfig.py                 # GPIO/SPI abstraction
│   └── DEV_Config_*.so             # Hardware driver binaries
├── pic/                             # Image storage
│   ├── 01.bmp                      # Sample image
│   └── Font.ttc                    # Font file
├── image_draw.py                    # Main display script
├── clear.py                         # Clear screen script
├── button_trigger.py                # USB button controller
│
# ESP32 Camera Bootloader Sketches (USB serial + MJPEG streaming)
├── esp32_camera.cpp                 # Primary camera sketch - sends frames via USB
├── esp32_simple.cpp                  # Simple OLED preview sketch on XIAO board
├── esp32_camera_test.cpp             # Debug/monitor mode sketch
├── esp32_camera_v2.cpp               # MJPEG stream with START handshake
└── esp32_camera_v3.cpp               # Optimized MJPEG streaming (REV 3)
│
# Camera preview & debugging scripts on Pi
├── cam_preview.py                    # OpenCV camera preview in window
├── cam_preview_debug.py              # Raw data inspector for ESP32 boot mode
│
# Windows batch files
├── camera_feed.bat                    # Run camera feed with admin access
├── run_camera.bat                     # Quick camera test (dual windows)
├── test_camera.bat                    # Test via WSL
├── run_camera_admin.bat               # Admin-privileged camera run
└── enable_admin_usb.bat               # Enable permanent USB admin access
│
# Utilities
├── check_usb.py                      # Quick USB serial port checker
├── converter.py                       # BMP to e-Paper color converter
├── env_refresh.ps1                    # PowerShell environment refresh script
└── button listener instructions.txt   # Button trigger setup guide
```

---

## 🚀 Quick Start (Raspberry Pi Side)

### 1. Install Dependencies

On Raspberry Pi (WSL2):
```bash
# Install Waveshare e-Paper SDK
pip install opencv-python numpy pyserial spidev gpiozero

# Clone/Download this project to `/home/pi/image_draw`
cd /home/pi/image_draw
```

### 2. Button Trigger Configuration

The touch button is configured on **BCM pin 26** (physical pin 37):
- **Hold > 3 seconds**: Display an image from `pic/01.bmp`
- **Double tap (< 0.4s between presses)**: Clear the screen

### 3. Running on Pi

```bash
# Start button controller (runs continuously, waiting for events)
python3 /home/pi/image_draw/button_trigger.py

# Start display script (when hold triggered)
python3 /home/pi/image_draw/image_draw.py
```

### 4. Camera Integration (Optional/Future)

For XIAO ESP32S3 camera capture:

**ESP32 Sketch:** `esp32_camera.cpp` or `esp32_camera_v3.cpp`
**Pi Preview Script:** `cam_preview.py`
**Debug Tool:** `cam_preview_debug.py`

See [CAMERA_SETUP.md](CAMERA_SETUP.md) for detailed instructions.

---

## 🛠️ Building & Running on Windows Host

### Step 1: Verify Serial Port
```bash
# List available COM ports
python3 -c "import serial; from serial.tools import list_ports; [print(f'{p}: {p.device}') for p in list_ports.comports()]"

# Quick USB check (sees if ESP32 is sending data)
python3 check_usb.py  # Uses default COM5
```

### Step 2: Enable Admin Access (If Needed)

Some ESP32 boards require admin privileges to access the USB serial port:
```bash
# Permanently enable admin access for COM5
enable_admin_usb.bat

# Or set via Device Manager:
# 1. Open Device Manager → Universal Serial Bus controllers
# 2. Right-click XIAO ESP32S3 → Properties → Access tab
# 3. Check "Allow administrator to access"
```

### Step 3: Upload ESP32 Sketch

**Arduino CLI method:**
```bash
arduino-cli core install esp32 @espressif:esp32
arduino-cli upload --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 esp32_camera.cpp
```

**PlatformIO method:**
- Install PlatformIO IDE in VS Code
- Upload sketch via Arduino IDE or PlatformIO CLI

### Step 4: Run Camera Feed

**Option A: Quick run (dual Windows windows)**
```bash
# Starts both ESP32 debug viewer and camera preview
run_camera.bat
```

**Option B: With admin access (recommended for some boards)**
```bash
# Run as Administrator, starts camera feed
camera_feed.bat
```

**Option C: Via WSL**
```bash
test_camera.bat
```

---

## 🖥️ Camera Feed Flow

```
┌─────────────────────────────┐
│    XIAO ESP32S3             │
│  ┌─────── Touch Button ────┤
│  │  ┌───────── OLED Preview┤
│  │  │     (0.96" 128x64)   │
│  │  └───── Camera Sensor───┤
│  │         (OV7670/5640)   │
│  └─── USB → Pi             │
│                             │
└─────────────────────────────┘
              │ (when hold > 3s)
              ▼
┌─────────────────────────────┐
│    Raspberry Pi (WSL)       │
│      cam_preview.py         │  ← Shows live MJPEG stream
│        button_trigger.py    │  ← Detects trigger events
│ └──→ e-Paper Display        │  ← Shows image from pic/01.bmp
└─────────────────────────────┘
```

**ESP32 → Pi Data Protocol:**
1. ESP32 captures MJPEG frame (OV7670/OV5640 sensor)
2. Sends `START` handshake (5 bytes)
3. Sends frame size (4-byte little-endian uint32)
4. Streams JPEG payload directly over USB serial
5. Pi receives and displays via OpenCV preview

---

## 📝 Configuration Files

### ESP32 Camera Sketches

| File | Purpose | Features |
|------|---------|----------|
| `esp32_camera.cpp` | Primary camera sketch | Full MJPEG streaming protocol |
| `esp32_simple.cpp` | OLED preview only | Shows frames on XIAO's built-in screen |
| `esp32_camera_test.cpp` | Debug/monitor mode | Basic frame output, sensor ID test |
| `esp32_camera_v2.cpp` | MJPEG stream v2 | START handshake protocol |
| `esp32_camera_v3.cpp` | Optimized streaming | REV 3 with callback-based capture |

### Python Scripts on Pi

| File | Purpose |
|------|---------|
| `cam_preview.py` | OpenCV camera preview (visual display) |
| `cam_preview_debug.py` | Raw byte inspector for ESP32 boot mode |
| `check_usb.py` | Quick serial port checker (COM5 default) |

### Windows Batch Files

| File | Purpose |
|------|---------|
| `camera_feed.bat` | Full camera feed with admin access |
| `run_camera.bat` | Quick test (dual windows - debug + preview) |
| `test_camera.bat` | Run via WSL command prompt |
| `run_camera_admin.bat` | Admin-privileged single session |
| `enable_admin_usb.bat` | Enable permanent USB admin access |

---

## 🔧 Configuration Files

### `button_trigger.py`
- Port configuration (default: Windows COM5, adjust to actual port)
- Double-tap threshold: 0.4 seconds
- Hold trigger time: 3 seconds

### `image_draw.py`
- Reads image from `/home/pi/image_draw/pic/01.bmp`
- Converts to 7-color palette for e-Paper display
- Uses SPI bus (config in `waveshare_epd`)

### `clear.py`
- Simple screen clearing utility

---

## 🛠️ Building & Running on Windows Host

### Step 1: Verify Serial Port
```bash
# List available COM ports
python3 -c "import serial; from serial.tools import list_ports; [print(f'{p}: {p.device}') for p in list_ports.comports()]"

# Run preview script
python3 cam_preview.py <COM_PORT>  # e.g., python3 cam_preview.py COM5
```

### Step 2: Upload ESP32 Sketch

**Arduino CLI method:**
```bash
arduino-cli core install esp32 @espressif:esp32
arduino-cli upload --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 esp32_camera.cpp
```

**PlatformIO method:**
- Install PlatformIO IDE in VS Code
- Upload sketch via Arduino IDE or PlatformIO CLI

### Step 3: Run Button Controller on Windows (Optional)
Test button detection locally before deploying to Pi:
```bash
python3 button_trigger.py <COM_PORT>
```

---

## 📸 Expected Flow

```
┌──────────────────────┐
│ XIAO ESP32S3         │
│ ┌─── Touch Button ───┤
│ └─── USB → Pi        │
│                     │
└──────────────────────┘
              │ (when hold > 3s)
              ▼
┌──────────────────────┐
│ Raspberry Pi (WSL)   │
│ button_trigger.py    │  → Run image_draw.py
│ └──→ e-Paper Display│  → Show pic/01.bmp
└──────────────────────┘

Camera Feed Flow:
┌─────────────────┐       ┌─────────────────┐
│ ESP32 OLED      │       │ OpenCV Window    │
│ Preview (local) │ ◄─────► │ cam_preview.py  │
└─────────────────┘       └────────┬──────────┘
                                    │ USB Serial (115200/921600)
                                    ▼
                               ┌─────────────────┐
                               │ Raw Data Viewer │
                               │ cam_preview_    │
                               │  debug.py        │
                               └─────────────────┘
```

---

## 🔍 Troubleshooting

### Grey Screen / No Output
| Issue | Solution |
|-------|-------------|
| Grey screen on e-ink | Check e-Paper display is powered on (check DC/CS pins) |
| Button not responding | Verify serial port number matches actual COM/ttyACM0 |
| Image not displaying | Check image dimensions match e-paper (400×600) |

### USB Serial Issues
| Issue | Solution |
|-------|-------------|
| "Failed to open port" | Check Windows Device Manager or `ls -l /dev/ttyACM*` on WSL |
| Wrong baud rate | Set to 115200 (default in scripts) or try 921600 for ESP32 bootloader |
| Missing COM ports | Ensure XIAO ESP32S3 is powered and connected |
| Port requires admin access | Run `enable_admin_usb.bat` or enable via Device Manager Access tab |

### ESP32 Camera Issues
| Issue | Solution |
|-------|-------------|
| No camera frames | Check OV7670/OV5640 sensor initialization in sketch |
| MJPEG stream broken | Verify START/size protocol matches between ESP32 and Pi scripts |
| XIAO OLED black screen | Check pin configuration (P29-P32) in sketch |

### e-Paper Display Issues
| Issue | Solution |
|-------|-------------|
| Black screen on startup | Check reset pin timing in `waveshare_epd/epdconfig.py` |
| Image corrupted | Verify BMP file exists in `/pic/` directory |
| Color artifacts | Ensure BMP is converted to 7-color palette before display |

---

## 📝 License

MIT License - See individual project files for full terms.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
