from pathlib import Path
import sqlite3

script_directory = Path(__file__).resolve().parent.parent
database_path = script_directory/ "data"/ "raw" / "northwind.db"
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

print("---------------------- Table: Order Details --------------------------")
order_details_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT OrderID, ProductID FROM [Order Details] GROUP BY OrderID, ProductID HAVING COUNT(*)>1);")
composite_key_duplicates = cursor.fetchone()[0]
order_details_quality_report.append({
    "Check": "Composite key duplicates",
    "Result": composite_key_duplicates,
    "Status": "OK" if composite_key_duplicates == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM [Order Details] WHERE UnitPrice <= 0 OR Quantity <= 0")
invalid_price_or_quantity = cursor.fetchone()[0]
order_details_quality_report.append({
    "Check": "Invalid price or quantity",
    "Result": invalid_price_or_quantity,
    "Status": "OK" if invalid_price_or_quantity == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM [Order Details] WHERE Discount < 0 OR Discount > 1")
invalid_discount = cursor.fetchone()[0]
order_details_quality_report.append({
    "Check": "Invalid discount",
    "Result": invalid_discount,
    "Status": "OK" if invalid_discount == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM [Order Details] WHERE typeof(UnitPrice) != "real" AND typeof(UnitPrice) != "integer"')
invalid_data_type_unit_price = cursor.fetchone()[0]
order_details_quality_report.append({
    "Check": "Invalid data type unit price",
    "Result": invalid_data_type_unit_price,
    "Status": "OK" if invalid_data_type_unit_price == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM [Order Details] WHERE typeof(Quantity) != "real" AND typeof(Quantity) != "integer"')
invalid_data_type_quantity = cursor.fetchone()[0]
order_details_quality_report.append({
    "Check": "Invalid data type quantity",
    "Result": invalid_data_type_quantity,
    "Status": "OK" if invalid_data_type_quantity == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM [Order Details] WHERE typeof(Discount) != "real" AND typeof(Discount) != "integer"')
invalid_data_type_discount = cursor.fetchone()[0]
order_details_quality_report.append({
    "Check": "Invalid data type discount",
    "Result": invalid_data_type_discount,
    "Status": "OK" if invalid_data_type_discount == 0 else "WARNING"
})

for obj in order_details_quality_report: 
    print("//////----------------------//////")
    for key, value in obj.items():
        print(f"{key}: {value}")



print("---------------------- Table: Orders --------------------------")
orders_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT OrderID From Orders GROUP BY OrderID HAVING COUNT(*)>1)")
duplicate_order_ids = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Duplicate Ids",
    "Result": duplicate_order_ids,
    "Status": "OK" if duplicate_order_ids == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NULL")
missing_shipped_dates = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Missing shipped dates",
    "Result": missing_shipped_dates,
    "Status": "OK" if missing_shipped_dates == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Orders WHERE OrderDate > RequiredDate OR (ShippedDate IS NOT NULL AND OrderDate > ShippedDate)")
invalid_dates = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Invalid dates",
    "Result": invalid_dates,
    "Status": "OK" if invalid_dates == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Orders WHERE Freight < 0")
negative_freight = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Negative freight",
    "Result": negative_freight,
    "Status": "OK" if negative_freight == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE typeof(Freight) != "real" AND typeof(Freight) != "integer"')
invalid_data_type_freight = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Invalid data type freight",
    "Result": invalid_data_type_freight,
    "Status": "OK" if invalid_data_type_freight == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE typeof(OrderDate) != "text" OR datetime(OrderDate) IS NULL')
invalid_data_type_order_date = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Invalid data type order date",
    "Result": invalid_data_type_order_date,
    "Status": "OK" if invalid_data_type_order_date == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE typeof(RequiredDate) != "text" OR datetime(RequiredDate) IS NULL')
invalid_data_type_required_date = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Invalid data type required date",
    "Result": invalid_data_type_required_date,
    "Status": "OK" if invalid_data_type_required_date == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NOT NULL AND (typeof(ShippedDate) != "text" OR datetime(ShippedDate) IS NULL)')
invalid_data_type_shipped_date = cursor.fetchone()[0]
orders_quality_report.append({
    "Check": "Invalid data type shipped date",
    "Result": invalid_data_type_shipped_date,
    "Status": "OK" if invalid_data_type_shipped_date == 0 else "WARNING"
})

for obj in orders_quality_report:
    print("//////-----------------//////////")
    for key, value in obj.items():
        print(f"{key}: {value}")


print("---------------------- Table: Products --------------------------")
products_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT ProductID From Products GROUP BY ProductID HAVING COUNT(*)>1)")
duplicate_product_ids = cursor.fetchone()[0]
products_quality_report.append({
    "Check": "Duplicate Ids",
    "Result": duplicate_product_ids,
    "Status": "OK" if duplicate_product_ids == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Products WHERE UnitPrice < 0")
invalid_price = cursor.fetchone()[0]
products_quality_report.append({
    "Check": "Invalid price",
    "Result": invalid_price,
    "Status": "OK" if invalid_price == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Products WHERE UnitsInStock < 0 OR UnitsOnOrder < 0 OR ReorderLevel < 0")
invalid_stock_order_and_reorder_level = cursor.fetchone()[0]
products_quality_report.append({
    "Check": "Invalid units in stock, units in order or reorder level",
    "Result": invalid_stock_order_and_reorder_level,
    "Status": "OK" if invalid_stock_order_and_reorder_level == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Products WHERE typeof(UnitPrice) != "real" AND typeof(UnitPrice) != "integer"')
invalid_data_type_unit_price = cursor.fetchone()[0]
products_quality_report.append({
    "Check": "Invalid data type unit price",
    "Result": invalid_data_type_unit_price,
    "Status": "OK" if invalid_data_type_unit_price == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Products WHERE TRIM(ProductName) == "" OR TRIM(QuantityPerUnit) == ""')
invalid_name_or_quantity = cursor.fetchone()[0]
products_quality_report.append({
    "Check": "Invalid product name or quantity per unit",
    "Result": invalid_name_or_quantity,
    "Status": "OK" if invalid_name_or_quantity == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Products WHERE Discontinued != "0" AND Discontinued != "1"')
invalid_discontinued = cursor.fetchone()[0]
products_quality_report.append({
    "Check": "Invalid discontinued",
    "Result": invalid_discontinued,
    "Status": "OK" if invalid_discontinued == 0 else "WARNING"
})

for obj in products_quality_report:
    print("//////////--------------------///////////")
    for key, value in obj.items():
        print(f"{key}: {value}")

