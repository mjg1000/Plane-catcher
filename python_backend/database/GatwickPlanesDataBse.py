import sqlite3
import random
import os
import json
from datetime import datetime, timedelta

def MakeDB(cur: sqlite3.Cursor):
    # Ensures the schema includes the PlaneModel column
    cur.execute("CREATE TABLE IF NOT EXISTS Planes(PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel)")

def NewPlane(cur: sqlite3.Cursor, PlaneID: str, Airline: str, Miles: int, Age: int, Angle: float, ArrivalTime: int, ArrivalDate: str, PlaneModel: str):
    query = "INSERT INTO Planes VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel))

def LoadFlightData(cur: sqlite3.Cursor, folder_path: str = r"C:\Users\Steve\Documents\plane catcher\Plane-catcher\python_backend\database\FlightDataComp"):
    """
    Reads JSON files from the specified folder and inserts them into the database.
    Calculates ArrivalTime and ArrivalDate to determine starting positions.
    """
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return

    now = datetime.now()

    # Iterate through every file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                # 1. Extract PlaneID (Tail number)
                plane_id = filename.replace(".json", "").strip()

                # 2. Map JSON fields to database schema
                airline = data.get("airline", "Unknown")
                miles = data.get("direct_distance_miles", random.randint(100, 3000))
                
                # Normalize Model for Frontend
                raw_model = data.get("aircraft_model", "")
                if "A320" in raw_model: plane_model = "A320"
                elif "A380" in raw_model: plane_model = "A380"
                elif "737" in raw_model: plane_model = "B737"
                elif "777" in raw_model: plane_model = "B777"
                else: plane_model = "Other"

                # 3. GENERATE STARTING LOCATIONS LOGIC (Timing)
                # Attempt to get arrival from JSON, otherwise generate a random one in the next hour
                arrival_str = data.get("estimated_arrival")
                
                if arrival_str:
                    try:
                        arrival_datetime = datetime.strptime(arrival_str, "%Y-%m-%d %H:%M:%S")
                        # If the JSON time has already passed, set it to a future time so it's visible on map
                        if arrival_datetime < now:
                             arrival_datetime = now + timedelta(minutes=random.randint(5, 60))
                    except ValueError:
                        arrival_datetime = now + timedelta(minutes=random.randint(5, 60))
                else:
                    # Logic from previous file: Randomly sample a time in the next 1 hour
                    random_minutes_ahead = random.randint(5, 60)
                    arrival_datetime = now + timedelta(minutes=random_minutes_ahead)

                # Format Date as "D/M/YYYY" and Time as minutes elapsed in day
                arrival_date = arrival_datetime.strftime("%d/%m/%Y").lstrip("0").replace("/0", "/")
                arrival_time = (arrival_datetime.hour * 60) + arrival_datetime.minute

                # 4. Generate random data for physical missing fields
                age = random.randint(0, 30)
                angle = random.randint(0, 35999) / 100 # Random bearing for approach angle

                # 5. Insert into Database
                NewPlane(cur, plane_id, airline, miles, age, angle, arrival_time, arrival_date, plane_model)

    print(f"Successfully processed {len(os.listdir(folder_path))} flight data files.")