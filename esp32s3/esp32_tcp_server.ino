// esp32_tcp_server.ino - Simple TCP Client for receiving signals from Pi
// Connect to home WiFi, send test ping to Pi

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>

#define WIFI_SSID     "dangus"
#define WIFI_PASSWORD "eraserhead"

bool connected = false;
IPAddress piIP(192, 168, 12, 106);
int piPort = 80;

WiFiClient client;

void connectToWiFi() {
  Serial.println("Connecting to WiFi 'dangus'...");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempt = 0;
  while (WiFi.status() != WL_CONNECTED && attempt < 120) {
    delay(500);
    Serial.print(".");
    attempt++;
  }

  Serial.println();
  Serial.println("WiFi connected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  // Check if on same network as Pi
  IPAddress localIP = WiFi.localIP();
  int localSubnet = localIP[0];

  // Get Pi's actual IP from button_trigger.py or use known value
  piPort = 80;
}

void testConnection() {
  // First, disconnect any existing connection
  if (client.connected()) {
    client.stop();
  }

  Serial.println("\nTesting TCP connection to Pi...");

  // Try connecting to Pi on port 80
  connected = client.connect(piIP, piPort);

  if (connected) {
    Serial.println("✅ SUCCESS: Connected to Pi!");
    Serial.println("Pi is reachable - try pressing button now.");
  } else {
    Serial.println("❌ FAILED: Could not connect to Pi");
  }
}

void setup() {
  Serial.begin(115200);
  while (!Serial) { delay(100); }

  connectToWiFi();
  testConnection();

  Serial.print("\nWaiting for signal from ");
  Serial.println(piIP.toString());
  Serial.println("Press and hold Pi's GPIO 26 button for 3 seconds...");
}

void loop() {
  if (connected) {
    if (client.available()) {
      char request = client.read();

      // Look for "CAPTURE" keyword in HTTP request
      if (request == 'C' || request == 'A' || request == 'P' ||
          request == 'T' || request == 'U' || request == 'R' || request == 'E') {
        Serial.println("CAPTURE keyword detected!");

        // TODO: Trigger actual photo capture here
      }
    }
  }

  delay(50);
}
