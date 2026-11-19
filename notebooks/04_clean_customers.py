
import pandas as pd
from pathlib import Path

# Set project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load customer data
customers = pd.read_csv(DATA_DIR / "olist_customers_dataset.csv")

print("--- CUSTOMER DATA VALIDATION ---")
print("Rows and columns:", customers.shape)
print("\nMissing values:\n", customers.isnull().sum())
print("\nDuplicate rows:", customers.duplicated().sum())

print("\nDuplicate customer IDs:",
      customers["customer_id"].duplicated().sum())

print("\nDuplicate customer unique IDs:",
      customers["customer_unique_id"].duplicated().sum())

print("\nUnique customer states:")
print(customers["customer_state"].nunique())

print("\nTop 10 states by customer records:")
print(customers["customer_state"].value_counts().head(10))

# Save a copy without deleting any records
REPORT_DIR.mkdir(exist_ok=True)
customers.to_csv(DATA_DIR / "customers_cleaned.csv", index=False)

print("\nCleaned customers saved to data/customers_cleaned.csv")
