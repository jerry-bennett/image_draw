/*
 * XIAO ESP32S3 Camera Bootloader - USB Serial + Camera Streaming
 * Sends MJPEG camera frames via USB serial to Pi running cam_preview.py
 *
 * Protocol:
 *   1. "START" (5 bytes) - handshake
 *   2. Size header (4 bytes little-endian unsigned int)
 *   3. JPEG payload
 */

#include <Arduino.h>
#include <Wire.h>

#define ESP32_CAMERA_ESP_PORT Serial
#define SERIAL_BUFFER_SIZE 512

// Serial port to Pi (adjust if COM port differs - Windows shows as "COM*" on Linux)
#ifdef WINDOWS
#define PORT "/dev/ttyUSB0" // Or /dev/ttyACM0 for ESP32-SIDECAR
#else
#define PORT "/dev/ttyACM0" // Default for XIAO ESP32S3 via USB
#endif

// Camera parameters (XIAO ESP32S3 CAM module, OV7670 or OV5640)
#ifdef XIAO_ESP32_S3_CAM_MODULE
#define CAMERA_PIN 38   // P29 - camera select on XIAO ESP32S3
#define CSI_CLK Pin(39) // P30 - I2C clock for camera sensor
#define CSI_DOUT Pin(40) // P31 - Camera data out
#else
// Default camera pins if module not detected
#define CAMERA_PIN 28   // GPIO28
#define CSI_CLK Pin(25)
#define CSI_DOUT Pin(23)
#endif

volatile bool serial_data_available = false;
SerialBuffer buffer;

void setup() {
    Serial.begin(115200);
    delay(1000);

#ifdef WINDOWS
    ESP.setPin(CAMERA_PIN);
    Serial.printf("Connecting to %s at 115200 baud...\n", PORT);
    Serial.flush();
    if (!Serial.begin(PORT, 115200)) {
        Serial.printf("Failed to open port: %s\n", PORT);
    } else {
        Serial.println("Serial port opened successfully!");
    }
#else
    ESP.setPin(CAMERA_PIN);
    Serial.printf("Connecting to USB Serial at 115200 baud...\n");
    if (!Serial.begin(PORT, 115200)) {
        Serial.printf("Failed to open port: %s\n", PORT);
    } else {
        Serial.println("Serial port opened successfully!");
    }
#endif

    // Initialize camera sensor (OV7670/7675 or OV5640)
    esp_camera_init();
    Serial.printf("Camera initialized\n");

    // Start camera
    Serial.print("Starting camera capture...\n");
    esp_capture_start();
}

void loop() {
    serial_data_available = false;

    // Check USB serial buffer for incoming data from Pi
    if (Serial.available() > 0) {
        int available = Serial.readAvailable();
        Serial.println(F("USB Serial: "), available);

        // Read "START" handshake (5 bytes)
        char header[6];
        header[0] = 'S';
        header[1] = 'T';
        header[2] = 'A';
        header[3] = 'R';
        header[4] = 'T';

        // Read size header (4 bytes little-endian)
        uint32_t size;
        Serial.readBytes(header, 5);
        for (int i = 0; i < 4; i++) {
            size |= ((uint8_t)Serial.read() << (i * 8));
        }

        if (!Serial.available()) continue;

        // Read JPEG payload
        std::vector<uint8_t> jpeg(size);
        int read_count = Serial.readBytes(reinterpret_cast<char*>(&jpeg[0]), size);
        while(read_count < static_cast<int>(size)) {
            read_count += Serial.readBytes(reinterpret_cast<char*>(&jpeg[size_count + 1]), 4096);
        }

        // Decode and send camera data to Pi
        uint8_t *buf;
        int len;
        esp_camera_decode( reinterpret_cast<uint32_t>(&jpeg[0]), jpeg.size(), buf, &len );

        if (buf && len > 0) {
            Serial.printf("Transmitting camera frame: %d bytes\n", len);
            Serial.write(reinterpret_cast<const uint8_t*>(buf), len);
            delete[] buf;
            serial_data_available = true;
        } else {
            Serial.println("Decoding failed");
        }
    }
}

void loop_camera() {
    Serial.println(F("\nStarting Camera Loop"));

    // Main camera loop - this is typically handled by esp_camera_fb_capture
    while (1) {
        uint8_t *buf;
        int len;

        esp_camera_frame_acquire(&buf, &len);

        if (buf && len > 0) {
            Serial.printf("Camera frame: %d bytes\n", len);

            // Transmit the frame to Pi via USB serial
            Serial.write(reinterpret_cast<const uint8_t*>(buf), len);

            // Notify Pi that data is ready
            serial_data_available = true;

            delete[] buf;
        }
    }
}
