import numpy as np
import sqlite3
import UserDataBse
import InventoryDataBse
import random
import GatwickPlanesDataBse
        

con = sqlite3.connect("Users.db")
def OutDb(cur : sqlite3.Cursor, Table : str):
    print(f"{Table}:")
    for row in cur.execute(f"Select * From {Table}"):
        print(row)
    print("\n")


def TestUserDB(cur : sqlite3.Cursor):
    OutDb(cur, "Users")
    cur.execute("DROP TABLE Users")
    UserDataBse.MakeUserDataBase(cur)
    UserDataBse.NewUser(cur, "john@johnmail.com", "johntheguy", "HashJohn")
    con.commit()
    OutDb(cur, "Users")
    
    
def TestInventoryDB(cur : sqlite3.Cursor):
    #OutDb(cur, "Inventory")
    #cur.execute("DROP TABLE Inventory")
    #InventoryDataBse.MakeUserDataBase(cur)
    #InventoryDataBse.NewPlane(cur, 1, 2207)
    #InventoryDataBse.GoneOn(cur, 1, 2207)
    OutDb(cur, "Inventory")
    #con.commit()

def TestGatwickDB(cur : sqlite3.Cursor):
    cur.execute("DROP TABLE Planes")
    GatwickPlanesDataBse.MakeDB(cur)
      
def DropAll(cur : sqlite3.Cursor):
    cur.execute("DROP TABLE Users")
    cur.execute("DROP TABLE Inventory")
    cur.execute("DROP TABLE Planes")

def DeployDB(cur : sqlite3.Cursor):
    UserDataBse.MakeDB(cur)
    InventoryDataBse.MakeDB(cur)
    GatwickPlanesDataBse.MakeDB(cur)

def DeployRandomDB(cur : sqlite3.Cursor):
    DeployDB(cur)
    UserDataBse.MakeDumbyData(cur)
    GatwickPlanesDataBse.MakeDumbyData(cur, 2000)
    UserDataBse.MakeDumbyData(cur)
    

def main():
    cur = con.cursor()
    DeployRandomDB(cur)
    con.close()
    
if __name__ == "__main__":
    main()

