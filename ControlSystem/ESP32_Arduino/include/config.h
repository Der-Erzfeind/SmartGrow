// Device settings
#define DEVICE_ID "10:06:1C:81:4E:10"        // Identifier of the esp32 device
#define SLEEP_DURATION 60          // Sleep between to runs in seconds
#define EMERGENCY_HIBERNATE 1 * 60 // Emergency hibernate countdown in seconds
#define BATTERY_INTERVAL 1         // How often should the battery be read - in run count
#define BATTERY_THRESHOLD_LOW 20   // Battery threshold when battery gets low
#define BATTERY_THRESHOLD_MED 80   // Battery threshold when battery gets medium
#define SENSOR_RETRY 2             // How often should a sensor be retried in a run when something fails

// Wifi settings
#define WIFI_SSID "WLAN von Jonas"              // SSID of your WiFi network
#define WIFI_PASSWORD "7Hqlg9(oL29Wpg3;"        // Password of your WiFi network

// Mqtt settings
#define MQTT_HOST "192.168.0.78"                 // Mqtt broker ip address or hostname
#define MQTT_PORT 1883                           // Mqqt port (default: 1883)
#define MQTT_USERNAME "esp1"                      // Mqtt username [optional]
#define MQTT_PASSWORD "esp1"                         // Mqtt username [optional]
#define MQTT_BASE_TOPIC "smartgrow"                // The Miflora base topic
#define MQTT_RETRY_WAIT 5000                     // Retry delay between attempts to connect to the Mqtt broker
#define MQTT_RETAIN false                        // Retain Mqtt messages (default: false)