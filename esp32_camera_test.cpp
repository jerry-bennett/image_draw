/*
 * XIAO ESP32S3 Camera Bootloader - Debug/Monitor Mode
 * Sends basic USB serial messages to test connection with Pi
 */

#include <Arduino.h>
#include <Wire.h>

#ifdef WINDOWS
#define PORT "/dev/ttyUSB0"
#else
#define PORT "/dev/ttyACM0"
#endif

void setup() {
    Serial.begin(115200);
    Wire.begin();

    delay(1000);

#ifdef WINDOWS
    Serial.printf("Windows: Connecting to %s...\n", PORT);
#else
    Serial.printf("Connecting to %s at 115200 baud...\n", PORT);
#endif

    Serial.flush();

    Serial.println();
    Serial.println("=== XIAO ESP32S3 Bootloader ===");
    Serial.print("Initializing ESP32 camera...\n");

    esp_camera_init();
    Serial.println("Camera initialized!");

    // Print sensor info
#ifdef OV7670
    uint8_t id[] = {0x6F, 0x55};
    bool ok = (esp_sensor_id(id) == ESP_CAMERA_OK);
    Serial.printf("Sensor ID: %s\n", ok ? "OK" : "FAILED");
#endif

    // Test USB serial to Pi connection
    Serial.println("Testing USB connection...");
    uint32_t test_data = 0x12345678;
    Serial.write(reinterpret_cast<const uint8_t*>(&test_data), sizeof(test_data));
    Serial.println("Test data transmitted (size: 4 bytes)");

    // Start camera capture
    Serial.println("\nStarting continuous MJPEG stream...");
    esp_camera_fb_acquire();

    while(1) {
        uint8_t* frame = nullptr;
        size_t len = 0;

        esp_camera_fb_capture(&frame, &len);

        if (frame && len > 0) {
            Serial.printf("Camera frame: %zu bytes\n", len);
            Serial.write(frame, len);
            delete[] frame;
        }
    }
}
