
"""Main backtest runner"""
import json
import logging
from backtester.engine import Backtester
from backtester.performance import create_tearsheet

if __name__ == "__main__":
    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    # Run backtest
    bt = Backtester(config)
    results = bt.run_backtest()
    
    # Performance report
    print("\n=== BACKTEST RESULTS ===")
    print(f"Signals generated: {results.get('signals', 0)}")
    print(f"Total fills: {results.get('fills', 0)}")
    print("\nPortfolio stats:", results['stats'])
    
    print("\nBacktest complete!")
