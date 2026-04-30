# ============================================================
#  Uber Eats Bangalore - Complete Data Cleaning
# ============================================================

import pandas as pd
import numpy as np

# ─────────────────────────────────────────
# STEP 1: Load CSV
# ─────────────────────────────────────────
print("STEP 1: Loading data...")
df = pd.read_csv("Uber_Eats_data.csv")
print(f"✅ Rows loaded: {len(df)}")

# ─────────────────────────────────────────
# STEP 2: Remove duplicates
# ─────────────────────────────────────────
print("\nSTEP 2: Removing duplicates...")
before = len(df)
df = df.drop_duplicates()
print(f"✅ Removed {before - len(df)} duplicate rows")

# ─────────────────────────────────────────
# STEP 3: Fix 'rate' column (4.1/5 → 4.1)
# ─────────────────────────────────────────
print("\nSTEP 3: Fixing rate column...")

def clean_rate(value):
    if pd.isnull(value):
        return np.nan
    value = str(value).strip()
    if "/" in value:
        value = value.split("/")[0]
    try:
        return float(value)
    except:
        return np.nan  # NEW, - போன்றவை NaN ஆகும்

df["rate"] = df["rate"].apply(clean_rate)
print(f"✅ Rate column fixed!")
print(f"   Sample values: {df['rate'].dropna().unique()[:5]}")

# ─────────────────────────────────────────
# STEP 4: Fix cost column
# ─────────────────────────────────────────
print("\nSTEP 4: Fixing cost column...")

def clean_cost(value):
    if pd.isnull(value):
        return np.nan
    value = str(value).replace(",", "").strip()
    try:
        return float(value)
    except:
        return np.nan

df["cost_for_two"] = df["approx_cost(for two people)"].apply(clean_cost)
print(f"✅ Cost column fixed!")
print(f"   Sample values: {df['cost_for_two'].dropna().unique()[:5]}")

# ─────────────────────────────────────────
# STEP 5: Clean Yes/No columns
# ─────────────────────────────────────────
print("\nSTEP 5: Cleaning Yes/No columns...")
df["online_order"] = df["online_order"].str.strip().str.capitalize()
df["book_table"]   = df["book_table"].str.strip().str.capitalize()
print(f"✅ online_order values: {df['online_order'].unique()}")
print(f"✅ book_table values  : {df['book_table'].unique()}")

# ─────────────────────────────────────────
# STEP 6: Handle missing values
# ─────────────────────────────────────────
print("\nSTEP 6: Handling missing values...")
print("Nulls before:")
print(df[["name","location","rate","cost_for_two","cuisines"]].isnull().sum())

# முக்கியமான columns null-ஆ இருந்தா அந்த row delete பண்ணு
df = df.dropna(subset=["name", "location"])

# Rating null-ஆ இருந்தா average போடு
avg_rate = round(df["rate"].mean(), 2)
df["rate"] = df["rate"].fillna(avg_rate)

# Cost null-ஆ இருந்தா median போடு
median_cost = df["cost_for_two"].median()
df["cost_for_two"] = df["cost_for_two"].fillna(median_cost)

# Cuisines null-ஆ இருந்தா Unknown போடு
df["cuisines"] = df["cuisines"].fillna("Unknown")

print("\nNulls after:")
print(df[["name","location","rate","cost_for_two","cuisines"]].isnull().sum())

# ─────────────────────────────────────────
# STEP 7: Price Segments (புது column)
# ─────────────────────────────────────────
print("\nSTEP 7: Creating price segments...")

def price_segment(cost):
    if cost <= 300:
        return "Low"       # ₹300 கீழே
    elif cost <= 700:
        return "Mid"       # ₹301 - ₹700
    else:
        return "Premium"   # ₹700 மேலே

df["price_segment"] = df["cost_for_two"].apply(price_segment)
print(f"✅ Price segments:")
print(df["price_segment"].value_counts())

# ─────────────────────────────────────────
# STEP 8: Rating Category (புது column)
# ─────────────────────────────────────────
print("\nSTEP 8: Creating rating categories...")

def rating_category(rate):
    if rate < 3.0:
        return "Poor"
    elif rate < 3.8:
        return "Average"
    elif rate <= 4.2:
        return "Good"
    else:
        return "Excellent"

df["rating_category"] = df["rate"].apply(rating_category)
print(f"✅ Rating categories:")
print(df["rating_category"].value_counts())

# ─────────────────────────────────────────
# STEP 9: Save clean data
# ─────────────────────────────────────────
print("\nSTEP 9: Saving clean data...")
df.to_csv("uber_eats_cleaned.csv", index=False)
print(f"✅ Saved as 'uber_eats_cleaned.csv'")
print(f"✅ Total clean rows : {len(df)}")
print(f"✅ Total columns    : {len(df.columns)}")
print("\n🎉 Data Cleaning Complete! Next: database_setup.py")