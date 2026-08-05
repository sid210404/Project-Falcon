from statistics import mean, pstdev
from math import sqrt


class PerformanceAnalyzer:
    """
    Calculates advanced trading performance metrics.
    """

    @staticmethod
    def analyze(portfolio):

        if portfolio.total_trades == 0:
            return {
                "expectancy": 0.0,
                "average_rr": 0.0,
                "average_holding_minutes": 0.0,
                "largest_winner": 0.0,
                "largest_loser": 0.0,
                "consecutive_wins": 0,
                "consecutive_losses": 0,
                "sharpe_ratio": 0.0,
            }

        trades = portfolio.trades

        pnl = [trade.pnl for trade in trades]

        returns = [
            trade.return_pct / 100
            for trade in trades
        ]

        # ---------- Expectancy ----------

        win_rate = portfolio.winning_trades / portfolio.total_trades

        loss_rate = portfolio.losing_trades / portfolio.total_trades

        avg_win = mean(
            [t.pnl for t in trades if t.pnl > 0]
        ) if portfolio.winning_trades else 0

        avg_loss = abs(mean(
            [t.pnl for t in trades if t.pnl < 0]
        )) if portfolio.losing_trades else 0

        expectancy = (
            (win_rate * avg_win)
            -
            (loss_rate * avg_loss)
        )

        # ---------- Average RR ----------

        rr = [
            t.risk_reward
            for t in trades
            if t.risk_reward is not None
        ]

        average_rr = mean(rr) if rr else 0

        # ---------- Holding ----------

        average_holding = mean(
            [t.holding_minutes for t in trades]
        )

        # ---------- Largest ----------

        largest_winner = max(pnl)

        largest_loser = min(pnl)

        # ---------- Consecutive ----------

        max_win_streak = 0
        max_loss_streak = 0

        current_win = 0
        current_loss = 0

        for trade in trades:

            if trade.pnl > 0:

                current_win += 1
                current_loss = 0

            else:

                current_loss += 1
                current_win = 0

            max_win_streak = max(
                max_win_streak,
                current_win,
            )

            max_loss_streak = max(
                max_loss_streak,
                current_loss,
            )

        # ---------- Sharpe ----------

        if len(returns) > 1 and pstdev(returns) > 0:

            sharpe = (
                mean(returns)
                /
                pstdev(returns)
            ) * sqrt(len(returns))

        else:

            sharpe = 0

        return {

            "expectancy":
                round(expectancy, 2),

            "average_rr":
                round(average_rr, 2),

            "average_holding_minutes":
                round(average_holding, 2),

            "largest_winner":
                round(largest_winner, 2),

            "largest_loser":
                round(largest_loser, 2),

            "consecutive_wins":
                max_win_streak,

            "consecutive_losses":
                max_loss_streak,

            "sharpe_ratio":
                round(sharpe, 2),
        }