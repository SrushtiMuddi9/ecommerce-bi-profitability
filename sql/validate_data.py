
import sqlite3

connection = sqlite3.connect("ecommerce.db")
cursor = connection.cursor()

print("\n========== SALES DATA VALIDATION ==========")

# Total sales rows
cursor.execute("SELECT COUNT(*) FROM sales")
print("Total sales rows:", cursor.fetchone()[0])

# Unique orders
cursor.execute("SELECT COUNT(DISTINCT order_id) FROM sales")
print("Unique orders:", cursor.fetchone()[0])

# Unique products
cursor.execute("SELECT COUNT(DISTINCT product_id) FROM sales")
print("Unique products:", cursor.fetchone()[0])

# Revenue
cursor.execute("SELECT SUM(item_revenue) FROM sales")
print("Total item revenue:", cursor.fetchone()[0])

# Freight
cursor.execute("SELECT SUM(freight_value) FROM sales")
print("Total freight:", cursor.fetchone()[0])

# Missing values
print("\n========== MISSING VALUES ==========")

cursor.execute("PRAGMA table_info(sales)")
columns = [row[1] for row in cursor.fetchall()]

for column in columns:
    query = f'''
        SELECT COUNT(*)
        FROM sales
        WHERE "{column}" IS NULL
    '''
    cursor.execute(query)
    print(f"{column}: {cursor.fetchone()[0]}")

# Duplicate order items
print("\n========== DUPLICATE CHECK ==========")

cursor.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT order_id, order_item_id
        FROM sales
        GROUP BY order_id, order_item_id
        HAVING COUNT(*) > 1
    )
""")
print("Duplicate order-item combinations:", cursor.fetchone()[0])

# Payment rows per order
print("\n========== PAYMENT VALIDATION ==========")

cursor.execute("""
    SELECT COUNT(*),
           COUNT(DISTINCT order_id)
    FROM payments
""")
print("Payment rows and unique orders:", cursor.fetchone())

cursor.execute("""
    SELECT COUNT(*)
    FROM (
        SELECT order_id
        FROM payments
        GROUP BY order_id
        HAVING COUNT(*) > 1
    )
""")
print("Orders with multiple payment records:", cursor.fetchone()[0])

# Review rows per order
print("\n========== REVIEW VALIDATION ==========")

cursor.execute("""
    SELECT COUNT(*),
           COUNT(DISTINCT order_id)
    FROM reviews
""")
print("Review rows and unique orders:", cursor.fetchone())

# Date range
print("\n========== DATE VALIDATION ==========")

cursor.execute("""
    SELECT MIN(order_purchase_timestamp),
           MAX(order_purchase_timestamp)
    FROM sales
""")
print("Purchase date range:", cursor.fetchone())

connection.close()

print("\nData validation completed successfully.")
