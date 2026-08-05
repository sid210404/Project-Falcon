from app.analytics.drawdown import DrawdownAnalyzer


def test_drawdown():

    equity = [
        100000,
        105000,
        103000,
        99000,
        101000,
    ]

    result = DrawdownAnalyzer.analyze(equity)

    assert result["peak_equity"] == 105000
    assert result["max_drawdown_pct"] > 0
    assert len(result["drawdown_curve"]) == len(equity)