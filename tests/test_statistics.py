import pytest

from app.backtesting.portfolio import Portfolio
from app.backtesting.statistics import Statistics


def test_empty_statistics():

    portfolio = Portfolio(capital=100000)

    result = Statistics.summary(portfolio)

    assert result["trades"] == 0
    assert result["net_profit"] == 0
    assert result["win_rate"] == 0
    assert result["profit_factor"] == 0