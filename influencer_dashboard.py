import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Influencer Campaign Dashboard", layout="wide")

st.title("📊 Influencer Campaign Dashboard")

# --- Sidebar Filters at Top ---
st.sidebar.header("🔍 Filters")

# Load default CSV initially for filtering dropdown
default_influencers = pd.read_csv("influencers.csv")
platforms = default_influencers["platform"].unique().tolist()
selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + platforms)

# --- Sidebar File Uploaders ---
st.sidebar.header("📤 Upload Data")
influencer_file = st.sidebar.file_uploader("Upload Influencers Data", type=["csv"])
post_file = st.sidebar.file_uploader("Upload Posts Data", type=["csv"])
tracking_file = st.sidebar.file_uploader("Upload Tracking Data", type=["csv"])
payouts_file = st.sidebar.file_uploader("Upload Payouts Data", type=["csv"])

# --- Load Data ---
if influencer_file and post_file and tracking_file and payouts_file:
    influencers = pd.read_csv(influencer_file)
    posts = pd.read_csv(post_file)
    tracking = pd.read_csv(tracking_file)
    payouts = pd.read_csv(payouts_file)
else:
    influencers = default_influencers
    posts = pd.read_csv("posts.csv")
    tracking = pd.read_csv("tracking_data.csv")
    payouts = pd.read_csv("payouts.csv")

# --- Apply Filter ---
if selected_platform != "All":
    influencers = influencers[influencers["platform"] == selected_platform]

# --- Merge Data ---
merged = tracking.merge(influencers, left_on="influencer_id", right_on="id")
merged = merged.merge(payouts, on="influencer_id")

# --- ROAS & Incremental ROAS ---
merged["ROAS"] = merged["revenue"] / merged["total_payout"]
merged["baseline_revenue"] = merged["revenue"] * 0.6
merged["incremental_revenue"] = merged["revenue"] - merged["baseline_revenue"]
merged["incremental_ROAS"] = merged["incremental_revenue"] / merged["total_payout"]

# --- Campaign Summary ---
st.subheader("📈 Campaign Summary")
summary = merged.groupby("platform").agg({
    "revenue": "sum",
    "total_payout": "sum",
    "ROAS": "mean",
    "incremental_ROAS": "mean"
}).reset_index()
st.dataframe(summary)

# --- Top Influencers Table ---
st.subheader("🏆 Top Influencers by Engagement")
posts["engagement"] = posts["likes"] + posts["comments"]
top_posts = posts.sort_values("engagement", ascending=False).head(5)
st.dataframe(top_posts)

# --- Export Data ---
st.subheader("📤 Export Data")
st.download_button("Download Top Influencers (CSV)", top_posts.to_csv(index=False), file_name="top_influencers.csv")
st.download
