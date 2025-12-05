"""Main event-driven backtesting engine"""
import queue
import logging
from datetime import datetime
from backtester.events import *
from backtester.data_handler import DataHandler
from backtester.portfolio import Portfolio
from backtester.execution import ExecutionHandler
from strategies.ma import MACrossoverStrategy

class Backtester:
    def __init__(self, config):
        self.config = config
        self.data_handler = None
        self.strategy = None
        self.portfolio = None
        self.execution_handler = None
        self.events_queue = queue.Queue()
        self.signals = []
        self.fills = []

    def _initialize_components(self):
        data_config = self.config['data']
        backtest_config = self.config['backtest']
        
        self.data_handler = DataHandler(
            data_config['csv_path'],
            data_config['symbol']
        )
        
        self.strategy = MACrossoverStrategy(
            self.config['strategies']['ma']['short_window'],
            self.config['strategies']['ma']['long_window'],
            data_config['symbol']
        )
        
        self.portfolio = Portfolio(
            backtest_config['initial_capital'],
            backtest_config['slippage_bps'],
            backtest_config['commission_per_trade']
        )
        
        self.execution_handler = ExecutionHandler(
            backtest_config['slippage_bps'],
            backtest_config['commission_per_trade']
        )

    def run_backtest(self):
        logging.basicConfig(level=logging.INFO)
        self._initialize_components()
        
        while self.data_handler.current_bar < self.data_handler.bars_total:
            # Update market data
            market_events = self.data_handler.update_bars()
            for market_event_data in market_events:
                self.events_queue.put(MarketEvent(market_event_data))
            
            # Handle events
            while not self.events_queue.empty():
                event = self.events_queue.get()
                
                if isinstance(event, MarketEvent):
                    self.portfolio.update_timeindex(event.data)
                    
                    bars = self.data_handler.get_bars(self.data_handler.symbol)
                    signals = self.strategy.generate_signals(bars, self.signals, {
                        'current_positions': self.portfolio.current_positions
                    })
                    
                    for signal in signals:
                        signal_event = SignalEvent(**signal)
                        self.events_queue.put(signal_event)
                        self.signals.append(signal)
                
                elif isinstance(event, SignalEvent):
                    quantity = int(self.portfolio.current_capital * 0.1 / 100)
                    order = OrderEvent(
                        event.symbol,
                        event.datetime,
                        'MARKET',
                        quantity,
                        event.signal_type
                    )
                    self.events_queue.put(order)
                
                elif isinstance(event, OrderEvent):
                    market_price = event.data['close'] if 'data' in event.__dict__ else 100.0
                    fill = self.execution_handler.execute_order(vars(event), market_price)
                    fill_event = FillEvent(**fill)
                    self.events_queue.put(fill_event)
                    self.fills.append(fill)
                    self.portfolio.execute_fill(fill)
            
            self.data_handler.current_bar += 1
        
        return {
            'signals': len(self.signals),
            'fills': len(self.fills),
            'stats': self.portfolio.stats
        }
