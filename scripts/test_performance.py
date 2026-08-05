from app.analytics.performance import PerformanceAnalyzer
from app.backtesting.engine import BacktestEngine
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.strategy.orb_strategy import ORBStrategy


def main():

    print("Fetching historical data...")

    df = HistoricalData.fetch(
        symbol="RELIANCE",
        interval="15m",
        days=30,
    )

    print(f"Downloaded {len(df)} candles")

    print("Applying indicators...")

    df = IndicatorEngine.apply_all(df)

    print(f"After indicators: {len(df)} candles")

    print("Running backtest...")

    engine = BacktestEngine(
        strategy=ORBStrategy(),
        symbol="RELIANCE",
    )

    portfolio = engine.run(df)

    print("\n========== PERFORMANCE ==========\n")

    result = PerformanceAnalyzer.analyze(portfolio)

    for key, value in result.items():
        print(f"{key:<30}: {value}")


if __name__ == "__main__":
    main()