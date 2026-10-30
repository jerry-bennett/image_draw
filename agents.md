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
| XIAO ESP32-S3 Sense | WiFi camera streaming | OV5640 sensor, built-in PSRAM |
| Raspberry Pi 3 | Frame conversion & E-Ink display + SD Card | Runs Python scripts |
| Waveshare Spectra6 E-Ink | 4" color e-ink display | SPI interface (SPI3) |
| Custom Button | GPIO trigger | Connected to Pi GPIO 26 |

## 📁 File Structure

### Project Root (`image_draw/`)
```
image_draw/
├── README.md              # Main documentation
├── agents.md              # Agent guidelines
├── esp32s3/
│   └── esp32s3.ino       # ESP32 camera/SD auto-capture sketch
├── xiao_take_photo.cpp   # Standalone ESP32 photo capture example
├── button_trigger.py      # Pi button input handler (GPIO 26)
├── image_draw.py          # Captures frame, converts JPEG→BMP, displays on E-Ink
├── clear.py               # Clears E-Ink display
└── lib/waveshare_epd/    # E-Ink library and drivers
```

### Key Directories (on Pi)
- `/image_draw/` - Python scripts for image capture/display
- `/boot/config.txt` - Camera interface configuration

## 📖 Key Files

| File | Purpose | Language | Location |
|------|---------|----------|----------|
| `esp32s3.ino` | ESP32 camera auto-capture every 60 seconds, saves to SD | Arduino (C++) | `esp32s3/esp32s3.ino` |
| `xiao_take_photo.cpp` | Standalone ESP32 photo capture with OV5640 AF support | Arduino (C++) | Root directory |
| `button_trigger.py` | Monitors Pi GPIO 26 button, triggers scripts | Python | Root directory |
| `image_draw.py` | Main loop: captures stream frame → BMP → E-Ink display | Python | `/image_draw/` |
| `cam_preview.py` | Alternative continuous preview script | Python | Root directory |

## 🎮 Trigger Modes

### Pi Button (GPIO 26 / BCM Pin 37)
- **Double-click**: Clears E-Ink display via `clear.py`
- **3-second hold**: Captures photo via `image_draw.py`

### ESP32 Auto-Capture
- Takes photos every 60 seconds automatically
- Saves directly to SD card
- No Pi intervention needed
- No SD card currently in XIAO, can change that if needed.

## 🔌 XIAO ESP32-S3 Camera Pins

For OV5640 expansion board setup:

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

## 📡 ESP32 Camera Stream Endpoint

When ESP32 is streaming MJPEG frames:
```
http://<ESP32_IP>:8080/stream.txt
```

### ESP32 Setup Options

**Option A: WiFi Network Mode (Requires Pi to connect to ESP32)**
- Connect ESP32 to home WiFi first
- Get IP from `ipconfig /all` on Windows

**Option B: Access Point Mode (For standalone use)**
- Default SSID: `XIAO_ESP32S3_Sense`
- Default Password: `seeedstudio`
- AP IP: Usually `192.168.4.1`

## 🔌 Pi → ESP32 Communication

To enable ESP32 photo capture triggered by Pi button signals:

### TCP/IP Signaling (Recommended)
1. Modify `esp32s3.ino` to listen for TCP/IP signals via WiFi
2. Pi button press triggers Python script
3. Python sends signal to ESP32 over WiFi
4. ESP32 receives signal, takes photo, saves to SD

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
- WiFi connection fails: Reboot ESP32 or try default AP credentials
- "CAMERA" error in stream: Verify camera firmware is running

### Pi/Display Issues
- E-Ink not responding: Verify SPI3 connection and library loaded
- BMP conversion errors: Check frame dimensions match display
- Camera stream unavailable: Ensure ESP32 is streaming correctly

## 📚 Documentation References

- **ESP32-S3**: Seeed Wiki - `xiao_esp32s3_camera_usage/`, `wifi_usage/`
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

### Tools Available for Agents in This Repo

- **Grep**: Search Python/Arduino code patterns
- **Glob**: Find files matching patterns (`**/*.cpp`, `**/*.py`)
- **Read**: Full file content (up to 2000 lines)
- **WebFetch**: Seeed Wiki pages for ESP32 documentation
- **Bash**: Execute shell commands on Pi or local testing

### Best Practices

1. **Preserve existing trigger logic** - Don't break `button_trigger.py` unless explicitly requested
2. **Keep camera pin mapping** - Use default XIAO ESP32-S3 pins from Seeed Wiki
3. **PSRAM is enabled by default** - Configure accordingly in sketches
4. **OV5640 AF needs SXGA resolution** - Switch to focus, then restore capture size
5. **E-Ink display uses SPI3** - Verify overlay config in `/boot/config.txt`
6. **Camera stream endpoint** - Typically `8080/stream.txt` on ESP32

### Memory Patterns for AI Agents

Use these memory file patterns:
- `feedback`: Documentation updates, correction of agent guidance
- `reference`: External documentation links (Seeed Wiki URLs)
- `project`: Ongoing tasks like "extend ESP32 button-trigger", "add WiFi communication"

## ⚠️ Important Notes

1. The `esp32s3.ino` currently has **no working code** beyond camera config - it's a template to be completed with actual capture/button logic
2. The OV5640 auto-focus requires switching to SXGA resolution (minimum 1280×1024) before focusing
3. `image_draw.py` is the main active Python script that captures stream frames
4. `button_trigger.py` on Pi monitors GPIO 26 for double-click and 3-second hold triggers

## 🔮 Future Enhancement Goals

- [ ] Enable ESP32 photo capture triggered by TCP signal from Pi button
- [ ] Remove auto-capture timer when using button-trigger mode
- [ ] Add status LED or serial output for ESP32 to confirm capture success
- [ ] Support different camera resolutions via configuration option
- [ ] Add JPEG quality setting in `esp32s3.ino`

