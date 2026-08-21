"""Virtual cash, margin and equity accounting for paper trading."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.backtesting.position import Position
from app.paper_trading.paper_trade import PaperTrade


@dataclass(frozen=True, slots=True)
class EquityPoint:
    timestamp: datetime
    equity: float


@dataclass(slots=True)
class PaperPortfolio:
    """
    Paper trading portfolio.

    Supports:
    - LONG positions
    - SHORT positions
    - Margin reservation
    - Realized PnL
    - Unrealized PnL
    - Drawdown
    """

    initial_cash: float
    margin_requirement: float = 0.20

    cash: float = field(init=False)
    reserved_margin: float = field(default=0.0)

    open_position: Position | None = None

    closed_trades: list[PaperTrade] = field(default_factory=list)
    equity_curve: list[EquityPoint] = field(default_factory=list)

    last_price: float | None = None

    def __post_init__(self) -> None:
        if self.initial_cash <= 0:
            raise ValueError("initial_cash must be positive.")

        self.cash = float(self.initial_cash)

    @property
    def holdings(self) -> dict[str, int]:
        if self.open_position is None:
            return {}

        qty = self.open_position.quantity

        if self.open_position.direction == "SHORT":
            qty = -qty

        return {self.open_position.symbol: qty}

    @property
    def realized_pnl(self) -> float:
        return sum(item.trade.pnl for item in self.closed_trades)

    @property
    def unrealized_pnl(self) -> float:
        if self.open_position is None or self.last_price is None:
            return 0.0

        return self.open_position.current_pnl(self.last_price)

    @property
    def equity(self) -> float:
        """
        Equity = Free Cash + Reserved Margin + Unrealized PnL
        """

        return (
            self.cash
            + self.reserved_margin
            + self.unrealized_pnl
        )

    @property
    def available_cash(self) -> float:
        return self.cash

    @property
    def exposure(self) -> float:
        if self.open_position is None:
            return 0.0

        return self.open_position.quantity * self.open_position.entry_price

    @property
    def drawdown_pct(self) -> float:
        if not self.equity_curve:
            return 0.0

        peak = max(point.equity for point in self.equity_curve)

        if peak == 0:
            return 0.0

        return (peak - self.equity) / peak * 100

    @property
    def win_rate(self) -> float:
        if not self.closed_trades:
            return 0.0

        winners = sum(item.trade.is_winner for item in self.closed_trades)

        return winners / len(self.closed_trades) * 100

    def open(self, position: Position) -> None:
        if self.open_position is not None:
            raise ValueError("A position is already open.")

        exposure = position.entry_price * position.quantity

        if position.direction == "LONG":
            if exposure > self.cash:
                raise ValueError("Insufficient virtual cash.")

            self.cash -= exposure

        else:
            margin = exposure * self.margin_requirement

            if margin > self.cash:
                raise ValueError("Insufficient virtual margin.")

            self.cash -= margin
            self.reserved_margin = margin

        self.open_position = position

    def close(self, paper_trade: PaperTrade) -> None:
        if self.open_position is None:
            raise ValueError("No open position.")

        trade = paper_trade.trade
        position = self.open_position

        if position.direction == "LONG":
            proceeds = trade.exit_price * trade.quantity

            self.cash += proceeds - trade.brokerage

        else:
            self.cash += self.reserved_margin
            self.cash += trade.pnl - trade.brokerage
            self.reserved_margin = 0.0

        self.closed_trades.append(paper_trade)
        self.open_position = None

    def mark_to_market(
        self,
        price: float,
        timestamp: datetime,
    ) -> None:

        self.last_price = price

        self.equity_curve.append(
            EquityPoint(
                timestamp=timestamp,
                equity=self.equity,
            )
        )

    def summary(self) -> dict[str, float | int]:

        return {
            "cash": round(self.cash, 2),
            "available_cash": round(self.available_cash, 2),
            "reserved_margin": round(self.reserved_margin, 2),
            "equity": round(self.equity, 2),
            "exposure": round(self.exposure, 2),
            "realized_pnl": round(self.realized_pnl, 2),
            "unrealized_pnl": round(self.unrealized_pnl, 2),
            "open_positions": int(self.open_position is not None),
            "closed_trades": len(self.closed_trades),
            "win_rate": round(self.win_rate, 2),
            "drawdown_pct": round(self.drawdown_pct, 2),
        }