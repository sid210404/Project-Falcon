"""Bidirectional candle-by-candle live paper-trading engine."""

from __future__ import annotations

import logging

from app.backtesting.exit_manager import ExitManager
from app.backtesting.risk_manager import RiskManager
from app.paper_trading.execution_engine import PaperExecutionEngine
from app.paper_trading.live_session import LiveSession, SessionStatus
from app.paper_trading.market_data_feed import LiveCandle
from app.paper_trading.paper_order import (
    OrderSide,
    OrderStatus,
    PaperOrder,
)
from app.paper_trading.paper_trade import PaperTrade
from app.paper_trading.strategy_runner import StrategyRunner

LOGGER = logging.getLogger(__name__)


class PaperEngine:
    """Execute a strategy against completed candles."""

    def __init__(
        self,
        brokerage: float = 20.0,
        slippage: float = 0.001,
    ) -> None:
        self._execution = PaperExecutionEngine(
            brokerage=brokerage,
            slippage=slippage,
        )
        self._risk = RiskManager()
        self._exit = ExitManager()

    # ------------------------------------------------------------------
    # Warm-up
    # ------------------------------------------------------------------

    def seed_history(
        self,
        session: LiveSession,
        candles: list[LiveCandle],
    ) -> None:
        """Warm indicators without executing trades."""

        import pandas as pd

        session.candle_history = pd.DataFrame(
            [c.to_dict() for c in candles]
        )

        if getattr(session, "runner", None) is None:
            session.runner = StrategyRunner(session.strategy)

        if candles:
            session.last_candle_at = candles[-1].timestamp
            session.portfolio.mark_to_market(
                candles[-1].close,
                candles[-1].timestamp,
            )

    # ------------------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------------------

    def on_candle(
        self,
        session: LiveSession,
        candle: LiveCandle,
    ) -> None:
        """Process one completed candle."""

        import pandas as pd

        if (
            session.status is not SessionStatus.RUNNING
            or session.last_candle_at == candle.timestamp
        ):
            return

        session.candle_history = pd.concat(
            [
                session.candle_history,
                pd.DataFrame([candle.to_dict()]),
            ],
            ignore_index=True,
        )

        session.last_candle_at = candle.timestamp

        self._process_pending_orders(session, candle)

        signal_event = session.runner.run(session.candle_history)

        if signal_event is None:
            session.portfolio.mark_to_market(
                candle.close,
                candle.timestamp,
            )
            return

        latest = signal_event.candle
        signal = signal_event.signal

        position = session.portfolio.open_position

        # --------------------------------------------------------------
        # No position
        # --------------------------------------------------------------

        if position is None:

            if signal == 1:
                self._open_position(
                    session,
                    latest,
                    OrderSide.BUY,
                )

            elif signal == -1:
                self._open_position(
                    session,
                    latest,
                    OrderSide.SELL,
                )

        # --------------------------------------------------------------
        # Existing position
        # --------------------------------------------------------------

        else:

            self._apply_trailing_stop(
                session,
                candle.close,
            )

            should_exit, exit_price, reason = self._exit.should_exit(
                position,
                latest,
            )

            if should_exit:

                self._close_position(
                    session,
                    float(exit_price),
                    candle.timestamp,
                    reason,
                )

                # Re-enter immediately if signal persists

                if signal == 1:
                    self._open_position(
                        session,
                        latest,
                        OrderSide.BUY,
                    )

                elif signal == -1:
                    self._open_position(
                        session,
                        latest,
                        OrderSide.SELL,
                    )

            else:

                if (
                    position.direction == "LONG"
                    and signal == -1
                ):

                    self._close_position(
                        session,
                        candle.close,
                        candle.timestamp,
                        "REVERSAL",
                    )

                    self._open_position(
                        session,
                        latest,
                        OrderSide.SELL,
                    )

                elif (
                    position.direction == "SHORT"
                    and signal == 1
                ):

                    self._close_position(
                        session,
                        candle.close,
                        candle.timestamp,
                        "REVERSAL",
                    )

                    self._open_position(
                        session,
                        latest,
                        OrderSide.BUY,
                    )

        session.portfolio.mark_to_market(
            candle.close,
            candle.timestamp,
        )

    # ------------------------------------------------------------------
    # Strategy Entries
    # ------------------------------------------------------------------

    def _open_position(
        self,
        session: LiveSession,
        candle,
        side: OrderSide,
    ) -> None:

        atr = float(candle["ATR_14"])
        price = float(candle["close"])

        direction = (
            "LONG"
            if side is OrderSide.BUY
            else "SHORT"
        )

        stop_loss = self._risk.calculate_stop_loss(
            price,
            atr,
            direction,
        )

        target = self._risk.calculate_target(
            price,
            stop_loss,
            direction,
        )

        quantity = self._risk.calculate_position_size(
            session.portfolio.equity,
            price,
            stop_loss,
        )

        quantity = min(
            quantity,
            max(1, int(session.portfolio.equity / price)),
        )

        if quantity <= 0:

            session.notify(
                "Entry skipped: insufficient capital.",
                "warning",
            )

            return

        order = PaperOrder(
            symbol=session.symbol,
            side=side,
            quantity=quantity,
            stop_loss=stop_loss,
            target=target,
        )

        session.order_log.append(order)

        position = self._execution.open_position(
            order,
            price,
            candle["datetime"],
        )

        session.portfolio.open(position)

        session.notify(
            f"{direction} {quantity} {session.symbol} @ {price:.2f}",
            "success",
        )

        LOGGER.info(
            "%s opened on %s",
            direction,
            session.symbol,
        )

    # ------------------------------------------------------------------
    # Close Position
    # ------------------------------------------------------------------

    def _close_position(
        self,
        session: LiveSession,
        price: float,
        timestamp,
        reason: str,
    ) -> None:

        position = session.portfolio.open_position

        if position is None:
            return

        trade = self._execution.close_position(
            position,
            price,
            timestamp,
            reason,
        )

        session.portfolio.close(
            PaperTrade(session.session_id, trade)
        )

        session.notify(
            f"{reason} | P&L {trade.pnl:.2f}",
            "success" if trade.pnl >= 0 else "warning",
        )

        LOGGER.info("Position closed (%s)", reason)

    # ------------------------------------------------------------------
    # Manual Orders
    # ------------------------------------------------------------------

    def submit_order(
        self,
        session: LiveSession,
        order: PaperOrder,
    ) -> None:

        order.validate()

        session.pending_orders.append(order)
        session.order_log.append(order)

        session.notify(
            f"{order.side} {order.order_type} queued."
        )

    def _process_pending_orders(
        self,
        session: LiveSession,
        candle: LiveCandle,
    ) -> None:

        for order in list(session.pending_orders):

            price = self._execution.fill_price(order, candle)

            if price is None:
                continue

            session.pending_orders.remove(order)

            position = session.portfolio.open_position

            if position is None:

                if (
                    order.stop_loss is None
                    or order.target is None
                ):

                    order.status = OrderStatus.REJECTED
                    order.rejection_reason = (
                        "Stop loss and target required."
                    )

                    continue

                try:

                    new_position = self._execution.open_position(
                        order,
                        price,
                        candle.timestamp,
                    )

                    session.portfolio.open(new_position)

                except ValueError as error:

                    order.status = OrderStatus.REJECTED
                    order.rejection_reason = str(error)

                else:

                    session.notify(
                        f"{order.side} filled @ {price:.2f}",
                        "success",
                    )

            else:

                opposite = (
                    position.direction == "LONG"
                    and order.side is OrderSide.SELL
                ) or (
                    position.direction == "SHORT"
                    and order.side is OrderSide.BUY
                )

                if opposite:

                    self._close_position(
                        session,
                        price,
                        candle.timestamp,
                        "MANUAL_ORDER",
                    )

                else:

                    order.status = OrderStatus.REJECTED
                    order.rejection_reason = (
                        "Conflicts with open position."
                    )

    # ------------------------------------------------------------------
    # Trailing Stop
    # ------------------------------------------------------------------

    @staticmethod
    def _apply_trailing_stop(
        session: LiveSession,
        price: float,
    ) -> None:

        position = session.portfolio.open_position

        if position is None:
            return

        trailing = next(
            (
                order.trailing_stop_pct
                for order in reversed(session.order_log)
                if order.trailing_stop_pct
            ),
            None,
        )

        if trailing is None:
            return

        if position.direction == "LONG":

            position.stop_loss = max(
                position.stop_loss,
                price * (1 - trailing / 100),
            )

        else:

            position.stop_loss = min(
                position.stop_loss,
                price * (1 + trailing / 100),
            )