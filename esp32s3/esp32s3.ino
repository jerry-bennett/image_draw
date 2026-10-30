#include "esp_camera.h"
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include <WiFi.h>
#include <WiFiServer.h>

#define CAMERA_MODEL_XIAO_ESP32S3 // Has PSRAM

#include "camera_pins.h"
#include "ESP32_OV5640_AF.h"   // OV5640 auto-focus library (github.com/0015/ESP32-OV5640-AF)

OV5640 ov5640 = OV5640();

// WiFi server for TCP/IP signaling from Pi button
WiFiServer server(8080);
bool tcp_capture_request_received = false;

// Handle TCP/IP capture request from Pi button
void handleCaptureRequest() {
  tcp_capture_request_received = false;
  Serial.println("\n--- Capture Request Received via WiFi ---");

  // Take a photo (directly, no stream needed when triggered)
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Failed to get camera frame buffer");
    return;
  }

  // Save photo to SD card immediately
  char filename[32];
  sprintf(filename, "/image%d.jpg", imageCount);
  writeFile(SD, filename, fb->buf, fb->len);

  // Release image buffer
  esp_camera_fb_return(fb);

  Serial.printf("Photo saved: %s\n", filename);
}

// Save pictures to SD card
void photo_save(const char * fileName) {
  // Take a photo (for auto-capture mode)
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Failed to get camera frame buffer");
    return;
  }
  // Save photo to file
  writeFile(SD, fileName, fb->buf, fb->len);

  // Release image buffer
  esp_camera_fb_return(fb);

  Serial.println("Photo saved to file");
}

// SD card write file
void writeFile(fs::FS &fs, const char * path, uint8_t * data, size_t len){
    Serial.printf("Writing file: %s\r\n", path);

    File file = fs.open(path, FILE_WRITE);
    if(!file){
        Serial.println("Failed to open file for writing");
        return;
    }
    if(file.write(data, len) == len){
        Serial.println("File written");
    } else {
        Serial.println("Write failed");
    }
    file.close();
}

// Wait for the OV5640 continuous auto-focus to settle (FW_STATUS == 0x10 FOCUSED)
bool waitForOv5640Focus() {
  const uint32_t started = millis();
  uint8_t status = 0;
  while (millis() - started < OV5640_FOCUS_TIMEOUT_MS) {
    status = ov5640.getFWStatus();
    if (status == 0x10) {
      Serial.printf("OV5640 focus settled: FW_STATUS=0x%02X\n", status);
      return true;
    }
    delay(100);
  }
  Serial.printf("ERROR: OV5640 focus not settled within %u ms; last FW_STATUS=0x%02X\n",
                OV5640_FOCUS_TIMEOUT_MS, status);
  return false;
}

void setup() {
  Serial.begin(115200);
  while(!Serial); // When the serial monitor is turned on, the program starts to execute

  // Initialize WiFi for TCP/IP signaling from Pi button
  Serial.println("Initializing WiFi server on port 8080...");
  WiFi.mode(WIFI_STA);
  tcp_capture_request_received = false;

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  config.grab_mode = CAMERA_GRAB_WHEN_EMPTY;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(config.pixel_format == PIXFORMAT_JPEG){
    if(psramFound()){
      config.jpeg_quality = 10;
      config.fb_count = 2;
      config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
      // Limit the frame size when PSRAM is not available
      config.frame_size = FRAMESIZE_SVGA;
      config.fb_location = CAMERA_FB_IN_DRAM;
    }
  } else {
    // Best option for face detection/recognition
    config.frame_size = FRAMESIZE_240X240;
#if CONFIG_IDF_TARGET_ESP32S3
    config.fb_count = 2;
#endif
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  camera_sign = true; // Camera initialization check passes

  // --- OV5640 auto-focus init (a key step missing from factory firmware; without it the lens defaults out of focus) ---
  sensor_t *s = esp_camera_sensor_get();
  if (s && s->id.PID == OV5640_PID) {
    Serial.println("OV5640 detected, initializing auto-focus...");
    // Switch to SXGA for focusing (the AF firmware needs >=1280x1024 to evaluate contrast)
    if (s->set_framesize(s, OV5640_AF_FOCUS_FRAMESIZE) != 0) {
      Serial.println("WARN: cannot set SXGA for AF focus, captures will be out of focus");
    } else if (!ov5640.start(s)) {
      Serial.println("WARN: OV5640 CHIPID check failed, AF skipped");
      s->set_framesize(s, config.frame_size); // restore the capture framesize
    } else {
      int r1 = ov5640.focusInit();                       // load focus firmware, 0 = success
      int r2 = (r1 == 0) ? ov5640.autoFocusMode() : -1;  // enable continuous auto-focus
      Serial.printf("  focusInit=%d autoFocusMode=%d\n", r1, r2);
      if (r1 == 0 && r2 == 0 && waitForOv5640Focus()) {
        Serial.println("OV5640 AF ready.");
      } else {
        Serial.println("ERROR: OV5640 AF setup failed; captures will be out of focus.");
      }
      // Restore the capture framesize
      if (s->set_framesize(s, config.frame_size) != 0) {
        Serial.println("WARN: cannot restore capture framesize");
      }
    }
  }

  // Initialize WiFi server for TCP/IP signaling from Pi button
  Serial.println("Setting up WiFi TCP server...");
  IPAddress pi_ip(192, 168, 4, 1); // Default ESP32 AP IP (adjust based on your network)
  server.begin();
  Serial.print("WiFi server listening for capture requests at http://");
  Serial.print(WiFi.localIP());
  Serial.println(":8080/capture");

  // Initialize SD card
  if(!SD.begin(21)){
    Serial.println("Card Mount Failed");
    return;
  }
  uint8_t cardType = SD.cardType();

  // Determine if the type of SD card is available
  if(cardType == CARD_NONE){
    Serial.println("No SD card attached");
    return;
  }

  Serial.print("SD Card Type: ");
  if(cardType == CARD_MMC){
    Serial.println("MMC");
  } else if(cardType == CARD_SD){
    Serial.println("SDSC");
  } else if(cardType == CARD_SDHC){
    Serial.println("SDHC");
  } else {
    Serial.println("UNKNOWN");
  }

  sd_sign = true; // sd initialization check passes

  Serial.println("Photos will begin in one minute, please be ready.");
}

// Handle WiFi TCP requests from Pi button
bool handleTcpServer() {
  if (!tcp_capture_request_received) return false;

  // Read incoming data from TCP connection
  while (server.available()) {
    char request = (char)server.read();

    // Look for "CAPTURE" keyword in HTTP request
    if (request == 'C' || request == 'A' || request == 'P' ||
        request == 'T' || request == 'U' || request == 'R' || request == 'E') {
      tcp_capture_request_received = true;
    }
  }

  return true;
}

void loop() {
  // Handle WiFi TCP requests from Pi button
  handleTcpServer();

  // Camera & SD available, start taking pictures
  if(camera_sign && sd_sign){
    // Get the current time
    unsigned long now = millis();

    //If it has been more than 1 minute since the last shot, take a picture and save it to the SD card
    if ((now - lastCaptureTime) >= 60000) {
      char filename[32];
      sprintf(filename, "/image%d.jpg", imageCount);
      photo_save(filename);
      Serial.printf("Saved picture: %s\r\n", filename);
      Serial.println("Photos will begin in one minute, please be ready.");
      imageCount++;
      lastCaptureTime = now;
    }
  }

  // Drain any remaining TCP data after processing
  handleTcpServer();
}
