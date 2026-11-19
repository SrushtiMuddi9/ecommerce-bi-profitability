
import pandas as pd
import sqlite3
import logging
from pathlib import Path

# PROJECT FOLDER
BASE_DIR = Path(__file__).resolve().parent

# FILE PATHS
INPUT_FILE = BASE_DIR / "sales.csv"
OUTPUT_FILE = BASE_DIR / "cleaned_sales.csv"
DATABASE_FILE = BASE_DIR / "sales.db"
LOG_FILE = BASE_DIR / "pipeline.log"

# LOGGING CONFIGURATION
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

def run_pipeline():
    logging.info("ETL pipeline started")

    try:
        # STEP 1: EXTRACT
        data = {
            "Order_ID": [101, 102, 102, 103, 104],
            "Product": [
                "Laptop", "Mouse", "Mouse", "Keyboard", "Monitor"
            ],
            "Quantity": [2, 3, 3, None, 1],
            "Price": [50000, 500, 500, 1200, 15000]
        }

        # Create source CSV for this practice exercise
        pd.DataFrame(data).to_csv(INPUT_FILE, index=False)

        # Read source data
        df = pd.read_csv(INPUT_FILE)

        print("STEP 1: EXTRACT")
        print(df)
        print("Original rows:", len(df))

        logging.info("Source CSV extracted successfully")

        # STEP 2: TRANSFORM
        rows_before = len(df)
        df = df.drop_duplicates()
        duplicates_removed = rows_before - len(df)

        # Remove rows missing required values
        rows_before = len(df)
        df = df.dropna(
            subset=["Order_ID", "Product", "Quantity", "Price"]
        )
        missing_rows_removed = rows_before - len(df)

        # VALIDATION CHECKS
        if df["Order_ID"].isna().any():
            raise ValueError("Order_ID cannot be missing")

        if (df["Quantity"] < 0).any():
            raise ValueError("Quantity cannot be negative")

        if (df["Price"] < 0).any():
            raise ValueError("Price cannot be negative")

        df["Quantity"] = df["Quantity"].astype(int)
        df["Total_Sales"] = df["Quantity"] * df["Price"]

        print("\nSTEP 2: TRANSFORM")
        print(df)
        print("Cleaned rows:", len(df))
        print("Duplicate rows removed:", duplicates_removed)
        print("Rows with missing values removed:", missing_rows_removed)

        logging.info("Duplicates removed: %s", duplicates_removed)
        logging.info("Rows with missing values removed: %s", missing_rows_removed)
        logging.info("Data validation passed")

        # STEP 3: LOAD
        df.to_csv(OUTPUT_FILE, index=False)

        with sqlite3.connect(DATABASE_FILE) as conn:
            df.to_sql("sales", conn, if_exists="replace", index=False)

            # STEP 4: VALIDATE USING SQL
            result = pd.read_sql_query(
                """
                SELECT Product, SUM(Total_Sales) AS Revenue
                FROM sales
                GROUP BY Product
                ORDER BY Revenue DESC
                """,
                conn
            )

            database_rows = pd.read_sql_query(
                "SELECT COUNT(*) AS row_count FROM sales",
                conn
            )["row_count"].iloc[0]

        if database_rows != len(df):
            raise ValueError("CSV and database row counts do not match")

        print("\nSTEP 3: LOAD")
        print("Cleaned CSV:", OUTPUT_FILE)
        print("SQLite database:", DATABASE_FILE)

        print("\nSTEP 4: VALIDATE")
        print(result)
        print("Database rows:", database_rows)
        print("CSV and database row counts match.")

        logging.info("Cleaned CSV saved successfully")
        logging.info("SQLite database loaded successfully")
        logging.info("SQL revenue validation completed")
        logging.info("ETL pipeline completed successfully")

        print("\nPipeline completed successfully!")

    except Exception:
        logging.exception("ETL pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()
