import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="Influencer Campaign Dashboard", layout="wide")

# --- Title ---
st.title("📊 Influencer Campaign Dashboard")

# --- Sidebar Filters (TOP) ---
st.sidebar.header("🔍 Filters")

# Load default influencers data for filter dropdown
default_influencers = pd.read_csv("influencers.csv")
platforms = default_influencers["platform"].unique().tolist()
selected_platform = st.sidebar.selectbox("Select Platform", ["All"] + platforms)

st.sidebar.markdown("---")  # separator line

# --- Sidebar Uploaders ---
st.sidebar.header("📤 Upload Campaign Data")
influencer_file = st.sidebar.file_uploader("Upload Influencers Data", type=["csv"])
post_file = st.sidebar.file_uploader("Upload Posts Data", type=["csv"])
tracking_file = st.sidebar.file_uploader("Upload Tracking Data", type=["csv"])
payouts_file = st.sidebar.file_uploader("Upload Payouts Data", type=["csv"])

# --- Load Data ---
# --- Load Data ---
try:
    if influencer_file:
        influencers = pd.read_csv(influencer_file)
    else:
        influencers = pd.read_csv("data/influencers.csv")

    if post_file:
        posts = pd.read_csv(post_file)
    else:
        posts = pd.read_csv("data/posts.csv")

    if tracking_file:
        tracking = pd.read_csv(tracking_file)
    else:
        tracking = pd.read_csv("data/tracking_data.csv")

    if payouts_file:
        payouts = pd.read_csv(payouts_file)
    else:
        payouts = pd.read_csv("data/payouts.csv")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()


# --- Apply Filter ---
if selected_platform != "All":
    influencers = influencers[influencers["platform"] == sel]()
