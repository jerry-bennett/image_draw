/*
 * XIAO ESP32S3 Camera Bootloader - USB Serial + Camera Streaming (REV 2)
 * Sends MJPEG camera frames via USB serial to Pi running cam_preview.py
 *
 * For: XIAO ESP32S3 with CAM module (ov7670/ov5640 OV sensors)
 * Pins: P29-CMSI, P30-CLK_I2C, P31-DOUT_CAM, P32-WIO_SPI_CS
 */

#include <Arduino.h>

#define ESP32_CAMERA_ESP_PORT Serial
#define SERIAL_BUFFER_SIZE 512
#ifdef WINDOWS
#define PORT "/dev/ttyUSB0"  // Adjust if different - XIAO outputs on USB-C
#else
#define PORT "/dev/ttyACM0" // Default for XIAO ESP32S3
#endif

// Camera capture callback
extern "C" void camera_capture_cb(void *user_ctx) {
    uint8_t* frame = (uint8_t*)user_ctx;
    size_t len = esp_camera_frame_get_size(frame);

    Serial.printf("Capture: %zu bytes\n", len);

    // Send size header (little-endian unsigned int)
    Serial.write(reinterpret_cast<const uint8_t*>(&len), sizeof(len));

    // Copy frame data to serial buffer
    Serial.write(frame, len);
}

void setup() {
    Serial.begin(115200);
    delay(1000);

#ifdef WINDOWS
    Serial.printf("Connecting to %s at 115200 baud...\n", PORT);
    Serial.flush();
#else
    Serial.printf("Connecting to USB Serial (%s) at 115200 baud...\n", PORT);
#endif

    // Initialize camera
    esp_camera_init(camera_capture_cb, NULL);

    Serial.println("Camera initialized");

    // Start continuous capture
    Serial.print("Starting MJPEG stream...\n");
    esp_camera_fb_acquire();

    // Begin camera loop - this reads from sensor and sends to USB
    while (1) {
        uint8_t* frame = nullptr;
        size_t len = 0;

        esp_camera_fb_capture(&frame, &len);

        if (frame && len > 0) {
            Serial.printf("Frame: %zu bytes\n", len);

            // Send "START" handshake
            Serial.write("ST");

            // Send frame size
            Serial.write(reinterpret_cast<const uint8_t*>(&len), sizeof(len));

            // Send JPEG data
            Serial.write(frame, len);

            delete[] frame;
        }
    }
}
