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

    if not distance or not id:
       return "Distance or id value is missing", 400

    try:
        with mysql.connector.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE Sensor_datas SET Percentage = %s WHERE id = %s",(distance, id))
                if cursor.rowcount == 0:
                    return "No record found with the provided id.", 404
                conn.commit()
                return "Record updated successfully", 200
    except mysql.connector.Error as e:
        return f"Database error: {e}", 500
    
def get_sensor_data_as_json():

    conn = mysql.connector.connect(
    user='avnadmin',
    password='AVNS_cjiPLX8eX4XKlgCiKnU',
    host='mysql-25dad718-jhonjeri92-ebde.k.aivencloud.com',
    port=19558,
    database='defaultdb'
    )

    cursor = conn.cursor()

    query = "SELECT id, Percentage, latitude, longitude FROM Sensor_datas"
    cursor.execute(query)
    results = cursor.fetchall()
    data = {}
    for row in results:
        bin_id = row[0]  # 'id' from the database
        data[f"bin{bin_id}"] = {
            "id": bin_id,
            "Level": row[1],  # 'Percentage' from the database
            "Coordinates": [row[2], row[3]]  # 'latitude' and 'longitude' from the database
        }
    json_data = json.dumps(data, indent=4)
    return json_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    print(get_sensor_data_as_json())
