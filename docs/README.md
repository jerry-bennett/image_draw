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
|-----------|---------|
| XIAO ESP32-S3 Sense | WiFi-enabled ESP32 board with OV5640/OV3660 camera sensor, PSRAM built-in |
| Raspberry Pi 3 | Runs the camera capture and E-Ink display software |
| Waveshare Spectra6 E-Ink Display | 4-inch color e-ink display (E Ink Color HAT) |
| Custom Button | GPIO-triggered button on Pi for manual photo capture |

---

## 📡 ESP32 Camera Stream

The XIAO ESP32-S3 Sense streams MJPEG video frames over HTTP. This can be used with the `cam_preview.py` Python script on the Pi, OR with a direct C++ sketch (like `esp32s3.ino`) that runs entirely on the ESP32 to capture photos and save directly to an SD card.

**Recently added `esp32_tcp_server.ino`. This allows TCP/IP signaling from the Pi to trigger photo captures.**

### ESP32 Setup Options

**Option A: WiFi Client Mode (Recommended for TCP signaling)**
- Connect ESP32 to home WiFi network (`SSID`, `PW`)
- ESP32 gets IP via DHCP
- Uses Wi-Fi client mode for receiving signals from Pi
- Example credentials: `WiFi.begin("dangus", "eraserhead")`

**Option B: Access Point Mode (For standalone use)**
- Default SSID: `XIAO_ESP32S3_Sense`
- Default Password: `seeedstudio`
- AP IP: Usually `192.168.4.1` (configurable)

---

## 🐛 Raspberry Pi Setup

The Raspberry Pi runs a Python script that:
1. Connects to the ESP32 camera stream over WiFi
2. Downloads JPEG frames continuously (~2 FPS)
3. Converts each frame to BMP format for E-Ink display
4. Renders the BMP on the Waveshare Spectra6 E-Ink display

### Prerequisites

#### Raspberry Pi OS Packages (For Python Script)

```bash
# Install required packages
sudo apt update
sudo apt install -y rpi-camera libjpeg-dev python3-pip
pip3 install opencv-python Pillow scapy requests
```

#### Camera Interface Setup (E-Ink Display)

Connect the Spectra6 E-Ink display to the Pi using SPI. Configure the Raspberry Pi to use your E-Ink interface:

```bash
# Set up camera interface (adjust for your display configuration)
sudo nano /boot/config.txt
```

Add or modify lines for your E-Ink HAT. For Waveshare Spectra6 E-Paper:

```ini
# Waveshare Spectra6 E-Ink Display settings
dtoverlay=spi3-hd430pga5a-8bit=2,0=hdmi_cvt
```

**Note:** Specific configuration depends on your display's GPIO pin mapping. Check Waveshare documentation or use the camera config tool.

---

## 🔌 Pi → ESP32 Communication (TCP/IP Signaling)

To enable **ESP32** photo capture triggered by Pi button signals:

1. Connect ESP32 to home WiFi (`WiFi.begin("dangus", "eraserhead")`)
2. Configure Pi `button_trigger.py` script with correct IP
3. Verify both devices on **same network** for TCP communication
4. Update URLs in `button_trigger.py`:
   ```python
   ESP32_CAPTURE_ENDPOINT = "http://<ESP32_IP>:80/capture"  # Actual IPs!
   ```

5. Pi button press (hold 3s) triggers Python script → sends signal to ESP32
6. ESP32 receives signal via WiFi client mode, takes photo, saves to SD

**Critical Requirement:** Both ESP32 and Pi must connect to the **same WiFi network**. The current configuration shows:
- ESP32 Client IP: `192.168.12.228` (from Serial Monitor)
- Pi IP: `192.168.12.106`

**Getting Device IPs:**
- **ESP32**: View via Serial Monitor in Arduino IDE (shows `WiFi.localIP`)
- **Pi**: Use `ip a` or check `/boot/config.txt` for network configuration

### Troubleshooting TCP Connection Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Connection refused" | Wrong IP/Port in `button_trigger.py` | Update with actual ESP32 IP from Serial output |
| No connection at all | Router blocking inter-device traffic | Ensure both on same subnet, check firewall |

---

## 📷 button_trigger.py Behavior

The Python script on Pi monitors GPIO 26 button with two actions:

| Action | Script Triggered | Effect |
|--------|-----------------|--------|
| **Double-click** | `/image_draw/clear.py` | Clears E-Ink display |
| **3-second hold** | `/image_draw/image_draw.py` | Captures frame from ESP32 stream |

---

## 📷 button_trigger.py Behavior (ESP32 Capture Mode)

When using `esp32_tcp_server.ino`:

| Action | Signal Sent | Effect |
|--------|-------------|--------|
| **Double-click** | TCP signal to ESP32 | ESP32 takes photo, saves to SD |
| **3-second hold** | Same as above + Pi display capture | Both ESP32 and Pi capture simultaneously |

---

## 📷 ESP32 Button Trigger (Alternative)

The `esp32s3.ino` sketch can be configured to take photos when a button on the **ESP32 board** is pressed. This option allows you to run the camera/SD code entirely on the ESP32 with no Python script on the Pi needed.

See the Seeed Wiki's **"Project I: Making a handheld camera"** for an example of taking photos via touch input on the XIAO's round display.

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
| ESP32 won't connect to WiFi | Reboot ESP32, try default AP credentials or check WiFi password |
| No stream at `http://<ESP32_IP>:8080/stream.txt` | Verify camera firmware is running (check LED status) |
| Camera stream shows "CAMERA" or similar error | Check ESP32 console output in serial monitor |
| TCP connection fails | Ensure both devices on same subnet, check `esp32_tcp_server.ino` for proper WiFi config |

### Raspberry Pi Display Issues?

- Ensure the E-Ink display is properly powered and connected to Pi GPIO
- Verify the BMP-to-E-Ink conversion script is running correctly
- Check that the E-Ink library is compatible with your Spectra6 model
- Confirm the custom button wiring is connecting to a GPIO pin (typically GPIO 4/17 or similar)

### Common Problems

- **ESP32 Camera disabled**: Reboot ESP32 firmware or adjust boot settings
- **Resolution mismatch**: Adjust conversion script if BMP dimensions don't match E-Ink display resolution
- **WiFi connectivity**: Ensure both devices are on the same network and ESP32 is within WiFi range of Pi
- **TCP signaling fails**: Check `esp32_tcp_server.ino` Serial output for connection status

---

## 📚 Documentation References

### XIAO ESP32-S3 Sense Board

- **[XIAO ESP32-S3 Getting Started Guide](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)** - Basic board setup, flashing firmware, and configuration
- **[ESP32 Camera Guide](https://www.seeedstudio.com/blog/2026/05/06/esp32-camera-guide/)** - Camera module setup, MJPEG streaming, and frame capture
- **[Waveshare Spectra6 E-Ink Display](https://www.waveshare.com/wiki/4inch_e-Paper_HAT+_(E))** - Official Waveshare documentation for display configuration and driver information
- **[WiFi Information for XIAO ESP32S3](https://wiki.seeedstudio.com/xiao_esp32s3_wifi_usage/)** - WiFi client mode and credentials
- **[Camera Usage for XIAO ESP32S3](https://wiki.seeedstudio.com/xiao_esp32s3_camera_usage/)** - Photo capture and SD card writing
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
