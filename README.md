# 💼 HealthKart Influencer Campaign ROI Dashboard

## 📌 Overview

This interactive dashboard simulates and visualizes influencer marketing performance for **HealthKart** across platforms like Instagram, YouTube, and Twitter. It enables stakeholders to evaluate influencer efficiency, compare campaign ROAS, and track payouts — all using simulated data modeled around real-world influencer campaign logic.

🔗 **[Live App](https://influencer-campaign-dashboard-v2-fhsubfxmnqfz26qqww63sy.streamlit.app/)**  

📁 **Tool**: Built using Python, Streamlit, and Plotly  
🧪 **Data Modeling**: 4 simulated datasets created in CSV

---

## 🎯 Objective

To build a robust, open-source dashboard that enables:

- Tracking **campaign performance** across brands
- Calculating and visualizing **incremental ROAS**
- Gaining **influencer-level insights**
- Monitoring and analyzing **payout structures**

---

## 📊 Key Features

✅ **Top Influencers by ROAS**  
✅ **Revenue & Payout Summary**  
✅ **Engagement Rate per Influencer**  
✅ **Platform-wise Filtering (Instagram, YouTube, etc.)**  
✅ **Campaign ROAS & Performance Table**  
✅ **Payment Basis (Post vs. Order)**  
✅ **Downloadable CSV summaries**

---

## 📁 Simulated Data Sources

Located in `/data/` folder:

| File | Description |
|------|-------------|
| `influencers.csv` | Influencer ID, Name, Platform, Gender, Follower Count |
| `posts.csv` | Post details: influencer, date, caption, likes, comments, reach |
| `tracking_data.csv` | Tracks user interactions: campaign, orders, revenue |
| `payouts.csv` | Influencer payout basis, rates, and total payouts |

---

## 📈 Metrics Tracked

- **ROAS** = Revenue / Total Payout  
- **Total Revenue & Payout** across campaigns  
- **Top Influencers by ROI Efficiency**  
- **Engagement Rate per Influencer**  
- **Payout split by Post vs Order**  
- **Campaign-level ROAS comparison**

---

## 🧠 Insights

- **Best ROI**: Dev led with a ROAS of **4.17**, followed by John and Riya.
- **Top Revenue Generator**: Aman had the highest revenue contribution (~₹11,500) but lowest ROAS (0.31).
- **Engagement Leaders**: John had the highest average engagement rate.
- **Payment Basis**: Majority of payouts (~75%) are based on **per-post**, not orders.
- **Low Performing Campaigns**: SummerFit and MusclePush campaigns had low ROAS due to high payouts.

---

## 🔍 Filters & Interactions

- Platform-based filters (All, Instagram, YouTube, etc.)
- Hover-over tooltips for deeper data visibility
- Interactive tables and charts with pagination and scroll

---

## 📤 Export

- Option to download Influencer & Campaign summaries in CSV
- Clean, printable layout for PDF export if needed (manual)

---

## 🛠 Setup Instructions

1. Clone this repository  
   ```bash
   git clone https://github.com/your-username/influencer-campaign-dashboard.git
   cd influencer-campaign-dashboard
   ```

2. Install dependencies  
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app  
   ```bash
   streamlit run influencer_dashboard.py
   ```

4. Upload data or use preloaded `/data/*.csv` files

---

## 📌 Assumptions

- Influencer payouts are either based on the number of **posts** or **orders**.
- ROAS is computed as **Revenue / Payout**; no attribution lag or decay is modeled.
- Engagement rate is based on a simple average of post-level interactions.
- Revenue and payouts are assumed to be inclusive of GST and in INR.

---


---

## 🧠 Final Thoughts

This dashboard brings together product sense, analytical depth, and storytelling through a data-centric lens. It helps brands like **HealthKart** not only **optimize ROI** from influencer campaigns but also discover **top-performing personas** and identify **cost-inefficient marketing efforts**.
