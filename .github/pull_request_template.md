# Pull Request Template

**Branch naming format:** `type/short-desc` (e.g., `fix/overclock-esp32-camera`)  
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
pip install opencv-python Pillow
python --version

# Ensure hardware is ready (ESP32 streaming via WiFi)
# Verify stream endpoint works: http://<ESP32_IP>:8080/stream.txt
```

### Testing Steps

1. **Verify baseline functionality** - Confirm existing behavior before changes
2. **Apply change** - Run or deploy the modified code
3. **Expected result** - What should happen with correct inputs
4. **Edge cases** - Test boundary conditions (e.g., no SD card, disconnected WiFi)

### Expected Output Examples

```bash
$ python script.py
# Should produce: "Photo saved successfully" or similar success message

$ curl http://<ESP32_IP>:8080/stream.txt
# Should return valid JPEG frames (~2 FPS, not "CAMERA" error)
```

---

## 📋 Additional Notes

<!-- 
Optional: include breaking changes, deprecation warnings, or migration guides -->

- **Breaking changes:** Will require updates to dependent code
- **Deprecation:** Marking `component` for removal in next major version
- **Configuration changes:** New settings in `config.yaml` requiring restart

---

## 🚀 Deploy Instructions

<!-- 
Include if this PR requires deployment steps, configuration changes, or infrastructure updates -->

- No deployment needed (local testing only)
- Update Docker Compose: `compose.yaml:1024` section
- Rollback plan: [steps to revert if issue occurs]

---

**[ ] Self-review complete before opening**  
**[ ] Marked as ready for review after merge**

🤖 Generated with [Claude Code](https://claude.com/claude-code)
