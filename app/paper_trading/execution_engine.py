"""Execution adapter for live paper trading."""

from __future__ import annotations

from datetime import datetime

from app.backtesting.execution import ExecutionEngine
from app.backtesting.position import Position
from app.backtesting.trade import Trade
from app.paper_trading.market_data_feed import LiveCandle
from app.paper_trading.paper_order import OrderSide, OrderStatus, OrderType, PaperOrder


class PaperExecutionEngine:
    """Evaluate paper orders and reuse Falcon's fill-cost model.

    Supports both long and short entries. Position accounting is delegated to
    the existing Falcon ``Position`` model and portfolio layer.
    """

    def __init__(
        self,
        brokerage: float = 20.0,
        slippage: float = 0.001,
    ) -> None:
        self._execution = ExecutionEngine(
            brokerage=brokerage,
            slippage=slippage,
        )

    def fill_price(
        self,
        order: PaperOrder,
        candle: LiveCandle,
    ) -> float | None:
        """Return a simulated fill price when the candle triggers the order."""

        if order.order_type is OrderType.MARKET:
            return candle.close

        if order.order_type is OrderType.LIMIT:
            if (
                order.side is OrderSide.BUY
                and order.limit_price is not None
                and candle.low <= order.limit_price
            ):
                return float(order.limit_price)

            if (
                order.side is OrderSide.SELL
                and order.limit_price is not None
                and candle.high >= order.limit_price
            ):
                return float(order.limit_price)

        if order.order_type is OrderType.STOP:
            if (
                order.side is OrderSide.BUY
                and order.stop_price is not None
                and candle.high >= order.stop_price
            ):
                return float(order.stop_price)

            if (
                order.side is OrderSide.SELL
                and order.stop_price is not None
                and candle.low <= order.stop_price
            ):
                return float(order.stop_price)

        return None

    def open_position(
        self,
        order: PaperOrder,
        price: float,
        timestamp: datetime,
    ) -> Position:
        """Create a filled LONG or SHORT paper position."""

        if order.stop_loss is None or order.target is None:
            raise ValueError(
                "Entry orders require both stop_loss and target."
            )

        direction = (
            "LONG"
            if order.side is OrderSide.BUY
            else "SHORT"
        )

        position = self._execution.open_position(
            symbol=order.symbol,
            direction=direction,
            quantity=order.quantity,
            price=price,
            entry_time=timestamp,
            stop_loss=order.stop_loss,
            target=order.target,
        )

        order.status = OrderStatus.FILLED
        order.filled_price = position.entry_price
        order.filled_at = timestamp

        return position

    def close_position(
        self,
        position: Position,
        price: float,
        timestamp: datetime,
        reason: str,
    ) -> Trade:
        """Close a paper position using Falcon's existing execution model."""

        return self._execution.close_position(
            position,
            price,
            timestamp,
            exit_reason=reason,
        )