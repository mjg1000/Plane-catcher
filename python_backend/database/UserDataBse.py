import sqlite3 
from itertools import permutations
import random

#This file contains all functions on the user table and creation of the user table
#UID: unique int, Email: str, Usermame: str, Password: str

#Maybe good argument for making this into a class idk
Columns = ["Email", "Username", "Password"]

def MakeDB(cur:sqlite3.Cursor):
    cur.execute("CREATE TABLE Users(UID, Email, Username, Password)")

def NewUser(cur:sqlite3.Cursor, Email : str, Username : str, Password : str):
    #Function for adding new users: assumes hashing done client side
    #Makes UIDs iterative. Should Change later
    #Also do regex on userside entries
    PrevID = cur.execute("""SELECT MAX(UID) FROM Users""").fetchone()[0]
    ID = PrevID + 1 if PrevID != None else 0
    cur.execute(f"""INSERT INTO Users VALUES ({ID}, "{Email}", "{Username}", "{Password}")""")
    
def UpdateUser(cur:sqlite3.Cursor, Username : str, ToUpdate : str, Data : str):
    if ToUpdate in Columns:
        ID = GetID(cur, Username)
        print(Data)
        cur.execute(f"""UPDATE Users SET {ToUpdate} = "{Data}" WHERE UID = {ID} """)
    else:
        raise ValueError

def DelUser(cur:sqlite3.Cursor, Username : str):
    ID = GetID(cur,Username)
    cur.execute(f"""DELETE FROM Users WHERE UID={ID}""")
    
def GetID(cur:sqlite3.Cursor, Username : str):
    return cur.execute(f"""SELECT UID FROM Users WHERE Username="{Username}" """).fetchone()[0]

def MakeDumbyData(cur:sqlite3.Cursor):
    names = list(permutations("abcde"))
    names = [str(x[0]) + str(x[1]) + str(x[2]) + str(x[3]) + str(x[4]) for x in names]
    Emails = ["@outlook.com", "@Gmail.com", "@hotmail.com"]
    
    for name in names:
        NewUser(cur, name+random.choice(Emails), name, hash(name))