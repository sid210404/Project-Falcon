"""Virtual cash, position, and equity accounting for paper trading."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.backtesting.position import Position
from app.paper_trading.paper_trade import PaperTrade


@dataclass(frozen=True, slots=True)
class EquityPoint:
    """A marked-to-market portfolio equity observation."""

    timestamp: datetime
    equity: float


@dataclass(slots=True)
class PaperPortfolio:
    """Cash-account paper portfolio supporting one strategy position per session."""

    initial_cash: float
    cash: float = field(init=False)
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
        """Return current virtual holdings by symbol."""
        if self.open_position is None:
            return {}
        return {self.open_position.symbol: self.open_position.quantity}

    @property
    def realized_pnl(self) -> float:
        """Return aggregate PnL from closed virtual trades."""
        return sum(item.trade.pnl for item in self.closed_trades)

    @property
    def unrealized_pnl(self) -> float:
        """Return current marked-to-market PnL for the open position."""
        if self.open_position is None or self.last_price is None:
            return 0.0
        return self.open_position.current_pnl(self.last_price)

    @property
    def equity(self) -> float:
        """Return cash plus the current marked value of holdings."""
        if self.open_position is None or self.last_price is None:
            return self.cash
        return self.cash + self.open_position.quantity * self.last_price

    @property
    def drawdown_pct(self) -> float:
        """Return current drawdown from the highest recorded equity point."""
        if not self.equity_curve:
            return 0.0
        peak = max(point.equity for point in self.equity_curve)
        return 0.0 if peak == 0 else (peak - self.equity) / peak * 100

    @property
    def win_rate(self) -> float:
        """Return percentage of profitable closed trades."""
        if not self.closed_trades:
            return 0.0
        winners = sum(item.trade.is_winner for item in self.closed_trades)
        return winners / len(self.closed_trades) * 100

    def open(self, position: Position) -> None:
        """Reserve virtual cash for a filled long position."""
        if self.open_position is not None:
            raise ValueError("A position is already open.")
        if position.invested_amount > self.cash:
            raise ValueError("Insufficient virtual cash for this position.")
        self.cash -= position.invested_amount
        self.open_position = position

    def close(self, paper_trade: PaperTrade) -> None:
        """Release proceeds and record a completed virtual trade."""
        trade = paper_trade.trade
        self.cash += trade.exit_price * trade.quantity - trade.brokerage
        self.closed_trades.append(paper_trade)
        self.open_position = None

    def mark_to_market(self, price: float, timestamp: datetime) -> None:
        """Update the latest market price and append an equity observation."""
        self.last_price = price
        self.equity_curve.append(EquityPoint(timestamp=timestamp, equity=self.equity))

    def summary(self) -> dict[str, float | int]:
        """Return UI-ready, accounting-owned portfolio metrics."""
        return {
            "cash": self.cash,
            "equity": self.equity,
            "realized_pnl": self.realized_pnl,
            "unrealized_pnl": self.unrealized_pnl,
            "open_positions": int(self.open_position is not None),
            "closed_trades": len(self.closed_trades),
            "win_rate": self.win_rate,
            "drawdown_pct": self.drawdown_pct,
        }
