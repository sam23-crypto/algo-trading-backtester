"""Moving Average Crossover Strategy"""
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame, events: list, portfolio: Dict) -> list:
        pass

class MACrossoverStrategy(Strategy):
    def __init__(self, short_window: int, long_window: int, symbol: str):
        self.short_window = short_window
        self.long_window = long_window
        self.symbol = symbol

    def generate_signals(self, data: pd.DataFrame, events: list, portfolio: Dict) -> list:
        signals = []

        if len(data) < self.long_window:
            return signals

        closes = data[\'close\'].values
        short_ma = pd.Series(closes).rolling(self.short_window).mean().iloc[-1]
        long_ma = pd.Series(closes).rolling(self.long_window).mean().iloc[-1]

        current_pos = portfolio.get(\'current_positions\', {}).get(self.symbol, 0)

        # Generate signals
        if short_ma > long_ma and current_pos <= 0:
            signals.append({
                \'symbol\': self.symbol,
                \'datetime\': data.index[-1],
                \'signal_type\': \'LONG\',
                \'strength\': 1.0
            })
        elif short_ma < long_ma and current_pos >= 0:
            signals.append({
                \'symbol\': self.symbol,
                \'datetime\': data.index[-1],
                \'signal_type\': \'SHORT\',
                \'strength\': 1.0
            })

        return signals
