from database.database_app import get_db
from database import UserDataBse
from database import GatwickPlanesDataBse
from database import InventoryDataBse

conn = get_db()
cur = conn.cursor()

# 1️⃣ Drop existing tables if they exist
cur.execute("DROP TABLE IF EXISTS Users")
cur.execute("DROP TABLE IF EXISTS Planes")
cur.execute("DROP TABLE IF EXISTS Inventory")

# 2️⃣ Re-create tables
UserDataBse.MakeDB(cur)
GatwickPlanesDataBse.MakeDB(cur)
InventoryDataBse.MakeDB(cur)

# 3️⃣ Populate with dummy data
UserDataBse.MakeDumbyData(cur)
GatwickPlanesDataBse.MakeDumbyData(cur, 50)
# InventoryDataBse.MakeDumbyInventory(cur)  # optional

conn.commit()

# 4️⃣ Verify
cur.execute('SELECT * FROM Planes')
rows = cur.fetchall()
print(f"Planes in DB: {len(rows)}")
# for row in rows:
#     print(dict(row))
print("done")

# 5️⃣ Close connection
conn.close()