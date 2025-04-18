#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <AESLib.h>
#include <base64.h>
#include <ArduinoJson.h>

#include "secrets.h"
#include "images.h"

String selectedImage;
uint8_t remainingLoops = 0;
unsigned long lastSend = 0;
int sendInterval = 45000; // 45 seconds

WiFiClientSecure espClient;
PubSubClient * client;
AESLib aesLib;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  WiFiClient client;
  if (client.connect("www.google.com", 80)) {
    Serial.println("Internet connection verified");
    client.stop();
  } else {
    Serial.println("No internet connection");
  }
}

void setDateTime() {
  const char *ntpServer1 = "pool.ntp.org";
  const char *ntpServer2 = "ntp.ubuntu.com";

  configTime(0, 0, ntpServer1, ntpServer2);

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    Serial.print(".");
    delay(1000);
    now = time(nullptr);
  }
  Serial.println();

  struct tm timeinfo;
  if (!getLocalTime(&timeinfo, 10000)) {
    Serial.println("Failed to obtain time");
    return;
  }
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));
}

void callback(char* topic, byte* payload, unsigned int length) {
  String msg = "";
  for (int i = 0; i < length; i++) {
    msg += (char)payload[i];
  }

  remainingLoops = msg.toInt();
  lastSend = 0;
  Serial.printf("Set remaining loops: %d\n", remainingLoops);
}

void sendImage() {
  Serial.printf("Image size: %zu bytes\n", img_len);

  byte iv[16];
  for (int i = 0; i < 16; i++) {
    iv[i] = random(0, 256);
  }

  Serial.print("Generated IV: ");
  for (int i = 0; i < 16; i++) {
    Serial.printf("%02X", iv[i]);
  }
  Serial.println();

  const size_t chunkSize = 1024;
  const size_t totalChunks = (img_len + chunkSize - 1) / chunkSize;
  size_t offset = 0;
  size_t chunkNumber = 1;

  client->setBufferSize(4096);

  while (offset < img_len) {
    size_t bytesToProcess = min(chunkSize, img_len - offset);

    byte chunk[chunkSize];
    for (size_t i = 0; i < bytesToProcess; i++) {
      chunk[i] = pgm_read_byte(&img[offset + i]);
    }

    byte encryptedChunk[chunkSize + 16];
    int enc_len = aesLib.encrypt(chunk, bytesToProcess, encryptedChunk, AES_KEY, 128, iv);
    if (enc_len <= 0) {
      Serial.printf("Encryption failed at chunk %zu\n", chunkNumber);
      return;
    }

    byte payloadBin[16 + enc_len];
    memcpy(payloadBin, iv, 16);
    memcpy(payloadBin + 16, encryptedChunk, enc_len);

    String encoded = base64::encode(payloadBin, 16 + enc_len);

    time_t now = time(nullptr);
    String payload = "{\"timestamp\":" + String(now) +
                     ",\"remaining_loops\":" + String(remainingLoops) +
                     ",\"chunk\":" + String(chunkNumber) +
                     ",\"total_chunks\":" + String(totalChunks) +
                     ",\"data\":\"" + encoded + "\"}";
    
    bool success = client->publish(MQTT_PUB_TOPIC, payload.c_str());
    Serial.printf("Sent chunk %zu/%zu (%zu bytes), publish %s\n",
                  chunkNumber, totalChunks, bytesToProcess,
                  success ? "OK" : "FAILED");

    chunkNumber++;
    offset += bytesToProcess;
  }

  Serial.println("Image encryption and chunked publish completed.");
}


void setup() {
  delay(500);

  Serial.begin(115200);
  delay(500);

  setup_wifi();
  setDateTime();

  espClient.setCACert(root_ca);

  client = new PubSubClient(espClient);
  client->setServer(MQTT_BROKER, MQTT_PORT);
  client->setCallback(callback);

  while (!client->connected()) {
    if (client->connect("ESP32Client - UTS IoT", MQTT_USERNAME, MQTT_PASSWORD)) {
      Serial.println("Connected to MQTT broker");
      client->subscribe(MQTT_SUB_TOPIC);
    } else {
      Serial.print("Failed to connect to MQTT broker, state: ");
      Serial.println(client->state());
      delay(2000);
    }
  }
}

void loop() {
  client->loop();

  if (remainingLoops > 0) {
    if (millis() - lastSend >= sendInterval) {
      sendImage();
      remainingLoops--;
      lastSend = millis();
    }
  }
}
