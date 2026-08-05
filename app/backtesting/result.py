from dataclasses import dataclass

import pandas as pd

from app.backtesting.portfolio import Portfolio


@dataclass(frozen=True)
class BacktestResult:
    """
    Complete result of a backtest.

    Every consumer (dashboard, reports, charts,
    optimizer, replay, paper trading) should use this
    object instead of individual dictionaries.
    """

    portfolio: Portfolio

    dataframe: pd.DataFrame

    strategy: object

    statistics: dict

    performance: dict

    drawdown: dict