"""Volume Breakout Strategy"""
import pandas as pd
import numpy as np
from .ma import Strategy
from datetime import datetime

class VolumeBreakoutStrategy(Strategy):
    def __init__(self, window: int, volume_multiplier: float, symbol: str):
        self.window = window
        self.volume_multiplier = volume_multiplier
        self.symbol = symbol

    def generate_signals(self, data: pd.DataFrame, events: list, portfolio: Dict) -> list:
        signals = []

        if len(data) < self.window:
            return signals

        current_volume = data[\'volume\'].iloc[-1]
        avg_volume = data[\'volume\'].tail(self.window).mean()

        current_pos = portfolio.get(\'current_positions\', {}).get(self.symbol, 0)
        current_price = data[\'close\'].iloc[-1]
        prev_high = data[\'high\'].tail(5).max()

        # Volume breakout above recent high
        if (current_volume > avg_volume * self.volume_multiplier 
            and current_price > prev_high * 0.999 
            and current_pos <= 0):
            signals.append({
                \'symbol\': self.symbol,
                \'datetime\': data.index[-1],
                \'signal_type\': \'LONG\',
                \'strength\': 1.0
            })
        # Exit on volume contraction
        elif current_volume < avg_volume * 0.7 and current_pos > 0:
            signals.append({
                \'symbol\': self.symbol,
                \'datetime\': data.index[-1],
                \'signal_type\': \'SHORT\',
                \'strength\': 1.0
            })

        return signals
