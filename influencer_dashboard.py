import streamlit as st
import pandas as pd
import plotly.express as px

# ── PAGE SETUP ──
st.set_page_config(page_title="Influencer Campaign Dashboard", layout="wide")
st.title("📊 HealthKart Influencer Campaign Dashboard")

# ── DATA LOADING ──
@st.cache_data
def load_data():
    influencers = pd.read_csv("influencers.csv")                # must contain influencer_id, name, platform, etc.
    posts       = pd.read_csv("posts.csv", parse_dates=["date"])# must contain influencer_id, date, reach, likes, comments
    tracking    = pd.read_csv("tracking_data.csv")              # must contain influencer_id, campaign, revenue, etc.
    payouts     = pd.read_csv("payouts.csv")                    # must contain influencer_id, basis, total_payout
    return influencers, posts, tracking, payouts

influencers, posts, tracking, payouts = load_data()

# ── SIDEBAR FILTER: PLATFORM ONLY ──
st.sidebar.header("🔍 Filters")
platforms = influencers["platform"].unique().tolist()
selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + platforms)

if selected_platform != "All":
    influencers = influencers[influencers["platform"] == selected_platform]

# ── MERGE & METRICS ──
# Merge tracking with the (filtered) influencers, then add payouts
merged = (
    tracking
    .merge(influencers, on="influencer_id", how="inner")
    .merge(payouts,     on="influencer_id", how="left")
)

# Ensure missing payouts become zero
merged["total_payout"] = merged["total_payout"].fillna(0)

# Compute ROAS
merged["ROAS"] = merged["revenue"] / merged["total_payout"].replace(0, pd.NA)

# ── KPI CARDS ──
total_rev    = merged["revenue"].sum()
total_payout = merged["total_payout"].sum()



# Compute ROAS
overall_roas     = total_rev / total_payout if total_payout else 0
overall_roas_pct = overall_roas * 100

# Create three columns
col1, col2, col3 = st.columns(3)

# Render the first two as before, and the third as percent only
col1.metric("Total Revenue", f"₹{total_rev:,.0f}")
col2.metric("Total Payout",  f"₹{total_payout:,.0f}")
col3.metric("Overall ROAS",  f"{overall_roas_pct:.0f}%")

# ── TOP INFLUENCERS BY ROAS ──
st.subheader("🏆 Top Influencers by ROAS")
top_inf = (
    merged
    .groupby("name")[["revenue","total_payout"]]
    .sum()
    .assign(ROAS=lambda df: df["revenue"] / df["total_payout"].replace(0, pd.NA))
    .sort_values("ROAS", ascending=False)
    .reset_index()
)
st.dataframe(top_inf)

# ── CAMPAIGN PERFORMANCE ──
st.subheader("📈 Campaign Performance")
camp = merged.groupby("campaign").agg({
    "revenue":      "sum",
    "total_payout": "sum"
})
if "orders" in merged.columns:
    camp["orders"] = merged.groupby("campaign")["orders"].sum()
camp["ROAS"] = camp["revenue"] / camp["total_payout"].replace(0, pd.NA)
st.dataframe(camp.reset_index())

# ── ENGAGEMENT METRICS ──
# Limit posts to only those influencers in the current filter
posts_filtered = posts[posts["influencer_id"].isin(influencers["influencer_id"])]
posts_filtered["engagement_rate"] = (posts_filtered["likes"] + posts_filtered["comments"]) / posts_filtered["reach"]
eng = (
    posts_filtered
    .groupby("influencer_id")["engagement_rate"]
    .mean()
    .reset_index()
    .merge(influencers[["influencer_id","name"]], on="influencer_id", how="left")
)
st.subheader("💬 Engagement Rate by Influencer")
fig_eng = px.bar(
    eng, x="name", y="engagement_rate",
    labels={"name":"Influencer","engagement_rate":"Engagement Rate"},
    title="Average Engagement Rate"
)
st.plotly_chart(fig_eng, use_container_width=True)

# ── PAYOUT BREAKDOWN ──
st.subheader("💸 Payout Breakdown by Basis")
pay_sum = payouts.groupby("basis")["total_payout"].sum().reset_index()
fig_pay = px.pie(
    pay_sum, names="basis", values="total_payout",
    title="Payout by Basis"
)
st.plotly_chart(fig_pay, use_container_width=True)

# ── REVENUE BY INFLUENCER ──
st.subheader("💰 Revenue by Influencers")
fig_rev = px.bar(
    top_inf.sort_values("revenue", ascending=False),
    x="name", y="revenue", color="name",
    labels={"name":"Influencer","revenue":"Revenue Earned"},
    title="Revenue per Influencer"
)
st.plotly_chart(fig_rev, use_container_width=True)

# ── ROAS BY CAMPAIGN ──
st.subheader("📊 ROAS by Campaign")
fig_roas = px.bar(
    camp.reset_index(), x="campaign", y="ROAS", color="campaign",
    labels={"campaign":"Campaign","ROAS":"Return on Ad Spend"},
    title="ROAS per Campaign"
)
st.plotly_chart(fig_roas, use_container_width=True)

# ── KEY TAKEAWAYS ──
st.markdown("""
---
### 📝 Key Takeaways
- **Scale** influencers with ROAS > 2× while keeping an eye on engagement.  
- **Reallocate** spend from low-ROAS campaigns to top performers.  
- **Balance** high-engagement vs. high-ROAS when planning your next push.
""")

# ── EXPORT CSV BUTTONS ──
st.subheader("📤 Export Data")
csv_top  = top_inf.to_csv(index=False).encode("utf-8")
csv_camp = camp.reset_index().to_csv(index=False).encode("utf-8")

st.download_button("⬇️ Download Top Influencers (CSV)",  csv_top,  file_name="top_influencers.csv")
st.download_button("⬇️ Download Campaign Summary (CSV)", csv_camp, file_name="campaign_summary.csv")
