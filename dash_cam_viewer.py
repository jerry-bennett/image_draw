"""
ESP32 Camera Viewer - Display camera feed from XIAO ESP32-S3 Sense over WiFi

The XIAO ESP32-S3 Sense comes with WebCam firmware pre-installed that streams
camera feeds at http://<local_ip>:8080 when connected to WiFi.

Dependencies: pip install Pillow requests opencv-python-headless (optional)
"""

import socket
import time
from PIL import Image
import sys


# Camera specs based on documentation (XIAO ESP32-S3 Sense)
# OV5640 (AF): 2592x1944 | OV3660: 2048x1536 | OV2640: 1600x1200


class ESP32CameraViewer:
    """Class to capture and display frames from ESP32 camera stream."""

    def __init__(self, ip_address):
        """Initialize viewer with ESP32 IP address.

        Args:
            ip_address: ESP32's local IP (e.g., "192.168.4.100")
        """
        self.ip = ip_address
        # ESP32 camera streams use MJPEG format over TCP port 8080
        self.stream_port = 8080
        self.sock = None
        self.buffer = []

    def connect(self):
        """Establish TCP connection to ESP32 camera stream."""
        try:
            print(f"\n{'='*50}")
            print(f"Connecting to ESP32 at {self.ip}:{self.stream_port}...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.ip, self.stream_port))
            print(f"✓ Connected to ESP32!")

            # Send HTTP request to start stream (if needed)
            sock.sendall(b"GET /stream.txt HTTP/1.0\r\nHost: http://localhost\r\n\r\n")

            return sock
        except Exception as e:
            print(f"\n✗ Connection failed: {e}")
            print("Ensure ESP32 is connected and camera stream enabled")
            return None

    def process_frame(self, data):
        """Process raw MJPEG frame data and save to file.

        Args:
            data: Raw byte data containing JPEG frames

        Returns:
            Path to saved image file, or None on error
        """
        try:
            # Decode JPEG frames
            img = Image.open(socket.socketpair((self.ip, self.stream_port)))
            img.load()

            # Save with timestamp
            filename = f"{time.strftime('%H%M%S_%f')}.jpg"
            print(f"\n📹 Frame captured: {img.size[0]}x{img.size[1]}")
            print(f"  Mode: {img.mode}, Pixels: {img.size[0] * img.size[1]}")

            from io import BytesIO as BIO
            img.save(filename)
            print(f"  Saved to: {filename}")
            return filename

        except Exception as e:
            print(f"Error processing frame: {e}")
            return None


class SingleFrameMode(ESP32CameraViewer):
    """Capture and display a single frame."""

    def capture_once(self, timeout=5.0):
        """Capture one frame from the stream.

        Returns:
            (Image, socket) tuple or (None, None) on error
        """
        self.sock = self.connect()
        if not self.sock:
            return None, None

        try:
            start_time = time.time()

            # Read chunks until we complete a frame (0xFFD9 marker)
            data = b''
            while True:
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                data += chunk

                # Look for JPEG end marker
                if b'\xff\xd9' in data:
                    frame_end = data.find(b'\xff\xd9')
                    frame = data[:frame_end]

                    filename = self.process_frame(frame)
                    return (Image.open(BytesIO(frame)), self.sock) if filename else None

            print("Timeout waiting for frame")
            return None, None

        except Exception as e:
            print(f"Capture error: {e}")
            return None, None


def main():
    """Main function - configure and run viewer."""

    # Configuration (can also use environment variables)
    ESP32_IP = "192.168.4.100"  # Set to your ESP32's local IP
    USE_DEFAULT_IP = True        # Set False to manually specify IP

    print("=" * 50)
    print("ESP32 Camera Viewer v1.0")
    print("=" * 50)

    # Try to auto-detect ESP32 IP (requires scapy and elevated privileges on Windows)
    auto_detect_ip = True if USE_DEFAULT_IP else False

    if auto_detect_ip:
        try:
            from scapy.all import conf, ARP, Ether, IP, sr1

            conf.disable_verbose()

            arp_pkt = Ether(src="ff:ff:ff:ff:ff:ff") / \
                       IP(dst="255.255.255.255") / \
                       ARP(psrc="192.168.4.1", pdst="255.255.255.255")

            response = sr1(arp_pkt, timeout=3)

            if response:
                for packet in response:
                    if hasattr(packet, 'payload') and hasattr(packet.payload, 'src'):
                        ip = packet.payload.src
                        print(f"✓ Auto-detected ESP32 IP: {ip}")
                        ESP32_IP = ip
        except ImportError:
            print("scapy not installed (pip install scapy)")
        except Exception as e:
            print(f"Auto-detect failed: {e}")

    # Start viewer
    print(f"\n🎥 Target: {ESP32_IP}")
    print("=" * 50)

    try:
        if len(sys.argv) > 1 and sys.argv[1] in ["-s", "--stream"]:
            # Stream mode (continuous capture)
            print("\n📡 Starting continuous stream mode...")
            viewer = ESP32CameraViewer(ESP32_IP)
            while True:
                # Simple polling loop - can be optimized for real-time streaming
                time.sleep(1.0)  # Adjust based on desired capture rate

        else:
            # Single frame mode (default)
            print("\n📸 Using single-frame capture mode...\n")

            viewer = SingleFrameMode(ESP32_IP)
            img, sock = viewer.capture_once(timeout=5.0)

            if sock:
                sock.close()
                if img:
                    print(f"\n✓ Saved frame to {time.strftime('%H%M%S_%f')}.jpg")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")


if __name__ == "__main__":
    main()
