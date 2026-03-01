from database.database_app import get_db
from database import UserDataBse
from database import GatwickPlanesDataBse
from database import InventoryDataBse

conn = get_db()
cur = conn.cursor()
# Use your existing logic from Database.py
UserDataBse.MakeDB(cur)
GatwickPlanesDataBse.MakeDB(cur)
InventoryDataBse.MakeDB(cur)
UserDataBse.MakeDumbyData(cur)
GatwickPlanesDataBse.MakeDumbyData(cur, 50)
# InventoryDataBse.MakeDumbyInventory(cur)
conn.commit()


cur.execute('select * from Planes')

# 4. See the outputs (Fetch all rows)
rows = cur.fetchall()
print(len(rows))
# for row in rows:
#     print(dict(row))
print("done")
# 5. Close the connection when finished
conn.close()