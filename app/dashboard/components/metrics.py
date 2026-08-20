"""
Dashboard Metrics Component

Displays key performance indicators from a BacktestResult.
"""

import streamlit as st

from app.dashboard.components.cards.metric_card import (
    render_metric_card,
)


def _currency(value: float) -> str:
    """Format currency values."""
    return f"₹{value:,.2f}"


def _percent(value: float) -> str:
    """Format percentage values."""
    return f"{value:.2f}%"


def render_metrics(result) -> None:
    """
    Render Falcon performance dashboard.
    """

    statistics = result.statistics
    performance = result.performance
    drawdown = result.drawdown

    st.subheader("📊 Performance Summary")

    # ==========================================================
    # Row 1
    # ==========================================================

    row1 = st.columns(4)

    with row1[0]:

        render_metric_card(
            title="Net Profit",
            value=_currency(statistics["net_profit"]),
            icon="💰",
            help_text="Net profit after all completed trades.",
        )

    with row1[1]:

        render_metric_card(
            title="Return %",
            value=_percent(statistics["return_pct"]),
            icon="📈",
            help_text="Overall percentage return.",
        )

    with row1[2]:

        render_metric_card(
            title="Trades",
            value=statistics["trades"],
            icon="📋",
            help_text="Total completed trades.",
        )

    with row1[3]:

        render_metric_card(
            title="Win Rate",
            value=_percent(statistics["win_rate"]),
            icon="🎯",
            help_text="Winning trades as a percentage.",
        )

    # ==========================================================
    # Row 2
    # ==========================================================

    row2 = st.columns(4)

    with row2[0]:

        render_metric_card(
            title="Profit Factor",
            value=f'{statistics["profit_factor"]:.2f}',
            icon="⚖️",
            help_text="Gross Profit ÷ Gross Loss.",
        )

    with row2[1]:

        render_metric_card(
            title="Sharpe Ratio",
            value=f'{performance["sharpe_ratio"]:.2f}',
            icon="📊",
            help_text="Risk-adjusted performance.",
        )

    with row2[2]:

        render_metric_card(
            title="Max Drawdown",
            value=_percent(drawdown["max_drawdown_pct"]),
            icon="📉",
            help_text="Maximum equity decline.",
        )

    with row2[3]:

        render_metric_card(
            title="Expectancy",
            value=_currency(performance["expectancy"]),
            icon="💹",
            help_text="Average expected profit per trade.",
        )

    # ==========================================================
    # Detailed Statistics
    # ==========================================================

    with st.expander("📈 Detailed Statistics", expanded=False):

        left, right = st.columns(2)

        with left:

            st.markdown("### Portfolio")

            st.write(
                f"**Initial Capital:** {_currency(statistics['initial_capital'])}"
            )

            st.write(
                f"**Final Capital:** {_currency(statistics['final_capital'])}"
            )

            st.write(
                f"**Gross Profit:** {_currency(statistics['gross_profit'])}"
            )

            st.write(
                f"**Gross Loss:** {_currency(statistics['gross_loss'])}"
            )

            st.write(
                f"**Wins:** {statistics['wins']}"
            )

            st.write(
                f"**Losses:** {statistics['losses']}"
            )

            st.write(
                f"**Best Trade:** {_currency(statistics['best_trade'])}"
            )

            st.write(
                f"**Worst Trade:** {_currency(statistics['worst_trade'])}"
            )

        with right:

            st.markdown("### Performance")

            st.write(
                f"**Average Trade:** {_currency(statistics['average_trade'])}"
            )

            st.write(
                f"**Average Win:** {_currency(statistics['average_win'])}"
            )

            st.write(
                f"**Average Loss:** {_currency(statistics['average_loss'])}"
            )

            st.write(
                f"**Average Risk/Reward:** {performance['average_rr']:.2f}"
            )

            st.write(
                f"**Average Holding:** "
                f"{performance['average_holding_minutes']:.2f} min"
            )

            st.write(
                f"**Largest Winner:** "
                f"{_currency(performance['largest_winner'])}"
            )

            st.write(
                f"**Largest Loser:** "
                f"{_currency(performance['largest_loser'])}"
            )

            st.write(
                f"**Max Win Streak:** "
                f"{performance['consecutive_wins']}"
            )

            st.write(
                f"**Max Loss Streak:** "
                f"{performance['consecutive_losses']}"
            )