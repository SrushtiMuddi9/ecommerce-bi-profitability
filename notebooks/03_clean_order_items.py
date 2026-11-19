
import pandas as pd
from pathlib import Path

# Set project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load order items
items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

print("--- BEFORE CLEANING ---")
print("Rows and columns:", items.shape)
print("Missing values:\n", items.isnull().sum())
print("Duplicate rows:", items.duplicated().sum())
print("Duplicate order-item pairs:",
      items.duplicated(subset=["order_id", "order_item_id"]).sum())

# Validate numeric columns
items["price"] = pd.to_numeric(items["price"], errors="coerce")
items["freight_value"] = pd.to_numeric(
    items["freight_value"], errors="coerce"
)

print("\n--- PRICE VALIDATION ---")
print("Missing prices:", items["price"].isna().sum())
print("Prices <= 0:", (items["price"] <= 0).sum())
print("Missing freight values:", items["freight_value"].isna().sum())
print("Freight values < 0:", (items["freight_value"] < 0).sum())

# Save cleaned copy without deleting records
REPORT_DIR.mkdir(exist_ok=True)
items.to_csv(DATA_DIR / "order_items_cleaned.csv", index=False)

print("\nCleaned order items saved to data/order_items_cleaned.csv")
