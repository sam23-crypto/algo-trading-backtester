"""Main event-driven backtesting engine"""
import queue
import logging
from typing import Dict, List, Any
from datetime import datetime

from .events import *
from .data_handler import DataHandler
from .portfolio import Portfolio
from .execution import ExecutionHandler
from ..strategies.ma import MACrossoverStrategy

class Backtester:
    def __init__(self, config: Dict):
        self.config = config
        self.data_handler = None
        self.strategy = None
        self.portfolio = None
        self.execution_handler = None

        self.events_queue = queue.Queue()
        self.signals = []
        self.fills = []

    def _initialize_components(self):
        """Initialize all backtester components"""
        data_config = self.config[\'data\']
        backtest_config = self.config[\'backtest\']

        self.data_handler = DataHandler(
            data_config[\'csv_path\'],
            data_config[\'symbol\']
        )

        self.strategy = MACrossoverStrategy(
            self.config[\'strategies\'][\'ma\'][\'short_window\'],
            self.config[\'strategies\'][\'ma\'][\'long_window\'],
            data_config[\'symbol\']
        )

        self.portfolio = Portfolio(
            backtest_config[\'initial_capital\'],
            backtest_config[\'slippage_bps\'],
            backtest_config[\'commission_per_trade\']
        )

        self.execution_handler = ExecutionHandler(
            backtest_config[\'slippage_bps\'],
            backtest_config[\'commission_per_trade\']
        )

    def run_backtest(self):
        """Main backtest loop"""
        logging.basicConfig(level=logging.INFO)
        self._initialize_components()

        while True:
            # Update market data
            market_events = self.data_handler.update_bars()
            for market_event_data in market_events:
                self.events_queue.put(MarketEvent(market_event_data))

            if self.data_handler.current_bar >= self.data_handler.bars_total:
                break

            # Handle all events in queue
            while not self.events_queue.empty():
                event = self.events_queue.get()

                if isinstance(event, MarketEvent):
                    # Update portfolio
                    self.portfolio.update_timeindex(event.data)

                    # Generate strategy signals
                    bars = self.data_handler.get_bars(event.data[\'symbol\'])
                    signals = self.strategy.generate_signals(bars, self.signals, {
                        \'current_positions\': self.portfolio.current_positions
                    })

                    for signal in signals:
                        signal_event = SignalEvent(**signal)
                        self.events_queue.put(signal_event)
                        self.signals.append(signal)

                elif isinstance(event, SignalEvent):
                    # Create orders from signals
                    current_price = event.datetime  # Simplified
                    quantity = int(self.portfolio.current_capital * 0.1 / 100)  # 10% position

                    order = OrderEvent(
                        event.symbol,
                        event.datetime,
                        \'MARKET\',
                        quantity,
                        event.signal_type,
                        0.0
                    )
                    self.events_queue.put(order)

                elif isinstance(event, OrderEvent):
                    # Execute order
                    fill = self.execution_handler.execute_order(event.__dict__, event.data[\'close\'])
                    fill_event = FillEvent(**fill)
                    self.events_queue.put(fill_event)
                    self.fills.append(fill)
                    self.portfolio.execute_fill(fill)

        return self.portfolio.stats

    def get_results(self):
        return {
            \'signals\': len(self.signals),
            \'fills\': len(self.fills),
            \'stats\': self.portfolio.stats
        }
