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
| Custom Button | GPIO-triggered button on Pi for manual photo capture |

---

## 📡 ESP32 Camera Stream

The XIAO ESP32-S3 Sense streams MJPEG video frames over HTTP. This can be used with the `cam_preview.py` Python script on the Pi, OR with a direct C++ sketch (like `esp32s3.ino`) that runs entirely on the ESP32 to capture photos and save directly to an SD card.

**Recently added `make_xiao_an_access_point.cpp`. This will be used in the future when the device is on the go, so the Raspberry Pi can connect to the XIAO's WiFi.**

---

## 🔌 XIAO ESP32-S3 Camera Pin Definitions

For your C++ sketches to work with the OV5640 expansion board, you'll need the correct GPIO pin definitions. The Seeed Wiki documentation provides these default pin mappings:

| GPIO Number | Signal |
|-------------|--------|
| 10 (XMCLK) | XCLK |
| 11 (DVP_Y8) | Y8 (D7) |
| 12 (DVP_Y7) | Y7 (D6) |
| 13 (DVP_PCLK) | PCLK (D5) |
| 14 (DVP_Y6) | Y6 (D4) |
| 15 (DVP_Y2) | Y2 (D3) |
| 16 (DVP_Y5) | Y5 (D2) |
| 17 (DVP_Y3) | Y3 (D1) |
| 18 (DVP_Y4) | Y4 (D0) |
| 38 (DVP_VSYNC) | VSYNC |
| 39 (CAM_SCL) | SCL (I2C clock) |
| 40 (CAM_SDA) | SDA (I2C data) |
| 47 (DVP_HREF) | HREF |
| 48 (DVP_Y9) | Y9 |

**Note:** The ESP32-S3 has PSRAM built-in, which is important for camera buffer operations. You'll need to include `camera_pins.h` in your sketches with these definitions.

---

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

## 🔌 ESP32 Button Trigger (Alternative to Pi Button)

The `esp32s3.ino` sketch can be configured to take photos when a button on the **ESP32 board** is pressed. This option allows you to run the camera/SD code entirely on the ESP32 with no Python script on the Pi needed.

See the Seeed Wiki's **"Project I: Making a handheld camera"** for an example of taking photos via touch input on the XIAO's round display.

---

## 🔌 Pi Button Signal to ESP32 (Current Setup)

If you have a **button soldered directly to the Raspberry Pi** (not ESP32), you'll need to signal the ESP32 to take a photo over WiFi using one of these methods:

### Option A: TCP/IP Signaling (Recommended)
1. Connect a GPIO button pin on the Pi to trigger the script
2. The Python script connects to the ESP32 via WiFi and sends a capture command
3. ESP32 receives signal, takes photo, saves to SD card

### Option B: Serial Over WiFi (TCP Server)
1. ESP32 acts as an HTTP server at `http://<ESP32_IP>:8080/capture`
2. Pi button press triggers Python script which sends HTTP POST request
3. ESP32 captures photo on receiving signal

The **esp32s3.ino** sketch supports both approaches and can be extended to receive the TCP signal via WiFi network.

---

---

## 📷 ESP32 Camera Sketches

### xiao_take_photo.cpp - Auto-Capture Mode

This sketch (`esp32s3.ino`) takes photos automatically every 60 seconds and saves them directly to an SD card. No Python script on the Pi is needed for this mode.

Key features:
- Automatic photo capture every minute
- Direct SD card storage (no conversion needed)
- OV5640 auto-focus support for sharper images
- Full camera pin configuration for XIAO ESP32-S3

## 🔌 ESP32 Button Trigger (Alternative to Pi Button)

The `esp32s3.ino` sketch can be configured to take photos when a button on the **ESP32 board** is pressed, eliminating the need for any Python script on the Pi. To enable this:

1. Connect a GPIO interrupt pin on the ESP32 to a button (e.g., GPIO 21 / PULLUP)
2. Include `esp_camera.h`, `FS.h`, `SD.h`, and `SPI.h` in your sketch
3. Add SPI and SD card setup for saving directly to SD
4. Use the button pin number when configuring your camera

See the Seeed Wiki's **"Project I: Making a handheld camera"** for an example of taking photos via touch input on the XIAO's round display.

---

## 🔌 Pi → ESP32 Communication (Optional Extension)

To extend this setup to let the **ESP32** take photos directly (rather than displaying stream frames):

1. Modify `esp32s3.ino` to listen for TCP/IP signals via WiFi
2. When a signal arrives, the ESP32 takes a photo and saves to SD card
3. Optionally remove auto-capture timer from `esp32s3.ino`

---


## 📷 button_trigger.py Behavior

The Python script on Pi monitors GPIO 26 button with two actions:

| Action | Script Triggered | Effect |
|--------|-----------------|--------|
| **Double-click** | `/image_draw/clear.py` | Clears E-Ink display |
| **3-second hold** | `/image_draw/image_draw.py` | Captures frame from ESP32 stream |

---


## 🎮 How to Take a Photo

### Option A: Pi Button Trigger (Current Setup with button_trigger.py)

Use the custom button soldered to the Raspberry Pi (GPIO 26 / BCM Pin 37):

1. Ensure ESP32 is connected to WiFi and streaming
2. Verify the camera stream endpoint works (e.g., from another device):
   ```bash
   http://<ESP32_IP>:8080/stream.txt
   ```
3. Press your custom button on the Raspberry Pi
4. `button_trigger.py` detects 3-second hold and runs `/image_draw/image_draw.py`
5. Script captures frame from ESP32 stream, converts to BMP, displays on E-Ink screen

### Option B: Auto-Capture (ESP32 Direct - Every 60 seconds)

The `esp32s3.ino` sketch automatically takes photos once every minute and saves them directly to the SD card on ESP32. No Python script on Pi is needed for this mode. This is ideal for "set-and-forget" operation with handheld camera use.

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
- **[Waveshare Spectra6 E-Ink Display](https://www.waveshare.com/wiki/4inch_e-Paper_HAT+_(E))** - Official Waveshare documentation for display configuration and driver information
- **[WiFi Information for XIAO ESP32S3](https://wiki.seeedstudio.com/xiao_esp32s3_wifi_usage/)**
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
