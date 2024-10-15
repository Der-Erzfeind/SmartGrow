// Device settings
#define DEVICE_ID "10:06:1C:81:4E:10"       // Identifier of the esp32 device
#define SLEEP_DURATION 60 * 60 * 3          // Sleep between to runs in seconds
#define EMERGENCY_HIBERNATE 20 * 60          // Emergency hibernate countdown in seconds
#define BATTERY_INTERVAL 1                  // How often should the battery be read - in run count
#define BATTERY_THRESHOLD_LOW 20            // Battery threshold when battery gets low
#define BATTERY_THRESHOLD_MED 80            // Battery threshold when battery gets medium
#define SENSOR_RETRY 2                      // How often should a sensor be retried in a run when something fails

// Wifi settings
#define WIFI_SSID "smartgrow"               // SSID of your WiFi network
#define WIFI_PASSWORD "smartgrow"           // Password of your WiFi network
#define STATIC_IP "10, 42, 0, 100"          // IP Adress of the ESP32
#define STATIC_GATEWAY "10.42.0.1"          // IP Adress of the Raspberry PI Server
#define SUBNET_MASK "255.255.255.000"       // Subnet Mask of the Network

// Mqtt settings
#define MQTT_HOST "10.42.0.1"                 // Mqtt broker ip address or hostname
#define MQTT_PORT 1883                        // Mqtt port (default: 1883)
#define MQTT_USERNAME "esp1"                  // Mqtt username [optional]
#define MQTT_PASSWORD "esp1"                  // Mqtt username [optional]
#define MQTT_BASE_TOPIC "smartgrow"           // The Miflora base topic
#define MQTT_RETRY_WAIT 5000                  // Retry delay between attempts to connect to the Mqtt broker
#define MQTT_RETAIN false                     // Retain Mqtt messages (default: false)
