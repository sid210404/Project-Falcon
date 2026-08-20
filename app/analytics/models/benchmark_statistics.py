from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BenchmarkStatistics:
    """
    Strategy vs Buy & Hold performance.
    """

    strategy_return_pct: float
    benchmark_return_pct: float
    outperformance_pct: float

    strategy_final_capital: float
    benchmark_final_capital: float

    strategy_cagr: float
    benchmark_cagr: float