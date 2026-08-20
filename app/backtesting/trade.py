"""
Trade Model

Represents a completed trade executed during a backtest.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Trade:
    """
    Represents a completed trade.
    """

    # ==========================================================
    # Trade Details
    # ==========================================================

    symbol: str
    direction: str
    quantity: int

    # ==========================================================
    # Entry
    # ==========================================================

    entry_time: datetime
    entry_price: float

    # ==========================================================
    # Exit
    # ==========================================================

    exit_time: datetime
    exit_price: float
    exit_reason: str

    # ==========================================================
    # Performance
    # ==========================================================

    pnl: float
    return_pct: float

    # ==========================================================
    # Risk Metrics
    # ==========================================================

    risk_amount: float
    reward_amount: float
    risk_reward: float

    # ==========================================================
    # Costs
    # ==========================================================

    brokerage: float
    slippage: float

    # ==========================================================
    # Portfolio
    # ==========================================================

    capital_after_trade: float

    # ==========================================================
    # Computed Properties
    # ==========================================================

    @property
    def holding_minutes(self) -> float:
        """
        Holding time in minutes.
        """

        return (
            self.exit_time - self.entry_time
        ).total_seconds() / 60

    @property
    def holding_hours(self) -> float:
        """
        Holding time in hours.
        """

        return self.holding_minutes / 60

    @property
    def is_winner(self) -> bool:
        """
        Returns True if trade is profitable.
        """

        return self.pnl > 0

    @property
    def is_loser(self) -> bool:
        """
        Returns True if trade is a losing trade.
        """

        return self.pnl < 0

    @property
    def is_breakeven(self) -> bool:
        """
        Returns True if trade closed at breakeven.
        """

        return self.pnl == 0

    # ==========================================================
    # Serialization
    # ==========================================================

    def to_dict(self) -> dict:
        """
        Convert Trade into a dictionary.

        Includes computed properties so that analytics,
        reports and dashboards can directly create
        DataFrames.
        """

        return {

            # Trade
            "symbol": self.symbol,
            "direction": self.direction,
            "quantity": self.quantity,

            # Entry
            "entry_time": self.entry_time,
            "entry_price": self.entry_price,

            # Exit
            "exit_time": self.exit_time,
            "exit_price": self.exit_price,
            "exit_reason": self.exit_reason,

            # Performance
            "pnl": self.pnl,
            "return_pct": self.return_pct,

            # Risk
            "risk_amount": self.risk_amount,
            "reward_amount": self.reward_amount,
            "risk_reward": self.risk_reward,

            # Costs
            "brokerage": self.brokerage,
            "slippage": self.slippage,

            # Portfolio
            "capital_after_trade": self.capital_after_trade,

            # Computed
            "holding_minutes": self.holding_minutes,
            "holding_hours": self.holding_hours,
            "is_winner": self.is_winner,
            "is_loser": self.is_loser,
            "is_breakeven": self.is_breakeven,
        }

    def __repr__(self) -> str:
        """
        Readable representation for debugging.
        """

        return (
            f"Trade("
            f"{self.symbol}, "
            f"{self.direction}, "
            f"PnL={self.pnl:.2f}, "
            f"Return={self.return_pct:.2f}%, "
            f"Holding={self.holding_minutes:.1f} min)"
        )