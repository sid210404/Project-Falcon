from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class BacktestConfig:
    """
    Configuration for a backtest.
    """

    exchange: str = "NSE"

    symbol: str = "RELIANCE"

    interval: str = "15m"

    start_date: date = date(2025, 1, 1)

    end_date: date = date(2025, 1, 31)

    capital: float = 100000

    brokerage: float = 20

    slippage: float = 0.001

    @property
    def days(self) -> int:
        """
        Number of days between start and end date.
        """
        return (self.end_date - self.start_date).days + 1