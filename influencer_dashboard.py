import streamlit as st
import pandas as pd
import plotly.express as px

# Set wide layout
st.set_page_config(page_title="Influencer Campaign Dashboard", layout="wide")

# Title
st.title("📊 Influencer Campaign Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")

# Load default influencers CSV to get platform options
try:
    default_influencers = pd.read_csv("influencers.csv")
    platforms = default_influencers["platform"].unique().tolist()
except Exception as e:
    st.sidebar.error("⚠️ Failed to load default influencers.csv")
    platforms = []

selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + platforms)

st.sidebar.markdown("---")

# --- Sidebar Uploads ---
st.sidebar.header("📤 Upload Campaign Data")
influencer_file = st.sidebar.file_uploader("Upload Influencers Data", type=["csv"])
post_file = st.sidebar.file_uploader("Upload Posts Data", type=["csv"])
tracking_file = st.sidebar.file_uploader("Upload Tracking Data", type=["csv"])
payouts_file = st.sidebar.file_uploader("Upload Payouts Data", type=["csv"])

# --- Load Data ---
try:
    if influencer_file and post_file and tracking_file and payouts_file:
        influencers = pd.read_csv(influencer_file)
        posts = pd.read_csv(post_file)
        tracking = pd.read_csv(tracking_file)
        payouts = pd.read_csv(payouts_file)
    else:
        influencers = pd.read_csv("influencers.csv")
        posts = pd.read_csv("posts.csv")
        tracking = pd.read_csv("tracking_data.csv")
        payouts = pd.read_csv("payouts.csv")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

# --- Apply Filter ---
if selected_platform != "All":
    influencers = influencers[influencers["platform"] == selected_platform]

# --- Merge Data ---
try:
    merged = tracking.merge(influencers, left_on="influencer_id", right_on="id")
    merged = merged.merge(payouts, on="influencer_id")

    # ROAS Calculations
    merged["ROAS"] = merged["revenue"] / merged["total_payout"]
    merged["baseline_revenue"] = merged["revenue"] * 0.6
    merged["incremental_revenue"] = merged["revenue"] - merged["baseline_revenue"]
    merged["incremental_ROAS"] = merged["incremental_revenue"] / merged["total_payout"]
except Exception as e:
    st.error(f"❌ Error merging or calculating data: {e}")
    st.stop()

# --- Campaign Summary Table ---
st.subheader("📈 Campaign Summary")
summary = merged.groupby("platform").agg({
    "revenue": "sum",
    "total_payout": "sum",
    "ROAS": "mean",
    "incremental_ROAS": "mean"
}).reset_index()
st.dataframe(summary, use_container_width=True)

# --- Top Influencers ---
st.subheader("🏆 Top Influencers by Engagement")
posts["engagement"] = posts["likes"] + posts["comments"]
top_posts = posts.sort_values("engagement", ascending=False).head(5)
st.dataframe(top_posts, use_container_width=True)

# --- Download Button ---
st.subheader("📤 Export Data")
st.download_button("Download Top_
