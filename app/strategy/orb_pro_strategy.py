"""
Opening Range Breakout Pro (ORB Pro)

Professional intraday ORB strategy for NSE.
"""

from __future__ import annotations

from datetime import time

import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class ORBProStrategy(BaseStrategy):
    name = "ORB Pro"

    def __init__(
        self,
        range_start: str = "09:15",
        range_end: str = "09:30",
        volume_multiplier: float = 1.5,
        min_range_pct: float = 0.003,
    ) -> None:

        self.range_start = time.fromisoformat(range_start)
        self.range_end = time.fromisoformat(range_end)
        self.volume_multiplier = volume_multiplier
        self.min_range_pct = min_range_pct

    @property
    def parameters(self) -> dict:
        return {
            "range_start": self.range_start.isoformat(),
            "range_end": self.range_end.isoformat(),
            "volume_multiplier": self.volume_multiplier,
            "min_range_pct": self.min_range_pct,
        }

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:

        df = data.copy()

        required = {"datetime", "open", "high", "low", "close", "volume"}

        missing = required - set(df.columns)

        if missing:
            raise ValueError(f"Missing columns: {missing}")

        df["datetime"] = pd.to_datetime(df["datetime"])
        df["date"] = df["datetime"].dt.date
        df["time"] = df["datetime"].dt.time

        df["VOL_MA20"] = df["volume"].rolling(20).mean()
        df["signal"] = 0

        traded_days: set = set()

        for day in df["date"].unique():

            day_mask = df["date"] == day
            day_df = df.loc[day_mask]

            opening = day_df[
                (day_df["time"] >= self.range_start)
                &
                (day_df["time"] <= self.range_end)
            ]

            if opening.empty:
                continue

            orb_high = opening["high"].max()
            orb_low = opening["low"].min()

            opening_close = opening.iloc[-1]["close"]

            range_pct = (orb_high - orb_low) / opening_close

            if range_pct < self.min_range_pct:
                continue

            after_open = day_df[day_df["time"] > self.range_end]

            for idx, row in after_open.iterrows():

                if day in traded_days:
                    break

                strong_volume = (
                    row["volume"]
                    >= row["VOL_MA20"] * self.volume_multiplier
                )

                if pd.isna(row["VOL_MA20"]):
                    continue

                if (
                    row["close"] > orb_high
                    and strong_volume
                ):

                    df.at[idx, "signal"] = 1
                    traded_days.add(day)
                    break

                if (
                    row["close"] < orb_low
                    and strong_volume
                ):

                    df.at[idx, "signal"] = -1
                    traded_days.add(day)
                    break

        return df

    @staticmethod
    def description() -> str:
        return (
            "Opening Range Breakout strategy with volume confirmation "
            "and one trade per session."
        )