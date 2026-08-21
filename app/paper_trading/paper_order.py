"""Order models for Falcon paper trading."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from uuid import uuid4


# ----------------------------------------------------------------------
# Order Enums
# ----------------------------------------------------------------------


class OrderSide(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(StrEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class OrderStatus(StrEnum):
    PENDING = "PENDING"
    TRIGGERED = "TRIGGERED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    REJECTED = "REJECTED"


class TimeInForce(StrEnum):
    DAY = "DAY"
    GTC = "GTC"
    IOC = "IOC"
    FOK = "FOK"


# ----------------------------------------------------------------------
# Paper Order
# ----------------------------------------------------------------------


@dataclass(slots=True)
class PaperOrder:
    """
    Simulated trading order.

    Compatible with Falcon's existing PaperEngine while preparing
    for broker integrations.
    """

    symbol: str
    side: OrderSide
    quantity: int

    order_type: OrderType = OrderType.MARKET
    time_in_force: TimeInForce = TimeInForce.DAY

    limit_price: float | None = None
    stop_price: float | None = None

    stop_loss: float | None = None
    target: float | None = None
    trailing_stop_pct: float | None = None

    parent_order_id: str | None = None
    oco_group: str | None = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    order_id: str = field(default_factory=lambda: uuid4().hex)

    status: OrderStatus = OrderStatus.PENDING

    filled_quantity: int = 0
    remaining_quantity: int = field(init=False)

    filled_price: float | None = None
    filled_at: datetime | None = None

    rejection_reason: str | None = None

    def __post_init__(self) -> None:
        self.remaining_quantity = self.quantity

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> None:

        if self.quantity <= 0:
            raise ValueError("Order quantity must be positive.")

        if self.order_type is OrderType.LIMIT and self.limit_price is None:
            raise ValueError("Limit orders require limit_price.")

        if self.order_type is OrderType.STOP and self.stop_price is None:
            raise ValueError("Stop orders require stop_price.")

        if self.order_type is OrderType.STOP_LIMIT:
            if self.stop_price is None or self.limit_price is None:
                raise ValueError(
                    "STOP_LIMIT requires stop_price and limit_price."
                )

        if self.trailing_stop_pct is not None:
            if self.trailing_stop_pct <= 0:
                raise ValueError(
                    "Trailing stop must be greater than zero."
                )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def trigger(self) -> None:
        """Mark a stop order as triggered."""

        if self.status is OrderStatus.PENDING:
            self.status = OrderStatus.TRIGGERED
            self.updated_at = datetime.now()

    def fill(
        self,
        price: float,
        quantity: int,
        timestamp: datetime,
    ) -> None:
        """
        Fill all or part of an order.
        """

        if quantity > self.remaining_quantity:
            raise ValueError("Fill quantity exceeds remaining quantity.")

        self.filled_quantity += quantity
        self.remaining_quantity -= quantity

        self.filled_price = price
        self.filled_at = timestamp

        self.updated_at = timestamp

        if self.remaining_quantity == 0:
            self.status = OrderStatus.FILLED
        else:
            self.status = OrderStatus.PARTIALLY_FILLED

    def cancel(self) -> None:

        if self.status in (
            OrderStatus.FILLED,
            OrderStatus.CANCELLED,
        ):
            return

        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now()

    def reject(self, reason: str) -> None:

        self.status = OrderStatus.REJECTED
        self.rejection_reason = reason
        self.updated_at = datetime.now()

    @property
    def is_active(self) -> bool:
        return self.status in (
            OrderStatus.PENDING,
            OrderStatus.TRIGGERED,
            OrderStatus.PARTIALLY_FILLED,
        )

    def to_dict(self) -> dict:
        """
        Dashboard-friendly representation.
        """

        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "side": self.side,
            "type": self.order_type,
            "status": self.status,
            "quantity": self.quantity,
            "filled_quantity": self.filled_quantity,
            "remaining_quantity": self.remaining_quantity,
            "filled_price": self.filled_price,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }