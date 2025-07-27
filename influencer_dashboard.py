import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Influencer Campaign Dashboard", layout="wide")
st.title("📊 HealthKart Influencer Campaign Dashboard")

# --- Data
st.sidebar.header("📁 Upload Campaign Data")
influencer_file = st.sidebar.file_uploader("Upload Influencer Data", type=["csv"])
post_file = st.sidebar.file_uploader("Upload Posts Data", type=["csv"])
tracking_file = st.sidebar.file_uploader("Upload Tracking Data", type=["csv"])
payouts_file = st.sidebar.file_uploader("Upload Payouts Data", type=["csv"])

import os

# Check if uploaded, else fallback to local
if influencer_file and post_file and tracking_file and payouts_file:
    influencers = pd.read_csv(influencer_file)
    posts = pd.read_csv(post_file)
    tracking = pd.read_csv(tracking_file)
    payouts = pd.read_csv(payouts_file)
elif all(os.path.exists(f) for f in ["influencers.csv", "posts.csv", "tracking_data.csv", "payouts.csv"]):
    influencers = pd.read_csv("influencers.csv")
    posts = pd.read_csv("posts.csv")
    tracking = pd.read_csv("tracking_data.csv")
    payouts = pd.read_csv("payouts.csv")
else:
    st.error("❗ Please upload all files or include default CSVs in the same folder.")
    st.stop()


# Load data
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

# --- Filter ---
st.sidebar.header("🔍 Filters")
platforms = influencers["platform"].unique().tolist()
selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + platforms)
if selected_platform != "All":
    influencers = influencers[influencers["platform"] == selected_platform]

# --- Merge Data ---
merged = tracking.merge(influencers, left_on="influencer_id", right_on="id")
merged = merged.merge(payouts, on="influencer_id")

# --- ROAS & Incremental ROAS ---
merged["ROAS"] = merged["revenue"] / merged["total_payout"]
merged["baseline_revenue"] = merged["revenue"] * 0.6
merged["incremental_revenue"] = merged["revenue"] - merged["baseline_revenue"]
merged["incremental_roas"] = merged["incremental_revenue"] / merged["total_payout"]

# --- Top Influencers Table ---
st.subheader("🏆 Top Influencers by ROAS")
top_influencers = merged.groupby("name")[["revenue", "total_payout"]].sum()
top_influencers["ROAS"] = top_influencers["revenue"] / top_influencers["total_payout"]
top_influencers = top_influencers.sort_values("ROAS", ascending=False).reset_index()
st.dataframe(top_influencers)

# --- Campaign Performance Table ---
st.subheader("📈 Campaign Performance")
campaign_summary = merged.groupby("campaign").agg({
    "revenue": "sum",
    "total_payout": "sum",
    "incremental_revenue": "sum"
})
campaign_summary["ROAS"] = campaign_summary["revenue"] / campaign_summary["total_payout"]
campaign_summary["incremental_ROAS"] = campaign_summary["incremental_revenue"] / campaign_summary["total_payout"]
if 'orders' in merged.columns:
    campaign_summary["orders"] = merged.groupby("campaign")["orders"].sum()
st.dataframe(campaign_summary.reset_index())

# --- Revenue by Influencer ---
st.subheader("💰 Revenue by Influencers")
rev_chart = top_influencers.sort_values("revenue", ascending=False)
fig1 = px.bar(rev_chart, x="name", y="revenue", color="name", title="Influencer Revenue",
              labels={"name": "Influencer", "revenue": "Revenue Earned"}, height=400)
st.plotly_chart(fig1, use_container_width=True)

# --- ROAS by Campaign ---
st.subheader("📊 ROAS by Campaign")
fig2 = px.bar(campaign_summary.reset_index(), x="campaign", y="ROAS", color="campaign",
              title="ROAS per Campaign", labels={"campaign": "Campaign", "ROAS": "Return on Ad Spend"}, height=400)
st.plotly_chart(fig2, use_container_width=True)

# --- Incremental ROAS by Campaign ---
st.subheader("📈 Incremental ROAS by Campaign")
fig3 = px.bar(campaign_summary.reset_index(), x="campaign", y="incremental_ROAS", color="campaign",
              title="Incremental ROAS per Campaign", labels={"campaign": "Campaign", "incremental_ROAS": "Incremental ROAS"}, height=400)
st.plotly_chart(fig3, use_container_width=True)

# --- Persona-Based Analysis ---
bins = [0, 10000, 50000, 100000, 500000]
labels = ['Micro (<10k)', 'Mid (10k–50k)', 'Macro (50k–100k)', 'Mega (>100k)']
influencers["persona"] = pd.cut(influencers["follower_count"], bins=bins, labels=labels)
persona_df = merged.merge(influencers[["id", "persona"]], left_on="influencer_id", right_on="id")
persona_summary = persona_df.groupby("persona").apply(lambda x: x["revenue"].sum() / x["total_payout"].sum()).reset_index(name="ROAS")

st.subheader("🎯 ROAS by Influencer Persona")
st.bar_chart(persona_summary.set_index("persona"))

# --- Top Engaged Posts ---
st.subheader("📸 Top 5 Posts by Engagement")
posts["engagement"] = posts["likes"] + posts["comments"]
top_posts = posts.sort_values("engagement", ascending=False).head(5)
st.dataframe(top_posts[["influencer_id", "platform", "reach", "likes", "comments", "engagement"]])

# --- CSV Export ---
st.subheader("📤 Export Data")

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

st.download_button("⬇️ Download Top Influencers (CSV)", convert_df(top_influencers), "top_influencers.csv", "text/csv")
st.download_button("⬇️ Download Campaign Summary (CSV)", convert_df(campaign_summary.reset_index()), "campaign_summary.csv", "text/csv")
