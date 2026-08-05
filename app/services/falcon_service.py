"""
app/services/falcon_service.py

High-level service that orchestrates Falcon's workflow.
"""

from pathlib import Path

from app.backtesting.backtest_runner import BacktestRunner
from app.core.config import BacktestConfig
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.optimization.dataframe import OptimizationDataFrame
from app.optimization.optimizer import Optimizer
from app.reports.report_generator import ReportGenerator


class FalconService:
    """
    High-level orchestration service for Falcon.

    This class coordinates all modules but contains
    NO trading logic.
    """

    def __init__(self):

        self.data = HistoricalData()
        self.indicators = IndicatorEngine()
        self.optimizer = Optimizer()

        self.report_generator = ReportGenerator()

    ####################################################################
    # Backtesting
    ####################################################################

    def run_backtest(
        self,
        strategy,
        config: BacktestConfig,
        generate_report: bool = True,
    ):
        """
        Complete backtesting workflow.
        """

        print("Downloading historical data...")

        df = self.data.fetch(
            symbol=config.symbol,
            exchange=config.exchange,
            interval=config.interval,
            days=config.days,
        )

        print(f"Downloaded {len(df)} candles")

        print("Applying indicators...")

        df = self.indicators.apply_all(df)

        print(f"After indicators: {len(df)} candles")

        print("Running backtest...")

        result = BacktestRunner.run(
            strategy=strategy,
            symbol=config.symbol,
            df=df,
            capital=config.capital,
        )

        if generate_report:

            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)

            print("Generating report...")

            self.report_generator.generate(result)

        return result

    ####################################################################
    # Optimization
    ####################################################################

    def run_optimization(
        self,
        strategy_class,
        config: BacktestConfig,
    ):
        """
        Runs parameter optimization.
        """

        print("Downloading historical data...")

        df = self.data.fetch(
            symbol=config.symbol,
            exchange=config.exchange,
            interval=config.interval,
            days=config.days,
        )

        print("Applying indicators...")

        df = self.indicators.apply_all(df)

        print("Running optimization...")

        results = self.optimizer.optimize(
            strategy_class=strategy_class,
            df=df,
            symbol=config.symbol,
            capital=config.capital,
        )

        optimization_df = OptimizationDataFrame.build(results)

        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        output_file = reports_dir / "optimization_results.csv"

        optimization_df.to_csv(output_file, index=False)

        print(f"Optimization results exported to {output_file}")

        return results

    ####################################################################
    # Convenience
    ####################################################################

    def backtest_and_report(
        self,
        strategy,
        config: BacktestConfig,
    ):
        """
        Alias for a standard backtest.
        """

        return self.run_backtest(
            strategy=strategy,
            config=config,
            generate_report=True,
        )