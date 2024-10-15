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
- ESP32 [ESP32 auf AliExpress](https://www.aliexpress.com/item/1005005626482837.html?spm=a2g0o.order_list.order_list_main.42.133e1802JBKUlo)
- Xiaomi Flora Plant Sensor ([Xiaomi flora auf AliExpress](https://www.aliexpress.com/item/1005004193994534.html?spm=a2g0o.productlist.main.1.3e86z6Alz6Al3B&algo_pvid=8b2590e4-d1ef-4a2e-8f69-6f2006bd95c3&algo_exp_id=8b2590e4-d1ef-4a2e-8f69-6f2006bd95c3-0&pdp_npi=4%40dis%21EUR%2135.64%2124.59%21%21%2137.97%2126.20%21%40211b807017290070547776773e07c3%2112000028337922699%21sea%21DE%212004505613%21X&curPageLogUid=G1MOItTtKRdY&utparam-url=scene%3Asearch%7Cquery_from%3A))

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