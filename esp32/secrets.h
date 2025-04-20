#pragma once
#include <pgmspace.h>

// WiFi Configuration
#define WIFI_SSID ""
#define WIFI_PASS ""

// MQTT Broker Configuration
#define MQTT_BROKER     ""
#define MQTT_PORT       ####
#define MQTT_PUB_TOPIC  ""
#define MQTT_SUB_TOPIC  ""
#define MQTT_USERNAME   ""
#define MQTT_PASSWORD   ""
static const char *root_ca PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
)EOF";

// Encryption Key
const byte XOR_KEY = ;
