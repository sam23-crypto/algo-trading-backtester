"""Portfolio tracking with P&L accounting"""
from typing import Dict, List
from datetime import datetime
import pandas as pd
import numpy as np
import logging

class Portfolio:
    def __init__(self, initial_capital: float, slippage_bps: float, commission_per_trade: float):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.slippage_bps = slippage_bps / 10000  # Convert to decimal
        self.commission_per_trade = commission_per_trade

        self.all_positions = {}  # symbol: quantity
        self.current_positions = {}
        self.all_holdings = {}   # symbol: {\'avg_price\': x, \'quantity\': y}
        self.current_holdings = {}

        self.all_cash = [initial_capital]
        self.current_cash = initial_capital

        self.trades = []  # List of completed trades
        self.stats = {
            \'total_trades\': 0,
            \'wins\': 0,
            \'losses\': 0,
            \'gross_wins\': 0.0,
            \'gross_losses\': 0.0,
            \'total_fees\': 0.0
        }

    def update_timeindex(self, event: Dict):
        """Update portfolio state"""
        self.current_cash = self.initial_capital
        self.current_positions = self.all_positions.copy()
        self.current_holdings = self.all_holdings.copy()

    def execute_fill(self, fill: Dict):
        symbol = fill[\'symbol\']
        quantity = fill[\'quantity\']
        direction = fill[\'direction\']
        fill_price = fill[\'fill_price\']
        commission = fill[\'commission\']

        # Update holdings
        if symbol not in self.current_holdings:
            self.current_holdings[symbol] = {\'quantity\': 0, \'avg_price\': 0}
            self.all_holdings[symbol] = {\'quantity\': 0, \'avg_price\': 0}

        holding = self.current_holdings[symbol]
        new_quantity = holding[\'quantity\'] + (1 if direction == \'BUY\' else -1) * quantity

        if new_quantity == 0:
            del self.current_holdings[symbol]
        else:
            if holding[\'quantity\'] != 0:
                # Weighted average price
                total_cost = (holding[\'quantity\'] * holding[\'avg_price\'] 
                            + quantity * fill_price)
                holding[\'avg_price\'] = total_cost / new_quantity
            else:
                holding[\'avg_price\'] = fill_price
            holding[\'quantity\'] = new_quantity

            self.all_holdings[symbol] = holding.copy()

        # Update cash
        self.current_cash -= quantity * fill_price * (1 if direction == \'BUY\' else -1)
        self.current_cash -= commission

        # Record trade
        self.trades.append({
            \'symbol\': symbol,
            \'quantity\': quantity,
            \'direction\': direction,
            \'fill_price\': fill_price,
            \'commission\': commission,
            \'pnl\': 0.0  # Updated later
        })

        self.stats[\'total_trades\'] += 1
        self.stats[\'total_fees\'] += commission

    def calculate_performance(self, market_price: float) -> Dict:
        """Calculate current portfolio value and unrealized P&L"""
        total = self.current_cash

        for symbol, holding in self.current_holdings.items():
            market_value = holding[\'quantity\'] * market_price
            unrealized_pnl = market_value - (holding[\'quantity\'] * holding[\'avg_price\'])
            total += market_value

        return {
            \'total\': total,
            \'cash\': self.current_cash,
            \'positions_value\': total - self.current_cash,
            \'unrealized_pnl\': total - self.initial_capital - sum(h[\'quantity\'] * h[\'avg_price\'] for h in self.current_holdings.values())
        }
