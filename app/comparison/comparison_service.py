"""Workflow service for executing comparable strategy backtests."""

from __future__ import annotations

from typing import Sequence

from app.comparison.comparison_result import ComparisonResult
from app.comparison.comparison_runner import ComparisonRunner
from app.core.config import BacktestConfig
from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine


class ComparisonService:
    """Prepare market data once and run selected strategies against it."""

    def __init__(self) -> None:
        self._data = HistoricalData()
        self._indicators = IndicatorEngine()

    def compare(
        self,
        strategy_classes: Sequence[type],
        config: BacktestConfig,
    ) -> list[ComparisonResult]:
        """Execute every selected strategy on an identical dataset."""
        if len(strategy_classes) < 2:
            raise ValueError("Select at least two strategies to compare.")

        dataframe = self._data.fetch(
            symbol=config.symbol,
            exchange=config.exchange,
            interval=config.interval,
            days=config.days,
        )
        dataframe = self._indicators.apply_all(dataframe)

        return ComparisonRunner.compare(
            strategy_classes=list(strategy_classes),
            dataframe=dataframe,
            symbol=config.symbol,
            capital=config.capital,
        )
