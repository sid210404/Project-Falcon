import pandas as pd

from app.strategy.base_strategy import BaseStrategy


class ORBStrategy(BaseStrategy):

    name = "Opening Range Breakout"

    description = (
        "Buys on a breakout above the opening range and "
        "exits below the opening range low."
    )

    parameter_space = {
        "opening_candles": {
            "label": "Opening Candles",
            "values": [3, 6, 9],
            "default": 3,
        }
    }

    def __init__(self, opening_candles: int = 3):
        self.opening_candles = opening_candles

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df["signal"] = 0

        for _, day_df in df.groupby(df["datetime"].dt.date):

            opening = day_df.iloc[:self.opening_candles]

            if len(opening) < self.opening_candles:
                continue

            opening_high = opening["high"].max()
            opening_low = opening["low"].min()

            in_position = False

            for idx in day_df.index[self.opening_candles:]:

                close = df.loc[idx, "close"]

                if not in_position and close > opening_high:

                    df.loc[idx, "signal"] = 1
                    in_position = True

                elif in_position and close < opening_low:

                    df.loc[idx, "signal"] = -1
                    break

        return df