from dataclasses import dataclass
from datetime import datetime


@dataclass
class Position:
    """
    Represents an open trading position.
    """

    symbol: str
    direction: str          # LONG / SHORT
    quantity: int

    entry_price: float
    entry_time: datetime

    stop_loss: float
    target: float

    is_open: bool = True

    exit_price: float | None = None
    exit_time: datetime | None = None

    realized_pnl: float = 0.0

    @property
    def invested_amount(self) -> float:
        """Total capital invested."""
        return self.entry_price * self.quantity

    def current_pnl(self, current_price: float) -> float:
        """
        Returns unrealized PnL.
        """

        if self.direction == "LONG":
            return (current_price - self.entry_price) * self.quantity

        return (self.entry_price - current_price) * self.quantity

    @property
    def return_pct(self) -> float:
        """
        Percentage return after position is closed.
        """

        if self.invested_amount == 0:
            return 0.0

        return (self.realized_pnl / self.invested_amount) * 100

    def close(
        self,
        exit_price: float,
        exit_time: datetime,
    ):
        """
        Close the position.
        """

        if not self.is_open:
            raise ValueError("Position is already closed.")

        self.exit_price = exit_price
        self.exit_time = exit_time
        self.is_open = False

        self.realized_pnl = self.current_pnl(exit_price)