from app.analytics.charts import ChartGenerator
from app.backtesting.backtest_runner import BacktestRunner
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.reports.report_generator import ReportGenerator
from app.strategy.orb_strategy import ORBStrategy


def main():

    # Configuration
    symbol = "RELIANCE"
    interval = "15m"
    days = 30
    capital = 100000

    print("Downloading historical data...")

    df = HistoricalData.fetch(
        symbol=symbol,
        interval=interval,
        days=days,
    )

    print(f"Downloaded {len(df)} candles")

    print("Applying indicators...")

    df = IndicatorEngine.apply_all(df)

    print(f"After indicators: {len(df)} candles")

    print("Running backtest...")

    result = BacktestRunner.run(
        strategy=ORBStrategy(),
        symbol=symbol,
        df=df,
        capital=capital,
    )

    print("Exporting trades...")

    result.portfolio.export_trades()

    print("Generating charts...")

    ChartGenerator.trade_chart(
        df,
        result.portfolio,
        save=True,
    )

    ChartGenerator.equity_curve(
        result.portfolio,
        save=True,
    )

    ChartGenerator.drawdown_curve(
        result.portfolio.equity_curve,
        save=True,
    )

    print("Generating report...")

    ReportGenerator.generate(
        result=result,
        strategy_name="ORB Strategy",
        symbol=symbol,
        interval=interval,
    )

    print("\n==============================")
    print(" Backtest Completed Successfully")
    print("==============================")

    print(f"Net PnL        : ₹{result.portfolio.total_pnl:.2f}")
    print(f"Return         : {result.portfolio.total_return_pct:.2f}%")
    print(f"Trades         : {result.portfolio.total_trades}")
    print(f"Win Rate       : {result.portfolio.win_rate:.2f}%")
    print(f"Profit Factor  : {result.portfolio.profit_factor:.2f}")

    print("\nReports saved in the 'reports' folder.")


if __name__ == "__main__":
    main()