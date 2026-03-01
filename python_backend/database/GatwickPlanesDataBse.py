import sqlite3
import random

def MakeDB(cur:sqlite3.Cursor):
    cur.execute("CREATE TABLE Planes(PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate)")
    
def NewPlane(cur:sqlite3.Cursor, PlaneID : int, Airline : str, Miles : int, Age : int, Angle : int, ArrivalTime : int, ArrivalDate : str):
    cur.execute(f"""INSERT INTO Planes VALUES ({PlaneID}, "{Airline}", {Miles}, {Age}, {Angle}, "{ArrivalTime}" ,"{ArrivalDate}")""")
    
def DelPlane(cur:sqlite3.Cursor, PlaneID : int):
    cur.execute(f"""DELETE FROM Planes WHERE PlaneID={PlaneID}""")
    
def MakeDumbyData(cur:sqlite3.Cursor, Entries : int):
    PlaneIDs = [x for x in range(10000)]
    Airlines = ["EasyJet", "RyanAir", "British Airways", "Emirate", "Lufthanse"]
    ArrivalDates = []
    for x in range(3,12):
        for y in range(1,30):
            ArrivalDates.append(f"{y}/{x}/2026")
    
    for x in range(Entries):
        PlaneID = random.choice(PlaneIDs)
        PlaneIDs.remove(PlaneID)
        Airline = random.choice(Airlines)
        Miles = random.randint(0,100000)
        Age = random.randint(0, 50)
        Angle = random.randint(0, 35999)/100
        ArrivalTime = random.randint(0, 239999)/100
        ArrivalDate = random.choice(ArrivalDates)
        
        NewPlane(cur, PlaneID, Airline, Miles, Age, Angle, ArrivalTime, ArrivalDate)