"""
Trade Analyzer

Computes trade-level statistics from a Portfolio.
"""

from app.analytics.models.trade_statistics import TradeStatistics


class TradeAnalyzer:

    @staticmethod
    def analyze(portfolio) -> TradeStatistics:

        trades = portfolio.trades

        if not trades:

            return TradeStatistics(
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0.0,
                gross_profit=0.0,
                gross_loss=0.0,
                net_profit=0.0,
                average_winner=0.0,
                average_loser=0.0,
                largest_winner=0.0,
                largest_loser=0.0,
                average_holding_minutes=0.0,
                longest_trade_minutes=0.0,
                shortest_trade_minutes=0.0,
                average_return_pct=0.0,
                expectancy=0.0,
            )

        winners = [t for t in trades if t.pnl > 0]
        losers = [t for t in trades if t.pnl < 0]

        gross_profit = sum(t.pnl for t in winners)
        gross_loss = abs(sum(t.pnl for t in losers))

        average_winner = (
            gross_profit / len(winners)
            if winners
            else 0.0
        )

        average_loser = (
            gross_loss / len(losers)
            if losers
            else 0.0
        )

        largest_winner = (
            max((t.pnl for t in winners), default=0.0)
        )

        largest_loser = (
            abs(min((t.pnl for t in losers), default=0.0))
        )

        holding_times = [
            t.holding_minutes
            for t in trades
        ]

        average_holding = (
            sum(holding_times) / len(holding_times)
        )

        average_return = (
            sum(t.return_pct for t in trades)
            / len(trades)
        )

        expectancy = (
            sum(t.pnl for t in trades)
            / len(trades)
        )

        return TradeStatistics(

            total_trades=len(trades),

            winning_trades=len(winners),

            losing_trades=len(losers),

            win_rate=portfolio.win_rate,

            gross_profit=gross_profit,

            gross_loss=gross_loss,

            net_profit=portfolio.total_pnl,

            average_winner=average_winner,

            average_loser=average_loser,

            largest_winner=largest_winner,

            largest_loser=largest_loser,

            average_holding_minutes=average_holding,

            longest_trade_minutes=max(holding_times),

            shortest_trade_minutes=min(holding_times),

            average_return_pct=average_return,

            expectancy=expectancy,

        )