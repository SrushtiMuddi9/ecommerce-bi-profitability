
import pandas as pd
from pathlib import Path

# Set project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load orders
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")

# Convert date columns
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Investigate delivered orders with missing delivery dates
problem_orders = orders[
    (orders["order_status"] == "delivered")
    & (orders["order_delivered_customer_date"].isna())
]

print("Total orders:", len(orders))
print("Delivered orders missing delivery dates:", len(problem_orders))
print("\nProblem orders:")
print(problem_orders[
    ["order_id", "order_status",
     "order_purchase_timestamp",
     "order_delivered_carrier_date",
     "order_delivered_customer_date"]
].to_string(index=False))

# Save a cleaned copy; preserve missing dates for investigation
REPORT_DIR.mkdir(exist_ok=True)
orders.to_csv(DATA_DIR / "orders_cleaned.csv", index=False)

print("\nCleaned orders saved to data/orders_cleaned.csv")



# Validate the cleaned file
cleaned_orders = pd.read_csv(DATA_DIR / "orders_cleaned.csv")

print("\n--- CLEANED DATA VALIDATION ---")
print("Total rows:", len(cleaned_orders))
print("Duplicate order IDs:", cleaned_orders["order_id"].duplicated().sum())
print("Missing order IDs:", cleaned_orders["order_id"].isna().sum())
print(
    "Delivered orders missing delivery date:",
    (
        (cleaned_orders["order_status"] == "delivered")
        & cleaned_orders["order_delivered_customer_date"].isna()
    ).sum()
)
print("Cleaned file exists:", (DATA_DIR / "orders_cleaned.csv").exists())
