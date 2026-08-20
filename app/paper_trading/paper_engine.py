"""Candle-by-candle live paper-trading engine."""

from __future__ import annotations

import logging

import pandas as pd

from app.backtesting.exit_manager import ExitManager
from app.backtesting.risk_manager import RiskManager
from app.indicators.indicator_engine import IndicatorEngine
from app.paper_trading.execution_engine import PaperExecutionEngine
from app.paper_trading.live_session import LiveSession, SessionStatus
from app.paper_trading.market_data_feed import LiveCandle
from app.paper_trading.paper_order import OrderSide, OrderStatus, PaperOrder
from app.paper_trading.paper_trade import PaperTrade


LOGGER = logging.getLogger(__name__)


class PaperEngine:
    """Execute a registered strategy against one completed candle at a time."""

    def __init__(self, brokerage: float = 20.0, slippage: float = 0.001) -> None:
        self._execution = PaperExecutionEngine(brokerage=brokerage, slippage=slippage)
        self._risk = RiskManager()
        self._exit = ExitManager()

    def seed_history(self, session: LiveSession, candles: list[LiveCandle]) -> None:
        """Load historical candles for indicator warm-up without placing orders."""
        session.candle_history = pd.DataFrame([candle.to_dict() for candle in candles])
        if candles:
            session.last_candle_at = candles[-1].timestamp
            session.portfolio.mark_to_market(candles[-1].close, candles[-1].timestamp)

    def on_candle(self, session: LiveSession, candle: LiveCandle) -> None:
        """Process one new completed candle when the session is running."""
        if session.status is not SessionStatus.RUNNING or session.last_candle_at == candle.timestamp:
            return
        session.candle_history = pd.concat([session.candle_history, pd.DataFrame([candle.to_dict()])], ignore_index=True)
        session.last_candle_at = candle.timestamp
        self._process_pending_orders(session, candle)
        prepared = IndicatorEngine.apply_all(session.candle_history.copy())
        if prepared.empty:
            session.portfolio.mark_to_market(candle.close, candle.timestamp)
            return
        latest = session.strategy.generate_signals(prepared).iloc[-1]
        position = session.portfolio.open_position
        if position is None and int(latest["signal"]) == 1:
            self._open_strategy_position(session, latest)
        elif position is not None:
            self._apply_trailing_stop(position, candle.close, session)
            should_exit, exit_price, reason = self._exit.should_exit(position, latest)
            if should_exit:
                self._close_position(session, float(exit_price), candle.timestamp, reason)
        session.portfolio.mark_to_market(candle.close, candle.timestamp)

    def submit_order(self, session: LiveSession, order: PaperOrder) -> None:
        """Validate and enqueue a manual paper order for the next candle."""
        order.validate()
        session.pending_orders.append(order)
        session.order_log.append(order)
        session.notify(f"{order.side} {order.order_type} order submitted.")

    def _open_strategy_position(self, session: LiveSession, candle: pd.Series) -> None:
        atr, price = float(candle["ATR_14"]), float(candle["close"])
        stop_loss = self._risk.calculate_stop_loss(price, atr, "LONG")
        target = self._risk.calculate_target(price, stop_loss, "LONG")
        quantity = min(self._risk.calculate_position_size(session.portfolio.equity, price, stop_loss), int(session.portfolio.cash / price))
        if quantity <= 0:
            session.notify("Buy signal skipped: insufficient virtual cash.", "warning")
            return
        order = PaperOrder(symbol=session.symbol, side=OrderSide.BUY, quantity=quantity, stop_loss=stop_loss, target=target)
        session.order_log.append(order)
        position = self._execution.open_position(order, price, candle["datetime"])
        session.portfolio.open(position)
        session.notify(f"BUY {quantity} {session.symbol} at {position.entry_price:.2f}.", "success")
        LOGGER.info("Paper position opened for %s", session.symbol)

    def _close_position(self, session: LiveSession, price: float, timestamp, reason: str) -> None:
        position = session.portfolio.open_position
        if position is None:
            return
        trade = self._execution.close_position(position, price, timestamp, reason)
        session.portfolio.close(PaperTrade(session.session_id, trade))
        session.notify(f"Position closed: {reason}; PnL {trade.pnl:.2f}.", "success" if trade.pnl >= 0 else "warning")
        LOGGER.info("Paper position closed for %s: %s", session.symbol, reason)

    def _process_pending_orders(self, session: LiveSession, candle: LiveCandle) -> None:
        for order in list(session.pending_orders):
            price = self._execution.fill_price(order, candle)
            if price is None:
                continue
            session.pending_orders.remove(order)
            if order.side is OrderSide.BUY and session.portfolio.open_position is None:
                if order.stop_loss is None or order.target is None:
                    order.status, order.rejection_reason = OrderStatus.REJECTED, "Entry requires stop loss and target."
                    continue
                position = self._execution.open_position(order, price, candle.timestamp)
                try:
                    session.portfolio.open(position)
                except ValueError as error:
                    order.status, order.rejection_reason = OrderStatus.REJECTED, str(error)
                else:
                    session.notify(f"BUY filled at {position.entry_price:.2f}.", "success")
            elif order.side is OrderSide.SELL and session.portfolio.open_position is not None:
                self._close_position(session, price, candle.timestamp, "MANUAL_ORDER")
            else:
                order.status, order.rejection_reason = OrderStatus.REJECTED, "Order conflicts with current position state."

    @staticmethod
    def _apply_trailing_stop(position, price: float, session: LiveSession) -> None:
        trailing = next((order.trailing_stop_pct for order in session.order_log if order.trailing_stop_pct), None)
        if trailing is not None:
            position.stop_loss = max(position.stop_loss, price * (1 - trailing / 100))
