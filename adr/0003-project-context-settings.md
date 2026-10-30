---
name: 0003-project-context-settings
description: Session-level configuration for project context and PR templates
metadata:
  type: reference
---

## Decision Log Entry

### Status: 🟢 Recommended / Adopted

**Context:** To ensure consistent project awareness across all Claude Code sessions, I need to document the session settings and PR template requirements that apply to this repository.

**Decision:** Add `.claude/settings.local.json` with automatic project context injection on every new session, plus enforce `pull_request_template.md` sections ("What Changed", "Why", "How to Test") for all PRs including AI-generated ones.

**Consequences:**
- **Positive:** New sessions will automatically have the image_draw architecture context injected before any user message. PRs follow a standard format ensuring testing steps are documented. Reduces onboarding time for agents by having context ready.
- **Negative:** Requires users to start fresh sessions (changes only apply after restarting). Local settings file (`settings.local.json`) may not be supported in all Claude Code versions - fallback to manual context injection is recommended.

---

## Session-Level Configuration

### Location: `.claude/settings.local.json`

This local settings file overrides global settings and injects project context into every new Claude session:

```json
{
  "projectContext": {
    "paths": [
      "C:/Users/Jerry Benenett/Documents/Programming Stuff/image_draw/",
      "agents.md",
      "README.md",
      "adr/*.md"
    ],
    "instruction": "Always review agents.md as the primary source of truth for hardware specs, pin mappings, trigger modes, and file structure."
  }
}
```

### Project Context Content

On every session start, inject this context:

```text
PROJECT CONTEXT - image_draw:
─────────────────────────────────────────────────────────────────
This is an ESP32-Pi camera project with E-Ink display.
- Hardware: XIAO ESP32-S3 Sense (OV5640 sensor, PSRAM) ↔ Pi 3 (E-Ink SPI3 + SD card)
- Stream endpoint: http://<ESP32_IP>:8080/stream.txt  
- Button trigger: Pi GPIO 26, double-click=clear display, 3s hold=capture
- Always review agents.md for pin mappings, file structure, and architecture details.
─────────────────────────────────────────────────────────────────
```

### Usage

- **Option A (Recommended):** Start a fresh Claude session - context will auto-inject
- **Option B (Fallback):** Paste the above "PROJECT CONTEXT" block at the start of any new prompt

---

## Pull Request Requirements

All PRs must include these three sections:

| Section | Purpose | Example Content |
|---------|---------|-----------------|
| **What Changed** | List modifications by file/type | `- Modified: esp32s3/esp32s3.ino - Added WiFi TCP listener` |
| **Why** | Technical rationale & issue reference | `Fixes #123 - Stream endpoint was timing out during capture` |
| **How to Test** | Verification steps with expected output | `1. Connect ESP32 to WiFi<br>2. Verify stream: http://<IP>:8080/stream.txt<br>3. Press button → "Photo saved" message` |

### Commit Message Format

```
type(scope): message

What changed...

Why...

How to test...
```

Types: `feat`, `fix`, `chore`, `refactor`, `docs`, `test`

---

## Fallback Strategy

If `settings.local.json` is not supported by your Claude Code version, manually inject the project context at the start of every new session. This ensures consistency regardless of environment configuration.

---

## Related Files

- `.claude/settings.local.json` - Session-level configuration
- `.github/pull_request_template.md` - PR template with required sections
- `agents.md` - Project-wide guidelines (read on every session)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
