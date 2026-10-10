import subprocess
import time
from gpiozero import Button
from signal import pause

# Set up button on BCM 26 (Physical Pin 37)
# hold_time=3.0 configures when held_time triggers
button = Button(26, hold_time=3.0, bounce_time=0.05)

# Double-press tracking variables
last_press_time = 0
DOUBLE_PRESS_THRESHOLD = 0.4  # Seconds between clicks to count as a double press

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
    print("3-second hold detected! Generating image...")
    run_script("/image_draw/image_draw.py")

# Bind event listeners
button.when_pressed = handle_press
button.when_held = handle_hold

print("Button listener active. Waiting for events...")
pause()