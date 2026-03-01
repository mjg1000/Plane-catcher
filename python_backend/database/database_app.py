from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
# Import your existing modules
from database import UserDataBse, GatwickPlanesDataBse, InventoryDataBse

app = Flask(__name__)
CORS(app) # Allows your React app to talk to this server

DB_PATH = "Users.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

@app.route('/init-db', methods=['POST'])
def initialize():
    """Initializes the database with dummy data if it doesn't exist."""
    conn = get_db()
    cur = conn.cursor()
    # Use your existing logic from Database.py
    UserDataBse.MakeDB(cur)
    GatwickPlanesDataBse.MakeDB(cur)
    InventoryDataBse.MakeDB(cur)
    UserDataBse.MakeDumbyData(cur)
    GatwickPlanesDataBse.MakeDumbyData(cur, 50)
    InventoryDataBse.MakeDumbyData(cur)
    conn.commit()
    conn.close()
    return jsonify({"status": "Database Initialized"})

@app.route('/planes', methods=['GET'])
def get_planes():
    """Query the database for all planes."""
    conn = get_db()
    cur = conn.cursor()
    planes = cur.execute("SELECT * FROM Planes").fetchall()
    conn.close()
    return jsonify([dict(row) for row in planes])

if __name__ == "__main__":
    app.run(debug=True, port=5000)