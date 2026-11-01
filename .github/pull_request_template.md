# Pull Request Template

**Branch naming format:** `type/short-desc` (e.g., `fix/esp32-wifi-tcp`)  
**Format:** `type(scope): message` with body containing "What Changed", "Why", and "How to Test"

---

## 📝 What Changed

<!-- 
Describe the specific changes made in this PR. Be concise and focused on one concern.
Use bullet points for multiple files or logic blocks.
-->

- Modified: `file/path` - brief description of change
- Added: `feature` - new functionality  
- Removed: `component` - deprecated feature removed
- Fixed: `bug` - broken behavior corrected

<!-- Keep PRs under 400 lines changed; split if larger -->

---

## 🔍 Why

<!-- 
Explain the reasoning behind this change. Include technical justification, performance impact, or architectural considerations.
Reference GitHub issues with Closes #<number> if applicable.
-->

- Addresses: `issue number` - problem being solved
- Technical rationale: why this solution was chosen over alternatives
- Risk assessment: any potential side effects or regressions

---

## ✅ How to Test

<!-- 
Provide clear, step-by-step instructions for testing this change locally.
Include prerequisites, expected results, and verification steps. -->

### Prerequisites

```bash
# Install/verify dependencies
pip install opencv-python Pillow scapy requests
python --version

# Ensure hardware is ready (ESP32 streaming via WiFi)
# Get ESP32 IP from Serial Monitor: http://<ESP32_IP>:8080/stream.txt
# Verify stream endpoint works:
```

### Testing Steps

1. **Verify baseline functionality** - Confirm existing behavior before changes
   - ESP32 connects to "dangus" WiFi network (password: eraserhead)
   - Serial Monitor shows `ESP32 IP: xxx`
   - Stream endpoint accessible at correct port (`8080`)

2. **Apply change** - Run or deploy the modified code
   - Upload ESP32 sketch to board
   - Ensure `button_trigger.py` is running on Pi
   - Verify TCP signal path from Pi → ESP32

3. **Expected result** - What should happen with correct inputs
   - Pi button press (hold 3s) triggers capture request
   - ESP32 receives signal via TCP at specified endpoint
   - Serial output confirms "CAPTURE keyword detected!"
   
4. **Edge cases** - Test boundary conditions 
   - Incorrect WiFi credentials → connection fails after 120s timeout
   - Wrong IP/Port in `button_trigger.py` → connection refused error
   - Pi off from WiFi network → TCP handshake fails

### Expected Output Examples

```bash
# ESP32 Serial Monitor output during test
ESP32 connected!
ESP32 IP: 192.168.12.228
Connected to 192.168.12.228:80
CAPTURE keyword detected!
--- CAPTURE REQUEST RECEIVED ---

# Pi output from button_trigger.py
Sending WiFi capture request to http://<ESP32_IP>:80/capture
WiFi capture signal sent!
```

---

## 📋 Additional Notes

<!-- 
Optional: include breaking changes, deprecation warnings, or migration guides -->

- **Breaking changes:** Will require updates to dependent code (update IPs in `button_trigger.py`)
- **Configuration:** ESP32 must connect to same WiFi as Pi for TCP communication
- **Network requirements:** Both devices on same subnet; router/firewall not blocking inter-device traffic

---

## 🚀 Deploy Instructions

<!-- 
Include if this PR requires deployment steps, configuration changes, or infrastructure updates -->

- Upload ESP32 sketch via Arduino IDE Serial Monitor
- Verify IP addresses in `button_trigger.py` match actual device IPs
- Restart Pi to reload `button_trigger.py` script
- Test button trigger from GPIO 26 (hold 3 seconds)

---

**[ ] Self-review complete before opening**  
**[ ] Marked as ready for review after merge**

🤖 Generated with [Claude Code](https://claude.com/claude-code)
