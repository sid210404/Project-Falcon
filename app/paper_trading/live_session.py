"""State model for an active paper-trading session."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import uuid4

import pandas as pd

from app.paper_trading.paper_order import PaperOrder
from app.paper_trading.paper_portfolio import PaperPortfolio
from app.strategy.base_strategy import BaseStrategy


class SessionStatus(StrEnum):
    """Allowed live-session states."""

    CREATED = "CREATED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"


@dataclass(frozen=True, slots=True)
class PaperNotification:
    """Event emitted for the live dashboard's notification stream."""

    timestamp: datetime
    message: str
    level: str = "info"


@dataclass(slots=True)
class LiveSession:
    """Runtime state kept separate from UI session state."""

    symbol: str
    exchange: str
    interval: str
    strategy: BaseStrategy
    portfolio: PaperPortfolio
    session_id: str = field(default_factory=lambda: uuid4().hex)
    status: SessionStatus = SessionStatus.CREATED
    candle_history: pd.DataFrame = field(default_factory=pd.DataFrame)
    pending_orders: list[PaperOrder] = field(default_factory=list)
    order_log: list[PaperOrder] = field(default_factory=list)
    notifications: list[PaperNotification] = field(default_factory=list)
    last_candle_at: datetime | None = None

    def notify(self, message: str, level: str = "info") -> None:
        """Append a timestamped, UI-consumable paper-trading event."""
        self.notifications.append(PaperNotification(datetime.now(), message, level))
