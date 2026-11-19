
import sqlite3

db_path = "ecommerce.db"

connection = sqlite3.connect(db_path)
cursor = connection.cursor()

print("\n========== DATABASE TABLES ==========")

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
""")

tables = cursor.fetchall()

for (table_name,) in tables:
    print(f"\nTABLE: {table_name}")

    cursor.execute(f'PRAGMA table_info("{table_name}")')
    columns = cursor.fetchall()

    print("COLUMNS:")
    for column in columns:
        print(f" - {column[1]} ({column[2]})")

    cursor.execute(f'SELECT * FROM "{table_name}" LIMIT 3')

    print("SAMPLE RECORDS:")
    for row in cursor.fetchall():
        print(row)

connection.close()

print("\nDatabase inspection completed.")
