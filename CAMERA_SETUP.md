# XIAO ESP32S3 Camera Bootloader Setup Guide

## 🎯 Purpose

Enable camera capture on **XIAO ESP32S3** with OV7670/OV5640 sensor, streaming MJPEG frames via USB serial to Raspberry Pi (WSL).

---

## 📋 Hardware Setup

### Connection
```
┌─────────────────┐   ┌─────────────────────┐
│ XIAO ESP32S3    │   │ Raspberry Pi        │
│                  │   │                      │
│ USB-A to C cable│──▶│ USB port            │
│                  │   │ (any USB-C or A)   │
└─────────────────┘   └─────────────────────┘
```

### XIAO ESP32S3 CAM Module Pinout
| Pin | Function | Description |
|-----|----------|-------------|
| P29 | CAM_S | Camera Select (CAM_S) |
| P30 | SCL_I2C | I2C Clock for sensor |
| P31 | D_CAM | Camera DOUT data output |
| P32 | SPI_CS | SPI camera chip select |

---

## 📂 Project Files

### ESP32 Side (`esp32_camera.cpp`)
- Captures MJPEG frames from OV7670/OV5640 sensor
- Sends to Pi over USB serial (115200 baud)
- Optional: Save images locally as `ESP_CAMERA_SAVED_IMAGE.bmp`

### Pi Side (`cam_preview.py`)
- Opens USB serial connection
- Receives MJPEG stream from ESP32
- Decodes and displays frames with OpenCV window

---

## 🚀 Running on Raspberry Pi (WSL2)

### 1. Check Serial Port Detection
```bash
# List available serial ports on WSL/Ubuntu
ls -l /dev/ttyACM*  # For XIAO ESP32S3 over USB-C
# or
ls -l /dev/ttyUSB0 # Alternative if not detected as ACM

# Windows Host side (alternative)
python3 -c "import serial; from serial.tools import list_ports; [print(f'{p}: {p.device}') for p in list_ports.comports()]"
```

### 2. Start Camera Preview Script
```bash
# On Pi side (WSL/WSL2 terminal)
python3 cam_preview.py /dev/ttyACM0  # Default serial port on Pi

# Or Windows host side
python3 cam_preview.py COM5           # Adjust to actual COM port number
```

### 3. Upload ESP32 Sketch

**Arduino CLI method:**
```bash
arduino-cli core install esp32 @espressif:esp32
arduino-cli upload --fqbn esp32:esp32s3:xiao-esp32-s3-cam-v1.0 esp32_camera.cpp
```

**PlatformIO method:**
- Install PlatformIO IDE in VS Code
- Upload via Arduino IDE or PlatformIO CLI

---

## 🔧 Configuration Files

### `cam_preview.py` Settings
- Default port: `COM5` (Windows) / `/dev/ttyACM0` (Pi WSL)
- Baud rate: 921600 (standard for ESP32 Camera Bootloader)
- MJPEG protocol: Handles partial frames until `0xD9` marker

### `esp32_camera.cpp` Settings
- Default port: `/dev/ttyACM0` (Pi side) or `COM5` (Windows)
- Baud rate: 115200 (USB serial speed)
- Camera sensor: OV7670/OV5640 via XIAO pinout

---

## 🔍 Expected Protocol Flow

**ESP32 → Pi (MJPEG Stream):**

1. ESP32 acquires frame from camera sensor (MJPG format)
2. Sends MJPEG data over USB serial to Pi
3. Pi receives stream and decodes frames via OpenCV
4. Frames displayed in real-time window ("XIAO Camera Feed")

---

## 📸 Testing Locally on Windows Host

The `cam_preview.py` script works on:
- **WSL/WSL2**: Using `/dev/ttyACM0` or `/dev/ttyUSB0`
- **Windows host**: Using actual COM port (e.g., `COM5`)

This allows testing the camera streaming **without** needing a Raspberry Pi first.

---

## 🔍 Troubleshooting

### "No EOL" Errors
| Issue | Solution |
|-------|----------|
| Grey/blank display | Verify baud rate matches ESP32 (921600 vs 115200) |
| No output at all | Check port number and serial connection |
| "Incomplete payload" | Ensure camera is active on ESP32 board |

### USB Serial Issues
| Issue | Solution |
|-------|----------|
| "Failed to open port" | XIAO must be powered via USB-C before connecting |
| Port not showing up | Check Device Manager (Windows) or `ls /dev/ttyACM*` |
| Wrong baud rate | Scripts default to 921600/115200, adjust as needed |

---

## 📝 License

MIT License - See individual project files for full terms.

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
