
import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"
SQL_DIR = BASE_DIR / "sql"

# Load the SQL-ready sales dataset
sales = pd.read_csv(
    REPORT_DIR / "sales_sql_ready.csv",
    parse_dates=["order_purchase_timestamp"]
)

# Create a SQLite database in the project folder
SQL_DIR.mkdir(exist_ok=True)
db_path = SQL_DIR / "ecommerce.db"

with sqlite3.connect(db_path) as conn:
    sales.to_sql(
        "sales",
        conn,
        if_exists="replace",
        index=False
    )

    row_count = pd.read_sql_query(
        "SELECT COUNT(*) AS total_rows FROM sales",
        conn
    )

    print("--- SQLITE DATABASE VALIDATION ---")
    print(row_count)
    print(
        "Unique orders:",
        pd.read_sql_query(
            "SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales",
            conn
        ).iloc[0, 0]
    )

print(f"\nDatabase saved to: {db_path}")
