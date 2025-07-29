import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="📊 Influencer Campaign Dashboard", layout="wide")

st.title("📊 Influencer Campaign Dashboard")

# Function to load default CSV from GitHub raw link
@st.cache_data
def load_csv_from_url(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.warning(f"⚠️ Failed to load data from: {url}")
        return pd.DataFrame()

# Default GitHub raw CSV links
default_influencers_url = "https://raw.githubusercontent.com/Shashankii/influencer-campaign-dashboard-v2/main/influencers.csv"
default_posts_url = "https://raw.githubusercontent.com/Shashankii/influencer-campaign-dashboard-v2/main/posts.csv"
default_tracking_url = "https://raw.githubusercontent.com/Shashankii/influencer-campaign-dashboard-v2/main/tracking_data.csv"
default_payouts_url = "https://raw.githubusercontent.com/Shashankii/influencer-campaign-dashboard-v2/main/payouts.csv"

# Sidebar
st.sidebar.header("🔍 Filters")
st.sidebar.subheader("📥 Upload Campaign Data")

# Uploaders
uploaded_influencers = st.sidebar.file_uploader("Upload Influencers Data", type="csv")
uploaded_posts = st.sidebar.file_uploader("Upload Posts Data", type="csv")
uploaded_tracking = st.sidebar.file_uploader("Upload Tracking Data", type="csv")
uploaded_payouts = st.sidebar.file_uploader("Upload Payouts Data", type="csv")

# Load data: uploaded or default
influencers_df = pd.read_csv(uploaded_influencers) if uploaded_influencers else load_csv_from_url(default_influencers_url)
posts_df = pd.read_csv(uploaded_posts) if uploaded_posts else load_csv_from_url(default_posts_url)
tracking_df = pd.read_csv(uploaded_tracking) if uploaded_tracking else load_csv_from_url(default_tracking_url)
payouts_df = pd.read_csv(uploaded_payouts) if uploaded_payouts else load_csv_from_url(default_payouts_url)

# Platform filter
if not influencers_df.empty and "platform" in influencers_df.columns:
    platforms = influencers_df["platform"].dropna().unique().tolist()
    selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + platforms)

    if selected_platform != "All":
        influencers_df = influencers_df[influencers_df["platform"] == selected_platform]

# Show data
st.subheader("👤 Influencers Data")
st.dataframe(influencers_df)

st.subheader("📢 Posts Data")
st.dataframe(posts_df)

st.subheader("📦 Tracking Data")
st.dataframe(tracking_df)

st.subheader("💰 Payouts Data")
st.dataframe(payouts_df)
