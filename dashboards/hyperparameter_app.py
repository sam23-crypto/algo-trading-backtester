import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
import os

st.set_page_config(page_title="Trading Backtester", layout="wide")
st.title("🚀 Algorithmic Trading Backtester")
st.markdown("#### Hyperparameter Tuning & Real Event-Driven Backtesting")

# Load data correctly
@st.cache_data
def load_data():
    return pd.read_csv("prices.csv", parse_dates=["datetime"]).tail()

st.sidebar.header("📊 Data Preview")
st.dataframe(load_data())

st.sidebar.header("Strategy Parameters")
strategy = st.sidebar.selectbox("Strategy", ["MA Crossover"])

if strategy == "MA Crossover":
    short = st.sidebar.slider("Short MA", 5, 50, 10)
    long = st.sidebar.slider("Long MA", 20, 100, 30)
    
if st.sidebar.button("🚀 Run Real Backtest"):
    with st.spinner("Running event-driven backtest..."):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['strategies']['ma']['short_window'] = short
        config['strategies']['ma']['long_window'] = long
        
        from backtester.engine import Backtester
        bt = Backtester(config)
        results = bt.run_backtest()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Signals", results['signals'])
        col2.metric("Fills/Trades", results['fills'])
        col3.metric("Total Fees", f"${results['stats']['total_fees']:.0f}")
        col4.metric("Total Trades", results['stats']['total_trades'])
        
        st.success("✅ Event-Driven Backtest Complete!")
        st.json(results['stats'])

# Mock equity curve (real data integration next)
st.subheader("📈 Equity Curve & Performance")
fig = go.Figure()
fig.add_trace(go.Scatter(y=[100000, 102500, 101000, 105000, 103500], 
                        mode="lines", name="Portfolio Value"))
st.plotly_chart(fig, use_container_width=True)


