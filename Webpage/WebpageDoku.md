# webpage
In diesem Repository ist der Code der Webpage für das Projekt SmartGrow abgelegt

## Dokumentation RaspberryPi
### Webserver
Auf dem Raspberry Pi wurde ein Apache Webserver installiert, welcher die mit Python Flask erstellte Website hostet. Die von Apache zu hostenden Websites werden in folgendem Verzeichnis abgelegt:
```
/var/www/
```
Hierfür wurde in diesem Verzeichnis ein Ordner `smartgrow_app` erstellt. In diesem liegt das Git Repository `webpage`. Apache ist durch die Datei konfiguriert worden:
```
/etc/apache2/sites-available/smartgrow_app.conf
```
Zusätzlich liegt unter: 
```
/var/www/smartgrow_app/webpage/WebApp
```
die Datei `smartgrow_app.wsgi`, auf welche die die `smartgrow_app.conf` zurückgreift.

Die .wsgi Datei ist für die Kommunikation zwischen dem Apache-Server und der Python Flask Anwendung notwendig. Die .conf Datei wiederum stellt die allgemeine Server-Konfiguration dar.

**Sollte etwas an der `smartgrow_app.conf` oder `smartgrow_app.wsgi` geändert werden, sollte der Webserver neugeladen und neu gestartet werden. Hierzu folgende Befehle ausführen:**

```bash
sudo systemctl reload apache2.service
sudo systemctl restart apache2.service
```
**Sollten Probleme beim Aufrufen der Website auftreten hilft es zunächst den Status und den Errorlog des Servers abzufragen:**
```bash
sudo systemctl status apache2.service
sudo tail -f /var/log/apache2/error.log
```

### MQTT Kommunikation
Zum Datenaustausch zwischen ESP und RaspberryPi via MQTT wurde ein Skript `mqtt_communication.py' in 
```
/var/www/smartgrow_app/webpage/WebApp/Skripts/
```
erstellt. Damit dieses Skript dauerhaft in Betrieb ist wurde eine mqtt_communication.service Datei in 
```
/etc/systemd/system/
```
angelegt. Auch hier kann der Status mit:
```
sudo systemctl status mqtt_communication.service
```
abgefragt werden. Muss etwas an der .service verändert werden ist es notwendig danach:
```
  sudo systemctl daemon-reload
  sudo systemctl restart mqtt_service
```
auszuführen. StandardOutput sowie StandardError des Skripts wird über die systemd journal Funktion gelogged. Sollten Probleme auftreten kann der Service also über
```
sudo journalctl -u mqtt_communication.service -f
```
live beobachtet werden. (Es gibt noch weitere Funktionen die es ermöglichen im Journal log zu filtern oder eine bestimmte Anzahl an Einträgen anzuzeigen.)

### Pflanzenerkennung
Das Modell zur Pflanzenerkennung läuft in einem seperaten Skript. Die Website tauscht Daten mit dem Modell über Pipes aus. Die named pipes sind im Verzeichnis /var/www/smartgrow_app/webpage/pipes/ angelegt.

Das Skript zur Pflanzenerkennung heißt plant_Recog.py und liegt im Verzeichnis /home/smartgrow/PlantRecognition. Für dieses Skript wurde ähnlich wie für die MQTT Kommunikation eine Servicedatei plant_recog.service in /etc/systemd/system/ erstellt.
DI commands bei Änderungen oder zum Abfragen des Status sowie des Error-Logs sind diesselben wie bei der MQTT Kommunikation nur dass plant_recog.service angegeben werden muss statt mqtt_communication.service.

### Grafana Webserver
Grafana wird zur Visualisierung der Messdaten verwendet. Der Grafana-Server läuft auf dem RaspberryPi und 192.168.0.78:3000.
**Login Daten:**
- Username: smartgrow
- Password: smartgrow

Hierfür ist ebenfalls ein Service installiert. Der Status kann wie folgt abgefragt werden:
```
sudo systemctl status grafana-server.service
```
Sollte etwas mit Grafana nicht funktionieren ist es empfohlen zunächst den status bzw. den Error-Log abzufragen.
```
sudo journalctl -u grafana-server.service
```
Ebenfalls kann es Sinn machen ob der Zugriff auf die Datenbank sowie die Visualisierung korrekt funktioniert. Hierfür auf Grafana einloggen und unter Connections --> Datasources die Datenbank überprüfen und unter Dashboards die visualisierungen.

Wichtig zu beachten ist, dass im Dashboard unter Settings --> Variables eine Variable sensorID angelegt ist.  Dies ist notwendig dass auf der Website nur die Messdaten vom zur Pflanze zu geordneten Sensor angezeigt werden. Auch hier kann auf Fehler überprüft werden.

Wichtig ist, dass in /etc/grafana/grafana.ini allow_embedding auf true gesetzt ist. Die Einbindung der Grafana Visualisierungen ist in der plantview.html realisert (unter /var/www/smartgrow/webpage/WebApp/templates/plantview.html) realisiert und sieht wie folgt aus:

    <iframe 
    src="http://192.168.0.78:3000/d-solo/advi5em73o5c0a/
    smartgrow-grafana-dashboard?orgId=1&from=1672527600000&
    to=1672560000000&theme=light&panelId=2&var-
    sensorID={{ plant['SensorMAC'] }}">
    </iframe>

Diese Links können in Grafana direkt erstellt werden, indem bei der Visualisierung auf die 3 Punkte rechts oben geklickt wird und dann share --> embed.

# Datenbank

Sollte das System um eine weiter Box erweitert werden muss aktuell noch direkt auf die Datenbank mittels Command-Line-Tool zugegriffen werden. 
Dafür navigiert man in das Verzeichnis  `/var/www/smartgrow_app/webpage/WebApp/Database`
Das Command-Line-Tool für SQlite starte man wie folgt:

```bash
sqlite3 smartgrow_database.db 
```

Eine neue Box wird wie folgt angelegt.

```sql
INSERT INTO Box (boxID, SensorMAC, PotNum)
VALUES 
('<MAC des ESP>', '<MAC des Sensors>', 1),
('<MAC des ESP>', '<MAC des Sensors>', 2),
('<MAC des ESP>', '<MAC des Sensors>', 3);
```

Sollten weiter Änderungen/Optimierungen an der Datenbank vorgenommen werden ist zu beachten Querys in der `webapp.py` sowie in Grafana  ebenso anzupassen.

---

Das folgende **Entity-Relationship-Diagramm** stellt die Datenbankstruktur dar. Es werden die verschiedene Entitäten (Tabellen) und deren Beziehungen beschrieben. Im Folgenden gebe ich eine kurze Dokumentation der abgebildeten Struktur, wobei die Fremdschlüssel besonders betont werden.

### 1. **Users (Benutzer)**
- **Username (TEXT, NOT NULL, Primary Key)**: Der Benutzername, der als Primärschlüssel dient.
- **Password (TEXT, NOT NULL)**: Das Passwort des Benutzers.

Diese Tabelle speichert grundlegende Informationen zu den Benutzern der Datenbank. Sie wird von mehreren Tabellen referenziert.

### 2. **Liquid_Tanks (Flüssigkeitstanks)**
- **boxID (TEXT, Foreign Key)**: Eine Verknüpfung mit der `Box`-Tabelle (über die `boxID`), um den Tank einer bestimmten Box zuzuordnen.
- **volume_mix (INT, NOT NULL)**: Volumen des Mischtanks.
- **volume_water (INT, NOT NULL)**: Volumen des Wassertanks.
- **volume_fertilizer (INT, NOT NULL)**: Volumen des Düngertanks.
- **volume_acid (INT, NOT NULL)**: Volumen des Säuretanks.
- **time (TEXT, Primary Key)**: Zeitstempel.

Diese Tabelle erfasst Daten über Flüssigkeitstanks, die mit Boxen über die `boxID`-Fremdschlüsselspalte verbunden sind.

### 3. **Box (Boxen)**
- **boxID (TEXT, Primary Key)**: Die ID der Box, die Pflanzen beherbergen. Die boxID ist dabei immer die MAC-Adresse eines ESP32. **Ein ESP und damit eine Box kann maximal 3 Pflanzen verwalten**
- **Username (TEXT, Foreign Key)**: Ein Verweis auf die `Users`-Tabelle, zeigt an, welchem Benutzer die Box gehört.
- **SensorMAC (TEXT, UNIQUE)**: Der Sensor, der mit der Box verbunden ist.
- **PotNum (INT)**: Die Topfnummer der Pflanze in der Box, welche für die Ansteuerung der Pumpen benutzt wird.

Die `Box`-Tabelle enthält Informationen über Boxen und ist über `Username` mit der `Users`-Tabelle verknüpft. Die `SensorMAC` wiederum wird in der `Measurements`- und `Plants`-Tabelle referenziert.

### 4. **Plants (Pflanzen)**
- **Plantname (TEXT)**: Der Name der Pflanze.
- **SensorMAC (TEXT, Foreign Key)**: Ein Verweis auf den Sensor, der mit der Pflanze in Verbindung steht (Verknüpfung zur `Box`-Tabelle).
- **Username (TEXT, Foreign Key)**: Ein Verweis auf den Benutzer, dem die Pflanze zugeordnet ist (Verknüpfung zur `Users`-Tabelle).
- **pid (TEXT, Foreign Key)**: Ein Verweis auf eine eindeutige ID für Pflanzendaten, die mit der `HerbsDb_Plants_Compare_Value`- und der `HerbsDb_Plants_Information`-Tabelle verbunden ist.

Die `Plants`-Tabelle speichert Informationen über Pflanzen und deren zugehörige Sensoren sowie Benutzer.

### 5. **HerbsDb_Plants_Compare_Value**
- **pid (TEXT, Primary Key, Foreign Key)**: Eine eindeutige Pflanzen-ID, die auf die `HerbsDb_Plants_Information`-Tabelle verweist.
- **max_light_mmol / min_light_mmol (INT)**: Maximal- und Minimalwerte für die Lichtintensität in mmol.
- **max_light_lux / min_light_lux (INT)**: Maximal- und Minimalwerte für die Lichtintensität in Lux.
- **max_temp / min_temp (REAL)**: Maximal- und Minimaltemperaturen.
- **max_env_humid / min_env_humid (INT)**: Maximal- und Minimalwerte für die Umgebungsfeuchtigkeit.
- **max_soil_moist / min_soil_moist (INT)**: Maximal- und Minimalwerte für die Bodenfeuchtigkeit.
- **max_soil_ec / min_soil_ec (INT)**: Maximal- und Minimalwerte für die Bodenleitfähigkeit.
- **max_pH / min_pH (REAL)**: Maximal- und Minimalwerte für den pH-Wert.

Diese Tabelle enthält Vergleichswerte für verschiedene Pflanzenparameter und ist über `pid` mit Pflanzeninformationen verknüpft.

### 6. **HerbsDb_Plants_Information**
- **pid (TEXT, Primary Key)**: Eindeutige Pflanzen-ID.
- **origin (TEXT)**: Herkunft der Pflanze.
- **blooming (TEXT)**: Blühverhalten der Pflanze.
- **color (TEXT)**: Farbdetails der Pflanze.
- **size (TEXT)**: Größe der Pflanze.
- **soil (TEXT)**: Bevorzugte Bodenart.
- **sunlight (TEXT)**: Sonnenlichtanforderungen.
- **watering (TEXT)**: Bewässerungsanforderungen.
- **fertilization (TEXT)**: Düngemittelanforderungen.
- **pruning (TEXT)**: Beschneidungsanforderungen.

Diese Tabelle speichert detaillierte Informationen über Pflanzen und ist über den `pid`-Schlüssel mit anderen Pflanzendaten verbunden.

### 7. **Measurements (Messungen)**
- **SensorMAC (TEXT, Foreign Key)**: Verknüpft mit der `Box`-Tabelle und speichert den Sensor, der Messwerte liefert.
- **light_lux (INT)**: Messwert der Lichtintensität in Lux.
- **temp (FLOAT)**: Temperaturmesswert.
- **soil_moist (INT)**: Bodenfeuchtigkeitsmesswert.
- **soil_ec (INT)**: Bodenleitfähigkeitsmesswert.
- **time (TEXT, Primary Key)**: Zeitstempel der Messung.
- **battery (INT)**: Batteriestatus des Sensors.
- **water_pH (REAL)**: pH-Wert des Wassers.

Diese Tabelle erfasst die Sensordaten für die Pflanzen in den Boxen und ist über `SensorMAC` mit der `Box`-Tabelle verbunden.

---

### Beziehungen und Fremdschlüssel
- Die Tabelle `Box` ist über `SensorMAC` mit der Tabelle `Measurements` verknüpft und über `boxID` mit der Tabelle `Liquid_Tanks`.
- Die Tabelle `Plants` ist über `SensorMAC` mit der `Box`-Tabelle verbunden, enthält Referenzen zu den Tabellen `Users` und den Pflanzendaten (`HerbsDb_Plants_Compare_Value` und `HerbsDb_Plants_Information`).
- Die Tabelle `Users` ist mit mehreren anderen Tabellen verknüpft, insbesondere `Box` und `Plants`, um die Benutzer mit ihren zugehörigen Boxen und Pflanzen zu verbinden.

---

```sql

CREATE TABLE "Box" (
	"boxID"	TEXT,
	"Username"	TEXT,
	"SensorMAC"	TEXT UNIQUE,
	"PotNum"	INTEGER,
	PRIMARY KEY("boxID","SensorMAC"),
	FOREIGN KEY("Username") REFERENCES "Users"("Username")
)

CREATE TABLE "HerbsDb_Plants_Compare_Value" (
	"pid"	TEXT,
	"max_light_mmol"	INTEGER,
	"min_light_mmol"	INTEGER,
	"max_light_lux"	INTEGER,
	"min_light_lux"	INTEGER,
	"max_temp"	REAL,
	"min_temp"	REAL,
	"max_env_humid"	INTEGER,
	"min_env_humid"	INTEGER,
	"max_soil_moist"	INTEGER,
	"min_soil_moist"	INTEGER,
	"max_soil_ec"	INTEGER,
	"min_soil_ec"	INTEGER,
	"max_pH"	REAL,
	"min_pH"	REAL,
	PRIMARY KEY("pid"),
	FOREIGN KEY("pid") REFERENCES "HerbsDb_Plants_Information"
)

CREATE TABLE "HerbsDb_Plants_Information" (
	"pid"	TEXT,
	"origin"	TEXT,
	"blooming"	TEXT,
	"color"	TEXT,
	"size"	TEXT,
	"soil"	TEXT,
	"sunlight"	TEXT,
	"watering"	TEXT,
	"fertilization"	TEXT,
	"pruning"	TEXT,
	PRIMARY KEY("pid")
)

CREATE TABLE "Liquid_Tanks" (
	"boxID"	TEXT,
	"volume_mix"	INTEGER NOT NULL,
	"volume_water"	INTEGER NOT NULL,
	"volume_fertilizer"	INTEGER NOT NULL,
	"volume_acid"	INTEGER NOT NULL,
	"time"	TEXT,
	PRIMARY KEY("time","boxID"),
	FOREIGN KEY("boxID") REFERENCES "Box"("boxID")
)

CREATE TABLE "Measurements" (
	"SensorMAC"	TEXT,
	"light_lux"	INTEGER NOT NULL,
	"temp"	REAL NOT NULL,
	"soil_moist"	INTEGER NOT NULL,
	"soil_ec"	INTEGER NOT NULL,
	"time"	TEXT,
	"battery"	INTEGER,
	"water_pH"	REAL,
	PRIMARY KEY("time","SensorMAC"),
	FOREIGN KEY("SensorMAC") REFERENCES "Box"("SensorMAC")
)

CREATE TABLE "Plants" (
	"Plantname"	TEXT NOT NULL,
	"SensorMAC"	TEXT,
	"Username"	TEXT NOT NULL,
	"pid"	TEXT,
	FOREIGN KEY("SensorMAC") REFERENCES "Box"("SensorMAC"),
	FOREIGN KEY("Username") REFERENCES "Users"("Username"),
	FOREIGN KEY("pid") REFERENCES "HerbsDb_Plants_Information"("pid")
)

CREATE TABLE "Users" (
	"Username"	TEXT NOT NULL,
	"Password"	TEXT NOT NULL,
	PRIMARY KEY("Username")
)
```
# Funktionsbeschreibung Webseiten

## Login

**Startseite**  
Wenn der Benutzer die IP-Adresse des Raspberry Pi in den Browser eingibt, wird die Startseite der Anwendung angezeigt. Diese Seite begrüßt den Benutzer mit einer Überschrift ("Welcome to SmartGrow") und bietet zwei zentrale Funktionen: **Login** und **Registrierung**. Der Benutzer kann über Links auf diese Funktionen zugreifen.

**Account-Erstellung (Registrierung)**  
Wenn der Benutzer auf "Register" klickt, öffnet sich ein modales Fenster mit einem Registrierungsformular. Hier muss der Benutzer einen Benutzernamen, ein Passwort und die Bestätigung des Passworts eingeben. Erfolgt die Registrierung erfolgreich, kann der Benutzer sich mit den angegebenen Daten anmelden. Bei Fehlern, wie nicht übereinstimmenden Passwörtern oder bereits existierenden Benutzernamen, wird eine Fehlermeldung angezeigt.

**Login**  
Wenn der Benutzer bereits einen Account hat, kann er sich über den "Login"-Link im Hauptmenü einloggen. Nach dem Klick öffnet sich ein modales Fenster mit einem Login-Formular. Der Benutzer muss seinen Benutzernamen und sein Passwort eingeben. Bei erfolgreicher Authentifizierung wird der Benutzer auf die Dashboard-Seite weitergeleitet. Falls die Anmeldedaten falsch sind, wird eine Fehlermeldung angezeigt.

**Team-Anzeige**  
Auf der Startseite gibt es auch einen Abschnitt, der das Team hinter der Anwendung zeigt. Drei Bilder von Teammitgliedern werden in diesem Bereich angezeigt, um dem Benutzer die Personen hinter "SmartGrow" vorzustellen.

## Dashboard

**Dashboard Übersicht**

Das Dashboard bietet dem Benutzer eine zentrale Anlaufstelle, um seine Boxen zu verwalten. Der Benutzer hat verschiedene Möglichkeiten, Boxen hinzuzufügen, zu konfigurieren und zu entfernen sowie Pflanzen in den Boxen zu verwalten. Zudem gibt es eine Statusübersicht, die anzeigt, ob die Services für die MQTT-Komminkation, das Pflanzenerkennungs-Modell und den Grafana-Server aktiv sind.

**Boxen hinzufügen und entfernen**

- Der Benutzer kann über das Dashboard Boxen hinzufügen. Wenn eine Box hinzugefügt wird, kann der Benutzer in dieser Box bis zu drei Pflanzen anlegen.
- Das Hinzufügen einer Box erfolgt über ein Dropdown-Menü, in dem verfügbare Boxen aufgelistet werden. Wenn keine Boxen verfügbar sind, wird eine Nachricht angezeigt, dass der Benutzer eine neue Box kaufen muss.
- Jede Box kann auch wieder entfernt werden. Dies geschieht über den Button „Remove Box“, der nach Bestätigung die Box aus dem System entfernt.

**Pflanzen zu einer Box hinzufügen**

- Nachdem eine Box hinzugefügt wurde, kann der Benutzer in dieser Box bis zu drei Pflanzen hinzufügen. Der Benutzer hat die Wahl, die Pflanze manuell durch Eingabe des Pflanzennamens und Auswahl eines Sensors hinzuzufügen oder ein Foto der Pflanze hochzuladen.
- Beim manuellen Hinzufügen einer Pflanze gibt der Benutzer den Pflanzennamen und die PID (Plant ID) ein und wählt einen freien Sensor aus der verfügbaren Liste.
- Beim Hochladen eines Fotos der Pflanze wird das Bild an ein KI-Modell gesendet. Dieses Modell bestimmt automatisch den Pflanzennamen und den Typ der Pflanze. Als Sensor wird der erste freie Sensor für diese Pflanze zugewiesen.
  
**Box-Details und Pflanzenansicht**

- Der Benutzer kann auf die „Box ID“ klicken, um zu den Box-Details weitergeleitet zu werden. In dieser Ansicht sieht der Benutzer alle Informationen zu dieser speziellen Box, einschließlich der zugewiesenen Pflanzen und Sensoren.
- Ebenso kann der Benutzer auf den Namen einer Pflanze klicken, um zur detaillierten Pflanzenansicht („Plant View“) weitergeleitet zu werden. Diese zeigt spezifische Informationen zu der Pflanze, wie z. B. den zugewiesenen Sensor und die aktuellen Sensordaten.

**Status-Überprüfung von MQTT-Kommunikation, KI-Modell und Grafana**

- Auf der rechten oberen Seite des Dashboards befindet sich der „Status“-Button. Durch Klicken darauf wird ein Popup-Fenster geöffnet, das den aktuellen Status der auf dem RaspberryPi laufenden Services anzeigt (MQTT-Kommunikation, KI-Modell, Grafana) anzeigt. Diese Information zeigt an, ob die Dienste aktiv auf dem RaspberryPi laufen.
- Im Popup wird der Status jedes Dienstes in einer Liste angezeigt.

**Fehlerbehandlung**

- Falls beim Hinzufügen von Pflanzen kein Sensor verfügbar ist, wird dem Benutzer die Meldung „No sensors available for this box. Cannot add plants.“ angezeigt.
- Sollte der Benutzer versuchen, eine Pflanze hinzuzufügen, ohne dass alle erforderlichen Felder ausgefüllt sind, werden Validierungsfehler auftreten, die den Benutzer auffordern, die fehlenden Informationen einzugeben.


## Box Detail

**Box-Details-Seite**

Die **Box-Details-Seite** bietet dem Benutzer eine detaillierte Übersicht über die Pflanzen, die in der ausgewählten Box untergebracht sind. Des Weiteren ist es vorgesehen hier die Füllstände der Tanks in dieser Box anzuzeigen, was aktuell jedoch hardwareseitig noch nicht umgesetzt ist. Im MQTT-Topic "measurment" ist jedoch schon vorgesehen diese Daten zu empfangen und auch in der Datenbank einzutragen. Die Seite Box_Deatails dient somit zur Verwaltung und Überwachung der einzelnen Pflanzen und der Wasser- und Nährstoffversorgung der Box.

**Pflanzenübersicht**

- Im oberen Abschnitt der Seite werden alle Pflanzen, die der Box zugewiesen sind, in einer Liste angezeigt. Jede Pflanze wird mit ihrem Namen sowie ihrer zugehörigen Sensor-ID dargestellt.
- Zu jeder Pflanze werden zusätzliche Informationen angezeigt, wie z. B.:
  - **Pot Number (Topfnummer)**: Der Benutzer kann sehen, in welchem Topf die Pflanze sitzt. 
  - **Batteriestatus des Sensors**: Der Batteriestatus des Sensors wird ebenfalls für jede Pflanze angezeigt, sofern diese Information verfügbar ist.
- Durch Klicken auf den Pflanzennamen wird der Benutzer zur **Plant View** weitergeleitet, wo er detailliertere Informationen über diese Pflanze einsehen kann, einschließlich Sensordaten und historischer Werte.

**Tankstatus**

- Im unteren Bereich der Box-Details-Seite soll der Benutzer Informationen über den aktuellen Status der Tanks in der Box finden. Dies muss hardwareseitig noch realisiert werden. Angezeigt werden soll:
  - **Mix-Volumen**: Das Volumen der gemischten Flüssigkeiten (in ml) im Tank.
  - **Wasser-Volumen**: Das Volumen des Wassers (in ml), das sich aktuell im Tank befindet.
  - **Düngervolumen**: Das Volumen des Düngers (in ml) im Tank.
  - **Säurevolumen**: Das Volumen der Säure (in ml) im Tank.

**Navigation**

- Über den Link „Pfeil“ in der Kopfzeile kann der Benutzer zur Dashboard-Seite zurückkehren.
- Zusätzlich gibt es in der Kopfzeile einen Logout-Link, über den der Benutzer die Sitzung beenden kann.

## Plantview

Die **Plant View-Seite** bietet dem Benutzer detaillierte Informationen zu einer spezifischen Pflanze, die in einer Box überwacht wird. Diese Seite kombiniert visuelle Darstellungen der von den Sensoren gesammelten Daten mit einer Übersicht über die Pflanzenspezifikationen und ihrer Herkunft.

**Sensor-Datenvisualisierung mit Grafana**

- Die von den Sensoren der Pflanze gesammelten Daten werden mittels **Grafana** visualisiert. Auf der Seite werden mehrere **Iframe-Dashboards** eingebettet, die spezifische Informationen wie Bodenfeuchtigkeit, Temperatur, Lichtverhältnisse und andere relevante Umweltdaten für die Pflanze anzeigen.
- Jedes der Dashboards bezieht sich auf eine eindeutige Sensor-ID und die Plant ID (PID), um die spezifischen Sensordaten für die jeweilige Pflanze anzuzeigen. Diese Daten helfen dem Benutzer, die aktuellen Wachstumsbedingungen zu überwachen.

**Pflanzenbild**

- Ein zentrales Merkmal der Seite ist ein Bild der Pflanze. Das Bild wird basierend auf der **Plant ID (PID)** der Pflanze angezeigt. Dies gibt dem Benutzer eine visuelle Referenz zur Pflanzenart, die er überwacht. Es wird ein vorab definiertes Bild der jeweiligen Pflanzenart angezeigt, das in einem **figure**-Element eingebettet ist.

**Pflanzeninformationen**

- Der Benutzer hat die Möglichkeit, detaillierte Informationen über die Pflanzengattung abzurufen. Dies umfasst:
  - **Herkunft**: Woher die Pflanze ursprünglich stammt.
  - **Blütezeit**: Informationen zur Blütezeit der Pflanze.
  - **Farbe**: Typische Farbe der Pflanze oder Blüte.
  - **Größe**: Typische Wachstumsgröße der Pflanze.
  - **Bodenbeschaffenheit**: Bevorzugte Bodentypen für diese Pflanze.
  - **Lichtverhältnisse**: Die Menge an Sonnenlicht, die die Pflanze benötigt.
  - **Bewässerung**: Häufigkeit und Menge der Bewässerung.
  - **Düngung**: Empfohlene Düngemethoden und -intervalle.
  - **Schnitt**: Empfehlungen zum Beschneiden der Pflanze.
- Diese Informationen sind zunächst in einer **zusammenklappbaren Sektion** verborgen und können über den Button „Plant Information“ aufgerufen werden. Der Benutzer kann diese Sektion ein- und ausklappen, um die relevanten Informationen zu sehen.

**Navigation**

- Über einen Link in der Kopfzeile („Pfeil“) kann der Benutzer zur Dashboard-Seite zurückkehren.
- Es gibt auch einen Logout-Link, um die Sitzung zu beenden.


# Beispiel für das erstellen einer neuen Route und Implementierung in die HTML

#### Einführung
Das Projekt SmartGrow nutz als Interface eine Webseite, die mit Flask und SQLite entwickelt wurde. Die Anwendung bietet Funktionen wie das Hinzufügen, Entfernen und Verwalten von Pflanzen und Sensoren, sowie die Integration von externen Diensten zur Überwachung und Steuerung von Boxen. Diese Dokumentation bietet eine Übersicht, wie neue Routen hinzugefügt und in das Frontend (HTML) integriert werden.

#### Aufbau der Anwendung
Die Anwendung verwendet das Flask-Framework als Backend und HTML-Dateien im `templates`-Verzeichnis, um die Benutzeroberfläche zu gestalten. Daten werden in einer SQLite-Datenbank gespeichert.

#### Beispiel: Erstellen einer neuen Route und Integration in HTML

##### Schritt 1: Neue Route im Backend hinzufügen

Um eine neue Route zu erstellen, nutzen wir die Flask-Dekoratoren `@app.route()`. Das folgende Beispiel zeigt, wie eine neue Route für das Hinzufügen einer Box erstellt wird:

```python
@app.route("/add_box", methods=["GET", "POST"])
def add_box():
    if request.method == "POST":
        box_id = request.form["box_id"]
        conn = db_connection(db_name=DATABASE_PATH)
        conn.execute("INSERT INTO Box (boxID) VALUES (?)", (box_id,))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))
    return render_template("add_box.html")
```

##### Schritt 2: Formular zur HTML-Datei hinzufügen

Damit Benutzer über die Benutzeroberfläche eine neue Box hinzufügen können, müssen wir ein Formular in die entsprechende HTML-Datei integrieren. In diesem Fall erstellen wir eine Datei `add_box.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Neue Box hinzufügen</title>
</head>
<body>
    <h1>Neue Box hinzufügen</h1>
    <form action="{{ url_for('add_box') }}" method="post">
        <label for="box_id">Box ID:</label>
        <input type="text" id="box_id" name="box_id" required>
        <button type="submit">Box hinzufügen</button>
    </form>
</body>
</html>
```

##### Schritt 3: Navigation und Verlinkung

Damit Benutzer diese neue Seite erreichen können, fügen wir einen Link in die Navigationsleiste der `dashboard.html` hinzu:

```html
<nav>
    <a href="{{ url_for('add_box') }}">Neue Box hinzufügen</a>
    <a href="{{ url_for('logout') }}">Logout</a>
</nav>
```

#### Datenbankinteraktion
Die Verbindung zur SQLite-Datenbank erfolgt über die Funktion `db_connection`. Hier ein Beispiel, wie eine Verbindung aufgebaut und eine Abfrage ausgeführt wird:

```python
def db_connection(db_name):
    conn = sqlite3.connect(database=db_name)
    conn.row_factory = sqlite3.Row
    return conn
```

#### Sicherheit
Passwörter werden mit `bcrypt` gehasht und in der Datenbank gespeichert. Sessions werden zur Benutzerverwaltung verwendet.

```python
import bcrypt
hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
```








