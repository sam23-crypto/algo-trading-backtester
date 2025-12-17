## What this project is about

This is an **algorithmic trading backtester + Streamlit dashboard** for **Indian stocks** (NIFTY, TCS, Reliance, SBI, Airtel). It:

- Runs a **moving‑average crossover strategy** through an event‑driven backtest engine (data handler → strategy → execution → portfolio).  
- Uses **real OHLCV data** for Indian stocks.  
- Produces **performance metrics** (cumulative return, annualized return/vol, Sharpe ratio, max drawdown) and an equity curve.  
- Includes a **dashboard** where you can refresh data, tune parameters, and re‑run the backtest.

---

## Where the data comes from

All market data is downloaded from **Yahoo Finance** using the Python library **`yfinance`**:

- Indian symbols are requested as Yahoo tickers, for example:
  - `^NSEI` – NIFTY 50 index  
  - `RELIANCE.NS` – Reliance Industries  
  - `TCS.NS` – TCS  
  - `SBIN.NS` – SBI  
  - `BHARTIARTL.NS` – Airtel  

The script `download_india_data.py` calls `yfinance.download(...)` for the chosen symbol and writes a CSV file:

prices.csv # columns: datetime, open, high, low, close, volume

text

Both the **backtester** and the **Streamlit dashboard** read from this `prices.csv` file.

---

## Commands to run (from project root)

Run these in your terminal in this order.

### 1) Install dependencies (one time)

pip install -r requirements.txt
pip install yfinance streamlit

text

### 2) Download Indian stock data into prices.csv

Edit `download_india_data.py` and set your symbol (for example):

SYMBOL = "RELIANCE.NS" # or "^NSEI", "TCS.NS", "SBIN.NS", "BHARTIARTL.NS"

text

Then run:

python download_india_data.py

text

This will download real Indian market data from Yahoo Finance using `yfinance` and create/overwrite `prices.csv`.

### 3) Run a backtest in the terminal

python run_backtest.py

text

This will:

- Load `prices.csv`  
- Run the moving‑average strategy through the backtest engine  
- Print a performance summary and portfolio statistics

You should see something like:

INFO:root:Loaded 1000 bars for TEST
Performance Summary
cumulative_return: ...
annualized_return: ...
annualized_vol: ...
sharpe_ratio: ...
max_drawdown: ...
Backtest complete!
Portfolio stats: {...}

text

### 4) Start the Streamlit dashboard

python -m streamlit run dashboards/hyperparameter_app.py --server.port 8080 --server.address 0.0.0.0

text

Then:

- Open the URL that Streamlit prints (for Codespaces use Ports → 8080 → globe icon).  
- In the sidebar:
  - Click **“Refresh data from market”** to pull the latest intraday data for your symbol and update `prices.csv`.  
  - Adjust **short/long MA windows**, starting cash, and fee per unit.  
- Click **“Run Backtest”** to execute the engine on the updated `prices.csv` and see the new equity curve + stats.
