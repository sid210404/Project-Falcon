import pandas as pd


class Statistics:
    """
    Generates portfolio performance statistics.
    """

    @staticmethod
    def _to_python(value):
        """
        Convert NumPy scalar types to native Python types.
        """
        if hasattr(value, "item"):
            return value.item()
        return value

    @staticmethod
    def summary(portfolio):

        if portfolio.total_trades == 0:
            return {
                "initial_capital": portfolio.initial_capital,
                "final_capital": portfolio.capital,
                "net_profit": 0.0,
                "return_pct": 0.0,
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0.0,
                "average_trade": 0.0,
                "average_win": 0.0,
                "average_loss": 0.0,
                "best_trade": 0.0,
                "worst_trade": 0.0,
                "gross_profit": 0.0,
                "gross_loss": 0.0,
                "profit_factor": 0.0,
                "average_holding_minutes": 0.0,
                "average_rr": 0.0,
                "total_brokerage": 0.0,
                "total_slippage": 0.0,
            }

        df = pd.DataFrame(
            [trade.to_dict() for trade in portfolio.trades]
        )

        wins = df[df["pnl"] > 0]
        losses = df[df["pnl"] < 0]

        average_holding = sum(
            trade.holding_minutes
            for trade in portfolio.trades
        ) / portfolio.total_trades

        average_rr = df["risk_reward"].mean()

        summary = {

            "initial_capital":
                round(portfolio.initial_capital, 2),

            "final_capital":
                round(portfolio.capital, 2),

            "net_profit":
                round(portfolio.total_pnl, 2),

            "return_pct":
                round(portfolio.total_return_pct, 2),

            "trades":
                portfolio.total_trades,

            "wins":
                portfolio.winning_trades,

            "losses":
                portfolio.losing_trades,

            "win_rate":
                round(
                    (
                        portfolio.winning_trades
                        / portfolio.total_trades
                    ) * 100,
                    2,
                ),

            "average_trade":
                round(df["pnl"].mean(), 2),

            "average_win":
                round(wins["pnl"].mean(), 2)
                if not wins.empty
                else 0.0,

            "average_loss":
                round(losses["pnl"].mean(), 2)
                if not losses.empty
                else 0.0,

            "best_trade":
                round(df["pnl"].max(), 2),

            "worst_trade":
                round(df["pnl"].min(), 2),

            "gross_profit":
                round(portfolio.gross_profit, 2),

            "gross_loss":
                round(portfolio.gross_loss, 2),

            "profit_factor":
                round(portfolio.profit_factor, 2)
                if portfolio.profit_factor != float("inf")
                else float("inf"),

            "average_holding_minutes":
                round(average_holding, 2),

            "average_rr":
                round(average_rr, 2),

            "total_brokerage":
                round(df["brokerage"].sum(), 2),

            "total_slippage":
                round(df["slippage"].sum(), 2),
        }

        return {
            key: Statistics._to_python(value)
            for key, value in summary.items()
        }