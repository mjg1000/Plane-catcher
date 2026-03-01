from database.database_app import get_db
from database import UserDataBse
from database import GatwickPlanesDataBse
from database import InventoryDataBse
from database import QuestDataBse  # New Import

conn = get_db()
cur = conn.cursor()

# 1️⃣ Drop existing tables if they exist
cur.execute("DROP TABLE IF EXISTS Users")
cur.execute("DROP TABLE IF EXISTS Planes")
cur.execute("DROP TABLE IF EXISTS Inventory")
cur.execute("DROP TABLE IF EXISTS Quest") # Drop new Quest table

# 2️⃣ Re-create tables
UserDataBse.MakeDB(cur)
GatwickPlanesDataBse.MakeDB(cur)
InventoryDataBse.MakeDB(cur)
QuestDataBse.MakeDB(cur) # Create Quest table

# 3️⃣ Populate with real and dummy data
UserDataBse.MakeDumbyData(cur)

# Use the new JSON loader for Planes instead of random dummy data
# This uses your FlightDataComp folder information
GatwickPlanesDataBse.LoadFlightData(cur)

# Populate Quests
QuestDataBse.MakeDumbyData(cur, 3)

conn.commit()

# 4️⃣ Verify
cur.execute('SELECT * FROM Planes')
rows = cur.fetchall()
print(f"Planes in DB: {len(rows)}")

cur.execute('SELECT * FROM Quest')
quest_rows = cur.fetchall()
print(f"Quests in DB: {len(quest_rows)}")

print("Database successfully initialized with Quest and JSON Plane data.")

# 5️⃣ Close connection
conn.close()