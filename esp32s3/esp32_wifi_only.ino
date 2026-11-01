// esp32_wifi_only.ino - Simple WiFi connection test for ESP32-S3 Sense
// Connect to home WiFi, prints IP address, waits for Pi signals

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>

// ============================================================================
// Configuration
// ============================================================================

#define WIFI_SSID     "dangus"
#define WIFI_PASSWORD "eraserhead"

// ============================================================================
// Global Variables
// ============================================================================

bool tcp_capture_request_received = false;
const char* esp32_ip_address = NULL;
char ip_string[16];

WiFiClient client;

// ============================================================================
// Functions for WiFi Client Mode
// ============================================================================

void connectToWiFi() {
  Serial.println("Connecting to WiFi 'dangus'...");

  // Connect to WiFi client mode (NOT server/AP mode)
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  // Wait for connection
  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < 120) {
    delay(500);
    Serial.print(".");
    attempt++;
  }

  Serial.println();
  Serial.println("WiFi connected!");

  // Get local IP address
  Serial.print("ESP32 IP: ");
  esp32_ip_address = WiFi.localIP().toString().c_str();
  strcpy(ip_string, esp32_ip_address);

  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());
}

// Handle TCP/IP capture requests from Pi button
void handleCaptureRequest() {
  tcp_capture_request_received = false;

  if (esp32_ip_address) {
    Serial.printf("Waiting for capture request from %s...", esp32_ip_address);
    delay(1000);
  }

  Serial.println("Ready to receive capture signal!");
}

// ============================================================================
// Main Setup and Loop
// ============================================================================

void setup() {
  // Initialize serial for debugging
  Serial.begin(115200);
  while (!Serial) { delay(100); }

  // Connect to WiFi
  connectToWiFi();

  // Wait for capture request
  handleCaptureRequest();

  // Continue waiting...
  Serial.println("Waiting for Pi button press signal...");
}

void loop() {
  // Check for capture request
  if (tcp_capture_request_received) {
    Serial.println("\n--- CAPTURE REQUEST RECEIVED ---");

    // TODO: Implement actual camera capture here
    // ESP32 Arduino would need ESP32_Arduino_Core installed
    // and proper libraries like esp_camera

    tcp_capture_request_received = false;
  }

  // Handle incoming WiFi data from Pi button
  if (WiFi.isConnected()) {
    handleWifiMessage();
  }

  delay(50);
}

// Read data from TCP client
void handleWifiMessage() {
  char request = (char)client.read();

  // Look for "CAPTURE" keyword in HTTP request
  if (request == 'C' || request == 'A' || request == 'P' ||
      request == 'T' || request == 'U' || request == 'R' || request == 'E') {

    tcp_capture_request_received = true;
    Serial.println("CAPTURE keyword detected!");

    // TODO: Send signal to ESP32 (would be WiFi or Bluetooth here)
  }
}
