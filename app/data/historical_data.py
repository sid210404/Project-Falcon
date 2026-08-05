from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf


class HistoricalData:
    """
    Downloads historical OHLCV data from Yahoo Finance.
    """

    @staticmethod
    def fetch(
        symbol: str,
        exchange: str = "NSE",
        interval: str = "5m",
        days: int = 30,
    ) -> pd.DataFrame:
        """
        Fetch historical OHLCV data from Yahoo Finance.
        """

        # ----------------------------------------------------------
        # Validate symbol
        # ----------------------------------------------------------

        if symbol is None:
            raise ValueError("Stock symbol cannot be empty.")

        symbol = symbol.strip().upper()

        if symbol == "":
            raise ValueError("Stock symbol cannot be empty.")

        # ----------------------------------------------------------
        # Yahoo ticker
        # ----------------------------------------------------------

        exchange = exchange.upper()

        if exchange == "NSE":

            yahoo_symbol = (
                symbol
                if symbol.endswith(".NS")
                else f"{symbol}.NS"
            )

        elif exchange == "BSE":

            yahoo_symbol = (
                symbol
                if symbol.endswith(".BO")
                else f"{symbol}.BO"
            )

        else:

            yahoo_symbol = symbol

        print(f"Downloading Yahoo Symbol: {yahoo_symbol}")

        # ----------------------------------------------------------
        # Download
        # ----------------------------------------------------------

        end = datetime.now()
        start = end - timedelta(days=days)

        df = yf.download(
            tickers=yahoo_symbol,
            start=start,
            end=end,
            interval=interval,
            auto_adjust=False,
            progress=False,
        )

        # ----------------------------------------------------------
        # Validate
        # ----------------------------------------------------------

        if df.empty:

            raise ValueError(
                f"""
No historical data found.

Symbol: {yahoo_symbol}
Interval: {interval}

Possible reasons:

• Invalid symbol
• Interval exceeds Yahoo limits
• Market holiday
• Yahoo Finance unavailable
""".strip()
            )

        # ----------------------------------------------------------
        # Flatten columns
        # ----------------------------------------------------------

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df.columns.name = None

        df.reset_index(inplace=True)

        # ----------------------------------------------------------
        # Rename
        # ----------------------------------------------------------

        df.rename(
            columns={
                "Datetime": "datetime",
                "Date": "datetime",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            },
            inplace=True,
        )

        # ----------------------------------------------------------
        # Missing adjusted close
        # ----------------------------------------------------------

        if "adj_close" not in df.columns:
            df["adj_close"] = df["close"]

        # ----------------------------------------------------------
        # Keep required columns
        # ----------------------------------------------------------

        df = df[
            [
                "datetime",
                "open",
                "high",
                "low",
                "close",
                "adj_close",
                "volume",
            ]
        ]

        df.sort_values("datetime", inplace=True)

        df.reset_index(drop=True, inplace=True)

        print(f"Downloaded {len(df)} candles")

        return df