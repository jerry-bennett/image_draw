#!/usr/bin/python3
# -*- coding:utf-8 -*-
from gpiozero import Button
import subprocess
import time
import logging

logging.basicConfig(level=logging.INFO)

# GPIO 17 (Physical Pin 11) connected to GND when pressed
button = Button(17)

# Target script path
SCRIPT_PATH = "/home/admin/Image_Draw/image_draw.py"

def trigger_display_update():
    logging.info("Button pressed! Running image_draw.py...")
    try:
        # Run the display script as a subprocess
        result = subprocess.run(["python3", SCRIPT_PATH], check=True)
        logging.info("Display update finished.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing script: {e}")

logging.info("Button listener active. Press the button on GPIO 17 to refresh screen...")

# Attach the press event
button.when_pressed = trigger_display_update

# Keep script running in background
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    logging.info("Exiting listener script.")