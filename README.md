# E-Ink Camera Viewer Project (Windows)

A hardware project that captures photos from a XIAO ESP32-S3 Sense camera board over WiFi, converts them to BMP format on a Raspberry Pi 3, and displays them on a Waveshare Spectra6 4-inch E-Ink display.

---

## 📋 Project Overview

This integrated system consists of three components working together:

1. **XIAO ESP32-S3 Sense** with pre-installed camera firmware that streams video over WiFi
2. **Raspberry Pi 3** running a Python script that captures JPEG frames from the ESP32, converts them to BMP, and displays them on an E-Ink display
3. **Waveshare Spectra6 4" E-Ink Display (E6)** connected to the Raspberry Pi for viewing captured photos

---

## 🔧 Hardware Components

| Component | Description |
|-----------|-------------|
| XIAO ESP32-S3 Sense | WiFi-enabled ESP32 board with OV5640/OV3660 camera sensor |
| Raspberry Pi 3 | Runs the camera capture and E-Ink display software |
| Waveshare Spectra6 E-Ink Display | 4-inch color e-ink display (E Ink Color HAT) |
| Custom Button | Soldered button on Pi to trigger photo capture |

---

## 📡 ESP32 Camera Stream

The XIAO ESP32-S3 Sense streams MJPEG video frames over HTTP at the following endpoint:

```
http://<ESP32_IP_ADDRESS>:8080/stream.txt
```

### ESP32 Setup Options

**Option A: WiFi Network (Recommended)**
- Connect ESP32 to your home WiFi network first
- Capture IP address from `ipconfig /all` on Windows

**Option B: Access Point Mode**
- Default SSID: `XIAO_ESP32S3_Sense`
- Default Password: `seeedstudio`
- Access point IP: Usually `192.168.4.1` (configurable)

---

## 🐛 Raspberry Pi Setup

The Raspberry Pi runs a Python script that:
1. Connects to the ESP32 camera stream over WiFi
2. Downloads JPEG frames continuously (~2 FPS)
3. Converts each frame to BMP format for E-Ink display
4. Renders the BMP on the Waveshare Spectra6 E-Ink display

### Prerequisites

#### Raspberry Pi OS Packages

```bash
# Install required packages
sudo apt update
sudo apt install -y rpi-camera libjpeg-dev python3-pip
pip3 install opencv-python Pillow scapy requests
```

#### Camera Interface Setup

Connect the Spectra6 E-Ink display to the Pi. Configure the Raspberry Pi Camera module to use your E-Ink display interface:

```bash
# Set up camera interface (adjust for your display configuration)
sudo nano /boot/config.txt
```

Add or modify lines as needed for your E-Ink HAT connection. Common settings include:

```
# Waveshare Spectra6 E-Ink Display settings
# Replace with your actual display settings
dtoverlay=spi3-hd430pga5a-8bit=2,0=hdmi_cvt
```

**Note:** The specific configuration depends on your display's GPIO pin mapping. Check Waveshare documentation or identify pins using the camera config tool.

---

## 🎮 How to Take a Photo

Use the custom button you soldered to the Raspberry Pi:

1. Ensure ESP32 is connected to WiFi and streaming
2. Verify the camera stream endpoint works (e.g., from another device):
   ```
   http://<ESP32_IP>:8080/stream.txt
   ```
3. Press your custom button on the Raspberry Pi
4. The script captures a frame, converts to BMP, and displays it on the E-Ink screen

---

## 📊 Display Options

- **Frame Rate**: Adjustable (~2 FPS default)
- **Resolution**: Dependent on ESP32 camera sensor (OV5640: 2592×1944, OV3660: 2048×1536, OV2640: 1600×1200)
- **Format**: JPEG (stream) → BMP (E-Ink display)

---

## 🔧 Troubleshooting

### Connection Failed?

| Issue | Solution |
|-------|----------|
| ESP32 won't connect to WiFi | Reboot ESP32, try default AP credentials |
| No stream at `http://<ESP32_IP>:8080/stream.txt` | Verify camera firmware is running (check LED status) |
| Camera stream shows "CAMERA" or similar error | Check ESP32 console output in serial monitor |

### Raspberry Pi Display Issues?

- Ensure the E-Ink display is properly powered and connected to Pi GPIO
- Verify the BMP-to-E-Ink conversion script is running correctly
- Check that the E-Ink library is compatible with your Spectra6 model
- Confirm the custom button wiring is connecting to a GPIO pin (typically GPIO 4/17 or similar)

### Common Problems

- **ESP32 Camera disabled**: Reboot ESP32 firmware or adjust boot settings
- **Resolution mismatch**: Adjust conversion script if BMP dimensions don't match E-Ink display resolution
- **WiFi connectivity**: Ensure both devices are on the same network and ESP32 is within WiFi range of Pi

---

## 📚 Documentation References

### XIAO ESP32-S3 Sense Board

- **[XIAO ESP32-S3 Getting Started Guide](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)** - Basic board setup, flashing firmware, and configuration
- **[ESP32 Camera Guide](https://www.seeedstudio.com/blog/2026/05/06/esp32-camera-guide/)** - Camera module setup, MJPEG streaming, and frame capture

### Waveshare Spectra6 E-Ink Display

- **Waveshare Spectra6 Documentation** - Official Waveshare documentation for display configuration and driver information

---

## 🛠️ Development Tools

This project uses the following development environments:

| Component | Development Environment | Notes |
|-----------|------------------------|-------|
| XIAO ESP32-S3 Sense | **Arduino IDE** | Used for testing and debugging C++ scripts on the ESP32 board |
| Raspberry Pi 3 | **VS Code** | Used for developing and running Python scripts that handle camera capture and E-Ink display |

### ESP32 Development Setup (Arduino IDE)

1. Install Arduino IDE with ESP32 support
2. Connect XIAO ESP32-S3 Sense via USB
3. Use the built-in serial monitor for debugging camera output
4. Flash C++ scripts using the Arduino IDE board manager

### Raspberry Pi Development Setup (VS Code)

1. Install Python 3 and required packages on Pi
2. Open VS Code with remote SSH connection to Raspberry Pi
3. Use VS Code extensions for Python development, SSH tunneling, and debugging
4. Deploy Python scripts directly from VS Code to the Pi

---

## 📖 Additional Documentation

Additional project files:

- **cam_preview.py**: Python script to capture and preview camera frames from XIAO ESP32-S3 Sense over WiFi
- **wifi_scan.cpp**: C++ program to scan available WiFi networks on ESP32
- **ESP32_CAMERA_VIEWER_README.md**: Detailed documentation for ESP32 camera streaming

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
