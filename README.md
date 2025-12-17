Here is a compact README you can paste as‑is, with everything set up in one place.

Algorithmic Trading Backtester – Indian Stocks (NIFTY, TCS, Reliance, SBI, Airtel)
This project is a complete mini quant stack: a Python event‑driven backtester plus a Streamlit dashboard for Indian stocks like NIFTY, TCS, RELIANCE, SBI, and Airtel. It downloads real market data via yfinance, runs a moving‑average crossover strategy, and shows performance metrics (Sharpe, drawdown, PnL) and an interactive equity curve.​

1. What it does
Pulls real Indian stock data (NSE/BSE) from Yahoo Finance into prices.csv as OHLCV.​

Runs an event‑driven backtest engine: data handler → strategy → execution → portfolio.​

Computes a proper performance tear sheet:

Cumulative return

Annualized return & volatility

Sharpe ratio

Max drawdown​

Exposes everything through a Streamlit dashboard with:

“Refresh data from market” (near real‑time feel using fresh intraday data).​

Strategy sliders (short/long MA).

Portfolio controls (starting cash, fee per unit).

Live‑updating equity curve and JSON stats.

You can use it as a resume‑ready demo or as a base for more advanced strategies.

2. Project structure
Top level

run_backtest.py – CLI entrypoint: runs a full backtest on prices.csv and prints stats.​

download_india_data.py – downloads Indian stock data via yfinance and writes prices.csv.​

config.json – simple config (kept minimal in this version).

prices.csv – historical / intraday OHLCV data used by the engine and dashboard.​

Backtester core (backtester/)

data_handler.py – loads prices.csv, parses datetime, indexes and sorts the time series.

portfolio.py – tracks cash, position, trades, total fees, and realized PnL.

execution.py – executes orders, applies per‑unit fees, and updates the portfolio.

performance.py – builds a performance summary (Sharpe, max drawdown, etc.).​

engine.py – orchestrates data, strategy, execution, and portfolio into a single backtest run.​

Strategies (strategies/)

ma.py – moving‑average crossover strategy that outputs +1 / 0 / −1 signals from close prices.​

Dashboard (dashboards/)

hyperparameter_app.py – Streamlit app: data preview, “Refresh data from market”, sliders, and visualization.​

3. One‑time setup
From the project root:

Install dependencies

bash
pip install -r requirements.txt
pip install yfinance streamlit
yfinance is used for real Indian stock data; Streamlit powers the dashboard UI.​​

Choose your market symbol

In download_india_data.py, set one symbol (examples):

^NSEI – NIFTY 50 index

RELIANCE.NS – Reliance Industries

TCS.NS – TCS

SBIN.NS – SBI

BHARTIARTL.NS – Airtel

The script uses yfinance.download(...) to pull historical/intraday data and writes a clean prices.csv with columns:
datetime, open, high, low, close, volume.​

Generate prices.csv (historical data)

bash
python download_india_data.py
After this, prices.csv exists in the repo root with real Indian market data.​

4. How to run everything (backtest + dashboard)
A) Terminal backtest
From the project root:

bash
python run_backtest.py
You should see a full tear sheet, for example:

text
INFO:root:Loaded 1000 bars for TEST
Performance Summary
-------------------
cumulative_return: 0.0062
annualized_return: 0.0016
annualized_vol: 0.0052
sharpe_ratio: 0.3033
max_drawdown: -0.0167
Backtest complete!
Portfolio stats: {'total_trades': ..., 'total_fees': ..., 'realized_pnl': ...}
This confirms the complete pipeline (data → strategy → execution → portfolio → performance) is working.​

B) Streamlit dashboard (near real‑time)
From the project root:

bash
python -m streamlit run dashboards/hyperparameter_app.py --server.port 8080 --server.address 0.0.0.0
Then:

Open the browser URL (e.g., in Codespaces: Ports → 8080 → globe icon).​​

In the sidebar:

Click “Refresh data from market” to fetch the latest intraday OHLCV for your chosen symbol via yfinance and update prices.csv.​

Adjust Short MA and Long MA windows, starting cash, and fee per unit.

Click “Run Backtest” to:

Run the same engine on the latest prices.csv.

See the updated equity curve and portfolio stats instantly.

Every time you hit “Refresh data from market” + “Run Backtest”, you are effectively doing a fresh backtest on the newest intraday data, giving a near real‑time trading dashboard feel.
