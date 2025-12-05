"""Execution handler with slippage and fills"""
import logging
from typing import Dict
from datetime import datetime
import numpy as np

class ExecutionHandler:
    def __init__(self, slippage_bps: float, commission_per_trade: float):
        self.slippage_bps = slippage_bps / 10000
        self.commission_per_trade = commission_per_trade

    def execute_order(self, order: Dict, market_price: float) -> Dict:
        """Execute market order with realistic slippage"""
        quantity = abs(order[\'quantity\'])
        direction = order[\'direction\']

        # Apply slippage (worse fill for market orders)
        slippage = market_price * self.slippage_bps * (1.5 if direction == \'BUY\' else 0.5)
        fill_price = market_price + slippage if direction == \'BUY\' else market_price - slippage

        commission = self.commission_per_trade

        fill = {
            \'symbol\': order[\'symbol\'],
            \'datetime\': order[\'datetime\'],
            \'exchange\': \'BACKTEST\',
            \'quantity\': quantity,
            \'direction\': direction,
            \'fill_price\': fill_price,
            \'commission\': commission
        }

        logging.info(f"FILL: {direction} {quantity} {order[\'symbol\']} @ {fill_price:.4f}")
        return fill
