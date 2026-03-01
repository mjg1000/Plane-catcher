from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
# Import your existing modules
from database import UserDataBse, GatwickPlanesDataBse, InventoryDataBse
import gemini_processing
import base64

app = Flask(__name__)
CORS(app) # Allows your React app to talk to this server

DB_PATH = "Users.db"

global component
component = gemini_processing.gemini_components()

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
    """Query the database for all planes."""
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    # 1. The image arrives as "data:image/png;base64,iVBORw0..."
    # We need to split the header off to get just the base64 encoded data
    image_b64 = data['image'].split(',')[1]
    
    # 2. Decode the image (if your AI function needs a file-like object)
    image_bytes = base64.b64decode(image_b64)
    # img = Image.open(io.BytesIO(image_bytes)) # Now you have a PIL Image object
    
    # 3. Call your AI/Identification logic here
    res = component.request_gemini(image_bytes, "PNG", "photo_taken")

    if res[1] == -1:
        return jsonify({
            "status": "Failure",
            "message": res[0],
        })
    
    tail_num = res[0]
    
    conn = get_db()
    cur = conn.cursor()
    
    # Use the tail_no variable directly from the function argument.
    # Cast to int to ensure it matches the PlaneID column type.
    query = "SELECT * FROM Planes WHERE PlaneID = " + str(tail_num)
    plane_data = cur.execute(query).fetchone()

    # Now do quest logic, add plane to inv etc....
    json_plane = jsonify(dict(plane_data))

    current_user_id = 1 #TESTING
    add_plane_to_inventory(current_user_id, tail_num, cur)

    query = "SELECT * FROM Quests WHERE UserID = " + str(current_user_id)
    quests = cur.execute(query).fetchone()
    json_quests = jsonify(dict(quests))

    update_quests(json_plane, json_quests)

    


    print("Image received and decoded!")
    
    # Example return
    return jsonify({
        "status": "success",
        "message": "Image received",
        "tail_no": res # Example found tail
    })
    
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
    """Query the database for a specific plane."""
    
    # Remove the request.args.get line entirely.
    # Use the tail_no from the URL path.
    
    conn = get_db()
    cur = conn.cursor()
    
    # Use the tail_no variable directly from the function argument.
    # Cast to int to ensure it matches the PlaneID column type.
    query = "SELECT * FROM Planes WHERE PlaneID = ?"
    plane_data = cur.execute(query, (str(tail_no),)).fetchone()
    
    conn.close()
    
    if plane_data:
        return jsonify(dict(plane_data))
    
    return jsonify({"error": "Plane not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)