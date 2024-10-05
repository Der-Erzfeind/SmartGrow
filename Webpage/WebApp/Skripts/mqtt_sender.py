import sqlite3
import paho.mqtt.client as mqtt
import json

# MQTT-Einstellungen
mqtt_broker = "192.168.0.78"
mqtt_port = 1883
mqtt_topic = "smartgrow/10:06:1C:81:4E:10/sensorparameter"
mqtt_username = "esp1"
mqtt_password = "esp1"
req_sensor_topic = "smartgrow/10:06:1C:81:4E:10/raspicontrol"  # Das Thema, auf das das Skript reagieren soll

# Verbindung zur SQLite-Datenbank herstellen
def execute_db_query():
    db_connection = sqlite3.connect('../Database/smartgrow_database.db')
    cursor = db_connection.cursor()

    # SQL-Abfrage zum Abrufen der benötigten Werte
    sql_query = """
    SELECT 
        p.SensorMAC,
        h.min_soil_moist,
        h.max_soil_moist,
        h.min_soil_ec,
        h.max_soil_ec,
        h.min_pH,
        h.max_pH,
        b.PotNum
    FROM 
        Plants p
    JOIN 
        HerbsDb_Plants_Compare_Value h
    ON 
        p.pid = h.pid
    JOIN 
        Box b
    ON 
        p.SensorMAC = b.SensorMAC;
    """

    cursor.execute(sql_query)
    werte = cursor.fetchall()
    db_connection.close()
    return werte

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode()

    # Prüfen, ob die Nachricht "REQ_SENSOR_PARAM" enthält
    if msg.topic == req_sensor_topic and payload_str == "REQ_SENSOR_PARAM":
        print("Gültige Nachricht empfangen, führe SQL-Abfrage aus...")
        werte = execute_db_query()
        
        payloads = []
        for wert in werte:
            payload = {
                "Mac": wert[0],
                "Pot": wert[7],
                "MinMoisture": wert[1],
                "MaxMoisture": wert[2],
                "MinConductivity": wert[3],
                "MaxConductivity": wert[4],
                "MinPh": wert[5],
                "MaxPh": wert[6]
            }
            payloads.append(payload)

        json_payloads = json.dumps(payloads)
        result = client.publish(mqtt_topic, json_payloads, qos=1)
        status = result.rc
        if status == 0:
            print(f"Gesendet: {json_payloads} an {mqtt_topic}")
        else:
            print(f"Fehler beim Senden der Nachricht an {mqtt_topic}, Statuscode: {status}")
    else:
        print("Nachricht ignoriert oder ungültige Aktion.")

# Vorhandenen MQTT-Client verwenden und nur on_message-Funktion hinzufügen
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

client.on_message = on_message

# Verbindung zum MQTT-Broker herstellen und Req_Sensor-Thema abonnieren
client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(req_sensor_topic)
client.loop_forever()
