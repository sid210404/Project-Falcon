"""Workflow service for live paper-trading sessions."""

from __future__ import annotations

import logging

from app.paper_trading.live_session import LiveSession, SessionStatus
from app.paper_trading.market_data_feed import MarketDataFeed, YahooFinancePollingFeed
from app.paper_trading.paper_engine import PaperEngine
from app.paper_trading.paper_order import PaperOrder
from app.paper_trading.paper_portfolio import PaperPortfolio
from app.strategy.base_strategy import BaseStrategy


LOGGER = logging.getLogger(__name__)


class PaperTradingService:
    """Own the lifecycle of a paper session and its market-data polling."""

    _WARMUP_CANDLES = 150

    def __init__(self, feed: MarketDataFeed | None = None, engine: PaperEngine | None = None) -> None:
        self._feed = feed or YahooFinancePollingFeed()
        self._engine = engine or PaperEngine()

    def create_session(
        self, symbol: str, exchange: str, interval: str, strategy: BaseStrategy, initial_cash: float
    ) -> LiveSession:
        """Create a session and warm indicators with recent market history."""
        session = LiveSession(symbol=symbol, exchange=exchange, interval=interval, strategy=strategy, portfolio=PaperPortfolio(initial_cash))
        candles = self._feed.fetch_candles(symbol, exchange, interval, self._WARMUP_CANDLES)
        self._engine.seed_history(session, candles)
        session.notify(f"Session created with {len(candles)} warm-up candles.")
        return session

    def start(self, session: LiveSession) -> None:
        """Start or resume candle processing."""
        if session.status is SessionStatus.STOPPED:
            raise ValueError("Stopped sessions cannot be restarted; create a new session.")
        session.status = SessionStatus.RUNNING
        session.notify("Paper trading started.", "success")

    def pause(self, session: LiveSession) -> None:
        """Pause processing while retaining account state."""
        if session.status is SessionStatus.RUNNING:
            session.status = SessionStatus.PAUSED
            session.notify("Paper trading paused.")

    def stop(self, session: LiveSession) -> None:
        """Stop a session; positions remain available for review only."""
        session.status = SessionStatus.STOPPED
        session.notify("Paper trading stopped.", "warning")

    def poll(self, session: LiveSession) -> None:
        """Poll the provider and process every newly available completed candle."""
        if session.status is not SessionStatus.RUNNING:
            return
        candles = self._feed.fetch_candles(session.symbol, session.exchange, session.interval, limit=2)
        for candle in candles:
            if session.last_candle_at is None or candle.timestamp > session.last_candle_at:
                self._engine.on_candle(session, candle)

    def submit_order(self, session: LiveSession, order: PaperOrder) -> None:
        """Submit a manual virtual order to the paper engine."""
        self._engine.submit_order(session, order)

    @staticmethod
    def reset() -> None:
        """Provide an explicit reset hook for UI-owned session-state removal."""
        LOGGER.info("Paper session reset requested")
