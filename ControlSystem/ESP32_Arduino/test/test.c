#include <Arduino.h>
#include <BLEDevice.h>
#include <WiFi.h>
#include <WiFiUdp.h>
#include <ArduinoJson.h>
#include "PubSubClient.h"
#include "test.h"
#include "Sensor.h"
#include "control.h"

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");

  // Convert the byte array to a String
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println(message);

  // Create a DynamicJsonDocument to hold the parsed JSON
  DynamicJsonDocument sensor_conf(sensorCapacity);

  // Deserialize the JSON data
  DeserializationError error = deserializeJson(sensor_conf, message);

  // Check for errors in deserialization
  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.f_str());
    return;
  }


  Serial.print("recieved message: \n");
  Serial.println(sensor_conf);

/* 
   for (int i = 0; i < 3; i++){
    FLORA_DEVICES[i][0] = sensor_conf["mac"];
    FLORA_DEVICES[i][1] = sensor_conf["location"];
    FLORA_DEVICES[i][2] = sensor_conf["pot_id"];
    FLORA_DEVICES[i][3].toInt() = sensor_conf["min_temperature"];
    FLORA_DEVICES[i][4].toInt() = sensor_conf["max_temperature"];
    FLORA_DEVICES[i][5].toInt() = sensor_conf["min_moisture"];
    FLORA_DEVICES[i][6].toInt() = sensor_conf["max_moisture"];
    FLORA_DEVICES[i][7].toInt() = sensor_conf["min_light"];
    FLORA_DEVICES[i][8].toInt() = sensor_conf["max_light"];
    FLORA_DEVICES[i][9].toInt() = sensor_conf["min_conductivity"];
    FLORA_DEVICES[i][10].toInt() = sensor_conf["max_conductivity"];
  } */
}
/* uint8_t mqtt_server = 192.268.0.78;
uint16_t mqtt_port =  */

void setup() {
  // Start serial communication
  Serial.begin(115200);

  // Connect to WiFi
  setup_wifi();

  // Set MQTT server and callback
  client.setServer(MQTT_HOST, MQTT_PORT);
  client.setCallback(callback);
  client.subscribe("test");
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      // Subscribe to the topic
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
