
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load product data
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

print("--- PRODUCT DATA VALIDATION ---")
print("Rows and columns:", products.shape)
print("\nMissing values:\n", products.isnull().sum())
print("\nDuplicate rows:", products.duplicated().sum())
print("\nDuplicate product IDs:",
      products["product_id"].duplicated().sum())

# Check missing categories
print("\nMissing product categories:",
      products["product_category_name"].isnull().sum())

# Check product dimensions and weight
numeric_columns = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]

for col in numeric_columns:
    products[col] = pd.to_numeric(products[col], errors="coerce")

print("\nInvalid or missing product measurements:")
for col in numeric_columns:
    print(f"{col}: {(products[col].isna() | (products[col] <= 0)).sum()}")

# Save without deleting records or inventing values
REPORT_DIR.mkdir(exist_ok=True)
products.to_csv(DATA_DIR / "products_cleaned.csv", index=False)

print("\nCleaned products saved to data/products_cleaned.csv")
