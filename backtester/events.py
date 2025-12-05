"""Event classes for the event-driven backtester"""
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from typing import Any, Dict

class EventType(Enum):
    MARKET = "MARKET"
    SIGNAL = "SIGNAL" 
    ORDER = "ORDER"
    FILL = "FILL"

class Event(ABC):
    """Abstract base class for all events"""
    def __init__(self, type_: EventType):
        self.type = type_

class MarketEvent(Event):
    """Handles market price updates"""
    def __init__(self, data: Dict[str, Any]):
        super().__init__(EventType.MARKET)
        self.data = data  # {\'datetime\': dt, \'open\': o, \'high\': h, \'low\': l, \'close\': c, \'volume\': v}

class SignalEvent(Event):
    """Strategy signal generation"""
    def __init__(self, symbol: str, datetime: datetime, signal_type: str, strength: float = 1.0):
        super().__init__(EventType.SIGNAL)
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type  # "LONG", "SHORT"
        self.strength = strength

class OrderEvent(Event):
    """Order placement"""
    def __init__(self, symbol: str, datetime: datetime, order_type: str, quantity: int, 
                 direction: str, slippage: float = 0.0):
        super().__init__(EventType.ORDER)
        self.symbol = symbol
        self.datetime = datetime
        self.order_type = order_type  # "MARKET"
        self.quantity = quantity
        self.direction = direction  # "BUY", "SELL"
        self.slippage = slippage

class FillEvent(Event):
    """Order fill confirmation"""
    def __init__(self, symbol: str, datetime: datetime, exchange: str, quantity: int,
                 direction: str, fill_price: float, commission: float = 0.0):
        super().__init__(EventType.FILL)
        self.symbol = symbol
        self.datetime = datetime
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_price = fill_price
        self.commission = commission
