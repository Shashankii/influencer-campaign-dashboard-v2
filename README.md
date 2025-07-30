# 💼 HealthKart Influencer Campaign ROI Dashboard

## 🚀 Live Demo

👉 **[Click here to try the live app](https://influencer-campaign-dashboard-v2-fhsubfxmnqfz26qqww63sy.streamlit.app/)**


This dashboard analyzes influencer campaign performance for HealthKart across platforms like Instagram, YouTube, and Twitter. It calculates key metrics like ROAS (Return on Ad Spend), influencer insights, and payout tracking.

---

## 📊 Features

- Upload and analyze simulated influencer campaign data
- View top influencers by ROAS
- Compare campaign performance by revenue and payout
- Interactive filters by platform
- Visualizations using Plotly
- Downloadable campaign and influencer summaries as CSV

---

## 📁 Simulated Datasets

All CSVs are located in the `/data/` folder:

- `influencers.csv`: Influencer profiles
- `posts.csv`: Individual post details
- `tracking_data.csv`: User interactions and order tracking
- `payouts.csv`: Payment structures

---

## 📈 Metrics Tracked

- **ROAS** (Return on Ad Spend) = Revenue / Total Payout
- **Campaign Revenue**, Orders, and Spending
- **Top Performing Influencers** based on ROAS
- **Platform-level filtering and comparison**

---

## 🚀 How to Run

Make sure you have Python 3.9+ installed.

### Step 1: Install dependencies

```bash
pip install streamlit pandas plotly
