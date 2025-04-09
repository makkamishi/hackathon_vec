from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'user': 'avnadmin',
    'password': 'AVNS_cjiPLX8eX4XKlgCiKnU',
    'host': 'mysql-25dad718-jhonjeri92-ebde.k.aivencloud.com',
    'port': '19558',
    'database': 'defaultdb'
}

@app.route('/insert_data', methods=['POST'])
def insert_data():
    distance = request.form.get('distance')
    id = request.form.get('id')

    if not distance or not id:
        return "Distance or id value is missing", 400

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Sensor_datas SET Percentage = %s WHERE id = %s", (distance, id))
                if cursor.rowcount == 0:
                    return "No record found with the provided id.", 404
                conn.commit()
                return "Record updated successfully", 200
    except mysql.connector.Error as e:
        return f"Database error: {e}", 500


@app.route('/sensor_data', methods=['GET'])
def sensor_data():
    try:
        data = get_sensor_data_as_json()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_sensor_data_as_json():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = "SELECT id, Percentage, latitude, longitude FROM Sensor_datas"
    cursor.execute(query)
    results = cursor.fetchall()
    data = {}
    for row in results:
        bin_id = row[0]
        data[f"bin{bin_id}"] = {
            "id": bin_id,
            "Level": row[1],
            "Coordinates": [row[2], row[3]]
        }
    cursor.close()
    conn.close()
    return data


@app.route('/high_level_bins', methods=['GET'])
def high_level_bins():
    try:
        data = get_high_level_bins()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_high_level_bins():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id, Percentage, latitude, longitude FROM Sensor_datas WHERE Percentage > 70")
    high_level_bins = cursor.fetchall()
    data = {}
    for row in high_level_bins:
        bin_id = row[0]
        data[f"bin{bin_id}"] = {
            "Coordinates": [row[2], row[3]]
        }
    cursor.close()
    conn.close()
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
