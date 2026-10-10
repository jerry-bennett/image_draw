# Quick check - see if ESP32 is sending any data over USB serial
import serial
import time

PORT = "COM5"  # Adjust to your actual COM port

print(f"Checking {PORT}...")

try:
    ser = serial.Serial(PORT, 921600, timeout=1)
    time.sleep(1)

    if not ser.is_open:
        print("Port not open! Check:")
        print("  1. XIAO ESP32S3 is powered via USB-C")
        print("  2. Device appears in Windows Device Manager as 'USB Serial Adapter' or 'FTDI USB-to-UART')")

    # Check available bytes
    count = ser.in_waiting
    print(f"Serial port opened - {count} bytes available in buffer")

    if count > 0:
        data = ser.read(count)
        print(f"\nRAW DATA ({len(data)} bytes):")
        for i in range(min(10, len(data))):
            b = data[i]
            ascii_char = chr(b) if 32 <= b < 127 else '.'
            print(f"  [{i:2d}] {b:3d} (0x{b:02x}) '{ascii_char}'")
    else:
        print("No data in buffer - ESP32 may not be active or baud rate mismatch")

    # Send test message to verify connection
    ser.write(b"TEST12345")
    time.sleep(0.5)

    response = ser.read(10)
    if len(response) > 0:
        print(f"\nTest response ({len(response)} bytes): {response}")
    else:
        print("\nNo response received - check baud rate (921600 vs 115200)")

except serial.SerialException as e:
    print(f"Serial error: {e}")

ser.close()
