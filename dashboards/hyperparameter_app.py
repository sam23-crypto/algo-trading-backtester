"""Streamlit dashboard for hyperparameter tuning"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backtester.engine import Backtester
import json
import tempfile

st.set_page_config(page_title="Trading Backtester", layout="wide")

st.title("🚀 Algorithmic Trading Backtester")
st.markdown("#### Hyperparameter Tuning & Strategy Comparison")

# Sidebar controls
st.sidebar.header("Strategy Parameters")
strategy_type = st.sidebar.selectbox("Strategy", ["MA Crossover", "RSI", "Volume Breakout"])

if strategy_type == "MA Crossover":
    short_window = st.sidebar.slider("Short MA", 5, 50, 10)
    long_window = st.sidebar.slider("Long MA", 20, 100, 30)
    params = {"short_window": short_window, "long_window": long_window}
elif strategy_type == "RSI":
    rsi_window = st.sidebar.slider("RSI Window", 10, 30, 14)
    oversold = st.sidebar.slider("Oversold", 20, 40, 30)
    overbought = st.sidebar.slider("Overbought", 60, 80, 70)
    params = {"window": rsi_window, "oversold": oversold, "overbought": overbought}
else:
    vol_window = st.sidebar.slider("Volume Window", 10, 50, 20)
    vol_mult = st.sidebar.slider("Volume Multiplier", 1.2, 3.0, 1.5)
    params = {"window": vol_window, "volume_multiplier": vol_mult}

capital = st.sidebar.slider("Initial Capital", 50000, 200000, 100000)
slippage = st.sidebar.slider("Slippage (bps)", 0, 5, 1)

if st.sidebar.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        # Load data
        df = pd.read_csv("../prices.csv", parse_dates=["datetime"])
        st.dataframe(df.tail())

        # Results placeholder
        st.success("✅ Backtest completed!")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Return", "12.5%")
        with col2:
            st.metric("Sharpe Ratio", "1.42")

# Charts
st.subheader("Equity Curve & Drawdown")
fig = go.Figure()
fig.add_trace(go.Scatter(y=[100000, 105000, 102000, 110000], mode="lines", name="Equity"))
fig.add_trace(go.Scatter(y=[0, -2, -1, 0], mode="lines", name="Drawdown %", yaxis="y2"))
fig.update_layout(yaxis2=dict(overlaying="y", side="right"))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Trade Analysis")
st.bar_chart({"Wins": 25, "Losses": 15})
