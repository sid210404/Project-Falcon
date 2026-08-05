from app.analytics.charts import ChartGenerator
from app.analytics.drawdown import DrawdownAnalyzer
from app.backtesting.engine import BacktestEngine
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.strategy.orb_strategy import ORBStrategy


def main():

    print("Downloading data...")

    df = HistoricalData.fetch(
        symbol="RELIANCE",
        interval="15m",
        days=30,
    )

    print("Applying indicators...")

    df = IndicatorEngine.apply_all(df)

    engine = BacktestEngine(
        strategy=ORBStrategy(),
        symbol="RELIANCE",
    )

    portfolio = engine.run(df)

    drawdown = DrawdownAnalyzer.analyze(
        portfolio.equity_curve
    )

    equity = ChartGenerator.equity_curve(
        portfolio,
        save=True,
    )

    dd = ChartGenerator.drawdown_curve(
        drawdown,
        save=True,
    )

    equity.show()
    dd.show()


if __name__ == "__main__":
    main()