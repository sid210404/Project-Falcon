"""Donchian-channel breakout strategy."""

from __future__ import annotations

import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class DonchianBreakoutStrategy(BaseStrategy):
    """Enter an upper-channel breakout and exit a lower-channel breakdown."""

    name = "Donchian Breakout"
    description = "Long-only trend following using prior-period Donchian channels."

    parameter_space = {
        "entry_period": {"label": "Entry Channel", "values": [20, 30, 55], "default": 20},
        "exit_period": {"label": "Exit Channel", "values": [5, 10, 20], "default": 10},
    }

    def __init__(self, entry_period: int = 20, exit_period: int = 10) -> None:
        if entry_period <= 1 or exit_period <= 1:
            raise ValueError("Donchian periods must be greater than one.")
        self.entry_period = entry_period
        self.exit_period = exit_period

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return breakout signals without using the current candle in channels."""
        frame = df.copy()
        entry_channel = frame["high"].rolling(self.entry_period).max().shift(1)
        exit_channel = frame["low"].rolling(self.exit_period).min().shift(1)

        frame["DONCHIAN_UPPER"] = entry_channel
        frame["DONCHIAN_LOWER"] = exit_channel
        frame["signal"] = 0
        frame.loc[frame["close"] > entry_channel, "signal"] = 1
        frame.loc[frame["close"] < exit_channel, "signal"] = -1
        return frame
