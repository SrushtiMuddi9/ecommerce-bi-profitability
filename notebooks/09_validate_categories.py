
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load category translation data
categories = pd.read_csv(
    DATA_DIR / "product_category_name_translation.csv"
)

print("--- CATEGORY TRANSLATION VALIDATION ---")
print("Rows and columns:", categories.shape)
print("\nMissing values:\n", categories.isnull().sum())
print("\nDuplicate rows:", categories.duplicated().sum())

print(
    "\nDuplicate Portuguese category names:",
    categories["product_category_name"].duplicated().sum()
)

print(
    "\nDuplicate English category names:",
    categories["product_category_name_english"].duplicated().sum()
)

print("\nSample translations:")
print(categories.head(10).to_string(index=False))

# Save validated lookup
REPORT_DIR.mkdir(exist_ok=True)
categories.to_csv(
    DATA_DIR / "categories_cleaned.csv",
    index=False
)

print("\nCleaned categories saved to data/categories_cleaned.csv")
