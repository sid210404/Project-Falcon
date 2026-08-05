import numpy as np
import pandas as pd


class IndicatorEngine:

    @staticmethod
    def sma(df: pd.DataFrame, period: int = 20, column: str = "close"):
        df[f"SMA_{period}"] = (
            df[column]
            .rolling(window=period)
            .mean()
        )
        return df

    @staticmethod
    def ema(df: pd.DataFrame, period: int = 20, column: str = "close"):
        df[f"EMA_{period}"] = (
            df[column]
            .ewm(span=period, adjust=False)
            .mean()
        )
        return df

    @staticmethod
    def rsi(df: pd.DataFrame, period: int = 14, column: str = "close"):

        delta = df[column].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        df[f"RSI_{period}"] = 100 - (100 / (1 + rs))

        return df

    @staticmethod
    def atr(df: pd.DataFrame, period: int = 14):

        high_low = df["high"] - df["low"]

        high_close = np.abs(df["high"] - df["close"].shift())

        low_close = np.abs(df["low"] - df["close"].shift())

        ranges = pd.concat(
            [high_low, high_close, low_close],
            axis=1
        )

        true_range = ranges.max(axis=1)

        df[f"ATR_{period}"] = (
            true_range
            .rolling(period)
            .mean()
        )

        return df

    @staticmethod
    def vwap(df: pd.DataFrame):

        typical_price = (
            df["high"] +
            df["low"] +
            df["close"]
        ) / 3

        cumulative_volume = df["volume"].cumsum()

        cumulative_tp_volume = (
            typical_price *
            df["volume"]
        ).cumsum()

        df["VWAP"] = (
            cumulative_tp_volume /
            cumulative_volume
        )

        return df

    @staticmethod
    def bollinger(df: pd.DataFrame, period: int = 20, std: int = 2):

        middle = (
            df["close"]
            .rolling(period)
            .mean()
        )

        deviation = (
            df["close"]
            .rolling(period)
            .std()
        )

        df["BB_MIDDLE"] = middle
        df["BB_UPPER"] = middle + std * deviation
        df["BB_LOWER"] = middle - std * deviation

        return df

    @staticmethod
    def macd(
        df: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9,
    ):

        ema_fast = (
            df["close"]
            .ewm(span=fast, adjust=False)
            .mean()
        )

        ema_slow = (
            df["close"]
            .ewm(span=slow, adjust=False)
            .mean()
        )

        macd = ema_fast - ema_slow

        signal_line = (
            macd
            .ewm(span=signal, adjust=False)
            .mean()
        )

        histogram = macd - signal_line

        df["MACD"] = macd
        df["MACD_SIGNAL"] = signal_line
        df["MACD_HIST"] = histogram

        return df

    @staticmethod
    def apply_all(df: pd.DataFrame):
        """
        Apply all indicators required by Falcon.
        """

        df = IndicatorEngine.sma(df)
        df = IndicatorEngine.ema(df)
        df = IndicatorEngine.rsi(df)
        df = IndicatorEngine.atr(df)
        df = IndicatorEngine.vwap(df)
        df = IndicatorEngine.bollinger(df)
        df = IndicatorEngine.macd(df)

        # Remove rows with NaN values from rolling indicators
        df = df.dropna().reset_index(drop=True)

        return df