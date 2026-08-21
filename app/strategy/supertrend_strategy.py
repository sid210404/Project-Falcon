"""
SuperTrend Strategy

ATR-based non-repainting trend-following strategy.
Compatible with Falcon Backtesting and Paper Trading.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class SuperTrendStrategy(BaseStrategy):
    """
    ATR-based SuperTrend.

    BUY  -> Trend flips bullish.
    SELL -> Trend flips bearish.
    HOLD -> Otherwise.
    """

    name = "SuperTrend"

    def __init__(
        self,
        atr_period: int = 10,
        multiplier: float = 3.0,
    ) -> None:
        self.atr_period = atr_period
        self.multiplier = multiplier

    @property
    def parameters(self) -> dict:
        return {
            "atr_period": self.atr_period,
            "multiplier": self.multiplier,
        }

    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        df = data.copy()

        required = {"high", "low", "close", "datetime"}

        missing = required - set(df.columns)

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        # ---------------------------------------------------------
        # ATR
        # ---------------------------------------------------------

        high_low = df["high"] - df["low"]

        high_close = (
            df["high"] - df["close"].shift()
        ).abs()

        low_close = (
            df["low"] - df["close"].shift()
        ).abs()

        true_range = pd.concat(
            [high_low, high_close, low_close],
            axis=1,
        ).max(axis=1)

        atr = (
            true_range
            .rolling(self.atr_period)
            .mean()
        )

        df["ATR"] = atr

        # ---------------------------------------------------------
        # Basic Bands
        # ---------------------------------------------------------

        hl2 = (df["high"] + df["low"]) / 2

        upper = hl2 + self.multiplier * atr
        lower = hl2 - self.multiplier * atr

        final_upper = upper.copy()
        final_lower = lower.copy()

        # ---------------------------------------------------------
        # Final Bands
        # ---------------------------------------------------------

        for i in range(1, len(df)):

            if (
                upper.iloc[i] < final_upper.iloc[i - 1]
                or df["close"].iloc[i - 1]
                > final_upper.iloc[i - 1]
            ):
                final_upper.iloc[i] = upper.iloc[i]
            else:
                final_upper.iloc[i] = final_upper.iloc[i - 1]

            if (
                lower.iloc[i] > final_lower.iloc[i - 1]
                or df["close"].iloc[i - 1]
                < final_lower.iloc[i - 1]
            ):
                final_lower.iloc[i] = lower.iloc[i]
            else:
                final_lower.iloc[i] = final_lower.iloc[i - 1]

        # ---------------------------------------------------------
        # Trend
        # ---------------------------------------------------------

        trend = np.ones(len(df))

        supertrend = np.zeros(len(df))

        for i in range(1, len(df)):

            if (
                trend[i - 1] == 1
                and df["close"].iloc[i]
                < final_lower.iloc[i]
            ):
                trend[i] = -1

            elif (
                trend[i - 1] == -1
                and df["close"].iloc[i]
                > final_upper.iloc[i]
            ):
                trend[i] = 1

            else:
                trend[i] = trend[i - 1]

            supertrend[i] = (
                final_lower.iloc[i]
                if trend[i] == 1
                else final_upper.iloc[i]
            )

        df["SuperTrend"] = supertrend
        df["Trend"] = trend

        # ---------------------------------------------------------
        # Signals
        # ---------------------------------------------------------

        df["signal"] = 0

        bullish = (
            (df["Trend"] == 1)
            &
            (df["Trend"].shift(1) == -1)
        )

        bearish = (
            (df["Trend"] == -1)
            &
            (df["Trend"].shift(1) == 1)
        )

        df.loc[bullish, "signal"] = 1
        df.loc[bearish, "signal"] = -1

        return df

    @staticmethod
    def description() -> str:
        return (
            "ATR-based SuperTrend strategy with non-repainting trend state."
        )