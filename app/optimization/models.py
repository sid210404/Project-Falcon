from dataclasses import dataclass


@dataclass(slots=True)
class OptimizationResult:
    """
    Stores the result of a single optimization run.
    """

    parameters: dict

    net_profit: float
    return_pct: float

    win_rate: float
    profit_factor: float

    sharpe_ratio: float
    max_drawdown: float

    total_trades: int