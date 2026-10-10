/*
 * XIAO ESP32S3 - Capture and Display on XIAO's Built-in OLED Screen
 * Shows camera preview directly on ESP32 board (not over USB)
 */

#include <Arduino.h>
#include <esp_camera.h>
#include "freertos/FreeRTOS.h"
#include "driver/gicc_spi.h"
#include "sdkconfig.h"

// Pin configuration for XIAO ESP32S3 CAM module (OV7670/OV5640)
#define CAMERA_PIN 38    // P29 - Camera select
#define CSI_CLK_PIN 39   // P30 - I2C clock for sensor
#define CSI_DOUT_PIN 40  // P31 - Camera data output
#define CAMERA_CS_PIN 40  // P32 - SPI camera CS

void setup() {
    Serial.begin(115200);

#ifdef CAMERA_PIN
    ESP.setPin(CAMERA_PIN);
#endif

    // Initialize camera sensor (OV7670/OV5640)
    esp_camera_init();

    Serial.println("Camera initialized");

    // Set camera output to RGB565 format
    esp_camera_fb_setrgb_format(ESP_CAMERA_BGR_10BPP);

    Serial.print("Starting camera capture at 30 fps...");
    ESP.setFrameRate(30);
}

void loop() {
    uint8_t* frame = nullptr;
    size_t len = 0;

    // Acquire camera buffer (RGB565 format, 24-bit color)
    esp_camera_fb_acquire();

    while (1) {
        // Capture frame from OV7670/OV5640 sensor
        esp_camera_fb_capture(&frame, &len);

        if (frame && len > 0) {
            Serial.printf("Frame: %zu bytes\n", len);

            // Get image dimensions
            uint32_t width = frame->width;
            uint32_t height = frame->height;

            // Display directly on XIAO's built-in OLED screen (0.96 inch 128x64)
#ifdef CAMERA_PIN
            esp_camera_display(frame, ESP_CAMERA_WIDTH, ESP_CAMERA_HEIGHT);
#else
            esp_camera_display_raw(frame, ESP_CAMERA_WIDTH, ESP_CAMERA_HEIGHT);
#endif

            delete[] frame;
        } else {
            Serial.println("Failed to capture frame");
        }
    }
}
