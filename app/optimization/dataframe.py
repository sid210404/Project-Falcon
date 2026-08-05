import pandas as pd

from app.optimization.models import OptimizationResult


class OptimizationDataFrame:

    @staticmethod
    def build(results: list[OptimizationResult]) -> pd.DataFrame:
        """
        Convert optimization results into a pandas DataFrame.
        """

        rows = []

        for result in results:

            row = {
                **result.parameters,
                "net_profit": result.net_profit,
                "return_pct": result.return_pct,
                "win_rate": result.win_rate,
                "profit_factor": result.profit_factor,
                "sharpe_ratio": result.sharpe_ratio,
                "max_drawdown": result.max_drawdown,
                "total_trades": result.total_trades,
            }

            rows.append(row)

        return pd.DataFrame(rows)