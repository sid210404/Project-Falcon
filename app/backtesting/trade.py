from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    # Trade Details
    symbol: str
    direction: str
    quantity: int

    # Entry
    entry_time: datetime
    entry_price: float

    # Exit
    exit_time: datetime
    exit_price: float
    exit_reason: str

    # Performance
    pnl: float
    return_pct: float

    # Risk Metrics
    risk_amount: float
    reward_amount: float
    risk_reward: float

    # Costs
    brokerage: float
    slippage: float

    # Portfolio
    capital_after_trade: float

    @property
    def holding_minutes(self) -> float:
        """Holding time in minutes."""
        return (
            self.exit_time - self.entry_time
        ).total_seconds() / 60

    @property
    def is_winner(self) -> bool:
        """True if trade is profitable."""
        return self.pnl > 0

    @property
    def is_loser(self) -> bool:
        """True if trade is a loss."""
        return self.pnl < 0