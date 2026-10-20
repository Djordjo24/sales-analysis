from pathlib import Path
import sqlite3

script_directory = Path(__file__).resolve().parent.parent
database_path = script_directory/ "data"/ "raw" / "northwind.db"
conn = sqlite3.connect(database_path)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

if not tables:
    print("The database is empty!")
else:
    cursor.execute("PRAGMA foreign_key_check;")
    foreign_key_violations = cursor.fetchall()
    print(f"Foreign key integrity check: {foreign_key_violations}")
    for table in tables:
        table_name = table[0]
        print(f"----------------------------TABLE: {table_name}------------------------------------")

        cursor.execute(f"PRAGMA table_info([{table_name}]);")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        print(f"Table name: {table_name} --- Column name: {column_names}")
        for col in columns:
            print(f"Data types: {col[1]} --- {col[2]}")

        for col_name in column_names:
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}" WHERE "{col_name}" IS NULL;')
            null_count = cursor.fetchone()[0]
            print(f"{col_name} column have {null_count} null values")

        primary_keys = [col[1] for col in columns if col[5] > 0]
        print(f"Primary key: {primary_keys}")

        cursor.execute(f"PRAGMA foreign_key_list([{table_name}]);")
        foreign_keys = cursor.fetchall()
        for fk in foreign_keys:
            child_table = table_name
            child_column = fk[3]
            parent_table = fk[2]
            parent_column = fk[4]
            print(f"Table relationship: {child_table}.{child_column} -> {parent_table}.{parent_column}")
        

        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}";')
        row_count = cursor.fetchone()[0]
        print(f"The {table_name} table has {row_count} rows.")
        if row_count == 0:
            print(f"Empty table: {table_name}")


        if table_name == "Orders":
            cursor.execute("SELECT MIN(OrderDate), MAX(OrderDate) FROM Orders")
            first_order_date, last_order_date = cursor.fetchone()
            print(f"First order date: {first_order_date}")
            print(f"Last order date: {last_order_date}")
        
conn.close()