import subprocess
import time
import requests
from gpiozero import Button
from signal import pause

# ESP32 WiFi server endpoint for TCP/IP signaling
ESP32_STREAM_URL = "http://192.168.4.1:8080/stream.txt"  # Use your ESP32's actual IP when connected to AP
ESP32_CAPTURE_ENDPOINT = "http://192.168.4.1:8080/capture"

# Set up button on BCM 26 (Physical Pin 37)
# hold_time=3.0 configures when held_time triggers
button = Button(26, hold_time=3.0, bounce_time=0.05)

# Double-press tracking variables
last_press_time = 0
DOUBLE_PRESS_THRESHOLD = 0.4  # Seconds between clicks to count as a double press

def send_wifi_capture_signal():
    """Send WiFi signal to ESP32 to trigger capture"""
    try:
        print(f"Sending WiFi capture request to {ESP32_CAPTURE_ENDPOINT}")
        requests.get(ESP32_CAPTURE_ENDPOINT)
        print("WiFi capture signal sent!")
    except Exception as e:
        print(f"Error sending WiFi signal: {e}")
        print("Falling back to stream capture mode...")

def run_stream_capture():
    """Run the image_draw.py script that captures from ESP32 stream"""
    # This is a fallback - requires image_draw.py to exist
    # Currently, we'll just log it since the script doesn't exist yet
    print("Stream capture available in image_draw.py (not yet implemented)")

def run_script(path):
    """Utility to safely launch a script in a subprocess."""
    try:
        print(f"Executing: {path}")
        subprocess.Popen(["python3", path])
    except Exception as e:
        print(f"Error running {path}: {e}")

def handle_press():
    global last_press_time
    current_time = time.time()

    # Check if this press happened within the double-press window
    if (current_time - last_press_time) < DOUBLE_PRESS_THRESHOLD:
        print("Double press detected! Clearing display...")
        run_script("/image_draw/clear.py")
        last_press_time = 0  # Reset
    else:
        last_press_time = current_time

def handle_hold():
    # Send WiFi capture signal to ESP32 (recommended mode)
    # OR use stream capture if image_draw.py exists
    send_wifi_capture_signal()

# Bind event listeners
button.when_pressed = handle_press
button.when_held = handle_hold

print("Button listener active. Waiting for events...")
pause()
