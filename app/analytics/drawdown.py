from typing import List


class DrawdownAnalyzer:
    """
    Calculates drawdown statistics from an equity curve.
    """

    @staticmethod
    def analyze(equity_curve):

        if not equity_curve:
            return {
                "peak_equity": 0.0,
                "max_drawdown_amount": 0.0,
                "max_drawdown_pct": 0.0,
                "current_drawdown_amount": 0.0,
                "current_drawdown_pct": 0.0,
                "drawdown_curve": [],
            }

        peak = equity_curve[0]

        max_drawdown_amount = 0.0
        max_drawdown_pct = 0.0

        current_drawdown_amount = 0.0
        current_drawdown_pct = 0.0

        drawdown_curve = []

        for equity in equity_curve:

            if equity > peak:
                peak = equity

            drawdown_amount = peak - equity

            drawdown_pct = (
                drawdown_amount / peak
            ) * 100 if peak else 0.0

            drawdown_curve.append(round(drawdown_pct, 2))

            if drawdown_pct > max_drawdown_pct:
                max_drawdown_pct = drawdown_pct
                max_drawdown_amount = drawdown_amount

            current_drawdown_amount = drawdown_amount
            current_drawdown_pct = drawdown_pct

        return {
            "peak_equity": round(peak, 2),
            "max_drawdown_amount": round(max_drawdown_amount, 2),
            "max_drawdown_pct": round(max_drawdown_pct, 2),
            "current_drawdown_amount": round(current_drawdown_amount, 2),
            "current_drawdown_pct": round(current_drawdown_pct, 2),
            "drawdown_curve": drawdown_curve,
        }