from app.backtesting.backtest_runner import BacktestRunner
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine

class BacktestService:
    """Owns the complete backtest workflow."""

    def __init__(self):
        self.data = HistoricalData()
        self.indicators = IndicatorEngine()

    def run(self, strategy, config):
        df = self.data.fetch(
            symbol=config.symbol,
            exchange=config.exchange,
            interval=config.interval,
            days=config.days,
        )
        df = self.indicators.apply_all(df)
        return BacktestRunner.run(
            strategy=strategy,
            symbol=config.symbol,
            df=df,
            capital=config.capital,
        )
