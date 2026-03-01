import sqlite3
import random 

def MakeDB(cur:sqlite3.Cursor):
    cur.execute("CREATE TABLE Inventory(UID, PlaneId, BeenOn)")

def NewItem(cur:sqlite3.Cursor, UID : int, PlaneID : int):
    #Function for adding new users: assumes hashing done client side
    #Makes UIDs iterative. Should Change later
    #Also do regex on userside entries
    cur.execute(f"""INSERT INTO Inventory VALUES ({UID}, {PlaneID}, 0)""")
    
def GoneOn(cur:sqlite3.Cursor, UID : int, PlaneID : int):
    cur.execute(f"""UPDATE Inventory SET BeenOn = 1 WHERE UID = {UID} AND PlaneID = {PlaneID}""")
    
def MakeDumbyInventory(cur:sqlite3.Cursor):
    UIDs = cur.execute("SELECT UID FROM Users").fetchall()
    UIDs = [x[0] for x in UIDs]
    PlaneIDs = cur.execute("SELECT PlaneID FROM Planes").fetchall()
    PlaneIDs = [x[0] for x in PlaneIDs]
    
    for ID in UIDs:
        for x in range(random.randint(1,15)):
            PlaneIDsTemp = PlaneIDs
            PlaneID = random.choice(PlaneIDsTemp)
            PlaneIDsTemp.remove(PlaneID)
            NewItem(cur, ID, PlaneID)
            