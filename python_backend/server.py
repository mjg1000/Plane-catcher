from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import base64
# Import your existing modules
from database import UserDataBse, GatwickPlanesDataBse, InventoryDataBse, QuestDataBse
import gemini_processing

app = Flask(__name__)
CORS(app)

DB_PATH = "Users.db"

global component
component = gemini_processing.gemini_components()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ... imports

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

@app.route('/tail', methods=['POST'])
def get_tail():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    image_b64 = data['image'].split(',')[1]
    image_bytes = base64.decodebytes(image_b64.encode()) # Cleaner decoding
    
    res = component.request_gemini(image_bytes, "PNG", "photo_taken")

    if res[1] == -1:
        return jsonify({"status": "Failure", "message": res[0]})
    
    tail_num = str(res[0]) 
    current_user_id = 1    

    conn = get_db()
    cur = conn.cursor()
    
    try:
        # Use parameterized query to handle string tail numbers safely
        query = "SELECT * FROM Planes WHERE PlaneID = ?"
        plane_data = cur.execute(query, (str(tail_num),)).fetchone()

        if not plane_data:
            return jsonify({"status": "Failure", "message": f"Plane {tail_num} not found in airspace"})

        # Logic helpers now take raw cursor to stay in one transaction
        add_plane_to_inventory(current_user_id, tail_num, cur)
        quest_reward = update_quests(current_user_id, tail_num, cur)

        conn.commit()
        return jsonify({
            "status": "success",
            "tail_no": tail_num,
            "quest_completed": quest_reward > 0,
            "reward": quest_reward
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def add_plane_to_inventory(user_id, tail_no, cur):  
    # Fix: Corrected query syntax
    existing = cur.execute("SELECT * FROM Inventory WHERE UID = ? AND PlaneID = ?", (user_id, tail_no)).fetchone()
    if not existing:
        cur.execute("INSERT INTO Inventory (UID, PlaneID, Count) VALUES (?, ?, ?)", (user_id, tail_no, 1))

def update_quests(user_id, tail_no, cur):
    # Fix: Query the Quest table, not 'Quests'
    quest = cur.execute("SELECT * FROM Quest WHERE UserID = ? AND PlaneID = ?", (user_id, tail_no)).fetchone()
    if quest:
        reward = quest['Reward']
        cur.execute("UPDATE Users SET Points = Points + ? WHERE UserID = ?", (reward, user_id))
        cur.execute("DELETE FROM Quest WHERE UserID = ? AND PlaneID = ?", (user_id, tail_no))
        return reward
    return 0

# ... rest of file

# ... keep other routes like /planes and /plane/<tail_no> ...
 
def add_plane_to_inventory(user_id, tail_no, cur):  
    cur.execute(f'select * from Inventory where UID = {user_id} AND PlaneID = {tail_no}')

    # 4. See the outputs (Fetch all rows)
    rows = cur.fetchall()
    if len(rows) == 0: # not already added this plane
        query = f"INSERT INTO Inventory({user_id}, {tail_no}, 0)"
        cur.execute(query)

def update_quests(json_plane, json_quests): # also incremenents point totals.
    pass

@app.route('/plane/<tail_no>', methods=['GET'])
def get_plane(tail_no):
    conn = get_db()
    cur = conn.cursor()
    # DO NOT use int(tail_no). Tail numbers like EJU8514 are strings.
    query = "SELECT * FROM Planes WHERE PlaneID = ?"
    plane_data = cur.execute(query, (str(tail_no),)).fetchone()
    conn.close()
    
    if plane_data:
        return jsonify(dict(plane_data))
    return jsonify({"error": "Plane not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)