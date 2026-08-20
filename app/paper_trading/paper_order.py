"""Order models for simulated execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import uuid4


class OrderSide(StrEnum):
    """Supported order directions."""

    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    """Supported simulated order types."""

    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


class OrderStatus(StrEnum):
    """Lifecycle states for paper orders."""

    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


@dataclass(slots=True)
class PaperOrder:
    """A virtual order submitted to the paper execution engine."""

    symbol: str
    side: OrderSide
    quantity: int
    order_type: OrderType = OrderType.MARKET
    limit_price: float | None = None
    stop_price: float | None = None
    stop_loss: float | None = None
    target: float | None = None
    trailing_stop_pct: float | None = None
    created_at: datetime = field(default_factory=datetime.now)
    order_id: str = field(default_factory=lambda: uuid4().hex)
    status: OrderStatus = OrderStatus.PENDING
    filled_price: float | None = None
    filled_at: datetime | None = None
    rejection_reason: str | None = None

    def validate(self) -> None:
        """Validate order fields before the order enters the book."""
        if self.quantity <= 0:
            raise ValueError("Order quantity must be positive.")
        if self.order_type is OrderType.LIMIT and self.limit_price is None:
            raise ValueError("A limit order requires limit_price.")
        if self.order_type is OrderType.STOP and self.stop_price is None:
            raise ValueError("A stop order requires stop_price.")
