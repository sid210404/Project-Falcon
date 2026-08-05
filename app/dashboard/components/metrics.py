"""
Dashboard metrics component.

Displays key performance indicators from a BacktestResult.
"""

import streamlit as st


def _currency(value):
    """Format currency values."""
    return f"₹{value:,.2f}"


def _percent(value):
    """Format percentage values."""
    return f"{value:.2f}%"


def render_metrics(result):
    """
    Render Falcon KPI dashboard.
    """

    statistics = result.statistics
    performance = result.performance
    drawdown = result.drawdown

    st.subheader("📊 Performance Summary")

    row1 = st.columns(4)

    with row1[0]:
        st.metric(
            "Net Profit",
            _currency(statistics["net_profit"]),
        )

    with row1[1]:
        st.metric(
            "Return %",
            _percent(statistics["return_pct"]),
        )

    with row1[2]:
        st.metric(
            "Trades",
            statistics["trades"],
        )

    with row1[3]:
        st.metric(
            "Win Rate",
            _percent(statistics["win_rate"]),
        )

    row2 = st.columns(4)

    with row2[0]:
        st.metric(
            "Profit Factor",
            f'{statistics["profit_factor"]:.2f}',
        )

    with row2[1]:
        st.metric(
            "Sharpe Ratio",
            f'{performance["sharpe_ratio"]:.2f}',
        )

    with row2[2]:
        st.metric(
            "Max Drawdown",
            _percent(drawdown["max_drawdown_pct"]),
        )

    with row2[3]:
        st.metric(
            "Expectancy",
            _currency(performance["expectancy"]),
        )

    with st.expander("📈 Detailed Statistics"):

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Initial Capital:** {_currency(statistics['initial_capital'])}")
            st.write(f"**Final Capital:** {_currency(statistics['final_capital'])}")
            st.write(f"**Gross Profit:** {_currency(statistics['gross_profit'])}")
            st.write(f"**Gross Loss:** {_currency(statistics['gross_loss'])}")
            st.write(f"**Wins:** {statistics['wins']}")
            st.write(f"**Losses:** {statistics['losses']}")
            st.write(f"**Best Trade:** {_currency(statistics['best_trade'])}")
            st.write(f"**Worst Trade:** {_currency(statistics['worst_trade'])}")

        with col2:
            st.write(f"**Average Trade:** {_currency(statistics['average_trade'])}")
            st.write(f"**Average Win:** {_currency(statistics['average_win'])}")
            st.write(f"**Average Loss:** {_currency(statistics['average_loss'])}")
            st.write(f"**Average RR:** {performance['average_rr']:.2f}")
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