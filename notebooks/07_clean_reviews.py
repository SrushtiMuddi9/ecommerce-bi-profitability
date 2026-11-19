
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"

# Load review data
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")

print("--- REVIEW DATA VALIDATION ---")
print("Rows and columns:", reviews.shape)
print("\nMissing values:\n", reviews.isnull().sum())
print("\nDuplicate rows:", reviews.duplicated().sum())

print("\nReview score distribution:")
print(reviews["review_score"].value_counts().sort_index())

print("\nReview score validation:")
print("Missing scores:", reviews["review_score"].isna().sum())
print("Scores outside 1-5:",
      (~reviews["review_score"].between(1, 5)).sum())

print("\nDuplicate review IDs:",
      reviews["review_id"].duplicated().sum())

# Save without deleting records
REPORT_DIR.mkdir(exist_ok=True)
reviews.to_csv(DATA_DIR / "reviews_cleaned.csv", index=False)

print("\nCleaned reviews saved to data/reviews_cleaned.csv")



# Investigate duplicate review IDs
duplicate_reviews = reviews[
    reviews.duplicated(subset=["review_id"], keep=False)
].sort_values("review_id")

print("\n--- DUPLICATE REVIEW ID INVESTIGATION ---")
print("Rows involved in duplicate IDs:", len(duplicate_reviews))

print(
    duplicate_reviews[
        ["review_id", "order_id", "review_score",
         "review_comment_title", "review_creation_date"]
    ].head(20).to_string(index=False)
)

print("\nDuplicate review IDs linked to multiple orders:")
print(
    duplicate_reviews.groupby("review_id")["order_id"]
    .nunique()
    .gt(1)
    .sum()
)



# Create an order-level review summary
order_reviews = (
    reviews.groupby("order_id", as_index=False)
    .agg(
        review_count=("review_id", "count"),
        average_review_score=("review_score", "mean")
    )
)

print("\n--- ORDER-LEVEL REVIEW SUMMARY ---")
print("Orders with reviews:", len(order_reviews))
print("Duplicate order IDs:", order_reviews["order_id"].duplicated().sum())
print("Average review score:", round(order_reviews["average_review_score"].mean(), 2))

# Save the summary separately
order_reviews.to_csv(
    REPORT_DIR / "order_review_summary.csv",
    index=False
)

print("Review summary saved to reports/order_review_summary.csv")
