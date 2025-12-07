# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

st.set_page_config(page_title="PL Dashboard", layout="wide")
st.title("PL Dashboard — Polymarket Arbitrage")
st.markdown("**Arbitragem em tempo real • P&L • Order Books**")

# Simulação (substitui depois com os teus dados)
df = pd.DataFrame({
    "Timestamp": pd.date_range(start="2025-04-05", periods=10, freq="H"),
    "Arbitragem %": [8.1, 8.3, 8.5, 9.0, 8.7, 8.2, 7.9, 8.4, 8.6, 9.1]
})

fig = px.line(df, x="Timestamp", y="Arbitragem %", title="Arbitragem (%)")
st.plotly_chart(fig, use_container_width=True)

st.metric("Lucro Total", "$3,210", "+12.4%")
st.success("Dashboard online e actualizado!")
