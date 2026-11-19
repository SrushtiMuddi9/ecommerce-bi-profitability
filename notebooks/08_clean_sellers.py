
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load seller data
sellers = pd.read_csv(DATA_DIR / "olist_sellers_dataset.csv")

print("--- SELLER DATA VALIDATION ---")
print("Rows and columns:", sellers.shape)
print("\nMissing values:\n", sellers.isnull().sum())
print("\nDuplicate rows:", sellers.duplicated().sum())
print("\nDuplicate seller IDs:",
      sellers["seller_id"].duplicated().sum())

print("\nUnique seller states:", sellers["seller_state"].nunique())

print("\nTop 10 seller states:")
print(sellers["seller_state"].value_counts().head(10))

# Save a copy without deleting records
REPORT_DIR.mkdir(exist_ok=True)
sellers.to_csv(DATA_DIR / "sellers_cleaned.csv", index=False)

print("\nCleaned sellers saved to data/sellers_cleaned.csv")
