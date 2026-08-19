from dataclasses import dataclass


@dataclass(slots=True)
class TradeStatistics:

    total_trades: int

    winning_trades: int

    losing_trades: int

    win_rate: float

    gross_profit: float

    gross_loss: float

    net_profit: float

    average_winner: float

    average_loser: float

    largest_winner: float

    largest_loser: float

    average_holding_minutes: float

    longest_trade_minutes: float

    shortest_trade_minutes: float

    average_return_pct: float

    expectancy: float