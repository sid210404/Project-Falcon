"""
VWAP Pullback Strategy

Intraday trend-following strategy using session VWAP.
Designed for NSE 5m/15m trading.
"""

from __future__ import annotations

import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class VWAPPullbackStrategy(BaseStrategy):
    """
    Buy:
        • Price above VWAP.
        • Pullback into VWAP.
        • Bullish recovery.

    Sell:
        • Price below VWAP.
        • Pullback into VWAP.
        • Bearish rejection.
    """

    name = "VWAP Pullback"

    def __init__(
        self,
        pullback_pct: float = 0.002,
        volume_multiplier: float = 1.2,
    ) -> None:

        self.pullback_pct = pullback_pct
        self.volume_multiplier = volume_multiplier

    @property
    def parameters(self) -> dict:
        return {
            "pullback_pct": self.pullback_pct,
            "volume_multiplier": self.volume_multiplier,
        }

    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        df = data.copy()

        required = {
            "datetime",
            "high",
            "low",
            "close",
            "volume",
        }

        missing = required - set(df.columns)

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df["date"] = pd.to_datetime(df["datetime"]).dt.date

        # ----------------------------------------------------------
        # Session VWAP
        # ----------------------------------------------------------

        typical_price = (
            df["high"] + df["low"] + df["close"]
        ) / 3

        tpv = typical_price * df["volume"]

        cumulative_tpv = tpv.groupby(df["date"]).cumsum()
        cumulative_volume = df["volume"].groupby(df["date"]).cumsum()

        df["VWAP"] = cumulative_tpv / cumulative_volume

        # ----------------------------------------------------------
        # Volume Filter
        # ----------------------------------------------------------

        df["VOL_MA20"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )

        strong_volume = (
            df["volume"]
            >= df["VOL_MA20"] * self.volume_multiplier
        )

        # ----------------------------------------------------------
        # Trend Filters
        # ----------------------------------------------------------

        bullish_trend = df["close"] > df["VWAP"]
        bearish_trend = df["close"] < df["VWAP"]

        # ----------------------------------------------------------
        # Pullback Detection
        # ----------------------------------------------------------

        near_vwap = (
            (df["close"] - df["VWAP"]).abs()
            / df["VWAP"]
            <= self.pullback_pct
        )

        bullish_recovery = (
            df["close"] > df["open"]
        )

        bearish_rejection = (
            df["close"] < df["open"]
        )

        buy = (
            bullish_trend
            &
            near_vwap
            &
            bullish_recovery
            &
            strong_volume
        )

        sell = (
            bearish_trend
            &
            near_vwap
            &
            bearish_rejection
            &
            strong_volume
        )

        df["signal"] = 0

        df.loc[buy, "signal"] = 1
        df.loc[sell, "signal"] = -1

        return df

    @staticmethod
    def description() -> str:
        return (
            "Session VWAP pullback strategy with volume confirmation."
        )