from pathlib import Path

import pandas as pd

from app.backtesting.trade import Trade


class Portfolio:
    """
    Represents the trading portfolio and maintains
    account capital, completed trades, and equity history.
    """

    def __init__(self, capital=100000):

        self.initial_capital = float(capital)
        self.capital = float(capital)

        # Completed trades
        self.trades: list[Trade] = []

        # Portfolio equity after every closed trade
        self.equity_curve: list[float] = [self.initial_capital]

    ########################################################
    # TRADE MANAGEMENT
    ########################################################

    def add_trade(self, trade: Trade):
        """
        Add a completed trade to the portfolio.
        """

        self.capital += trade.pnl

        trade.capital_after_trade = self.capital

        self.trades.append(trade)

        self.equity_curve.append(self.capital)

    ########################################################
    # TRADE DATAFRAME
    ########################################################

    def trade_dataframe(self) -> pd.DataFrame:
        """
        Return all completed trades as a pandas DataFrame.
        """

        rows = []

        for trade in self.trades:

            rows.append(
                {
                    "symbol": trade.symbol,
                    "direction": trade.direction,
                    "quantity": trade.quantity,

                    "entry_time": trade.entry_time,
                    "entry_price": round(trade.entry_price, 2),

                    "exit_time": trade.exit_time,
                    "exit_price": round(trade.exit_price, 2),

                    "holding_minutes": round(
                        trade.holding_minutes,
                        2,
                    ),

                    "pnl": round(
                        trade.pnl,
                        2,
                    ),

                    "return_pct": round(
                        trade.return_pct,
                        2,
                    ),

                    "risk_reward": round(
                        trade.risk_reward,
                        2,
                    ),

                    "brokerage": round(
                        trade.brokerage,
                        2,
                    ),

                    "slippage": round(
                        trade.slippage,
                        2,
                    ),

                    "capital_after_trade": round(
                        trade.capital_after_trade,
                        2,
                    ),

                    "exit_reason": trade.exit_reason,
                }
            )

        return pd.DataFrame(rows)

    ########################################################
    # EXPORT
    ########################################################

    def export_trades(
        self,
        filename="reports/trades.csv",
    ):
        """
        Export completed trades to CSV.
        """

        Path(filename).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.trade_dataframe().to_csv(
            filename,
            index=False,
        )

    ########################################################
    # PORTFOLIO STATISTICS
    ########################################################

    @property
    def total_pnl(self) -> float:
        return self.capital - self.initial_capital

    @property
    def total_return_pct(self) -> float:

        if self.initial_capital == 0:
            return 0.0

        return (
            self.total_pnl
            / self.initial_capital
        ) * 100

    @property
    def total_trades(self) -> int:
        return len(self.trades)

    @property
    def winning_trades(self) -> int:
        return sum(
            trade.is_winner
            for trade in self.trades
        )

    @property
    def losing_trades(self) -> int:
        return sum(
            trade.is_loser
            for trade in self.trades
        )

    @property
    def win_rate(self) -> float:

        if self.total_trades == 0:
            return 0.0

        return (
            self.winning_trades
            / self.total_trades
        ) * 100

    @property
    def gross_profit(self) -> float:

        return sum(
            trade.pnl
            for trade in self.trades
            if trade.pnl > 0
        )

    @property
    def gross_loss(self) -> float:

        return abs(
            sum(
                trade.pnl
                for trade in self.trades
                if trade.pnl < 0
            )
        )

    @property
    def profit_factor(self) -> float:

        if self.gross_loss == 0:
            return float("inf")

        return (
            self.gross_profit
            / self.gross_loss
        )

    @property
    def average_trade(self) -> float:

        if self.total_trades == 0:
            return 0.0

        return (
            self.total_pnl
            / self.total_trades
        )