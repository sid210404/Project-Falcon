from datetime import datetime

from app.analytics.models.benchmark_statistics import BenchmarkStatistics


class BenchmarkAnalyzer:
    """
    Compare strategy performance against Buy & Hold.
    """

    @staticmethod
    def analyze(
        dataframe,
        portfolio,
        initial_capital: float,
    ) -> BenchmarkStatistics:

        first_price = dataframe.iloc[0]["close"]
        last_price = dataframe.iloc[-1]["close"]

        benchmark_return = (
            (last_price - first_price) / first_price
        ) * 100

        benchmark_final = (
            initial_capital
            * (1 + benchmark_return / 100)
        )

        strategy_return = (
            (portfolio.final_capital - initial_capital)
            / initial_capital
        ) * 100

        outperformance = (
            strategy_return
            - benchmark_return
        )

        days = max(
            (dataframe.iloc[-1]["datetime"]
             - dataframe.iloc[0]["datetime"]).days,
            1,
        )

        years = days / 365.25

        strategy_cagr = (
            ((portfolio.final_capital / initial_capital)
             ** (1 / years) - 1) * 100
            if years > 0 else strategy_return
        )

        benchmark_cagr = (
            ((benchmark_final / initial_capital)
             ** (1 / years) - 1) * 100
            if years > 0 else benchmark_return
        )

        return BenchmarkStatistics(
            strategy_return_pct=round(strategy_return, 2),
            benchmark_return_pct=round(benchmark_return, 2),
            outperformance_pct=round(outperformance, 2),
            strategy_final_capital=round(
                portfolio.final_capital,
                2,
            ),
            benchmark_final_capital=round(
                benchmark_final,
                2,
            ),
            strategy_cagr=round(strategy_cagr, 2),
            benchmark_cagr=round(
                benchmark_cagr,
                2,
            ),
        )