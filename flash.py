from flask import Flask, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection parameters
db_config = {
    'user':'avnadmin',
    'password':'AVNS_cjiPLX8eX4XKlgCiKnU',
    'host':'mysql-25dad718-jhonjeri92-ebde.k.aivencloud.com',
    'port':'19558',
    'database':'defaultdb'
}

@app.route('/insert_data', methods=['POST'])
def insert_data():
    Percentage = request.form.get('Percentage')
    if Percentage is None:
        return "Distance value is missing", 400

    try:
        # Establish a database connection
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            cursor = conn.cursor()
            # Insert the distance value into the sensor_data table
            cursor.execute("INSERT INTO Sensor_data (Percentage) VALUES (%s)", (Percentage,))
            conn.commit()
            return "New record create successfully", 201
    except Error as e:
        return f"Error: {e}", 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run()
