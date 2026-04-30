# ============================================================
#  Uber Eats Bangalore - SQL Queries (10 Business Questions)
#  File: sql_queries.py
# ============================================================

import pandas as pd
import sqlite3

# Database connect பண்ணு
conn = sqlite3.connect("ubereats.db")
print("✅ Database connected!")
print("=" * 55)

# ─────────────────────────────────────────
# Q1: எந்த location-ல best rating இருக்கு?
# ─────────────────────────────────────────
print("\n📍 Q1: Top 10 Locations by Average Rating")
q1 = pd.read_sql("""
    SELECT location,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY location
    ORDER BY avg_rating DESC
    LIMIT 10
""", conn)
print(q1.to_string(index=False))

# ─────────────────────────────────────────
# Q2: எந்த area over-crowded?
# ─────────────────────────────────────────
print("\n🏙️  Q2: Most Saturated Locations (Too Many Restaurants)")
q2 = pd.read_sql("""
    SELECT location,
           COUNT(*) AS total_restaurants
    FROM restaurants
    GROUP BY location
    ORDER BY total_restaurants DESC
    LIMIT 10
""", conn)
print(q2.to_string(index=False))

# ─────────────────────────────────────────
# Q3: Online order rating-ஐ improve பண்றதா?
# ─────────────────────────────────────────
print("\n📱 Q3: Online Order vs Average Rating")
q3 = pd.read_sql("""
    SELECT online_order,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total
    FROM restaurants
    GROUP BY online_order
""", conn)
print(q3.to_string(index=False))

# ─────────────────────────────────────────
# Q4: Table booking பண்றவங்க rating நல்லாவா?
# ─────────────────────────────────────────
print("\n🪑 Q4: Table Booking vs Average Rating")
q4 = pd.read_sql("""
    SELECT book_table,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total
    FROM restaurants
    GROUP BY book_table
""", conn)
print(q4.to_string(index=False))

# ─────────────────────────────────────────
# Q5: எந்த price range-ல customers satisfied?
# ─────────────────────────────────────────
print("\n💰 Q5: Price Range vs Customer Satisfaction")
q5 = pd.read_sql("""
    SELECT price_segment,
           ROUND(AVG(rate), 2)        AS avg_rating,
           ROUND(AVG(cost_for_two), 0) AS avg_cost,
           COUNT(*)                    AS total
    FROM restaurants
    GROUP BY price_segment
    ORDER BY avg_rating DESC
""", conn)
print(q5.to_string(index=False))

# ─────────────────────────────────────────
# Q6: Low/Mid/Premium — எது better?
# ─────────────────────────────────────────
print("\n🏷️  Q6: Price Segment Performance")
q6 = pd.read_sql("""
    SELECT price_segment,
           COUNT(*) AS total_restaurants,
           ROUND(AVG(rate), 2) AS avg_rating,
           rating_category,
           COUNT(*) AS count
    FROM restaurants
    GROUP BY price_segment, rating_category
    ORDER BY price_segment, avg_rating DESC
""", conn)
print(q6.to_string(index=False))

# ─────────────────────────────────────────
# Q7: Most popular cuisines எவை?
# ─────────────────────────────────────────
print("\n🍽️  Q7: Most Popular Cuisines")
q7 = pd.read_sql("""
    SELECT cuisines,
           COUNT(*) AS total_restaurants
    FROM restaurants
    WHERE cuisines != 'Unknown'
    GROUP BY cuisines
    ORDER BY total_restaurants DESC
    LIMIT 10
""", conn)
print(q7.to_string(index=False))

# ─────────────────────────────────────────
# Q8: Highest rated cuisine எது?
# ─────────────────────────────────────────
print("\n⭐ Q8: Highest Rated Cuisines (min 50 restaurants)")
q8 = pd.read_sql("""
    SELECT cuisines,
           ROUND(AVG(rate), 2) AS avg_rating,
           COUNT(*) AS total
    FROM restaurants
    WHERE cuisines != 'Unknown'
    GROUP BY cuisines
    HAVING COUNT(*) >= 50
    ORDER BY avg_rating DESC
    LIMIT 10
""", conn)
print(q8.to_string(index=False))

# ─────────────────────────────────────────
# Q9: Niche cuisines opportunity இருக்கா?
# ─────────────────────────────────────────
print("\n🌟 Q9: Niche Cuisines with High Rating (Low Competition)")
q9 = pd.read_sql("""
    SELECT cuisines,
           COUNT(*) AS total_restaurants,
           ROUND(AVG(rate), 2) AS avg_rating
    FROM restaurants
    WHERE cuisines != 'Unknown'
    GROUP BY cuisines
    HAVING COUNT(*) < 20 AND AVG(rate) >= 4.0
    ORDER BY avg_rating DESC
    LIMIT 10
""", conn)
print(q9.to_string(index=False))

# ─────────────────────────────────────────
# Q10: Cost vs Rating — relation இருக்கா?
# ─────────────────────────────────────────
print("\n📊 Q10: Cost vs Rating Correlation by Segment")
q10 = pd.read_sql("""
    SELECT price_segment,
           ROUND(MIN(cost_for_two), 0)  AS min_cost,
           ROUND(MAX(cost_for_two), 0)  AS max_cost,
           ROUND(AVG(cost_for_two), 0)  AS avg_cost,
           ROUND(AVG(rate), 2)           AS avg_rating
    FROM restaurants
    GROUP BY price_segment
    ORDER BY avg_cost
""", conn)
print(q10.to_string(index=False))

# ─────────────────────────────────────────
# Save all results
# ─────────────────────────────────────────
print("\n" + "=" * 55)
print("💾 Saving all query results...")

results = {"Q1_top_locations": q1, "Q2_saturated_areas": q2,
           "Q3_online_order": q3, "Q4_book_table": q4,
           "Q5_price_satisfaction": q5, "Q6_segment_performance": q6,
           "Q7_popular_cuisines": q7, "Q8_top_rated_cuisines": q8,
           "Q9_niche_cuisines": q9, "Q10_cost_vs_rating": q10}

with pd.ExcelWriter("sql_results.xlsx") as writer:
    for sheet_name, df in results.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

conn.close()
print("✅ Results saved to 'sql_results.xlsx'")
print("🎉 All 10 SQL Queries Complete! Next: app.py (Streamlit)")