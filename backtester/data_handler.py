"""Data handler for loading and providing market data"""
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
import logging

class DataHandler:
    def __init__(self, csv_path: str, symbol: str):
        self.symbol = symbol
        self.data = self._load_data(csv_path)
        self.current_bar = 0
        self.bars_total = len(self.data)
        logging.info(f"Loaded {self.bars_total} bars for {symbol}")

    def _load_data(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path, parse_dates=[\'datetime\'])
        df.set_index(\'datetime\', inplace=True)
        df.sort_index(inplace=True)
        return df

    def get_latest_bar(self, symbol: str) -> Optional[Dict]:
        if self.current_bar >= len(self.data):
            return None
        bar = self.data.iloc[self.current_bar].to_dict()
        return bar

    def update_bars(self) -> List[Dict]:
        """Advance to next bar"""
        self.current_bar += 1
        return [self.get_latest_bar(self.symbol)] if self.get_latest_bar(self.symbol) else []

    def get_bars(self, symbol: str, num_bars: int = 500) -> pd.DataFrame:
        """Get recent N bars for strategy calculations"""
        end_idx = min(self.current_bar + 1, len(self.data))
        start_idx = max(0, end_idx - num_bars)
        return self.data.iloc[start_idx:end_idx]
