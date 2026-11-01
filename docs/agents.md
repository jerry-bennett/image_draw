# Agents Working Directory

This project uses a hybrid multi-device architecture: an ESP32-S3 Sense camera board connected to a Raspberry Pi 3 with an E-Ink display.

## 📋 Project Overview

A hardware system that:
1. Captures photos from XIAO ESP32-S3 Sense camera over WiFi
2. Converts JPEG frames to BMP format on the Pi
3. Displays images on Waveshare Spectra6 4" E-Ink display
4. Saves the BMP file onto a micro SD card on the Pi.

## 🔧 Hardware Components

| Component | Purpose | Notes |
|-----------|---------|-------|
| XIAO ESP32-S3 Sense | WiFi camera streaming | OV5640 sensor, PSRAM built-in, TCP/IP signaling support |
| Raspberry Pi 3 | Frame conversion & E-Ink display + SD Card | Runs Python scripts, GPIO 26 button trigger |
| Waveshare Spectra6 E-Ink | 4" color e-ink display | SPI interface (SPI3) |
| Custom Button | GPIO trigger | Connected to Pi GPIO 26 (BCM Pin 37) |

## 📁 File Structure

### Project Root (`image_draw/`)
```
image_draw/
├── README.md              # Main documentation (updated with esp32_tcp_server.ino details)
├── agents.md              # Agent guidelines (this file)
├── docs/
│   ├── README.md         # Enhanced project documentation
│   └── agents.md         # Agent-specific guidance
├── esp32s3/
│   ├── esp32s3.ino      # Main ESP32 camera sketch with TCP signaling support
│   ├── esp32_tcp_server.ino  # WiFi client mode for TCP/IP capture trigger
│   ├── esp32_wifi_only.ino    # WiFi-only connection test
│   ├── esp_camera.h      # ESP32 Camera library header
│   ├── esp_camera.c      # ESP32 Camera library implementation
│   ├── camera_pins.h     # XIAO ESP32-S3 pin definitions for OV5640
│   ├── ESP32_OV5640_AF.h  # OV5640 auto-focus support header
│   └── ESP32_OV5640_cfg.h  # OV5640 auto-focus configuration
├── xiao_take_photo.cpp   # Standalone ESP32 photo capture example with AF support
├── button_trigger.py     # Pi button input handler (GPIO 26)
├── image_draw.py         # Captures frame, converts JPEG→BMP, displays on E-Ink
├── clear.py              # Clears E-Ink display
└── lib/waveshare_epd/    # E-Ink library and drivers
```

### Key Directories (on Pi)
- `/image_draw/` - Python scripts for image capture/display
- `/boot/config.txt` - Camera interface configuration

## 📖 Key Files

| File | Purpose | Language | Location | Status |
|------|---------|----------|----------|--------|
| `esp32s3.ino` | ESP32 camera auto-capture + TCP signaling | Arduino (C++) | `esp32s3/esp32s3.ino` | Active |
| `esp32_tcp_server.ino` | WiFi client mode, receives TCP capture trigger | Arduino (C++) | `esp32s3/esp32_tcp_server.ino` | New feature |
| `xiao_take_photo.cpp` | Standalone ESP32 photo capture with OV5640 AF support | Arduino (C++) | Root directory | Active |
| `button_trigger.py` | Monitors Pi GPIO 26 button, triggers scripts | Python | Root directory | Active |
| `image_draw.py` | Main loop: captures stream frame → BMP → E-Ink display | Python | `/image_draw/` | Active |
| `cam_preview.py` | Alternative continuous preview script | Python | Root directory | Legacy |

## 🎮 Trigger Modes

### Pi Soldered Button (GPIO 26 / BCM Pin 37)
- **Double-click**: Clears E-Ink display via `clear.py`
- **3-second hold**: Captures photo via `image_draw.py` (Pi stream mode) OR triggers ESP32 via TCP signaling (new feature)

### ESP32 Auto-Capture (SD Card Direct - Recommended for Portability)
- Takes photos every 60 seconds automatically
- Saves directly to SD card on ESP32
- No Pi intervention needed
- **Note**: Requires SD card in XIAO ESP32-S3 Sense

### TCP/IP Signaling from Pi Button (New Feature)
- Pi button press sends "CAPTURE" signal over WiFi TCP to ESP32
- ESP32 receives signal, takes photo + stream frame, saves to SD
- **Requires both devices on same WiFi network** (`192.168.12.x` subnet)

### ESP32 Auto-Capture (SD Card Direct - Recommended for Portability)
- Takes photos every 60 seconds automatically
- Saves directly to SD card on ESP32
- No Pi intervention needed
- **Note**: Requires SD card in XIAO ESP32-S3 Sense

### TCP/IP Signaling (New Feature in `esp32_tcp_server.ino`)
- Connects ESP32 to home WiFi client mode (`"dangus"` network)
- Pi sends "CAPTURE" signal via TCP on port 80/8080
- ESP32 takes photo and saves to SD immediately
- **Requires both devices on same WiFi network**

## 🔌 XIAO ESP32-S3 Camera Pins

For OV5640 expansion board setup (Seeed Wiki default pin mapping):

| GPIO | Signal | Description |
|------|--------|-------------|
| 10   | XCLK   | Clock |
| 11   | Y8     | D7 (DVP_Y8) |
| 12   | Y7     | D6 (DVP_Y7) |
| 13   | PCLK   | D5 (DVP_PCLK) |
| 14   | Y6     | D4 (DVP_Y6) |
| 15   | Y2     | D3 (DVP_Y2) |
| 16   | Y5     | D2 (DVP_Y5) |
| 17   | Y3     | D1 (DVP_Y3) |
| 18   | Y4     | D0 (DVP_Y4) |
| 38   | VSYNC  | Vertical sync |
| 39   | SCL    | I2C clock |
| 40   | SDA    | I2C data |
| 47   | HREF   | Horizontal reference |
| 48   | Y9     | DVP_Y9 |

**Note**: ESP32-S3 has built-in PSRAM, important for camera buffer operations.

## 🐛 Raspberry Pi Setup

### Prerequisites
- **OS**: Raspberry Pi OS (arm64 recommended)
- **Python**: 3.x with packages: `opencv-python`, `Pillow`, `scapy`, `requests`
- **Camera Interface**: SPI configured for E-Ink display in `/boot/config.txt`

```bash
# Install required packages
sudo apt update
sudo apt install -y rpi-camera libjpeg-dev python3-pip
pip3 install opencv-python Pillow scapy requests
```

### E-Ink Display (Waveshare Spectra6)
- Connected via SPI3
- Overlay configuration: `spi3-hd430pga5a-8bit=2,0`
- May require additional overlay settings in `/boot/config.txt`

### Current Network Configuration

| Device | IP Address | Network Mode | Port Used |
|--------|------------|--------------|-----------|
| ESP32 (WiFi Client) | `192.168.12.228` | WiFi Client (`"dangus"` network) | 80 |
| Raspberry Pi | `192.168.12.106` | Home WiFi client | 80 |

## 📡 ESP32 Camera Stream Endpoint

When ESP32 is streaming MJPEG frames (continuous mode):
```
http://<ESP32_IP>:8080/stream.txt
```

### TCP/IP Signaling Endpoint (New Feature)
When ESP32 receives signals via WiFi client mode:
```
TCP connection to <ESP32_IP>:80
Send "CAPTURE" keyword when Pi button is held for 3 seconds
```

## 🔌 ESP32 WiFi Setup Options

**Option A: WiFi Client Mode (Recommended)**
- Connect ESP32 to home WiFi network (`SSID`, `PW`)
- ESP32 gets IP via DHCP
- Uses Wi-Fi client mode for receiving signals from Pi
- Example credentials: `WiFi.begin("dangus", "eraserhead")`

**Option B: Access Point Mode (For standalone use)**
- Default SSID: `XIAO_ESP32S3_Sense`
- Default Password: `seeedstudio`
- AP IP: Usually `192.168.4.1` (configurable)
- Requires Pi to connect to ESP32's network

### WiFi Connection Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Connection failed" | Wrong WiFi credentials | Verify SSID and password in `esp32s3.ino` |
| No IP address assigned | DHCP issue or max retries exceeded | Reboot ESP32, check Serial output for error details |
| "WiFi.status() == WL_NO_SIGNAL" | Out of range from router | Move closer to router or use AP mode |
| CAPTURE signal ignored | Wrong IP/Port in `button_trigger.py` | Update with actual ESP32 IP (e.g., `192.168.12.228`) |

## 🔌 Pi → ESP32 Communication

To enable ESP32 photo capture triggered by Pi button signals:

### TCP/IP Signaling (New Recommended Approach)

1. Connect ESP32 to home WiFi (`WiFi.begin("dangus", "eraserhead")`)
2. Configure Pi `button_trigger.py` script with correct IP
3. Verify both devices on **same network** for TCP communication
4. Update URLs in `button_trigger.py`:
   ```python
   ESP32_CAPTURE_ENDPOINT = "http://192.168.12.228:80/capture"  # Actual IPs!
   ```

5. Pi button press (hold 3s) triggers Python script → sends signal to ESP32
6. ESP32 receives signal via WiFi client mode, takes photo, saves to SD

### Troubleshooting TCP Connection Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| "Connection refused" | Wrong IP/Port in `button_trigger.py` | Update with actual ESP32 IP from Serial output |
| No connection at all | Router blocking inter-device traffic | Ensure both on same subnet, check firewall |

## 🛠️ Development Environments

| Component | Tool | Purpose |
|-----------|------|---------|
| XIAO ESP32-S3 | Arduino IDE | Flash C++ sketches, serial monitor |
| Raspberry Pi 3 | VS Code (SSH) | Python script development |

## Architecture decisions (`adr/`)

The [`adr/`](./adr/) directory is the architecture overview + decision log. Keep it
current as part of the work, not as an afterthought:

- **Made a significant architectural decision** (auth model, schema boundary, deployment
  shape, a new service or major dependency, superseding a past choice)? Add a new record
  `adr/NNNN-title-in-kebab-case.md` using the format of
  [ADR 0001](./adr/0001-record-architecture-decisions.md) — Status / Context / Decision /
  Consequences — and add a row to the decision-log table in
  [`adr/README.md`](./adr/README.md). To supersede an earlier decision, add a new ADR and
  flip the old one's status to `Superseded`.
- **Changed the architecture or directory layout** that the overview in `adr/README.md`
  describes (new app, new top-level dir, moved component)? Update that overview/diagram in
  the same change so it stays accurate.
- The bar is *significant* decisions, not every change — don't manufacture ADRs for
  routine work.
- **An ADR is plain Markdown with no external links**: no docs elsewhere. Summarise what a link would have said in the ADR
  itself, so an agent reading `adr/` alone has the whole context. Links to other
  files in this repo are fine.

## PR hygiene

- Keep PRs under 400 lines changed, one concern per PR. If a change is larger, flag it and suggest splitting before creating the PR.
- Self-review the diff before opening the PR — catch obvious issues before requesting a human review.
- Fill out the PR body using the template: what changed, why, and how to test.
- If the user mentions a GitHub issue, include `Closes #<number>` in the PR body so it auto-closes on merge.
- Always open PRs as drafts (`gh pr create --draft`); let a human mark them ready for review.

## Branch naming

Use lowercase, hyphenated branch names in the format `type/short-desc`:

| Prefix | When to use |
|--------|-------------|
| `feature/` | New functionality that didn't exist before |
| `fix/` | Correcting broken or incorrect behavior |
| `chore/` | Deps, config, CI, refactor, tooling — no functional change |
| `docs/` | READMEs, ADRs, comments only — no code change |

**One branch can cover several issues.** Sub-issues each get their own identifier, so
the default is one branch per issue — but small related sub-issues don't need splitting.
Name the branch after the parent (`chore/...`) and list the rest in the PR body;

**Classifying the type** — key off the user's words, not just the files touched:
- "add", "build", "implement", "new" → `feature/`
- "bug", "broken", "wrong", "not working", "handle error" → `fix/`
- "bump", "upgrade", "rename", "refactor", "config", "CI" → `chore/`
- Only docs files touched → `docs/`
- **When in doubt, ask** — if the user's description doesn't clearly map to a type, confirm before creating the branch.

**Mixed-type changes** — if a change spans more than one type with no clear dominant intent, that's a signal the work should be split into separate branches. Flag this to the user and ask which piece to tackle first. If the user wants it in one branch, ask them to name the type rather than guessing.

## Commit message format

Use Conventional Commits: `type(scope): message`

Types: `feat` | `fix` | `chore` | `refactor` | `docs` | `test`

Scope is optional but encouraged — e.g. `feat(api)`, `fix(auth)`, `chore(tf)`, `refactor(web)`.

- Imperative mood, present tense: "add X" not "added X"
- Subject line under 72 characters
- If more context is needed, leave a blank line after the subject and write a body

When you commit

Commit or push only when asked. Ask whether to land on `main` or a new branch rather than
deciding yourself. **Open PRs as drafts** (`gh pr create --draft`) and let a human mark them
ready for review — this prevents accidental merges.

- Use the same type classification rules as [Branch naming](#branch-naming) — the vocabulary heuristics and "when in doubt, ask" rule apply here too.

## ⚙️ Troubleshooting

### ESP32 Connection Issues
- Camera won't start: Check LED status and serial output
- WiFi connection fails: Reboot ESP32, try default AP credentials or check password
- "CAMERA" error in stream: Verify camera firmware is running
- TCP signaling ignored: Wrong IP/Port in `button_trigger.py`

### Pi/Display Issues
- E-Ink not responding: Verify SPI3 connection and library loaded
- BMP conversion errors: Check frame dimensions match display
- Camera stream unavailable: Ensure ESP32 is streaming correctly

## 📚 Documentation References

- **ESP32-S3**: Seeed Wiki - `xiao_esp32s3_getting_started/`, `wifi_usage/`
- **E-Ink**: Waveshare documentation for Spectra6 E-Paper HAT
- **OV5640**: Auto-focus firmware from github.com/0015/ESP32-OV5640-AF

## 🤖 Agent Guidelines for This Project

### Common Tasks to Delegate to Agents

| Task | Recommended Approach | Files Involved |
|------|---------------------|----------------|
| ESP32 camera config | Search Seeed Wiki, use default pin mapping | `esp32s3/esp32s3.ino` |
| OV5640 auto-focus setup | Include `ESP32_OV5640_AF.h`, set SXGA for AF | `xiao_take_photo.cpp` |
| SD card write to ESP32 | Use `File.write(data, len)` pattern | All C++ sketches |
| Pi script modifications | Check existing `button_trigger.py` structure | `/image_draw/*.py` |
| WiFi connectivity | Try AP mode or client mode, adjust credentials | Both sides |
| TCP/IP signaling | Use `esp32_tcp_server.ino` with WiFi client mode, verify IP in `button_trigger.py` | New files |

### Best Practices

1. **Preserve existing trigger logic** - Don't break `button_trigger.py` unless explicitly requested
2. **Keep camera pin mapping** - Use default XIAO ESP32-S3 pins from Seeed Wiki
3. **PSRAM is enabled by default** - Configure accordingly in sketches
4. **OV5640 AF needs SXGA resolution** - Switch to focus, then restore capture size
5. **E-Ink display uses SPI3** - Verify overlay config in `/boot/config.txt`
6. **Camera stream endpoint** - Typically `8080/stream.txt` on ESP32

### New: TCP/IP Signaling Pattern

When working with the new `esp32_tcp_server.ino`:

1. Ensure ESP32 is connected to WiFi client mode (`WiFi.begin("dangus", "eraserhead")`)
2. Get actual ESP32 IP from Serial Monitor output (e.g., `192.168.12.228`)
3. Update `button_trigger.py` with correct IP and port:
   ```python
   ESP32_IP = "192.168.12.228"  # Replace with actual IP
   ESPTCP_PORT = 80             # Default, can change to 8080 if needed
   ```
4. Verify both devices on same subnet/network

### Memory Patterns for AI Agents

Use these memory file patterns:
- `feedback`: Documentation updates, correction of agent guidance
- `reference`: External documentation links (Seeed Wiki URLs)
- `project`: Ongoing tasks like "extend ESP32 button-trigger", "add WiFi communication"

## 🔮 Future Enhancement Goals

- [x] Implement TCP/IP signaling in `esp32_tcp_server.ino`
- [ ] Fix ESP32 WiFi connection issue (device not connecting to "dangus" network)
- [ ] Remove auto-capture timer when using button-trigger mode
- [ ] Add status LED or serial output for ESP32 to confirm capture success
- [ ] Support different camera resolutions via configuration option
- [ ] Add JPEG quality setting in `esp32s3.ino`

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
