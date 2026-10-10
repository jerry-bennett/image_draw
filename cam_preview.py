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
BAUD = 115200    # Match ESP32 firmware baud rate (USB serial speed)

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

last_error_message = False

while True:
    try:
        # Keep reading data from ESP32 serial - MJPEG stream comes continuously
        # ESP32 Camera Bootloader sends data as partial frames

        # Read more data (adjust buffer size for better responsiveness)
        chunk = ser.read(1024)  # Read up to 1KB at a time
        if not chunk:
            time.sleep(0.05)
            continue

        # Check for error messages
        error_patterns = [b'Camera capture', b'capture failed', b'failed']
        is_error = False
        for pattern in error_patterns:
            if pattern in chunk:
                print(f"\n*** ERROR DETECTED ***")
                print("ESP32 Camera Bootloader may be stuck or failing!")

                # Clear the error buffer and wait longer for next attempt
                extra_chunk = ser.read(4096)
                total_data = b''.join([chunk, extra_chunk])
                time.sleep(5)  # Wait longer between attempts
                print("\nWaiting for ESP32 to reset...")

                is_error = True
                break

        if not is_error and chunk.startswith(b'START'):
            print("\n*** FOUND COMMUNICATION MARKER ***")
            time.sleep(0.1)

        # Look for EOI marker (0xD9) - end of JPEG frame
        eoi_pos = None
        for i in range(len(chunk)):
            if chunk[i] == 0xD9:
                eoi_pos = i
                break

        # If we found a complete frame with EOI marker, process it
        if eoi_pos is not None:
            frame_bytes = chunk[:eoi_pos+1]
            print(f"\nComplete frame received: {len(frame_bytes)} bytes")
            try:
                np_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    # Display the decoded image
                    cv2.imshow("XIAO Camera Feed", frame)

                    # Wait for key press to continue
                    while True:
                        key = cv2.waitKey(100) & 0xFF
                        if key == ord('q'):
                            break
                else:
                    print("OpenCV decode failed (possibly YUV format)")

            except Exception as e:
                print(f"Decode error: {e}")
                continue
        else:
            # No complete frame yet, check for START marker
            if chunk.startswith(b'START'):
                print("\n*** FOUND COMMUNICATION MARKER ***")
                time.sleep(0.1)
    except KeyboardInterrupt:
        break
    except serial.SerialException as e:
        print(f"\nSerial error: {e}")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue

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
