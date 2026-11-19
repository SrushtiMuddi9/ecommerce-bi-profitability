
import pandas as pd
from pathlib import Path

# Location of our dataset
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# CSV files to inspect
files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_sellers_dataset.csv",
]

for file in files:
    df = pd.read_csv(DATA_DIR / file)

    print("\n" + "=" * 50)
    print("FILE:", file)
    print("Rows and columns:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())

import pandas as pd
from pathlib import Path

# Location of our dataset
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# CSV files to inspect
files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_products_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_sellers_dataset.csv",
]

for file in files:
    df = pd.read_csv(DATA_DIR / file)

    print("\n" + "=" * 50)
    print("FILE:", file)
    print("Rows and columns:", df.shape)
    print("\nMissing values:")
    print(df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())

    
# Investigate order statuses and missing delivery dates

orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")

print("\nORDER STATUS COUNTS")
print(orders["order_status"].value_counts(dropna=False))

print("\nMISSING DELIVERY DATES BY ORDER STATUS")
print(
    orders.groupby("order_status")[
        [
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
        ]
    ]
    .apply(lambda group: group.isnull().sum())
)



# Create an order status quality report

status_report = orders.groupby("order_status").agg(
    total_orders=("order_id", "count"),
    missing_approval=("order_approved_at", lambda x: x.isnull().sum()),
    missing_carrier_date=(
        "order_delivered_carrier_date",
        lambda x: x.isnull().sum()
    ),
    missing_delivery_date=(
        "order_delivered_customer_date",
        lambda x: x.isnull().sum()
    )
).reset_index()

print("\nORDER DATA QUALITY REPORT")
print(status_report)

# Save the report
report_dir = DATA_DIR.parent / "reports"
report_dir.mkdir(exist_ok=True)

status_report.to_csv(
    report_dir / "order_data_quality_report.csv",
    index=False
)



# Create an order status quality report

status_report = orders.groupby("order_status").agg(
    total_orders=("order_id", "count"),
    missing_approval=("order_approved_at", lambda x: x.isnull().sum()),
    missing_carrier_date=(
        "order_delivered_carrier_date",
        lambda x: x.isnull().sum()
    ),
    missing_delivery_date=(
        "order_delivered_customer_date",
        lambda x: x.isnull().sum()
    )
).reset_index()

print("\nORDER DATA QUALITY REPORT")
print(status_report)

# Save the report
report_dir = DATA_DIR.parent / "reports"
report_dir.mkdir(exist_ok=True)

status_report.to_csv(
    report_dir / "order_data_quality_report.csv",
    index=False
)

print("\nQuality report saved successfully!")

