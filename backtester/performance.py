"""Performance metrics calculation"""
import numpy as np
import pandas as pd
from typing import List, Dict

def calculate_sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0) -> float:
    """Sharpe ratio calculation"""
    if len(returns) == 0 or np.std(returns) == 0:
        return 0.0

    excess_returns = np.array(returns) - risk_free_rate / 252  # Annualized
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)

def calculate_max_drawdown(equity_curve: List[float]) -> Dict:
    """Maximum drawdown calculation"""
    equity = np.array(equity_curve)
    peak = np.maximum.accumulate(equity)
    drawdown = (equity - peak) / peak
    return {
        \'max_drawdown\': np.min(drawdown),
        \'max_drawdown_pct\': abs(np.min(drawdown)) * 100
    }

def create_tearsheet(stats: Dict, equity_curve: List[float]) -> Dict:
    """Generate comprehensive performance report"""
    returns = np.diff(equity_curve) / equity_curve[:-1]

    return {
        \'sharpe_ratio\': calculate_sharpe_ratio(returns.tolist()),
        \'max_drawdown\': calculate_max_drawdown(equity_curve),
        \'total_return\': (equity_curve[-1] / equity_curve[0] - 1) * 100,
        \'num_trades\': stats.get(\'total_trades\', 0),
        \'win_rate\': stats.get(\'wins\', 0) / max(stats.get(\'total_trades\', 1), 1) * 100
    }
