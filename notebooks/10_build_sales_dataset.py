
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load cleaned datasets
orders = pd.read_csv(DATA_DIR / "orders_cleaned.csv")
items = pd.read_csv(DATA_DIR / "order_items_cleaned.csv")
products = pd.read_csv(DATA_DIR / "products_cleaned.csv")
sellers = pd.read_csv(DATA_DIR / "sellers_cleaned.csv")
categories = pd.read_csv(DATA_DIR / "categories_cleaned.csv")

# Keep only required order columns
orders = orders[
    [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
]

# Join order items to orders
sales = items.merge(
    orders,
    on="order_id",
    how="left",
    validate="many_to_one"
)

# Join products
sales = sales.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left",
    validate="many_to_one"
)

# Translate category names to English
sales = sales.merge(
    categories,
    on="product_category_name",
    how="left",
    validate="many_to_one"
)

# Add seller location
sales = sales.merge(
    sellers[["seller_id", "seller_state", "seller_city"]],
    on="seller_id",
    how="left",
    validate="many_to_one"
)

# Create sales metrics
sales["item_revenue"] = sales["price"]
sales["freight_value"] = pd.to_numeric(
    sales["freight_value"], errors="coerce"
)
sales["total_item_plus_freight"] = (
    sales["item_revenue"] + sales["freight_value"]
)

print("--- SALES DATASET VALIDATION ---")
print("Rows and columns:", sales.shape)
print("Unique orders:", sales["order_id"].nunique())
print("Unique products:", sales["product_id"].nunique())
print("Missing order IDs:", sales["order_id"].isna().sum())
print("Missing product IDs:", sales["product_id"].isna().sum())
print("Missing seller states:", sales["seller_state"].isna().sum())

print("\nOrder status distribution:")
print(sales["order_status"].value_counts(dropna=False))

print("\nRevenue summary:")
print("Item revenue:", round(sales["item_revenue"].sum(), 2))
print("Freight value:", round(sales["freight_value"].sum(), 2))
print(
    "Item revenue + freight:",
    round(sales["total_item_plus_freight"].sum(), 2)
)

# Save the analysis-ready dataset
REPORT_DIR.mkdir(exist_ok=True)
sales.to_csv(REPORT_DIR / "sales_analysis_dataset.csv", index=False)

print("\nSales dataset saved to reports/sales_analysis_dataset.csv")



# Additional validation checks
original_items = pd.read_csv(DATA_DIR / "order_items_cleaned.csv")

print("\n--- FINAL SALES DATA QUALITY CHECKS ---")
print("Original order-item rows:", len(original_items))
print("Sales dataset rows:", len(sales))
print("Row count preserved:", len(original_items) == len(sales))

print(
    "Missing English categories:",
    sales["product_category_name_english"].isna().sum()
)

print(
    "Missing customer IDs:",
    sales["customer_id"].isna().sum()
)

print(
    "Negative item revenue:",
    (sales["item_revenue"] < 0).sum()
)

print(
    "Negative freight values:",
    (sales["freight_value"] < 0).sum()
)

# Check whether each order-item pair is unique
print(
    "Duplicate order-item pairs:",
    sales.duplicated(subset=["order_id", "order_item_id"]).sum()
)



# Create a SQL-ready copy
sql_sales = sales.copy()

# Fill missing category labels, preserving all sales rows
sql_sales["product_category_name_english"] = (
    sql_sales["product_category_name_english"].fillna("unknown")
)

# Convert date fields to consistent datetime values
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_columns:
    sql_sales[col] = pd.to_datetime(sql_sales[col], errors="coerce")

# Save the final dataset
sql_sales.to_csv(
    REPORT_DIR / "sales_sql_ready.csv",
    index=False
)

print("\n--- SQL-READY DATASET ---")
print("Rows:", len(sql_sales))
print(
    "Missing category labels:",
    sql_sales["product_category_name_english"].isna().sum()
)
print(
    "Unknown category rows:",
    (sql_sales["product_category_name_english"] == "unknown").sum()
)
print("Saved to reports/sales_sql_ready.csv")
