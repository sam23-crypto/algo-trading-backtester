cat > download_india_data.py << 'EOF'
import yfinance as yf
import pandas as pd

SYMBOL = "RELIANCE.NS"   # change this for other stocks

data = yf.download(
    SYMBOL,
    start="2024-01-01",
    end="2024-06-30",
    interval="1d"
)

if data.empty:
    raise SystemExit(f"No data returned for {SYMBOL}")

data = data.reset_index()

if "Date" in data.columns:
    date_col = "Date"
else:
    date_col = "Datetime"

data = data.rename(columns={
    date_col: "datetime",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Volume": "volume"
})

data = data[["datetime", "open", "high", "low", "close", "volume"]]

data.to_csv("prices.csv", index=False)

print(data.head())
print(f"✅ Wrote {len(data)} rows to prices.csv for {SYMBOL}")
EOF
