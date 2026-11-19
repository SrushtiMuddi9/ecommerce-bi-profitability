
import pandas as pd
from pathlib import Path

# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"
CLEANED_DIR = PROJECT_DIR / "cleaned"

CLEANED_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD DATASETS
# ==========================================

print("\n========== LOADING DATASETS ==========")

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")

order_items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")

products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

print("Orders:", len(orders))
print("Order Items:", len(order_items))
print("Products:", len(products))

# ==========================================
# 3. CLEAN ORDER DATA
# ==========================================

print("\n========== CLEANING ORDER DATA ==========")

# Keep missing delivery dates empty.
# They may represent orders that were not delivered.

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column], errors="coerce"
    )

print("Missing delivery dates retained.")

# ==========================================
# 4. CLEAN PRODUCT DATA
# ==========================================

print("\n========== CLEANING PRODUCT DATA ==========")

products["product_category_name"] = (
    products["product_category_name"].fillna("Unknown")
)

print(
    "Missing product categories:",
    products["product_category_name"].eq("Unknown").sum()
)

# ==========================================
# 5. CREATE SALES DATASET
# ==========================================

print("\n========== CREATING SALES DATASET ==========")

sales = order_items.merge(
    orders,
    on="order_id",
    how="left"
)

sales = sales.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

sales["product_category_name"] = (
    sales["product_category_name"].fillna("Unknown")
)

sales["total_item_value"] = (
    sales["price"] + sales["freight_value"]
)

sales.to_csv(
    CLEANED_DIR / "sales_powerbi.csv",
    index=False
)

# ==========================================
# 6. CREATE ORDER SUMMARY DATASET
# ==========================================

print("\n========== CREATING ORDER SUMMARY ==========")

order_summary = sales.groupby(
    "order_id",
    as_index=False
).agg(
    item_revenue=("price", "sum"),
    freight_value=("freight_value", "sum"),
    total_order_value=("total_item_value", "sum"),
    total_items=("order_item_id", "count"),
    product_categories=("product_category_name", "nunique")
)

order_summary = order_summary.merge(
    orders,
    on="order_id",
    how="left"
)

order_summary.to_csv(
    CLEANED_DIR / "order_summary_powerbi.csv",
    index=False
)

# ==========================================
# 7. VALIDATION REPORT
# ==========================================

print("\n========== TRANSFORMATION VALIDATION ==========")

print("Sales dataset rows:", len(sales))
print("Unique sales orders:", sales["order_id"].nunique())

print("Order summary rows:", len(order_summary))
print("Unique summary orders:", order_summary["order_id"].nunique())

print(
    "Sales item revenue:",
    round(sales["price"].sum(), 2)
)

print(
    "Sales freight:",
    round(sales["freight_value"].sum(), 2)
)

print(
    "Sales total value:",
    round(sales["total_item_value"].sum(), 2)
)

print("\n========== OUTPUT FILES ==========")

print(CLEANED_DIR / "sales_powerbi.csv")
print(CLEANED_DIR / "order_summary_powerbi.csv")

print("\nTRANSFORMATION COMPLETED SUCCESSFULLY!")
