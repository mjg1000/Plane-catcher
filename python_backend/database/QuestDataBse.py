import sqlite3
import random

def MakeDB(cur: sqlite3.Cursor):
    # Matches the schema: UserID, PlaneID, Reward
    cur.execute("CREATE TABLE IF NOT EXISTS Quest(UserID, PlaneID, Reward)")
    
def NewQuest(cur: sqlite3.Cursor, UserID: int, PlaneID: str, reward: int):
    # Ensure PlaneID is treated as a string for tail numbers like 'EJU8514'
    query = "INSERT INTO Quest VALUES (?, ?, ?)"
    cur.execute(query, (UserID, PlaneID, reward))
    
def DelQuest(cur: sqlite3.Cursor, PlaneID: str, UserID: int):
    cur.execute("DELETE FROM Quest WHERE PlaneID=? AND UserID = ?", (PlaneID, UserID))
    
def MakeDumbyData(cur: sqlite3.Cursor, Entries: int):
    # Using real tail numbers from your FlightDataComp requirements
    PlaneIDs = ["EJU8514", "EZY824", "EZY6420"]
    UserId = 1 

    for _ in range(min(Entries, len(PlaneIDs))):
        PlaneID = random.choice(PlaneIDs)
        PlaneIDs.remove(PlaneID)
        reward = random.randint(2, 10) * 100
        
        NewQuest(cur, UserId, PlaneID, reward)