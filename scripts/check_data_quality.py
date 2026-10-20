from pathlib import Path
import sqlite3

script_directory = Path(__file__).resolve().parent.parent
database_path = script_directory/ "data"/ "raw" / "northwind.db"
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

print("---------------------- Table: Order Details --------------------------")
cursor.execute("SELECT COUNT(*) FROM (SELECT OrderID, ProductID FROM [Order Details] GROUP BY OrderID, ProductID HAVING COUNT(*)>1);")
composite_key_duplicates = cursor.fetchone()[0]
print(f"Composite key duplicates: {composite_key_duplicates}")

print("---------------------- Table: Orders --------------------------")
cursor.execute("SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NULL")
missing_shipped_dates = cursor.fetchone()[0]
print(f"Missing shipped dates: {missing_shipped_dates}")
cursor.execute("SELECT COUNT(*) FROM Orders WHERE OrderDate > RequiredDate OR (ShippedDate IS NOT NULL AND OrderDate > ShippedDate)")
invalid_dates = cursor.fetchone()[0]
print(f"Invalid dates: {invalid_dates}")
cursor.execute("SELECT COUNT(*) FROM (SELECT OrderID From Orders GROUP BY OrderID HAVING COUNT(*)>1)")
duplicate_ids = cursor.fetchone()[0]
print(f"Duplicate ids: {duplicate_ids}")
cursor.execute("SELECT COUNT(*) FROM Orders WHERE Freight < 0")
negative_freight = cursor.fetchone()[0]
print(f"Negative freight: {negative_freight}")

