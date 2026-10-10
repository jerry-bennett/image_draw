/*
 * XIAO ESP32S3 Camera Bootloader - USB Serial + Camera Streaming (REV 3)
 *
 * For: XIAO ESP32S3 with CAM module
 * Pins from XIAO spec sheet:
 *   P29: Camera Select (CAM_S)
 *   P30: I2C Clock (SCL_I2C)
 *   P31: Camera DOUT (D_CAM)
 *   P32: I2C SDA (SDA_I2C)
 *   P35: I2C SCLK (SCLK_I2C)
 */

#include <Arduino.h>
#include <esp_camera.h>

// Pin configuration for XIAO ESP32S3 CAM module
#define ESP_CAM_PIN 38    // P29 - Camera select
#define ESP_CLK_PIN 39    // P30 - I2C clock
#define ESP_DATA_OUT 40    // P31 - Camera data output
#define ESP_CS_PIN 40      // P32 - SPI camera CS

#define CAMERA_PORT Serial
#ifdef WINDOWS
#define SER_PORT "/dev/ttyUSB0"
#else
#define SER_PORT "/dev/ttyACM0"
#endif

// Callback function for MJPEG streaming
static void camera_mjpeg_callback(void *user_ctx, const uint8_t *data, size_t len) {
    (void)data;
    Serial.printf("MJPG data: %zu bytes\n", len);

#ifdef SER_PORT
    // Send data to Pi over USB serial
    // Size header (4 bytes little-endian unsigned int) + JPEG payload
    uint32_t size = len;
    if (!SER.begin(SER_PORT, 115200)) {
        Serial.println("Failed to open USB serial port!");
        return;
    }

    Serial.write(reinterpret_cast<const uint8_t*>(&size), sizeof(size));
    Serial.write(data, len);
#endif
}

void setup() {
    // Initialize SPI and camera hardware
    pinMode(ESP_CAM_PIN, OUTPUT);
    digitalWrite(ESP_CAM_PIN, HIGH);

    CameraConfig config = {0};
    config.pin_pwd = -1;
    config.pin_reset = -1;
    config.pin_mosi = ESP32_CAMERA_ESP_PORT;
    config.pin_sclk = 19;      // GPIO19 for XIAO ESP32S3
    config.pin_cs = ESP_CS_PIN;
    config.pin_d0 = ESP_DATA_OUT;

    esp_camera_init(config, camera_mjpeg_callback);

#ifdef SER_PORT
    Serial.printf("Connecting to %s at 115200 baud...\n", SER_PORT);
#else
    Serial.println("Serial port connected");
#endif

    Serial.println();
    Serial.print("Camera sensor: ");

    esp_camera_init(camera_mjpeg_callback, NULL);
}

void loop() {
    uint8_t* frame = nullptr;
    size_t len = 0;

    // Acquire camera buffer (MJPG format)
    esp_camera_fb_acquire();

    while(1) {
        // Capture a frame from the camera sensor
        esp_camera_fb_capture(&frame, &len);

        if (frame && len > 0) {
            Serial.printf("Frame acquired: %zu bytes\n", len);

            // Send "START" handshake (5 bytes)
            Serial.write('S');
            Serial.write('T');
            Serial.write('A');
            Serial.write('R');
            Serial.write('T');

            // Send frame size (4-byte little-endian uint32)
            uint32_t sz = len;
            Serial.write(reinterpret_cast<const uint8_t*>(&sz), sizeof(sz));

            // Send MJPEG payload directly to Pi
            Serial.write(frame, len);
            delete[] frame;
        } else {
            Serial.println("Failed to capture frame");
        }
    }
}
