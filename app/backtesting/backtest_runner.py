from app.analytics.drawdown import DrawdownAnalyzer
from app.analytics.performance import PerformanceAnalyzer
from app.backtesting.engine import BacktestEngine
from app.backtesting.result import BacktestResult
from app.backtesting.statistics import Statistics


class BacktestRunner:

    @staticmethod
    def run(
        strategy,
        symbol,
        df,
        capital=100000,
    ):

        print("1. Creating engine")

        engine = BacktestEngine(
            strategy=strategy,
            symbol=symbol,
            capital=capital,
        )

        print("2. Running engine")

        portfolio = engine.run(df)

        print("3. Engine finished")

        statistics = Statistics.summary(portfolio)

        print("4. Statistics finished")

        performance = PerformanceAnalyzer.analyze(portfolio)

        print("5. Performance finished")

        drawdown = DrawdownAnalyzer.analyze(
            portfolio.equity_curve
        )

        print("6. Drawdown finished")

        result = BacktestResult(
            portfolio=portfolio,
            dataframe=df,
            strategy=strategy,
            statistics=statistics,
            performance=performance,
            drawdown=drawdown,
        )

        print("7. Returning result")

        return result