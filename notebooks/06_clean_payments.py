
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load payment data
payments = pd.read_csv(DATA_DIR / "olist_order_payments_dataset.csv")

print("--- PAYMENT DATA VALIDATION ---")
print("Rows and columns:", payments.shape)
print("\nMissing values:\n", payments.isnull().sum())
print("\nDuplicate rows:", payments.duplicated().sum())

print("\nPayment types:")
print(payments["payment_type"].value_counts(dropna=False))

print("\nPayment value validation:")
print("Missing payment values:", payments["payment_value"].isna().sum())
print("Payment values <= 0:", (payments["payment_value"] <= 0).sum())

print("\nInstallment validation:")
print("Missing installments:", payments["payment_installments"].isna().sum())
print("Installments <= 0:", (payments["payment_installments"] <= 0).sum())

# Save a copy without deleting records
REPORT_DIR.mkdir(exist_ok=True)
payments.to_csv(DATA_DIR / "payments_cleaned.csv", index=False)

print("\nCleaned payments saved to data/payments_cleaned.csv")
