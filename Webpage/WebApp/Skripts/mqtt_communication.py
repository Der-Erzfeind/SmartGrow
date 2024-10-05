import json
import sqlite3
import paho.mqtt.client as mqtt

# MQTT Einstellungen
MQTT_BROKER = "192.168.0.78"
MQTT_PORT = 1883
MQTT_USERNAME = "esp1"
MQTT_PASSWORD = "esp1"
MQTT_TOPIC_MEAS = "smartgrow/meassurement"   # Thema zum Messdaten empfangen
MQTT_TOPIC_REQ_PARAM = "smartgrow/parameterrequest"   # Thema unter dem gehoert wird ob Sensorparameter veroeffentlicht werden sollen

# Verbindung zur Datenbank
def database_connection():
    conn = sqlite3.connect("../Database/smartgrow_database.db")
    return conn


def get_plant_params(espMAC):
        conn = database_connection()
        cursor =conn.cursor()

        sql_query = '''
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
                p.SensorMAC = b.SensorMAC
            WHERE boxID = ?;                    
        '''

        cursor.execute(sql_query, (espMAC,))
        plant_params = cursor.fetchall()
        conn.close()
        return plant_params


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(MQTT_TOPIC_MEAS)
        client.subscribe(MQTT_TOPIC_REQ_PARAM)
    else:
        print(f"Connection failed. Result Code: {rc}")


def on_message(client, userdata, msg):
    payload_str = msg.payload.decode()

    # Fall: Sensordaten schickem
    if msg.topic == MQTT_TOPIC_REQ_PARAM:
        print("Anfrage der Regelungsparameter empfangen")
        mac_address = msg.payload.decode()
        print(f"Empfange MAC: {mac_address}. Parameter werden extrahiert ...")
        
        # Anlegen des Topics zum senden der Parameter
        mqtt_topic_send_param = f"smartgrow/{mac_address}/sensorparameter"
        
        plant_params = get_plant_params(espMAC=mac_address)
        payloads = []

        for plant_param in plant_params:
            payload = {
                "Mac": plant_param[0],
                "Pot": plant_param[7],
                "MinMoisture": plant_param[1],
                "MaxMoisture": plant_param[2],
                "MinConductivity": plant_param[3],
                "MaxConductivity": plant_param[4],
                "MinPh": plant_param[5],
                "MaxPh": plant_param[6]
            }
            payloads.append(payload)

        json_payloads = json.dumps(payloads)
        rv_publish_params = client.publish(mqtt_topic_send_param, json_payloads, qos=2)
        if rv_publish_params.rc == 0:
            print("Regelungsparameter erfolgreich uebertragen")
        else:
            print(f"Fehler beim uebertragen der Regelungsparameter. Result Code: {rv_publish_params.rc}")
    elif msg.topic == MQTT_TOPIC_MEAS:  # Fall: Messdaten empfangen
        print(f"Nachricht auf {MQTT_TOPIC_MEAS} empfangen")
        conn = database_connection()
        cursor = conn.cursor()

        try:
            meas_data = json.loads(msg.payload)

            if not isinstance(meas_data, dict):
                print(f"Fehler: Erwartet ein Dictionary, aber erhalten: {type(meas_data)}")
                return

            # Extrahieren der Tankdaten
            boxID = meas_data["Mac"]
            volume_mix = meas_data["volmix"]
            volume_water = meas_data["volwater"]
            volume_fertelizer = meas_data["volfertilizer"]
            volume_acid = meas_data["volacid"]

            try:
                # Einfuegen der Tankdaten
                cursor.execute('''
                    INSERT INTO Liquid_Tanks (boxID, volume_mix, volume_water, volume_fertilizer, volume_acid, time)
                    VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'))
                ''', (boxID, volume_mix, volume_water, volume_fertelizer, volume_acid))
            except sqlite3.Error as e:
                print(f"Fehler beim einfuegen der Tankdaten. Fehlercode: {e}")

            # Verarbeitung der Pflanzenmessdaten
            for plant_sensor in meas_data["sensors"]:
                SensorMAC = plant_sensor["Mac"]
                light_lux = plant_sensor["light"]
                temp = plant_sensor["temperature"]
                soil_moist = plant_sensor["moisture"]
                soil_ec = plant_sensor["conductivity"]
                battery = plant_sensor["battery"]
                water_pH = plant_sensor["ph"]

                try:
                    # Einfuegen der Pflanzenmessdaten
                    cursor.execute('''
                        INSERT INTO Measurements (SensorMAC, light_lux, temp, soil_moist, soil_ec, time, battery, water_pH)
                        VALUES (?, ?, ?, ?, ?, datetime('now', 'localtime'), ?, ?)
                    ''', (SensorMAC, light_lux, temp, soil_moist, soil_ec, battery, water_pH))
                except sqlite3.Error as e:
                    print(f"Fehler beim einfuegen der Pflanzenmessdaten: {e}")

            # Messdaten in Database speichern
            try:
                conn.commit()
            except sqlite3.Error as e:
                print(f"Fehler beim speichern der Messdaten in der Datenbank. Fehlercode: {e}")
        except json.JSONDecodeError as e:
            print(f"Fehler beim dekodieren der Nachricht: {e}")
        except Exception as e:
            print(f"Allgemeiner Fehler beim verarbeiten der Nachricht: {e}")
        # Datenbankverbindung beenden
        conn.close()
    else:   # Fall: Unbekannt
        print(f"Unbekannte MQTT Nachricht oder Topic: {msg.topic}, {payload_str}")


client = mqtt.Client()
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
