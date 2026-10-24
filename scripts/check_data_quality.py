from pathlib import Path
import sqlite3
import pandas as pd

script_directory = Path(__file__).resolve().parent.parent
database_path = script_directory/ "data"/ "raw" / "northwind.db"
csv_path = script_directory / "data" / "processed"

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# ---- Table: Order Details ------
order_details_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT OrderID, ProductID FROM [Order Details] GROUP BY OrderID, ProductID HAVING COUNT(*)>1);")
composite_key_duplicates = cursor.fetchone()[0]
order_details_quality_report.append({
    "Table": "Order Details",
    "Check": "Composite key duplicates",
    "Result": composite_key_duplicates,
    "Status": "OK" if composite_key_duplicates == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM [Order Details] WHERE UnitPrice <= 0 OR Quantity <= 0")
invalid_price_or_quantity = cursor.fetchone()[0]
order_details_quality_report.append({
    "Table": "Order Details",
    "Check": "Invalid price or quantity",
    "Result": invalid_price_or_quantity,
    "Status": "OK" if invalid_price_or_quantity == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM [Order Details] WHERE Discount < 0 OR Discount > 1")
invalid_discount = cursor.fetchone()[0]
order_details_quality_report.append({
    "Table": "Order Details",
    "Check": "Invalid discount",
    "Result": invalid_discount,
    "Status": "OK" if invalid_discount == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM [Order Details] WHERE typeof(UnitPrice) != "real" AND typeof(UnitPrice) != "integer"')
invalid_data_type_unit_price = cursor.fetchone()[0]
order_details_quality_report.append({
    "Table": "Order Details",
    "Check": "Invalid data type unit price",
    "Result": invalid_data_type_unit_price,
    "Status": "OK" if invalid_data_type_unit_price == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM [Order Details] WHERE typeof(Quantity) != "real" AND typeof(Quantity) != "integer"')
invalid_data_type_quantity = cursor.fetchone()[0]
order_details_quality_report.append({
    "Table": "Order Details",
    "Check": "Invalid data type quantity",
    "Result": invalid_data_type_quantity,
    "Status": "OK" if invalid_data_type_quantity == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM [Order Details] WHERE typeof(Discount) != "real" AND typeof(Discount) != "integer"')
invalid_data_type_discount = cursor.fetchone()[0]
order_details_quality_report.append({
    "Table": "Order Details",
    "Check": "Invalid data type discount",
    "Result": invalid_data_type_discount,
    "Status": "OK" if invalid_data_type_discount == 0 else "WARNING"
})


#------ Table: Orders -----
orders_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT OrderID From Orders GROUP BY OrderID HAVING COUNT(*)>1)")
duplicate_order_ids = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Duplicate Ids",
    "Result": duplicate_order_ids,
    "Status": "OK" if duplicate_order_ids == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NULL")
missing_shipped_dates = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Missing shipped dates",
    "Result": missing_shipped_dates,
    "Status": "OK" if missing_shipped_dates == 0 else "WARNING"
})


cursor.execute("SELECT COUNT(*) FROM Orders WHERE OrderDate > RequiredDate OR (ShippedDate IS NOT NULL AND OrderDate > ShippedDate)")
invalid_dates = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Invalid dates",
    "Result": invalid_dates,
    "Status": "OK" if invalid_dates == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Orders WHERE Freight < 0")
negative_freight = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Negative freight",
    "Result": negative_freight,
    "Status": "OK" if negative_freight == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE typeof(Freight) != "real" AND typeof(Freight) != "integer"')
invalid_data_type_freight = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Invalid data type freight",
    "Result": invalid_data_type_freight,
    "Status": "OK" if invalid_data_type_freight == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE typeof(OrderDate) != "text" OR datetime(OrderDate) IS NULL')
invalid_data_type_order_date = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Invalid data type order date",
    "Result": invalid_data_type_order_date,
    "Status": "OK" if invalid_data_type_order_date == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE typeof(RequiredDate) != "text" OR datetime(RequiredDate) IS NULL')
invalid_data_type_required_date = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Invalid data type required date",
    "Result": invalid_data_type_required_date,
    "Status": "OK" if invalid_data_type_required_date == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Orders WHERE ShippedDate IS NOT NULL AND (typeof(ShippedDate) != "text" OR datetime(ShippedDate) IS NULL)')
invalid_data_type_shipped_date = cursor.fetchone()[0]
orders_quality_report.append({
    "Table": "Orders",
    "Check": "Invalid data type shipped date",
    "Result": invalid_data_type_shipped_date,
    "Status": "OK" if invalid_data_type_shipped_date == 0 else "WARNING"
})


#--------- Table: Products ------
products_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT ProductID From Products GROUP BY ProductID HAVING COUNT(*)>1)")
duplicate_product_ids = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Duplicate Ids",
    "Result": duplicate_product_ids,
    "Status": "OK" if duplicate_product_ids == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM (SELECT ProductName From Products GROUP BY ProductName HAVING COUNT(*)>1)")
duplicate_product_name = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Duplicate product name",
    "Result": duplicate_product_name,
    "Status": "OK" if duplicate_product_name == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Products WHERE UnitPrice < 0")
negative_price = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Invalid price",
    "Result": negative_price,
    "Status": "OK" if negative_price == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Products WHERE UnitsInStock < 0 OR UnitsOnOrder < 0 OR ReorderLevel < 0")
invalid_stock_order_and_reorder_level = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Invalid units in stock, units in order or reorder level",
    "Result": invalid_stock_order_and_reorder_level,
    "Status": "OK" if invalid_stock_order_and_reorder_level == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Products WHERE typeof(UnitPrice) != "real" AND typeof(UnitPrice) != "integer"')
invalid_data_type_unit_price = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Invalid data type unit price",
    "Result": invalid_data_type_unit_price,
    "Status": "OK" if invalid_data_type_unit_price == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Products WHERE TRIM(ProductName) = "" OR TRIM(QuantityPerUnit) = ""')
empty_product_name_or_quantity = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Empty product name or quantity per unit",
    "Result": empty_product_name_or_quantity,
    "Status": "OK" if empty_product_name_or_quantity == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Products WHERE Discontinued != "0" AND Discontinued != "1"')
invalid_discontinued = cursor.fetchone()[0]
products_quality_report.append({
    "Table": "Products",
    "Check": "Invalid discontinued",
    "Result": invalid_discontinued,
    "Status": "OK" if invalid_discontinued == 0 else "WARNING"
})


#-------- Table: Categories ------
categories_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT CategoryID From Categories GROUP BY CategoryID HAVING COUNT(*)>1)")
duplicate_categories_ids = cursor.fetchone()[0]
categories_quality_report.append({
    "Table": "Categories",
    "Check": "Duplicate Ids",
    "Result": duplicate_categories_ids,
    "Status": "OK" if duplicate_categories_ids == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM (SELECT CategoryName From Categories GROUP BY CategoryName HAVING COUNT(*)>1)")
duplicate_category_name = cursor.fetchone()[0]
categories_quality_report.append({
    "Table": "Categories",
    "Check": "Duplicate category name",
    "Result": duplicate_category_name,
    "Status": "OK" if duplicate_category_name == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Categories WHERE TRIM(CategoryName) = ""')
empty_category_name = cursor.fetchone()[0]
categories_quality_report.append({
    "Table": "Categories",
    "Check": "Empty category name",
    "Result": empty_category_name,
    "Status": "OK" if empty_category_name == 0 else "WARNING"
})


#-------- Table: Customers ------
customers_quality_report = []

cursor.execute("SELECT COUNT(*) FROM (SELECT CustomerID From Customers GROUP BY CustomerID HAVING COUNT(*)>1)")
duplicate_customers_ids = cursor.fetchone()[0]
customers_quality_report.append({
    "Table": "Customers",
    "Check": "Duplicate Ids",
    "Result": duplicate_customers_ids,
    "Status": "OK" if duplicate_customers_ids == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM (SELECT CompanyName From Customers GROUP BY CompanyName HAVING COUNT(*)>1)")
duplicate_company_name = cursor.fetchone()[0]
customers_quality_report.append({
    "Table": "Customers",
    "Check": "Duplicate company name",
    "Result": duplicate_company_name,
    "Status": "OK" if duplicate_company_name == 0 else "WARNING"
})

cursor.execute('SELECT COUNT(*) FROM Customers WHERE TRIM(CompanyName) = "" OR TRIM(ContactName) = "" OR TRIM(Address) = "" OR TRIM(City) = "" OR TRIM(Country) = ""')
empty_required_fields = cursor.fetchone()[0]
customers_quality_report.append({
    "Table": "Customers",
    "Check": "Empty company name, contact name, address, city or country",
    "Result": empty_required_fields,
    "Status": "OK" if empty_required_fields == 0 else "WARNING"
})

cursor.execute("SELECT COUNT(*) FROM Customers WHERE Address IS NULL OR City IS NULL OR Region IS NULL OR Country IS NULL")
null_required_fields = cursor.fetchone()[0]
customers_quality_report.append({
    "Table": "Customers",
    "Check": "NULL address, city, region or country",
    "Result": null_required_fields,
    "Status": "OK" if null_required_fields == 0 else "WARNING"
})


data_quality_reports = []
data_quality_reports.extend(order_details_quality_report)
data_quality_reports.extend(orders_quality_report)
data_quality_reports.extend(products_quality_report)
data_quality_reports.extend(categories_quality_report)
data_quality_reports.extend(customers_quality_report)

#Export quality report to CSV file
file_name = "data_quality_reports.csv"
df = pd.DataFrame(data_quality_reports)
df.to_csv(csv_path / file_name, index=False, encoding="utf-8")
print("Data quality reports DataFrame is sucessfully exported!")


#---------------  Data Quality Investigation --------\
data_quality_investigation = []

cursor.execute("SELECT * FROM Orders WHERE ShippedDate IS NULL")
missing_shipped_date_rows = cursor.fetchall()
data_quality_investigation.append({
    "Table": "Orders",
    "Check": "Missing shipped dates rows",
    "Result": missing_shipped_date_rows
})

cursor.execute("SELECT CompanyName, COUNT(*) AS NumberOfRecords FROM Customers GROUP BY CompanyName HAVING COUNT(*)>1")
duplicated_company_name = cursor.fetchall()
data_quality_investigation.append({
    "Table": "Customers",
    "Check": "Duplicated company name",
    "Result": duplicated_company_name
})

cursor.execute('SELECT *  FROM Customers WHERE CompanyName = "IT"')
duplicate_company_name_rows = cursor.fetchall()
data_quality_investigation.append({
    "Table": "Customers",
    "Check": "Rows that have a duplicated company name",
    "Result": duplicate_company_name_rows
})

cursor.execute("SELECT * FROM Customers WHERE Address IS NULL OR City IS NULL OR Region IS NULL OR Country IS NULL")
rows_with_missing_values = cursor.fetchall()
data_quality_investigation.append({
    "Table": "Customers",
    "Check": "Rows with missing values for Address, City, Region or Country column",
    "Result": rows_with_missing_values
})

#Export quality report to CSV file
file_name = "data_quality_investigation.csv"
df = pd.DataFrame(data_quality_investigation)
df.to_csv(csv_path / file_name, index=False, encoding="utf-8")
print("Data quality investigation DataFrame is sucessfully exported!")


conn.close()