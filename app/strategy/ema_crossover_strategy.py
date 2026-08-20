"""Exponential moving-average crossover strategy."""

from __future__ import annotations

import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class EMACrossoverStrategy(BaseStrategy):
    """Enter an uptrend when a fast EMA crosses above a slow EMA."""

    name = "EMA Crossover"
    description = "Long-only trend following using a fast and slow EMA crossover."

    parameter_space = {
        "fast_period": {"label": "Fast EMA", "values": [9, 12, 20], "default": 12},
        "slow_period": {"label": "Slow EMA", "values": [26, 50, 100], "default": 26},
    }

    def __init__(self, fast_period: int = 12, slow_period: int = 26) -> None:
        if fast_period >= slow_period:
            raise ValueError("fast_period must be lower than slow_period.")
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return entry and exit signals on completed EMA crossovers."""
        frame = df.copy()
        fast = frame["close"].ewm(span=self.fast_period, adjust=False).mean()
        slow = frame["close"].ewm(span=self.slow_period, adjust=False).mean()
        previous_fast = fast.shift(1)
        previous_slow = slow.shift(1)

        frame["signal"] = 0
        frame.loc[(fast > slow) & (previous_fast <= previous_slow), "signal"] = 1
        frame.loc[(fast < slow) & (previous_fast >= previous_slow), "signal"] = -1
        return frame
