import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from backtester.engine import Backtester
import json

st.set_page_config(page_title="Trading Backtester", layout="wide")
st.title("🚀 Algorithmic Trading Backtester")
st.markdown("#### Hyperparameter Tuning & Strategy Comparison")

# Sidebar
st.sidebar.header("Strategy Parameters")
strategy = st.sidebar.selectbox("Strategy", ["MA Crossover", "RSI", "Volume"])
if strategy == "MA Crossover":
    short = st.sidebar.slider("Short MA", 5, 50, 10)
    long = st.sidebar.slider("Long MA", 20, 100, 30)
    params = {"ma": {"short_window": short, "long_window": long}}
elif strategy == "RSI":
    window = st.sidebar.slider("RSI Window", 10, 30, 14)
    oversold = st.sidebar.slider("Oversold", 20, 40, 30)
    overbought = st.sidebar.slider("Overbought", 60, 80, 70)
    params = {"rsi": {"window": window, "oversold": oversold, "overbought": overbought}}
else:
    vol_win = st.sidebar.slider("Volume Window", 10, 50, 20)
    mult = st.sidebar.slider("Volume Mult", 1.2, 3.0, 1.5)
    params = {"volume": {"window": vol_win, "volume_multiplier": mult}}

if st.sidebar.button("🚀 Run Real Backtest"):
    with st.spinner("Running event-driven backtest..."):
        with open('config.json', 'r') as f:
            config = json.load(f)
        config['strategies'] = params
        
        bt = Backtester(config)
        results = bt.run_backtest()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Signals", results['signals'])
        col2.metric("Fills", results['fills']) 
        col3.metric("Total Fees", f"${results['stats']['total_fees']:.0f}")
        
        st.success("✅ Backtest Complete!")
        st.write(results['stats'])

