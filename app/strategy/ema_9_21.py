"""EMA 9/21 trend-following strategy."""

from __future__ import annotations

import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class EMA921Strategy(BaseStrategy):
    """
    EMA 9/21 crossover strategy.

    BUY  -> EMA9 crosses above EMA21
    SELL -> EMA9 crosses below EMA21
    HOLD -> Otherwise
    """

    name = "EMA 9/21 Trend"

    def __init__(
        self,
        fast_period: int = 9,
        slow_period: int = 21,
    ) -> None:

        self.fast_period = fast_period
        self.slow_period = slow_period

    @property
    def parameters(self) -> dict:
        return {
            "fast_period": self.fast_period,
            "slow_period": self.slow_period,
        }

    def generate_signals(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:

        df = data.copy()

        required = {"close", "datetime"}

        missing = required - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        df["EMA_FAST"] = (
            df["close"]
            .ewm(
                span=self.fast_period,
                adjust=False,
            )
            .mean()
        )

        df["EMA_SLOW"] = (
            df["close"]
            .ewm(
                span=self.slow_period,
                adjust=False,
            )
            .mean()
        )

        bullish = (
            (df["EMA_FAST"] > df["EMA_SLOW"])
            &
            (df["EMA_FAST"].shift(1) <= df["EMA_SLOW"].shift(1))
        )

        bearish = (
            (df["EMA_FAST"] < df["EMA_SLOW"])
            &
            (df["EMA_FAST"].shift(1) >= df["EMA_SLOW"].shift(1))
        )

        df["signal"] = 0

        df.loc[bullish, "signal"] = 1
        df.loc[bearish, "signal"] = -1

        return df

    @staticmethod
    def description() -> str:
        return (
            "Trend-following EMA crossover strategy using "
            "9 and 21-period exponential moving averages."
        )