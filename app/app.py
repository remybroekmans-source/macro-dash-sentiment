import os
import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path
import sys

# Make src importable
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))
from src.utils import rescale_to_0_100

DATA_PATH = ROOT / "data" / "processed" / "daily_factors.csv"

st.set_page_config(page_title="Macro Sentiment Dashboard", layout="wide")

@st.cache_data
def load_factors():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"], index_col="date")
    return df

df = load_factors()

st.title("Macro Dashboard & Sentiment Indicator")

st.subheader("1. Daily Macro Blocks (precomputed)")
st.line_chart(df[["macro_block", "policy_block", "risk_block"]])

st.subheader("2. Adjust weights to build your own 0–100 index")

col1, col2, col3 = st.columns(3)

with col1:
    w_macro = st.slider("Macro weight", 0.0, 1.0, 0.33, 0.01)
with col2:
    w_policy = st.slider("Policy weight", 0.0, 1.0, 0.33, 0.01)
with col3:
    w_risk = st.slider("Risk weight", 0.0, 1.0, 0.34, 0.01)

# Normalise weights to sum to 1
w_sum = w_macro + w_policy + w_risk
if w_sum == 0:
    w_macro = w_policy = 0.0
    w_risk = 1.0
    w_sum = 1.0

w_macro /= w_sum
w_policy /= w_sum
w_risk /= w_sum

st.write(f"Effective weights – Macro: {w_macro:.2f}, Policy: {w_policy:.2f}, Risk: {w_risk:.2f}")

# Compute weighted z-score and 0-100 index
z_index = (w_macro * df["macro_block"] +
           w_policy * df["policy_block"] +
           w_risk * df["risk_block"])

index_0_100 = rescale_to_0_100(z_index)

df_display = df.copy()
df_display["sentiment_custom_0_100"] = index_0_100

st.line_chart(df_display[["sentiment_0_100_equal", "sentiment_custom_0_100"]])

st.subheader("3. Latest reading")
latest_date = df_display.index[-1].date()
latest_value = df_display["sentiment_custom_0_100"].iloc[-1]
st.metric(label=f"Custom sentiment index (0–100) as of {latest_date}",
          value=f"{latest_value:.1f}")
