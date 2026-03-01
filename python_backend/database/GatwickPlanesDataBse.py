import sqlite3
import random
from datetime import datetime, timedelta

def MakeDB(cur:sqlite3.Cursor):
    cur.execute("CREATE TABLE Planes(PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate)")
    
def NewPlane(cur:sqlite3.Cursor, PlaneID : int, Airline : str, Miles : int, Age : int, Angle : int, ArrivalTime : int, ArrivalDate : str):
    cur.execute(f"""INSERT INTO Planes VALUES ({PlaneID}, "{Airline}", {Miles}, {Age}, {Angle}, "{ArrivalTime}" ,"{ArrivalDate}")""")
    
def DelPlane(cur:sqlite3.Cursor, PlaneID : int):
    cur.execute(f"""DELETE FROM Planes WHERE PlaneID={PlaneID}""")
    
def MakeDumbyData(cur: sqlite3.Cursor, Entries: int):
    PlaneIDs = list(range(10000))
    Airlines = ["EasyJet", "RyanAir", "British Airways", "Emirate", "Lufthanse"]
    
    # Get the current time as a starting point
    now = datetime.now()

    for _ in range(Entries):
        PlaneID = str(random.choice(PlaneIDs))
        PlaneIDs.remove(PlaneID)
        Airline = random.choice(Airlines)
        Miles = random.randint(0, 100000)
        Age = random.randint(0, 50)
        Angle = random.randint(0, 35999) / 100
        
        # 1. Randomly sample a time in the next 1 hours (in minutes)
        random_minutes_ahead = random.randint(0, 1 * 60)
        arrival_datetime = now + timedelta(minutes=random_minutes_ahead)
        
        # 2. Format ArrivalDate as "D/M/YYYY" to match your DB logic
        ArrivalDate = arrival_datetime.strftime("%d/%m/%Y").lstrip("0").replace("/0", "/")
        
        # 3. Calculate ArrivalTime as the number of minutes elapsed in THAT day
        # (Hours * 60) + Minutes
        ArrivalTime = (arrival_datetime.hour * 60) + arrival_datetime.minute
        
        # Use your existing NewPlane function to insert
        NewPlane(cur, PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate)