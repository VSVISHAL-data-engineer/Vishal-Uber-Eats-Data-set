# ============================================================
#  Uber Eats Bangalore - Database Setup
#  File: database_setup.py
# ============================================================

import pandas as pd
import sqlite3
import json

# ─────────────────────────────────────────
# STEP 1: Connect to SQLite database
# ─────────────────────────────────────────
print("STEP 1: Creating database...")

conn = sqlite3.connect("ubereats.db")
print("✅ Database 'ubereats.db' created!")

# ─────────────────────────────────────────
# STEP 2: Load cleaned CSV → Database
# ─────────────────────────────────────────
print("\nSTEP 2: Loading restaurants into database...")

df = pd.read_csv("uber_eats_cleaned.csv")
df.to_sql("restaurants", conn, if_exists="replace", index=False)
print(f"✅ {len(df)} restaurants saved to database!")

# ─────────────────────────────────────────
# STEP 3: Load orders JSON → Database
# ─────────────────────────────────────────
print("\nSTEP 3: Loading orders into database...")

with open("orders.json", "r", encoding="utf-8") as f:
    orders_data = json.load(f)

orders_df = pd.DataFrame(orders_data)
orders_df.to_sql("orders", conn, if_exists="replace", index=False)
print(f"✅ {len(orders_df)} orders saved to database!")

# ─────────────────────────────────────────
# STEP 4: Test - Read from database
# ─────────────────────────────────────────
print("\nSTEP 4: Testing database...")

test = pd.read_sql("SELECT name, location, rate, price_segment FROM restaurants LIMIT 5", conn)
print("✅ Sample data from database:")
print(test.to_string(index=False))

conn.close()
print("\n🎉 Database Setup Complete! Next: sql_queries.py")