# Smartgrow Control System

Dieses [PlatformIO](https://platformio.org) Projekt basiert auf dem [miflora-esp32](https://github.com/RaymondMouthaan/miflora-esp32) Projekt von [@RaymondMouthaan](https://github.com/RaymondMouthaan). 

Der ESP32 Controller bezieht Sollwerte für die System vorhandenen Pflanzen, sowie die Mac Adressen der Xiaomi MiFlora Sensoren über MQTT vom [Server](https://github.com/Der-Erzfeind/SmartGrow/tree/main/RaspberryPI). Anschließend werden die Sensoren ausgelesen und bei Bedarf Kommandos zum Ansteuern der Pumpen an den Arduino Nano gesendet. Abschließend werden die Messdaten über MQTT zurück an der Server gesendet.


## Features

Das Basisprojekt von @RaymondMouthaan wurde wie folgt verändert:

- Dynamische Zuweisung der Elemente der Elemente der Sensor Klasse
- Bezug der Parameter der Sensor Klasse vom Server über MQTT
- callback() Funktion zum Parsen der erhaltenen Parameter hinzugefügt
- MQTT Topics für Kommunikation mit Server geändert und Telegramme angepasst
- Klasse Box mit Elementen für Füllstände hinzugefügt
- control.cpp mit Funktionen zum Ansteuern der Pumpen und Sensoren hinzugefügt
- control.h mit Definitionen der Sensor Pins und UART Commands
- statische IP-Adressen Zuweisung für Verbindung mit Hotspot des Raspberry PI

__Beachte : Projekt befindet sich im Prototyp Stadium, es können Fehler auftreten. Weitere Features, wie eine Notfallabschaltung und Fehlerbehandlung werden noch hinzugefügt__

## Technische Voraussetzungen

Hardware:
- ESP32 ([ESP32 auf AliExpress](https://nl.aliexpress.com/wholesale?catId=0&initiative_id=SB_20200408062838&SearchText=MH-ET+Live+ESP32))
- Xiaomi Flora Plant Sensor (firmware revision >= 2.6.6) ([Xiaomi flora auf AliExpress](https://nl.aliexpress.com/wholesale?catId=0&initiative_id=SB_20200408063038&SearchText=xiaomi+flora))

![xiaomi-flora](xiaomi-miflora.png)

Software:
- MQTT broker (z.B. [Mosquitto](https://mosquitto.org))

## Benutzungsanleitung

Es werden Kenntnisse in der Nutzung von [Visual Studo Code](https://code.visualstudio.com) und [PlatformIO](https://platformio.org) angenommen. 

1) Öffnen Sie das Projekt in Visual Studio Code mit PlatformIO installiert.
2) Kopieren Sie `example/config.h.example` nach `include/config.h` und passen Sie folgende Einstellungen für Ihr Netzwerk an:
    - WLAN Settings
    - MQTT Settings
3) passen Sie platform.ini für Ihre Geräte an:
    - upload_port
    - monitor_port

## Mess- und Regelungszyklus

Beim aufwachen aus dem sleep des ESP32 wird der Code in setup() ausgeführt. Zuerst wird eine Verbindung mit dem MQTT Broker über Wifi aufgebaut. Bei erfolgreicher Verbindung werden die Pflanzen- und Sensorparameter über das parameterRequestTopic angefragt. Die Antwort des Servers wird auf dem parameterRecieveTopic empfangen und von der callback() Funktion geparsed. Anschließend wird das Wifi Modul deaktiviert, da es den ADC1 belegt, welcher zum Auslesen des PH Sensors benötigt wird.
Im Anschluss werden die Flora Sensoren mit der processFloraDevice() Funktion ausgelesen, wobei die Anzahl der Ausleseversuche mit SENSOR_RETRY in config.h eingestellt werden kann.
Die Messwerte der Feuchtigkeit und des Bodenleitwertes mit den Sollwerten verglichen. 
Bei zu niedrigen Messwerten wird dem Mischtank Wasser und Dünger hinzugefügt, der PH Wert geprüft und korrigiert und die Mischung in den Topf der entsprechenden Pflanze gepumpt. Nach der Bewässerung wird der ESP schlafen geschickt.
Wird im Zyklus keine Pflanze bewässert, schickt der ESP alle Messwerte über das MQTT meassurementTopic an den Server und geht anschließend schlafen.

Die Batterie der Flora Sensoren wird in jedem n-ten Zyklus ausgelesen, die Häufigkeit kann auch in config.h eingestellt werden.