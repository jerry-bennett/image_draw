# Camera preview script - Reads MJPEG from ESP32 Camera Bootloader via USB Serial
# For XIAO ESP32S3 connected to Raspberry Pi

import cv2
import serial
import numpy as np
import struct
import time
import sys

# Configuration for XIAO ESP32S3 via USB
PORT = sys.argv[1] if len(sys.argv) > 1 else 'COM5'  # Default: Windows COM5
BAUD = 921600      # ESP32 Camera Bootloader sends MJPEG at this rate

print(f"Connecting to {PORT} at {BAUD} baud...")

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(1)  # Allow serial reset sequence to settle
    print("Serial port opened successfully!")
except Exception as e:
    print(f"Could not open {PORT}: {e}")
    sys.exit()

print("Listening for MJPEG camera frames...")
print("(Press 'q' in terminal to stop)")

# OpenCV named window with auto-sizing for MJPEG stream
cv2.namedWindow("XIAO Camera Feed", cv2.WINDOW_AUTOSIZE)

while True:
    try:
        # MJPEG protocol detection - check if we have "START" sequence
        header = ser.read(5)

        # Verify valid start sequence (ESP32 sends partial MJPEG headers)
        if header == b'START':
            print("Received START marker")

            # Skip MJPEG SOF0 (Start of Frame 0) bytes if present
            time.sleep(0.1)  # Buffer for partial data

            # Read JPEG markers until we find SOF0 marker
            jpeg_data = b''
            while len(jpeg_data) < 4:
                new_byte = ser.read(1)
                if not new_byte or new_byte == b'\x00':
                    break
                jpeg_data += new_byte

            # Check for JPEG SOF0 marker (0xC0, 0xC2, or 0xC1)
            marker = jpeg_data[-4] | (jpeg_data[-3] << 8)
            if marker in [0xD9]:  # EOI (End of Image)
                continue

            # Read full MJPEG frame (until EOI marker 0xD9)
            frame_bytes = b''
            while len(frame_bytes) < 512:
                chunk = ser.read(4096)
                if not chunk or chunk == b'\x00':
                    break
                frame_bytes += chunk

            # Check for EOI marker
            if len(frame_bytes) > 0 and frame_bytes[-1] == 0xD9:
                print(f"Frame received: {len(frame_bytes)} bytes")

                try:
                    np_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    if frame is not None:
                        cv2.imshow("XIAO Camera Feed", frame)
                    else:
                        print("OpenCV decode failed (possibly YUV format)")

                except Exception as e:
                    print(f"Decode error: {e}")
            else:
                print(f"MJPEG incomplete")
        else:
            # Flush bytes until we find START sequence
            time.sleep(0.01)

    except KeyboardInterrupt:
        break
    except serial.SerialException as e:
        print(f"\nSerial error: {e}")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue

ser.close()
cv2.destroyAllWindows()
print("\nStream closed safely.")
