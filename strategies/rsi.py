"""RSI Mean Reversion Strategy"""
import pandas as pd
import numpy as np
from .ma import Strategy
from datetime import datetime

class RSIStrategy(Strategy):
    def __init__(self, window: int, oversold: int, overbought: int, symbol: str):
        self.window = window
        self.oversold = oversold
        self.overbought = overbought
        self.symbol = symbol

    def rsi(self, prices: pd.Series, window: int) -> pd.Series:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def generate_signals(self, data: pd.DataFrame, events: list, portfolio: Dict) -> list:
        signals = []

        if len(data) < self.window + 1:
            return signals

        rsi_values = self.rsi(data[\'close\'], self.window)
        current_rsi = rsi_values.iloc[-1]

        current_pos = portfolio.get(\'current_positions\', {}).get(self.symbol, 0)

        if current_rsi < self.oversold and current_pos <= 0:
            signals.append({
                \'symbol\': self.symbol,
                \'datetime\': data.index[-1],
                \'signal_type\': \'LONG\',
                \'strength\': 1.0
            })
        elif current_rsi > self.overbought and current_pos >= 0:
            signals.append({
                \'symbol\': self.symbol,
                \'datetime\': data.index[-1],
                \'signal_type\': \'SHORT\',
                \'strength\': 1.0
            })

        return signals
