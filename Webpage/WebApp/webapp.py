from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import sqlite3
import bcrypt
import secrets
import os
from werkzeug.utils import secure_filename
import json
import subprocess

app = Flask(__name__, template_folder="templates")
app.secret_key = secrets.token_hex(16)

DATABASE_PATH = "/var/www/smartgrow_app/webpage/WebApp/Database/smartgrow_database.db"
#DATABASE_PATH = "Database/smartgrow_database.db"

def db_connection(db_name):
    conn = sqlite3.connect(database=db_name)
    conn.row_factory = sqlite3.Row
    return conn

def check_service(service_name):
    try:
        result = subprocess.run(["systemctl", "is-active", service_name], stdout=subprocess.PIPE)
        status = result.stdout.decode("utf-8").strip()
        return status
    except Exception as e:
        return f"Error: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = db_connection(db_name=DATABASE_PATH)
        user = conn.execute("SELECT * FROM Users WHERE Username = ?", (username,)).fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user["Password"].encode("utf-8")):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return jsonify({"error": "Invalid username or password"}), 401

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))

    conn = db_connection(db_name=DATABASE_PATH)
    
    username = session["user"]

    user_boxes = conn.execute("""
        SELECT boxID, GROUP_CONCAT(SensorMAC) AS SensorMACs
        FROM Box
        WHERE Username = ?
        GROUP BY boxID
    """, (username,)).fetchall()

    available_boxes = conn.execute("""
        SELECT DISTINCT boxID 
        FROM Box 
        WHERE Username IS NULL
    """).fetchall()

    box_plants = {}
    box_sensors = {}
    for box in user_boxes:
        box_id = box['boxID']
        plants = conn.execute("""
            SELECT Plantname, SensorMAC
            FROM Plants
            WHERE SensorMAC IN (SELECT SensorMAC FROM Box WHERE boxID = ?)
        """, (box_id,)).fetchall()
        box_plants[box_id] = plants

        sensors = conn.execute("""
            SELECT DISTINCT SensorMAC
            FROM Box
            WHERE boxID = ?
        """, (box_id,)).fetchall()
        
        used_sensors = conn.execute("""
            SELECT DISTINCT SensorMAC
            FROM Plants
            WHERE SensorMAC IN (SELECT SensorMAC FROM Box WHERE boxID = ?)
        """, (box_id,)).fetchall()
        
        used_sensor_macs = {sensor['SensorMAC'] for sensor in used_sensors}
        available_sensors = [sensor for sensor in sensors if sensor['SensorMAC'] not in used_sensor_macs]
        
        box_sensors[box_id] = available_sensors

    plants_information = conn.execute("""
        SELECT pid FROM HerbsDb_Plants_Information
    """).fetchall()

    conn.close()

    services = ["mqtt_communication", "grafana-server", "plant_recog"]
    statuses = {service: check_service(service_name=service + ".service") for service in services}

    return render_template(
        "dashboard.html", 
        boxes=user_boxes,
        available_boxes=available_boxes,
        box_plants=box_plants,
        box_sensors=box_sensors,
        plants_information=plants_information,
        statuses=statuses
    )

@app.route("/box_details/<box_id>")
def box_details(box_id):
    if "user" not in session:
        return redirect(url_for("index"))

    conn = db_connection(db_name=DATABASE_PATH)

    plants = conn.execute("""
        SELECT Plantname, SensorMAC
        FROM Plants
        WHERE SensorMAC IN (SELECT SensorMAC FROM Box WHERE boxID = ?)
    """, (box_id,)).fetchall()

    water_tank = conn.execute("""
        SELECT volume_mix, volume_water, volume_fertilizer, volume_acid, time
        FROM Liquid_Tanks
        WHERE boxID = ?
        ORDER BY time DESC
        LIMIT 1
    """, (box_id,)).fetchone()

    box_info = conn.execute("""
        SELECT boxID, GROUP_CONCAT(SensorMAC) AS SensorMACs
        FROM Box
        WHERE boxID = ?
        GROUP BY boxID
    """, (box_id,)).fetchone()

    plant_battery_info = {}
    for plant in plants:
        sensor_mac = plant['SensorMAC']
        battery_info = conn.execute("""
            SELECT battery
            FROM Measurements
            WHERE SensorMAC = ?
            ORDER BY time DESC
            LIMIT 1
        """, (sensor_mac,)).fetchone()
        plant_battery_info[sensor_mac] = battery_info['battery'] if battery_info else None

    pot_assignments = {}
    for plant in plants:
        sensor_mac = plant['SensorMAC']
        pot_info = conn.execute("""
            SELECT PotNum
            FROM Box
            WHERE SensorMAC = ?
        """, (sensor_mac,)).fetchone()
        pot_assignments[sensor_mac] = pot_info['PotNum'] if pot_info else None

    conn.close()

    return render_template(
        "box_detail.html",
        box_id=box_id,
        plants=plants,
        water_tank=water_tank,
        box=box_info,
        plant_battery_info=plant_battery_info,
        pot_assignments=pot_assignments
    )

@app.route("/add_or_select_box", methods=["POST"])
def add_or_select_box():
    if "user" not in session:
        return redirect(url_for("index"))

    box_id = request.form["box_id"]
    conn = db_connection(db_name=DATABASE_PATH)
    username = session["user"]

    user_boxes = conn.execute("SELECT boxID FROM Box WHERE Username = ?", (username,)).fetchall()

    if not user_boxes:
        conn.execute("UPDATE Box SET Username = ? WHERE boxID = ?", (username, box_id))
    else:
        conn.execute("UPDATE Box SET Username = ? WHERE boxID = ?", (username, box_id))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route("/delete_box", methods=["POST"])
def delete_box():
    if "user" not in session:
        return redirect(url_for("index"))

    box_id = request.form["box_id"]
    username = session["user"]

    conn = db_connection(db_name=DATABASE_PATH)

    sensors = conn.execute("""
        SELECT SensorMAC
        FROM Box
        WHERE boxID = ?
    """, (box_id,)).fetchall()

    sensor_macs = [sensor['SensorMAC'] for sensor in sensors]

    if sensor_macs:
        placeholders = ','.join('?' * len(sensor_macs))
        conn.execute(f"""
            DELETE FROM Measurements
            WHERE SensorMAC IN ({placeholders})
        """, sensor_macs)

        conn.execute(f"""
            DELETE FROM Plants
            WHERE SensorMAC IN ({placeholders})
        """, sensor_macs)

    conn.execute("""
        DELETE FROM Liquid_Tanks
        WHERE boxID = ?
    """, (box_id,))

    conn.execute("""
        UPDATE Box
        SET Username = NULL
        WHERE boxID = ? AND Username = ?
    """, (box_id, username))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route("/get_options", methods=["GET"])
def get_options():
    conn = db_connection(db_name=DATABASE_PATH)

    pids = conn.execute("SELECT pid FROM HerbsDb_Plants_Information").fetchall()

    conn.close()

    return jsonify({"pids": [pid["pid"] for pid in pids]})

@app.route("/add_plant", methods=["POST"])
def add_plant():
    if "user" not in session:
        return redirect(url_for("index"))

    plant_name = request.form["plant_name"]
    pid = request.form["pid"]
    sensor_mac = request.form["sensor_mac"]
    box_id = request.form["box_id"]

    conn = db_connection(db_name=DATABASE_PATH)
    username = session["user"]

    conn.execute(
        "INSERT INTO Plants (Plantname, SensorMAC, Username, pid) VALUES (?, ?, ?, ?)",
        (plant_name, sensor_mac, username, pid)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route("/delete_plant", methods=["POST"])
def delete_plant():
    if "user" not in session:
        return redirect(url_for("index"))

    plant_name = request.form["plant_name"]
    sensor_mac = request.form["sensor_mac"]
    box_id = request.form["box_id"]

    conn = db_connection(db_name=DATABASE_PATH)
    username = session["user"]

    conn.execute("""
        DELETE FROM Measurements
        WHERE SensorMAC = ?
    """, (sensor_mac,))

    conn.execute("""
        DELETE FROM Plants
        WHERE Plantname = ? AND SensorMAC = ? AND Username = ?
    """, (plant_name, sensor_mac, username))

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    app.config['PlantSnaps'] = os.path.join(os.path.dirname(__file__), 'PlantSnaps')

    if not os.path.exists(app.config['PlantSnaps']):
        os.makedirs(app.config['PlantSnaps'])

    photo = request.files['photo']
    box_id = request.form['box_id']

    if photo:
        filename = secure_filename(f"{box_id}_{photo.filename}")
        filepath = os.path.join(app.config['PlantSnaps'], filename)
        photo.save(filepath)

        image_pipe_path = "/var/www/smartgrow_app/webpage/pipes/image_pipe"
        result_pipe_path = "/var/www/smartgrow_app/webpage/pipes/result_pipe"

        with open(image_pipe_path, 'w') as fifo:
            fifo.write(filepath)

        with open(result_pipe_path, 'r') as fifo:
            result_json = fifo.read().strip()

        result_data = json.loads(result_json)
        predicted_class = result_data["predicted_class"]
        confidence = result_data["confidence"]

        plant_name = predicted_class
        pid_map = {
            "Basilikum": "Basil",
            "Petersilie": "Parsley"
        }
        pid = pid_map.get(predicted_class, None)

        if not pid:
            os.remove(filepath)
            return jsonify({"error": "Unknown plant detected."}), 400

        conn = db_connection(db_name=DATABASE_PATH)

        used_sensors = conn.execute(
            """
            SELECT DISTINCT SensorMAC
            FROM Plants
            WHERE SensorMAC IN (
                SELECT SensorMAC
                FROM Box
                WHERE boxID = ?
            )
            """, (box_id,)
        ).fetchall()
        used_sensors = {row["SensorMAC"] for row in used_sensors}

        query = """
        SELECT SensorMAC
        FROM Box
        WHERE boxID = ? AND SensorMAC NOT IN ({})
        LIMIT 1
        """.format(','.join('?' * len(used_sensors)))

        free_sensor = conn.execute(
            query, 
            (box_id, *used_sensors)
        ).fetchone()

        if not free_sensor:
            os.remove(filepath)
            return jsonify({"error": "No free sensors available in the selected box."}), 400

        sensor_mac = free_sensor["SensorMAC"]
        username = session["user"]

        conn.execute(
            "INSERT INTO Plants (Plantname, SensorMAC, Username, pid) VALUES (?, ?, ?, ?)",
            (plant_name, sensor_mac, username, pid)
        )
        conn.commit()
        conn.close()

        os.remove(filepath)

        return redirect(url_for('dashboard'))

    return jsonify({"error": "No photo uploaded."}), 400

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmed_password = request.form["confirm_password"]

        if password != confirmed_password:
            return jsonify({"error": "Passwords do not match. Please try again."}), 400

        conn = db_connection(db_name=DATABASE_PATH)

        user = conn.execute("SELECT * FROM users WHERE Username = ?", (username,)).fetchone()
        if user:
            return jsonify({"error": "Username already exists. Please choose another one."}), 400

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        conn.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, hashed_pw.decode("utf-8")))
        conn.commit()
        conn.close()

        return jsonify({"success": "Thank you for registering!"}), 200

@app.route(rule="/plantview/<plant_sensor>", methods=["GET"])
def plantview(plant_sensor):
    if "user" not in session:
        return redirect(url_for("index"))

    conn = db_connection(db_name=DATABASE_PATH)

    username = session["user"]

    plant = conn.execute("SELECT * FROM plants WHERE SensorMAC=?", (plant_sensor,)).fetchone()

    if not plant:
        conn.close()
        return "Plant not found", 404

    plant_info = conn.execute("SELECT * FROM HerbsDb_Plants_Information WHERE pid=?", (plant['pid'],)).fetchone()

    conn.close()

    if plant_info is None:
        plant_info = {}

    return render_template("plantview.html", plant=plant, plant_info=plant_info)

#if __name__ == "__main__":
#    app.run(
#        host="0.0.0.0",
#        port=8000,
#        debug=True
#    )

