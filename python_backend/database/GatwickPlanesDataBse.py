import sqlite3
import random
from datetime import datetime, timedelta

def MakeDB(cur: sqlite3.Cursor):
    # Added PlaneModel to the schema
    cur.execute("CREATE TABLE IF NOT EXISTS Planes(PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel)")
    
def NewPlane(cur: sqlite3.Cursor, PlaneID: int, Airline: str, Miles: int, Age: int, Angle: float, ArrivalTime: int, ArrivalDate: str, PlaneModel: str):
    # Use '?' placeholders to handle types (like None/NULL) and security safely
    query = "INSERT INTO Planes VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    cur.execute(query, (PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel))
    
def DelPlane(cur: sqlite3.Cursor, PlaneID: int):
    cur.execute("DELETE FROM Planes WHERE PlaneID=?", (PlaneID,))
    
def MakeDumbyData(cur: sqlite3.Cursor, Entries: int):
    PlaneIDs = list(range(10000))
    Airlines = ["EasyJet", "RyanAir", "British Airways", "Emirates", "Lufthansa", "TUI"]
    # In Python, 'None' represents the SQL 'NULL' value
    PlaneModels = ["B737", "B777", "A320", "A380", "Other", None]
    
    now = datetime.now()

    for _ in range(Entries):
        PlaneID = random.choice(PlaneIDs)
        PlaneIDs.remove(PlaneID)
        Airline = random.choice(Airlines)
        Miles = random.randint(0, 100000)
        Age = random.randint(0, 50)
        Angle = random.randint(0, 35999) / 100
        
        # Select a model, which may be None (SQL NULL)
        PlaneModel = random.choice(PlaneModels)
        
        random_minutes_ahead = random.randint(0, 1 * 60)
        arrival_datetime = now + timedelta(minutes=random_minutes_ahead)
        
        ArrivalDate = arrival_datetime.strftime("%d/%m/%Y").lstrip("0").replace("/0", "/")
        ArrivalTime = (arrival_datetime.hour * 60) + arrival_datetime.minute
        
        # Pass the PlaneModel to the NewPlane function
        NewPlane(cur, PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate, PlaneModel)