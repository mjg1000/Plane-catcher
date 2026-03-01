import sqlite3
import random
import os
import json
from datetime import datetime

def MakeDB(cur: sqlite3.Cursor):
    # Ensures the schema includes the PlaneModel column
    cur.execute("CREATE TABLE IF NOT EXISTS Planes(PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel)")

def NewPlane(cur: sqlite3.Cursor, PlaneID: int, Airline: str, Miles: int, Age: int, Angle: float, ArrivalTime: int, ArrivalDate: str, PlaneModel: str):
    query = "INSERT INTO Planes VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (PlaneID, Airline, Miles, Age, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel))

def LoadFlightData(cur: sqlite3.Cursor, folder_path: str = r"C:\Users\Steve\Documents\plane catcher\Plane-catcher\python_backend\database\FlightDataComp"):
    """
    Reads JSON files from the specified folder and inserts them into the database.
    Missing schema fields are populated with random data.
    """
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found.")
        return

    # Iterate through every file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as f:
                data = json.load(f)

                # 1. Extract PlaneID from filename (stripping .json)
                # Example: "G-VZMA.json" -> PlaneID = "G-VZMA"
                # Note: If your PlaneID column must be an int, use a hash or a map
                plane_id = filename.replace(".json", "")

                # 2. Map JSON fields to database schema
                airline = data.get("airline", "Unknown")
                miles = data.get("direct_distance_miles", 0)
                
                # Extracting Model from aircraft_model string
                # Example: "Airbus A320 (twin-jet)" -> "A320"
                raw_model = data.get("aircraft_model", "")
                if "A320" in raw_model: plane_model = "A320"
                elif "A380" in raw_model: plane_model = "A380"
                elif "737" in raw_model: plane_model = "B737"
                elif "777" in raw_model: plane_model = "B777"
                else: plane_model = "Other"

                # 3. Parse Arrival Time and Date
                # Format: "2024-05-10 20:00:00"
                arrival_str = data.get("estimated_arrival")
                if arrival_str:
                    dt_obj = datetime.strptime(arrival_str, "%Y-%m-%d %H:%M:%S")
                    arrival_date = dt_obj.strftime("%d/%m/%Y").lstrip("0").replace("/0", "/")
                    arrival_time = (dt_obj.hour * 60) + dt_obj.minute
                else:
                    arrival_date = "1/1/2024"
                    arrival_time = 0

                # 4. Generate random data for missing fields
                age = random.randint(0, 30)
                angle = random.randint(0, 35999) / 100

                # 5. Insert into Database
                NewPlane(cur, plane_id, airline, miles, age, angle, arrival_time, arrival_date, plane_model)

    print(f"Successfully processed {len(os.listdir(folder_path))} flight data files.")