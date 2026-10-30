---
name: 0002-documentation-review-guidelines
description: Guidelines requiring AI agents to review agents.md for project context
metadata:
  type: reference
---

## Decision Log Entry

### Status: 🟢 Recommended / Adopted

**Context:** `agents.md` serves as the central source of truth for all AI agent operations in this project, containing hardware specifications, file structure, pin mappings, trigger modes, and best practices.

**Decision:** All AI agents (subagents spawned by any process) must review `agents.md` before beginning work on project-related tasks. This ensures consistent understanding of the hybrid ESP32-Pi architecture and prevents conflicting or duplicated work.

**Consequences:**
- **Positive:** Agents will understand hardware constraints (SPI3 for E-Ink, OV5640 pin mapping), existing trigger logic (`button_trigger.py`), and project goals. Reduces context-waste from agents reinventing documentation they already have access to.
- **Negative:** Adds a small overhead to agent initialization (~100 tokens read). Requires that `agents.md` stay current with any architectural changes.

---

## Implementation Pattern for AI Agents

When spawning a new agent for project work, always include this preamble instruction in the prompt:

```text
Before you begin, review and internalize these guidelines from agents.md:
- Hardware architecture: XIAO ESP32-S3 Sense (camera + PSRAM) ↔ Raspberry Pi 3 (Python + E-Ink display + SD card)
- Communication: Pi button (GPIO 26) triggers capture; ESP32 streams MJPEG over WiFi to http://<ESP32_IP>:8080/stream.txt
- File structure: See esp32s3/esp32s3.ino for ESP32 C++, /image_draw/*.py for Pi Python scripts, lib/waveshare_epd/ for E-Ink library
- Trigger modes: 3-second button hold = capture, double-click = clear display
- Pin mapping: XIAO uses default Seeed Wiki GPIO definitions (Y2-D0, Y8-D7, XMCLK/XCLK, etc.)
- OV5640 AF: Requires SXGA resolution (≥1280×1024) before auto-focus; restore original capture size after focus
- Memory patterns: Use feedback/project/reference memory files with consistent naming
```

This instruction should be included in **every** agent prompt for project-related work.

---

## Why This Matters

Agents.md is the only single source of truth for hardware-specific constraints and integration details. Without this review requirement, agents may:
- Recommend incompatible pin configurations
- Suggest resolutions incompatible with OV5640 AF requirements  
- Overwrite trigger logic in `button_trigger.py` without confirmation
- Forget that `image_draw.py` exists but is missing from the directory (needs to be implemented)

Always cross-reference `agents.md` before making hardware-related decisions, code modifications, or architectural changes.

---

## When `agents.md` Should Be Updated

Update this file when:
- Hardware configuration changes (new pins, different sensor)
- Trigger logic is modified
- New features are added to the architecture
- File structure changes significantly

Then mark it **Superseded** in the decision-log table below.

| ADR | Decision Date | Status | Notes |
|-----|---------------|--------|-------|
| 0001 | - | Superseded | Record Architecture Decisions (original) |
| 0002 | 2026-10-30 | Recommended | AI agents must review agents.md |

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
