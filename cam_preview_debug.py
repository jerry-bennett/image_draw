# Debug script to inspect raw data from ESP32 Camera Bootloader

import serial
import struct
import time
import sys

PORT = sys.argv[1] if len(sys.argv) > 1 else 'COM5'

print(f"Connecting to {PORT} at 115200 baud (ESP32 firmware USB Serial)...")

try:
    ser = serial.Serial(PORT, 921600, timeout=1)
    time.sleep(1)
    print("Serial port opened!")
except Exception as e:
    print(f"Could not open {PORT}: {e}")
    sys.exit()

print("\nWaiting for MJPEG stream... (Press 'q' to stop)")

while True:
    try:
        # ESP32 Camera Bootloader sends MJPEG stream
        # Baud rate MUST match! 921600 is standard for ESP32 Camera Bootloader

        # Read partial data from serial
        data = ser.read(4096)

        if not data or len(data) == 0:
            time.sleep(0.05)
            continue

        # Print raw data with error message detection
        print(f"\n--- RAW DATA (first {min(100, len(data))} bytes) ---")
        for i in range(0, min(100, len(data)), 10):
            chunk = data[i:i+10]
            hex_str = ''.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f"{i:4d}: {hex_str} '{ascii_str}'")

        # Check for error messages
        error_patterns = [b'Camera capture', b'capture failed', b'failed']
        is_error = False
        for pattern in error_patterns:
            if pattern in data:
                print(f"\n*** ERROR DETECTED: {data.find(pattern) > 0 and ' or '.join(patterns.split()) or 'error message' } ***")
                print("ESP32 Camera Bootloader may be stuck!")

                # Clear the error buffer and wait longer for next attempt
                data = ser.read(4096)
                total_data = b''.join([data])
                time.sleep(5)  # Wait longer between attempts
                print("\nWaiting for ESP32 to reset...")

                is_error = True
                break

        if not is_error and (b'START' in data or b'SIZE' in data):
            print("\n*** FOUND COMMUNICATION MARKER ***")

            if b'SIZE' in data:
                size_pos = data.find(b'SIZE')
                if size_pos > 0:
                    # Extract frame size (4 bytes after SIZE marker)
                    size_bytes = data[size_pos+5:size_pos+9]
                    size = struct.unpack('<I', size_bytes)[0]
                    print(f"Frame size header: {size} bytes")

                # Read remaining data up to 1MB max
                read_remaining = min(1024*1024 - len(data), 5000)
                jpeg_data = ser.read(read_remaining)
                total_size = len(jpeg_data)

                print(f"Read {total_size} bytes of MJPEG data")

                # Print JPEG markers for debugging
                jpeg_markers = []
                i = 0
                while i < min(20, total_size):
                    marker_byte = data[i] if i < len(data) else b''
                    jpeg_markers.append(marker_byte)
                    i += 1

                print(f"\nJPEG markers: {list(jpeg_markers)}")

            elif b'START' in data:
                # START handshake (5 bytes)
                start_pos = data.find(b'START')
                size_bytes = data[start_pos+5:start_pos+9]
                size = struct.unpack('<I', size_bytes)[0]
                print(f"START received, frame size: {size} bytes")

                # Read MJPEG frame (until EOI 0xD9)
                jpeg_data = b''
                while True:
                    new_byte = ser.read(1)
                    if not new_byte or new_byte == b'\x00':
                        break
                    jpeg_data += new_byte

                print(f"Total MJPEG frame size: {len(jpeg_data)} bytes")

                # Look for EOI marker (0xD9)
                endi = 0
                for i in range(min(10, len(jpeg_data))):
                    if jpeg_data[i] == 0xD9:
                        endi = i
                        break

                if len(jpeg_data) > 0 and jpeg_data[-1] == 0xD9:
                    print(f"EOI found at byte {endi}")

        # Check for EOI marker (0xD9 = end of image)
        if data[-1:] == b'\xd9':
            print("\n*** EOI DETECTED - Image complete ***")

        # Keep loop active to show raw bytes in terminal
        time.sleep(0.1)

    except serial.SerialException as e:
        print(f"\nSerial error: {e}")
        break
    except Exception as e:
        print(f"Error: {e}")
        continue

ser.close()
print("\nDebug session ended.")
