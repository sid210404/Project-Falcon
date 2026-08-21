"""
Falcon service facade.
"""

from app.optimization.optimizer import Optimizer
from app.reports.report_generator import ReportGenerator
from app.services.backtest_service import BacktestService

class FalconService:
    """Facade exposing Falcon subsystems."""

    def __init__(self):
        self.backtest = BacktestService()
        self.optimizer = Optimizer()
        self.report_generator = ReportGenerator()

    def run_backtest(self, strategy, config, generate_report=True):
        result = self.backtest.run(strategy, config)
        if generate_report:
            self.report_generator.generate(result)
        return result
