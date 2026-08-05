from pathlib import Path

import plotly.graph_objects as go

from app.analytics.drawdown import DrawdownAnalyzer


class ChartGenerator:

    REPORT_DIR = Path("reports")

    @staticmethod
    def equity_curve(portfolio, save=False):

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=list(range(len(portfolio.equity_curve))),
                y=portfolio.equity_curve,
                mode="lines",
                name="Equity",
                line=dict(width=3),
            )
        )

        fig.update_layout(
            title="Equity Curve",
            xaxis_title="Trade Number",
            yaxis_title="Capital (₹)",
            template="plotly_white",
            hovermode="x unified",
        )

        if save:
            ChartGenerator.REPORT_DIR.mkdir(exist_ok=True)
            fig.write_html(
                ChartGenerator.REPORT_DIR /
                "equity_curve.html"
            )

        return fig

    @staticmethod
    def drawdown_curve(equity_curve, save=False):

        result = DrawdownAnalyzer.analyze(equity_curve)

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=list(range(len(result["drawdown_curve"]))),
                y=result["drawdown_curve"],
                mode="lines",
                fill="tozeroy",
                name="Drawdown %",
            )
        )

        fig.update_layout(
            title="Drawdown Curve",
            xaxis_title="Trade Number",
            yaxis_title="Drawdown %",
            template="plotly_white",
        )

        if save:
            ChartGenerator.REPORT_DIR.mkdir(exist_ok=True)
            fig.write_html(
                ChartGenerator.REPORT_DIR /
                "drawdown_curve.html"
            )

        return fig

    @staticmethod
    def trade_chart(df, portfolio, save=False):
        """
        Interactive candlestick chart with trade markers.
        """

        fig = go.Figure()

        ##################################################
        # Candlesticks
        ##################################################

        fig.add_trace(
            go.Candlestick(
                x=df["datetime"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="Price",
            )
        )

        ##################################################
        # Trades
        ##################################################

        for trade in portfolio.trades:

            # BUY

            fig.add_trace(
                go.Scatter(
                    x=[trade.entry_time],
                    y=[trade.entry_price],
                    mode="markers",
                    marker=dict(
                        symbol="triangle-up",
                        size=12,
                        color="green",
                    ),
                    name="Buy",
                    hovertemplate=
                    (
                        "<b>BUY</b><br>"
                        f"{trade.symbol}<br>"
                        f"Entry: ₹{trade.entry_price:.2f}<br>"
                        f"Qty: {trade.quantity}<br>"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

            # SELL

            color = (
                "green"
                if trade.pnl >= 0
                else "red"
            )

            fig.add_trace(
                go.Scatter(
                    x=[trade.exit_time],
                    y=[trade.exit_price],
                    mode="markers",
                    marker=dict(
                        symbol="triangle-down",
                        size=12,
                        color=color,
                    ),
                    name="Sell",
                    hovertemplate=
                    (
                        "<b>SELL</b><br>"
                        f"{trade.symbol}<br>"
                        f"Exit: ₹{trade.exit_price:.2f}<br>"
                        f"PnL: ₹{trade.pnl:.2f}<br>"
                        f"Reason: {trade.exit_reason}<br>"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

        ##################################################
        # Layout
        ##################################################

        fig.update_layout(
            title="Trade Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white",
            xaxis_rangeslider_visible=False,
            hovermode="x unified",
        )

        if save:

            ChartGenerator.REPORT_DIR.mkdir(
                exist_ok=True
            )

            fig.write_html(
                ChartGenerator.REPORT_DIR /
                "trade_chart.html"
            )

        return fig

    @staticmethod
    def show_all(df, portfolio):

        ChartGenerator.trade_chart(
            df,
            portfolio,
        ).show()

        ChartGenerator.equity_curve(
            portfolio,
        ).show()

        ChartGenerator.drawdown_curve(
            portfolio.equity_curve,
        ).show()