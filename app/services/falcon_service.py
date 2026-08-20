"""
app/services/falcon_service.py

High-level orchestration service for Project Falcon.
"""

from pathlib import Path

from app.backtesting.backtest_runner import BacktestRunner
from app.core.config import BacktestConfig
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.optimization.dataframe import OptimizationDataFrame
from app.optimization.optimizer import Optimizer
from app.paper_trading.live_session import LiveSession
from app.paper_trading.paper_order import PaperOrder
from app.reports.report_generator import ReportGenerator
from app.services.paper_trading_service import PaperTradingService


class FalconService:
    """
    High-level orchestration service.

    Coordinates every Falcon subsystem but
    contains no business logic.
    """

    def __init__(self):

        ############################################################
        # Data
        ############################################################

        self.data = HistoricalData()

        self.indicators = IndicatorEngine()

        ############################################################
        # Backtesting
        ############################################################

        self.optimizer = Optimizer()

        self.report_generator = ReportGenerator()

        ############################################################
        # Paper Trading
        ############################################################

        self.paper = PaperTradingService()

    ####################################################################
    # Backtesting
    ####################################################################

    def run_backtest(
        self,
        strategy,
        config: BacktestConfig,
        generate_report: bool = True,
    ):

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

        optimization_df.to_csv(
            output_file,
            index=False,
        )

        print(
            f"Optimization results exported to {output_file}"
        )

        return results

    ####################################################################
    # Paper Trading
    ####################################################################

    def create_paper_session(
        self,
        strategy,
        config: BacktestConfig,
    ) -> LiveSession:
        """
        Create a new paper-trading session.
        """

        return self.paper.create_session(
            symbol=config.symbol,
            exchange=config.exchange,
            interval=config.interval,
            strategy=strategy,
            initial_cash=config.capital,
        )

    def start_paper_session(
        self,
        session: LiveSession,
    ) -> None:
        """
        Start paper trading.
        """

        self.paper.start(session)

    def pause_paper_session(
        self,
        session: LiveSession,
    ) -> None:
        """
        Pause paper trading.
        """

        self.paper.pause(session)

    def stop_paper_session(
        self,
        session: LiveSession,
    ) -> None:
        """
        Stop paper trading.
        """

        self.paper.stop(session)

    def poll_paper_session(
        self,
        session: LiveSession,
    ) -> None:
        """
        Process the newest candle.
        """

        self.paper.poll(session)

    def submit_paper_order(
        self,
        session: LiveSession,
        order: PaperOrder,
    ) -> None:
        """
        Submit a manual paper order.
        """

        self.paper.submit_order(
            session,
            order,
        )

    ####################################################################
    # Convenience
    ####################################################################

    def backtest_and_report(
        self,
        strategy,
        config: BacktestConfig,
    ):

        return self.run_backtest(
            strategy=strategy,
            config=config,
            generate_report=True,
        )