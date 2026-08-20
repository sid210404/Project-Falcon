"""Immediate simulated execution for paper orders."""

from __future__ import annotations

from datetime import datetime

from app.backtesting.execution import ExecutionEngine
from app.backtesting.position import Position
from app.backtesting.trade import Trade
from app.paper_trading.market_data_feed import LiveCandle
from app.paper_trading.paper_order import OrderSide, OrderStatus, OrderType, PaperOrder


class PaperExecutionEngine:
    """Evaluate paper-order triggers and reuse Falcon's fill-cost model."""

    def __init__(self, brokerage: float = 20.0, slippage: float = 0.001) -> None:
        self._execution = ExecutionEngine(brokerage=brokerage, slippage=slippage)

    def fill_price(self, order: PaperOrder, candle: LiveCandle) -> float | None:
        """Return a fill price when the current candle satisfies an order."""
        if order.order_type is OrderType.MARKET:
            return candle.close
        if order.order_type is OrderType.LIMIT:
            if order.side is OrderSide.BUY and candle.low <= order.limit_price:
                return float(order.limit_price)
            if order.side is OrderSide.SELL and candle.high >= order.limit_price:
                return float(order.limit_price)
        if order.order_type is OrderType.STOP:
            if order.side is OrderSide.BUY and candle.high >= order.stop_price:
                return float(order.stop_price)
            if order.side is OrderSide.SELL and candle.low <= order.stop_price:
                return float(order.stop_price)
        return None

    def open_position(self, order: PaperOrder, price: float, timestamp: datetime) -> Position:
        """Fill a buy order and construct an open Falcon position."""
        if order.side is not OrderSide.BUY:
            raise ValueError("Paper trading currently supports long entries only.")
        if order.stop_loss is None or order.target is None:
            raise ValueError("Entry orders require a stop loss and target.")
        position = self._execution.open_position(
            symbol=order.symbol, direction="LONG", quantity=order.quantity, price=price,
            entry_time=timestamp, stop_loss=order.stop_loss, target=order.target,
        )
        order.status = OrderStatus.FILLED
        order.filled_price = position.entry_price
        order.filled_at = timestamp
        return position

    def close_position(self, position: Position, price: float, timestamp: datetime, reason: str) -> Trade:
        """Close a paper position using the same slippage and cost model as backtests."""
        return self._execution.close_position(position, price, timestamp, exit_reason=reason)
