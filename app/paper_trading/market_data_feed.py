"""Pluggable live-market-data interfaces and Yahoo Finance polling adapter."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

import pandas as pd
import yfinance as yf


@dataclass(frozen=True, slots=True)
class LiveCandle:
    """Normalized OHLCV candle emitted by a live market-data feed."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def to_dict(self) -> dict[str, object]:
        """Convert this candle to Falcon's standard dataframe schema."""
        return {"datetime": self.timestamp, "open": self.open, "high": self.high,
                "low": self.low, "close": self.close, "volume": self.volume,
                "adj_close": self.close}


class MarketDataFeed(Protocol):
    """Feed contract that polling and future streaming adapters implement."""

    def fetch_candles(self, symbol: str, exchange: str, interval: str, limit: int) -> list[LiveCandle]:
        """Return normalized candles in chronological order."""


class YahooFinancePollingFeed:
    """Yahoo Finance polling feed; replaceable by a future WebSocket adapter."""

    def fetch_candles(self, symbol: str, exchange: str, interval: str, limit: int) -> list[LiveCandle]:
        """Poll Yahoo Finance and return up to ``limit`` candles."""
        ticker = self._ticker(symbol, exchange)
        period = "2y" if interval == "1d" else "5d"
        dataframe = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
        if dataframe.empty:
            raise RuntimeError(f"No live market data available for {ticker}.")
        if isinstance(dataframe.columns, pd.MultiIndex):
            dataframe.columns = dataframe.columns.get_level_values(0)
        dataframe = dataframe.reset_index().tail(limit)
        timestamp_column = "Datetime" if "Datetime" in dataframe.columns else "Date"
        return [
            LiveCandle(timestamp=pd.Timestamp(row[timestamp_column]).to_pydatetime(), open=float(row["Open"]),
                       high=float(row["High"]), low=float(row["Low"]), close=float(row["Close"]),
                       volume=float(row["Volume"]))
            for _, row in dataframe.iterrows()
        ]

    @staticmethod
    def _ticker(symbol: str, exchange: str) -> str:
        normalized = symbol.strip().upper()
        if exchange.upper() == "NSE" and not normalized.endswith(".NS"):
            return f"{normalized}.NS"
        if exchange.upper() == "BSE" and not normalized.endswith(".BO"):
            return f"{normalized}.BO"
        return normalized
