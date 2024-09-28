// Array of different Xiaomi Flora MAC addresses, their location, plant id and min, max values
// <mac_address>, <pot>, <min_temperature>, <max_temperature>, <min_moisture>, <max_moisture>, <min_light>, <max_light>, <min_conductivity>, <max_conductivity>
String FLORA_DEVICES[3][10] = {
    {"5C:85:7E:12:C6:B8", "1", "12", "32", "15", "65", "800", "20000", "350", "1000"},
    {"C4:7C:8D:67:58:A0", "2", "8", "32", "20", "60", "2500", "35000", "350", "2000"},
    {"C4:7C:8D:6A:0D:2F", "3", "10", "35", "15", "60", "2500", "35000", "350", "2000"},
};

// Device settings
#define DEVICE_ID "esp32-1"        // Identifier of the esp32 device
#define SLEEP_DURATION 60          // Sleep between to runs in seconds
#define EMERGENCY_HIBERNATE 1 * 60 // Emergency hibernate countdown in seconds
#define BATTERY_INTERVAL 1         // How often should the battery be read - in run count
#define BATTERY_THRESHOLD_LOW 20   // Battery threshold when battery gets low
#define BATTERY_THRESHOLD_MED 80   // Battery threshold when battery gets medium
#define SENSOR_RETRY 5             // How often should a sensor be retried in a run when something fails

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