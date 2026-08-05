from app.backtesting.portfolio import Portfolio


def test_portfolio_creation():

    portfolio = Portfolio(100000)

    assert portfolio.initial_capital == 100000
    assert portfolio.capital == 100000
    assert portfolio.total_trades == 0