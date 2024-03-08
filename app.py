"""
Author: shihan
Date: 2024-03-08 13:50:36
version: 1.0
description: 
"""

from flask import (
    Flask,
    jsonify,
    request
)


import psycopg2 as db
import requests
import os


app = Flask(__name__)

# SQL
DB_HOST = "db.doc.ic.ac.uk"
DB_USER = "sf23"
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_PORT = "5432"

event_data = []


def get_db_connection():
    server_params = {
        "dbname": DB_USER,
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "client_encoding": "utf-8",
    }
    return db.connect(**server_params)


@app.route("/get_events", methods=["GET"])
def get_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    username = request.args.get("username")
    userid = username
    query = "SELECT * FROM calendar WHERE userid = %s"
    cursor.execute(query, (userid,))
    events = cursor.fetchall()
    conn.close()
    # event_data = [{'start': event.startTime, 'end': event.endTime, 'title': event.title} for event in events]
    event_data = [
        {"start": event[2], "end": event[3], "title": event[4]} for event in events
    ]

    return jsonify(event_data)


@app.route("/add_events", methods=["POST"])
def add_event():
    data = request.get_json()
    userid = data.get("username")
    startTime = data.get("start")
    endTime = data.get("end")
    title = data.get("title")
    query = "INSERT INTO calendar (userid, startTime, endTime, title) VALUES (%s,%s, %s,%s) returning id"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        query,
        (
            userid,
            startTime,
            endTime,
            title,
        ),
    )
    events = cursor.fetchone()
    conn.commit()
    conn.close()
    print(events)
    return jsonify({"message": "Event added successfully"})


if __name__ == "__main__":
    app.run(debug=True)
