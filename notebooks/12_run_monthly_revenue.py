
import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sql" / "ecommerce.db"
QUERY_PATH = BASE_DIR / "sql" / "05_review_analysis.sql"

query = QUERY_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    result = pd.read_sql_query(query, conn)

print(result.to_string(index=False))

