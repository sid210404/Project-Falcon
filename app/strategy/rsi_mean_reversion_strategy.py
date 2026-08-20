"""RSI mean-reversion strategy."""

from __future__ import annotations

import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class RSIMeanReversionStrategy(BaseStrategy):
    """Buy an oversold RSI cross and exit after a recovery."""

    name = "RSI Mean Reversion"
    description = "Long-only mean reversion after an RSI oversold cross."

    parameter_space = {
        "rsi_period": {"label": "RSI Period", "values": [7, 14, 21], "default": 14},
        "oversold": {"label": "Oversold RSI", "values": [20, 25, 30], "default": 30},
        "exit_rsi": {"label": "Exit RSI", "values": [50, 55, 60], "default": 55},
    }

    def __init__(self, rsi_period: int = 14, oversold: int = 30, exit_rsi: int = 55) -> None:
        if not 0 < oversold < exit_rsi < 100:
            raise ValueError("RSI thresholds must satisfy 0 < oversold < exit_rsi < 100.")
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.exit_rsi = exit_rsi

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return signals using RSI threshold crossings on closed candles."""
        frame = df.copy()
        change = frame["close"].diff()
        gains = change.clip(lower=0)
        losses = -change.clip(upper=0)
        average_gain = gains.rolling(self.rsi_period).mean()
        average_loss = losses.rolling(self.rsi_period).mean()
        rsi = 100 - (100 / (1 + average_gain / average_loss))
        previous_rsi = rsi.shift(1)

        frame["RSI"] = rsi
        frame["signal"] = 0
        frame.loc[(rsi <= self.oversold) & (previous_rsi > self.oversold), "signal"] = 1
        frame.loc[(rsi >= self.exit_rsi) & (previous_rsi < self.exit_rsi), "signal"] = -1
        return frame
