"""Normalized metrics used to compare completed backtests."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.backtesting.result import BacktestResult


@dataclass(frozen=True, slots=True)
class ComparisonMetrics:
    """Metrics extracted from a :class:`BacktestResult` for comparison."""

    net_profit: float
    return_pct: float
    win_rate: float
    profit_factor: float
    sharpe_ratio: float
    max_drawdown_pct: float
    total_trades: int

    @classmethod
    def from_result(cls, result: BacktestResult) -> "ComparisonMetrics":
        """Create a normalized metric set from a completed backtest."""
        return cls(
            net_profit=float(result.statistics["net_profit"]),
            return_pct=float(result.statistics["return_pct"]),
            win_rate=float(result.statistics["win_rate"]),
            profit_factor=float(result.statistics["profit_factor"]),
            sharpe_ratio=float(result.performance["sharpe_ratio"]),
            max_drawdown_pct=float(result.drawdown["max_drawdown_pct"]),
            total_trades=int(result.statistics["trades"]),
        )

    def to_dict(self) -> dict[str, Any]:
        """Return serializable values suitable for tabular exports."""
        return {
            "Net Profit": self.net_profit,
            "Return %": self.return_pct,
            "Win Rate %": self.win_rate,
            "Profit Factor": self.profit_factor,
            "Sharpe Ratio": self.sharpe_ratio,
            "Max Drawdown %": self.max_drawdown_pct,
            "Trades": self.total_trades,
        }
