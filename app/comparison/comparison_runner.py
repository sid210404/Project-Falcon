import pandas as pd

from app.backtesting.backtest_runner import BacktestRunner
from app.comparison.comparison_metrics import ComparisonMetrics
from app.comparison.comparison_result import (
    ComparisonResult,
)


class ComparisonRunner:

    @staticmethod
    def compare(
        strategy_classes: list[type],
        dataframe: pd.DataFrame,
        symbol: str,
        capital: float,
    ) -> list[ComparisonResult]:
        """Run each strategy against the same prepared market dataset."""
        results: list[ComparisonResult] = []

        for strategy_class in strategy_classes:
            strategy = strategy_class()
            result = BacktestRunner.run(
                strategy=strategy,
                symbol=symbol,
                df=dataframe.copy(),
                capital=capital,
            )
            results.append(
                ComparisonResult(
                    strategy_name=strategy.name,
                    result=result,
                    metrics=ComparisonMetrics.from_result(result),
                )
            )

        return results
