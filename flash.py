from flask import Flask, request
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

db_config = {
    'user':'avnadmin',
    'password':'AVNS_cjiPLX8eX4XKlgCiKnU',
    'host':'mysql-25dad718-jhonjeri92-ebde.k.aivencloud.com',
    'port':'19558',
    'database':'defaultdb'
}

@app.route('/insert_data', methods=['POST'])
def insert_data():
    distance = request.form.get('distance')
    id = request.form.get('id')  

    if distance is None:
        return "Distance value is missing", 400

    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("Update Sensor_datas SET Percentage =%s Where id = %s", (distance,id,))
            conn.commit()
            return "New record created successfully", 201
    except Error as e:
        return f"Error: {e}", 500
        
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_sensor_data_as_json():

    conn = mysql.connector.connect(
    user='avnadmin',
    password='AVNS_cjiPLX8eX4XKlgCiKnU',
    host='mysql-25dad718-jhonjeri92-ebde.k.aivencloud.com',
    port=19558,
    database='defaultdb'
    )

    cursor = conn.cursor()

    query = "SELECT Percentage FROM Sensor_datas"
    cursor.execute(query)
    results = cursor.fetchall()
    data = {}
    for i, row in enumerate(results, start=1):
        key = f"bin{i}"
        data[key] = row[0]

    json_data = json.dumps(data, indent=4)
    return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    print(get_sensor_data_as_json())
