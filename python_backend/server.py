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

@app.route('/tail', methods=['POST'])
def get_tail():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    # Decode image
    image_b64 = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_b64)
    
    # Identify plane via Gemini
    res = component.request_gemini(image_bytes, "PNG", "photo_taken")
    if res[1] == -1:
        return jsonify({"status": "Failure", "message": res[0]})
    
    tail_num = str(res[0]) # Gemini identified tail
    current_user_id = 1    # Testing ID

    conn = get_db()
    cur = conn.cursor()
    
    try:
        # 1. Fetch plane details
        plane_data = cur.execute("SELECT * FROM Planes WHERE PlaneID = ?", (tail_num,)).fetchone()
        if not plane_data:
            return jsonify({"status": "error", "message": f"Plane {tail_num} not in database"}), 404

        # 2. Add to inventory
        add_plane_to_inventory(current_user_id, tail_num, cur)

        # 3. Check and update quests
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
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        conn.close()

def add_plane_to_inventory(user_id, tail_no, cur):  
    # Check if exists
    existing = cur.execute("SELECT * FROM Inventory WHERE UID = ? AND PlaneID = ?", (user_id, tail_no)).fetchone()
    
    if not existing:
        # Insert new inventory item (setting initial count/status to 0)
        cur.execute("INSERT INTO Inventory (UID, PlaneID, Count) VALUES (?, ?, ?)", (user_id, tail_no, 1))

def update_quests(user_id, tail_no, cur):
    """Checks if the plane completes a quest. Updates points and deletes quest if so."""
    # Look for a quest matching this user and this plane
    quest = cur.execute("SELECT * FROM Quest WHERE UserID = ? AND PlaneID = ?", (user_id, tail_no)).fetchone()
    
    if quest:
        reward = quest['Reward']
        
        # 1. Update user's total points (assuming column name 'Points' in Users table)
        cur.execute("UPDATE Users SET Points = Points + ? WHERE UserID = ?", (reward, user_id))
        
        # 2. Delete the completed quest
        cur.execute("DELETE FROM Quest WHERE UserID = ? AND PlaneID = ?", (user_id, tail_no))
        
        return reward
    return 0

# ... keep other routes like /planes and /plane/<tail_no> ...