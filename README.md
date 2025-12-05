# Algorithmic Trading System with Backtesting

## Features
- Event-driven backtester with realistic fills, slippage, transaction costs
- MA, RSI, Volume breakout strategies
- Performance analytics (Sharpe, drawdown, P&L)
- Interactive Streamlit dashboards for hyperparameter tuning

## Quick Start
```bash
pip install -r requirements.txt
streamlit run dashboards/hyperparameter_app.py
```

## Run Backtest
```bash
python run_backtest.py
```
## Run  INTERACTIVE DASHBOARD (Browser)
```
python -m streamlit run dashboards/hyperparameter_app.py --server.port 8080 --server.address 0.0.0.0
```
## Run DATA VALIDATION
```
  head -5 prices.csv
tail -5 prices.csv
wc -l prices.csv
```
