from dataclasses import dataclass

from app.backtesting.result import BacktestResult
from app.comparison.comparison_metrics import ComparisonMetrics


@dataclass(slots=True)
class ComparisonResult:

    strategy_name: str

    result: BacktestResult

    metrics: ComparisonMetrics
