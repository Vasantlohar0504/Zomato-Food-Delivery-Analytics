
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import altair as alt
from src.model import train_model, predict_rating

# ---------- PAGE ----------
st.set_page_config(page_title="Bangalore Food Analytics", layout="wide")

# ---------- LOAD ----------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return pd.read_csv(os.path.join(base_dir, "data/processed/zomato_cleaned_sample.csv"))

df = load_data()

# ---------- MODEL ----------
@st.cache_resource
def get_model():
    return train_model(df)

model = get_model()

# ---------- TITLE ----------
st.title("🍴 Bangalore's Zomato Food Delivery Dashboard")
st.markdown("📊 Advanced Analytics with Interactive Visualizations")

# ---------- SIDEBAR ----------
st.sidebar.header("Dashboard Filters")

locations = st.sidebar.multiselect("📍 Location", sorted(df['location'].unique()))

all_cuisines = df['cuisines'].str.split(',').explode().str.strip().unique()
cuisines = st.sidebar.multiselect("🍽️ Cuisine", sorted(all_cuisines))

cost_range = st.sidebar.slider("💰 Cost", int(df['cost'].min()), int(df['cost'].max()), (100, 1000))

rating_range = st.sidebar.slider("⭐ Rating", float(df['rate'].min()), float(df['rate'].max()), (3.0, 5.0))

votes_range = st.sidebar.slider("🗳️ Votes", int(df['votes'].min()), int(df['votes'].max()), (0, 1000))

only_high_rated = st.sidebar.checkbox("⭐ Only 4+ Rated")

sort_by = st.sidebar.selectbox("📊 Sort By", ["Rating", "Cost", "Votes"])

top_n = st.sidebar.slider("📌 Show Top", 5, 50, 10)

# ---------- FILTER ----------
filtered_df = df.copy()

if locations:
    filtered_df = filtered_df[filtered_df['location'].isin(locations)]

if cuisines:
    filtered_df = filtered_df[
        filtered_df['cuisines'].str.contains('|'.join(cuisines), case=False, na=False)
    ]

filtered_df = filtered_df[
    (filtered_df['cost'] >= cost_range[0]) &
    (filtered_df['cost'] <= cost_range[1]) &
    (filtered_df['rate'] >= rating_range[0]) &
    (filtered_df['rate'] <= rating_range[1]) &
    (filtered_df['votes'] >= votes_range[0]) &
    (filtered_df['votes'] <= votes_range[1])
]

if only_high_rated:
    filtered_df = filtered_df[filtered_df['rate'] >= 4.0]

# ---------- SORT ----------
if sort_by == "Rating":
    filtered_df = filtered_df.sort_values(by="rate", ascending=False)
elif sort_by == "Cost":
    filtered_df = filtered_df.sort_values(by="cost")
else:
    filtered_df = filtered_df.sort_values(by="votes", ascending=False)

# ---------- EMPTY CHECK ----------
if filtered_df.empty:
    st.warning("⚠️ No data found. Try adjusting filters.")
    st.stop()

# ---------- KPI ----------
st.subheader("📊 Key Metrics")

st.markdown("""
<style>
.kpi-card {padding: 25px; border-radius: 20px; color: white; text-align: center;}
.kpi-icon {font-size: 40px;}
.kpi-value {font-size: 28px;}
.kpi1 {background: linear-gradient(135deg, #ff7e5f, #feb47b);}
.kpi2 {background: linear-gradient(135deg, #6a11cb, #2575fc);}
.kpi3 {background: linear-gradient(135deg, #11998e, #38ef7d);}
.kpi4 {background: linear-gradient(135deg, #f7971e, #ffd200);}
</style>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='kpi-card kpi1'><div class='kpi-icon'>🍴</div><div class='kpi-value'>{len(filtered_df)}</div>Restaurants</div>", unsafe_allow_html=True)
c2.markdown(f"<div class='kpi-card kpi2'><div class='kpi-icon'>⭐</div><div class='kpi-value'>{round(filtered_df['rate'].mean(),2)}</div>Avg Rating</div>", unsafe_allow_html=True)
c3.markdown(f"<div class='kpi-card kpi3'><div class='kpi-icon'>💰</div><div class='kpi-value'>₹{int(filtered_df['cost'].mean())}</div>Avg Cost</div>", unsafe_allow_html=True)
c4.markdown(f"<div class='kpi-card kpi4'><div class='kpi-icon'>🗳️</div><div class='kpi-value'>{int(filtered_df['votes'].sum())}</div>Total Votes</div>", unsafe_allow_html=True)

st.divider()

# ---------- ROW 1 ----------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🍽️ Top Cuisines")
    cuisine_df = filtered_df['cuisines'].str.split(',').explode().value_counts().head(10).reset_index()
    cuisine_df.columns = ['Cuisine', 'Count']
    st.altair_chart(
        alt.Chart(cuisine_df).mark_bar().encode(
            x=alt.X('Cuisine', sort='-y'),
            y='Count',
            color=alt.Color('Count', scale=alt.Scale(scheme='reds'))
        ),
        width='stretch'
    )

with col2:
    st.subheader("📍 Top Locations")
    loc_df = filtered_df['location'].value_counts().head(10).reset_index()
    loc_df.columns = ['Location', 'Count']
    st.altair_chart(
        alt.Chart(loc_df).mark_bar().encode(
            x=alt.X('Location', sort='-y'),
            y='Count',
            color=alt.Color('Count', scale=alt.Scale(scheme='blues'))
        ),
        width='stretch'
    )

st.divider()

# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    st.subheader("💰 Cost Distribution")
    bins = [0, 150, 300, 400, 500, 700]
    labels = ["0-150", "150-300", "300-400", "400-500", "500-700"]
    filtered_df['cost_category'] = pd.cut(filtered_df['cost'], bins=bins, labels=labels)

    cost_df = filtered_df['cost_category'].value_counts().sort_index().reset_index()
    cost_df.columns = ['Range', 'Count']

    st.altair_chart(
        alt.Chart(cost_df).mark_bar().encode(
            x='Range',
            y='Count',
            color=alt.Color('Count', scale=alt.Scale(scheme='oranges'))
        ),
        width='stretch'
    )

with col4:
    st.subheader("⭐ Avg Rating by Cost")
    rating_cost_df = filtered_df.groupby('cost_category', observed=False)['rate'].mean().reset_index()

    st.altair_chart(
        alt.Chart(rating_cost_df).mark_bar().encode(
            x='cost_category',
            y='rate',
            color=alt.Color('rate', scale=alt.Scale(scheme='greenblue'))
        ),
        width='stretch'
    )

st.divider()

# ---------- ROW 3 ----------
col5, col6 = st.columns(2)

with col5:
    st.subheader("📈 Cost vs Rating")
    st.altair_chart(
        alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='cost',
            y='rate',
            color=alt.Color('rate', scale=alt.Scale(scheme='viridis')),
            tooltip=['name', 'cost', 'rate']
        ).interactive(),
        width='stretch'
    )

with col6:
    st.subheader("📊 Votes vs Rating")
    st.altair_chart(
        alt.Chart(filtered_df).mark_circle(size=60).encode(
            x='votes',
            y='rate',
            color=alt.Color('votes', scale=alt.Scale(scheme='plasma')),
            tooltip=['name', 'votes', 'rate']
        ).interactive(),
        width='stretch'
    )

st.divider()

# ---------- ML ----------
st.subheader("🤖 Predict Rating")

c9, c10, c11 = st.columns(3)

cost_input = c9.number_input("Cost", 100, 3000, 500)
votes_input = c10.number_input("Votes", 0, 5000, 200)
cuisine_input = c11.slider("Cuisine Count", 1, 5, 2)

if st.button("Predict"):
    pred = predict_rating(model, cost_input, votes_input, cuisine_input)
    st.success(f"⭐ Predicted Rating: {round(pred, 2)}")

st.divider()

# ---------- TABLE ----------
st.subheader("🏆 Top Restaurants")
st.dataframe(filtered_df.head(top_n), width='stretch')
