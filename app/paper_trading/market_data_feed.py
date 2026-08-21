"""Live market-data interfaces and Yahoo Finance polling adapter."""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol

import pandas as pd
import yfinance as yf


# ----------------------------------------------------------------------
# Candle Model
# ----------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class LiveCandle:
    """Normalized OHLCV candle."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> dict[str, object]:
        return {
            "datetime": self.timestamp,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "adj_close": self.close,
        }


# ----------------------------------------------------------------------
# Feed Contract
# ----------------------------------------------------------------------


class MarketDataFeed(Protocol):
    """Contract implemented by polling and streaming feeds."""

    def fetch_candles(
        self,
        symbol: str,
        exchange: str,
        interval: str,
        limit: int,
    ) -> list[LiveCandle]:
        ...


# ----------------------------------------------------------------------
# Yahoo Finance Adapter
# ----------------------------------------------------------------------


class YahooFinancePollingFeed:
    """
    Yahoo Finance polling feed.

    Designed so it can later be replaced by
    Zerodha/Upstox WebSocket feeds.
    """

    RETRIES = 3
    RETRY_DELAY = 2

    def fetch_candles(
        self,
        symbol: str,
        exchange: str,
        interval: str,
        limit: int,
    ) -> list[LiveCandle]:

        ticker = self._ticker(symbol, exchange)

        period = self._period(interval)

        last_error = None

        for attempt in range(self.RETRIES):

            try:

                df = yf.download(
                    ticker,
                    period=period,
                    interval=interval,
                    auto_adjust=False,
                    progress=False,
                )

                if df.empty:
                    raise RuntimeError(
                        f"No market data for {ticker}"
                    )

                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)

                df = df.reset_index()

                timestamp_column = (
                    "Datetime"
                    if "Datetime" in df.columns
                    else "Date"
                )

                df = self._drop_incomplete_candle(
                    df,
                    timestamp_column,
                    interval,
                )

                df = df.tail(limit)

                return [
                    LiveCandle(
                        timestamp=pd.Timestamp(
                            row[timestamp_column]
                        ).to_pydatetime(),
                        open=float(row["Open"]),
                        high=float(row["High"]),
                        low=float(row["Low"]),
                        close=float(row["Close"]),
                        volume=float(row["Volume"]),
                    )
                    for _, row in df.iterrows()
                ]

            except Exception as error:
                last_error = error

                if attempt < self.RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)

        raise RuntimeError(
            f"Yahoo feed failed for {ticker}: {last_error}"
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _ticker(symbol: str, exchange: str) -> str:

        symbol = symbol.strip().upper()

        exchange = exchange.upper()

        if exchange == "NSE":
            return (
                symbol
                if symbol.endswith(".NS")
                else f"{symbol}.NS"
            )

        if exchange == "BSE":
            return (
                symbol
                if symbol.endswith(".BO")
                else f"{symbol}.BO"
            )

        return symbol

    @staticmethod
    def _period(interval: str) -> str:

        mapping = {
            "1m": "7d",
            "2m": "60d",
            "5m": "60d",
            "15m": "60d",
            "30m": "60d",
            "60m": "730d",
            "90m": "60d",
            "1h": "730d",
            "1d": "5y",
            "1wk": "10y",
            "1mo": "max",
        }

        return mapping.get(interval, "60d")

    @staticmethod
    def _interval_duration(interval: str) -> timedelta:

        mapping = {
            "1m": timedelta(minutes=1),
            "2m": timedelta(minutes=2),
            "5m": timedelta(minutes=5),
            "15m": timedelta(minutes=15),
            "30m": timedelta(minutes=30),
            "60m": timedelta(hours=1),
            "90m": timedelta(minutes=90),
            "1h": timedelta(hours=1),
            "1d": timedelta(days=1),
            "1wk": timedelta(weeks=1),
        }

        return mapping.get(interval, timedelta(minutes=15))

    def _drop_incomplete_candle(
        self,
        df: pd.DataFrame,
        timestamp_column: str,
        interval: str,
    ) -> pd.DataFrame:
        """
        Remove the currently forming candle.

        This prevents duplicate strategy execution.
        """

        if df.empty:
            return df

        last_time = pd.Timestamp(
            df.iloc[-1][timestamp_column]
        ).to_pydatetime()

        now = datetime.now(last_time.tzinfo)

        duration = self._interval_duration(interval)

        if last_time + duration > now:
            return df.iloc[:-1]

        return df

    # ------------------------------------------------------------------
    # Future Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def is_market_open(exchange: str = "NSE") -> bool:
        """
        Simple market-hours helper.

        Will later be replaced with a trading-calendar service.
        """

        now = datetime.now()

        if exchange.upper() in {"NSE", "BSE"}:

            if now.weekday() >= 5:
                return False

            start = now.replace(
                hour=9,
                minute=15,
                second=0,
                microsecond=0,
            )

            end = now.replace(
                hour=15,
                minute=30,
                second=0,
                microsecond=0,
            )

            return start <= now <= end

        return True