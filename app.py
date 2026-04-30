# ============================================================
#  Uber Eats Bangalore - Streamlit Dashboard
#  File: app.py
#  Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
import sqlite3

# ─────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Uber Eats Bangalore Intelligence",
    page_icon="🍽️",
    layout="wide"
)

# ─────────────────────────────────────────
# Database Connection
# ─────────────────────────────────────────
@st.cache_resource
def get_connection():
    return sqlite3.connect("ubereats.db", check_same_thread=False)

conn = get_connection()

# ─────────────────────────────────────────
# Sidebar Navigation
# ─────────────────────────────────────────
st.sidebar.title("🍽️ Uber Eats Bangalore")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "📌 Page Select பண்ணு:",
    ["🏠 Dashboard", "❓ Business Q&A"]
)

# ════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ════════════════════════════════════════
if page == "🏠 Dashboard":

    st.title("🏠 Uber Eats Bangalore — Restaurant Dashboard")
    st.markdown("Filters use பண்ணி உனக்கு வேண்டிய restaurants பாரு!")
    st.markdown("---")

    # Load data
    df = pd.read_sql("SELECT * FROM restaurants", conn)

    # ── Filters Row ──
    col1, col2, col3 = st.columns(3)

    with col1:
        locations = ["All"] + sorted(df["location"].dropna().unique().tolist())
        selected_location = st.selectbox("📍 Location Select பண்ணு:", locations)

    with col2:
        segments = ["All"] + sorted(df["price_segment"].dropna().unique().tolist())
        selected_segment = st.selectbox("💰 Price Segment:", segments)

    with col3:
        online_options = ["All", "Yes", "No"]
        selected_online = st.selectbox("📱 Online Order:", online_options)

    # ── Apply Filters ──
    filtered = df.copy()

    if selected_location != "All":
        filtered = filtered[filtered["location"] == selected_location]
    if selected_segment != "All":
        filtered = filtered[filtered["price_segment"] == selected_segment]
    if selected_online != "All":
        filtered = filtered[filtered["online_order"] == selected_online]

    # ── Summary Numbers ──
    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("🏪 Total Restaurants", len(filtered))
    m2.metric("⭐ Avg Rating",
              round(filtered["rate"].mean(), 2) if len(filtered) > 0 else 0)
    m3.metric("💸 Avg Cost for 2",
              f"₹{int(filtered['cost_for_two'].mean())}" if len(filtered) > 0 else "₹0")
    m4.metric("📱 Online Order Available",
              f"{int((filtered['online_order']=='Yes').sum())} restaurants")

    # ── Results Table ──
    st.markdown("---")
    st.subheader(f"📋 Restaurants List ({len(filtered)} results)")

    if len(filtered) == 0:
        st.warning("⚠️ இந்த filter-க்கு restaurants இல்ல. வேற filter try பண்ணு!")
    else:
        show_cols = ["name", "location", "rate", "rating_category",
                     "cost_for_two", "price_segment",
                     "online_order", "book_table", "cuisines"]
        st.dataframe(
            filtered[show_cols].sort_values("rate", ascending=False),
            use_container_width=True,
            height=450
        )

# ════════════════════════════════════════
# PAGE 2 — BUSINESS Q&A
# ════════════════════════════════════════
elif page == "❓ Business Q&A":

    st.title("❓ Business Intelligence — 10 Questions & Answers")
    st.markdown("இந்த 10 questions-க்கும் data-based answers இங்க இருக்கு!")
    st.markdown("---")

    # Q1
    with st.expander("📍 Q1: எந்த location-ல best average rating இருக்கு?"):
        q1 = pd.read_sql("""
            SELECT location,
                   ROUND(AVG(rate),2) AS avg_rating,
                   COUNT(*) AS total_restaurants
            FROM restaurants
            GROUP BY location
            ORDER BY avg_rating DESC LIMIT 10
        """, conn)
        st.dataframe(q1, use_container_width=True)
        st.success("💡 Insight: இந்த areas-ல restaurant open பண்ணா high rating கிடைக்கும்!")

    # Q2
    with st.expander("🏙️ Q2: எந்த area-ல competition அதிகமா இருக்கு?"):
        q2 = pd.read_sql("""
            SELECT location, COUNT(*) AS total_restaurants
            FROM restaurants
            GROUP BY location
            ORDER BY total_restaurants DESC LIMIT 10
        """, conn)
        st.dataframe(q2, use_container_width=True)
        st.warning("⚠️ Insight: இந்த areas already saturated — புது restaurant-க்கு avoid பண்ணு!")

    # Q3
    with st.expander("📱 Q3: Online Order இருந்தா rating improve ஆகுதா?"):
        q3 = pd.read_sql("""
            SELECT online_order,
                   ROUND(AVG(rate),2) AS avg_rating,
                   COUNT(*) AS total
            FROM restaurants GROUP BY online_order
        """, conn)
        st.dataframe(q3, use_container_width=True)
        st.info("💡 Insight: Online order enable பண்ணா customer reach அதிகமாகும்!")

    # Q4
    with st.expander("🪑 Q4: Table Booking rating-ஐ affect பண்றதா?"):
        q4 = pd.read_sql("""
            SELECT book_table,
                   ROUND(AVG(rate),2) AS avg_rating,
                   COUNT(*) AS total
            FROM restaurants GROUP BY book_table
        """, conn)
        st.dataframe(q4, use_container_width=True)
        st.info("💡 Insight: Table booking available restaurants பொதுவா higher rated!")

    # Q5
    with st.expander("💰 Q5: எந்த price range customers-க்கு பிடிக்கும்?"):
        q5 = pd.read_sql("""
            SELECT price_segment,
                   ROUND(AVG(rate),2) AS avg_rating,
                   ROUND(AVG(cost_for_two),0) AS avg_cost,
                   COUNT(*) AS total
            FROM restaurants
            GROUP BY price_segment
            ORDER BY avg_rating DESC
        """, conn)
        st.dataframe(q5, use_container_width=True)
        st.success("💡 Insight: Premium restaurants higher rating பெறுகின்றன!")

    # Q6
    with st.expander("🏷️ Q6: Low/Mid/Premium — எது better perform பண்றது?"):
        q6 = pd.read_sql("""
            SELECT price_segment, rating_category, COUNT(*) AS count
            FROM restaurants
            GROUP BY price_segment, rating_category
            ORDER BY price_segment
        """, conn)
        st.dataframe(q6, use_container_width=True)

    # Q7
    with st.expander("🍽️ Q7: Bangalore-ல most popular cuisines எவை?"):
        q7 = pd.read_sql("""
            SELECT cuisines, COUNT(*) AS total_restaurants
            FROM restaurants WHERE cuisines != 'Unknown'
            GROUP BY cuisines
            ORDER BY total_restaurants DESC LIMIT 10
        """, conn)
        st.dataframe(q7, use_container_width=True)
        st.info("💡 Insight: இந்த cuisines-க்கு demand அதிகமா இருக்கு!")

    # Q8
    with st.expander("⭐ Q8: Highest rated cuisines எவை?"):
        q8 = pd.read_sql("""
            SELECT cuisines,
                   ROUND(AVG(rate),2) AS avg_rating,
                   COUNT(*) AS total
            FROM restaurants WHERE cuisines != 'Unknown'
            GROUP BY cuisines HAVING COUNT(*) >= 50
            ORDER BY avg_rating DESC LIMIT 10
        """, conn)
        st.dataframe(q8, use_container_width=True)
        st.success("💡 Insight: இந்த cuisines highest customer satisfaction!")

    # Q9
    with st.expander("🌟 Q9: Low competition, high rating — opportunity எங்க இருக்கு?"):
        q9 = pd.read_sql("""
            SELECT cuisines, COUNT(*) AS total, ROUND(AVG(rate),2) AS avg_rating
            FROM restaurants WHERE cuisines != 'Unknown'
            GROUP BY cuisines HAVING COUNT(*) < 20 AND AVG(rate) >= 4.0
            ORDER BY avg_rating DESC LIMIT 10
        """, conn)
        st.dataframe(q9, use_container_width=True)
        st.success("💡 Insight: இந்த niche cuisines-ல market gap இருக்கு — opportunity!")

    # Q10
    with st.expander("📊 Q10: Cost vs Rating — relation இருக்கா?"):
        q10 = pd.read_sql("""
            SELECT price_segment,
                   ROUND(MIN(cost_for_two),0) AS min_cost,
                   ROUND(MAX(cost_for_two),0) AS max_cost,
                   ROUND(AVG(cost_for_two),0) AS avg_cost,
                   ROUND(AVG(rate),2) AS avg_rating
            FROM restaurants
            GROUP BY price_segment ORDER BY avg_cost
        """, conn)
        st.dataframe(q10, use_container_width=True)
        st.info("💡 Insight: Cost அதிகமாக இருந்தால் rating அதிகமாக இருக்கிறது!")

    st.markdown("---")
    st.success("🎉 All 10 Business Questions Answered! Project Complete!")