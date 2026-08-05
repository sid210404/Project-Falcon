from app.analytics.charts import ChartGenerator
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

    print("Running backtest...")

    engine = BacktestEngine(
        strategy=ORBStrategy(),
        symbol="RELIANCE",
    )

    portfolio = engine.run(df)

    portfolio.export_trades()

    ChartGenerator.trade_chart(
        df,
        portfolio,
        save=True,
    ).show()

    print("\nTrade chart saved to reports/trade_chart.html")
    print("Trades exported to reports/trades.csv")


if __name__ == "__main__":
    main()