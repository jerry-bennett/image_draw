# image_draw

A simple e-Paper (e-ink) display control system for Raspberry Pi with touch button interface.

## 🎯 Purpose

Control an e-paper display from a **Raspberry Pi** using a **touch button controller** on a **XIAO ESP32S3** board. The system supports:
- Single image display (long press > 3s)
- Clear screen (double tap within 0.4s)

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
├── esp32_camera.cpp                 # ESP32 camera sketch (optional)
└── cam_preview.py                   # Camera preview on Pi (optional)
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

**ESP32 Sketch:** `esp32_camera.cpp`
**Pi Preview Script:** `cam_preview.py`

See [CAMERA_SETUP.md](CAMERA_SETUP.md) for detailed instructions.

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
```

---

## 🔍 Troubleshooting

### Grey Screen / No Output
| Issue | Solution |
|-------|----------|
| Grey screen on e-ink | Check e-Paper display is powered on (check DC/CS pins) |
| Button not responding | Verify serial port number matches actual COM/ttyACM0 |
| Image not displaying | Check image dimensions match e-paper (400×600) |

### USB Serial Issues
| Issue | Solution |
|-------|----------|
| "Failed to open port" | Check Windows Device Manager or `ls -l /dev/ttyACM*` on WSL |
| Wrong baud rate | Set to 115200 (default in scripts) |
| Missing COM ports | Ensure XIAO ESP32S3 is powered and connected |

### e-Paper Display Issues
| Issue | Solution |
|-------|----------|
| Black screen on startup | Check reset pin timing in `waveshare_epd/epdconfig.py` |
| Image corrupted | Verify BMP file exists in `/pic/` directory |

---

## 📝 License

MIT License - See individual project files for full terms.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
