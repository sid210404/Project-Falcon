import streamlit as st


def render():

    st.title("📊 Analytics")

    result = st.session_state.get("backtest_result")

    if result is None:

        st.info("Run a backtest first.")

        return

    overview_tab, trades_tab, risk_tab = st.tabs(
        [
            "📊 Overview",
            "📈 Trades",
            "⚠ Risk",
        ]
    )

    with overview_tab:

        st.subheader("Portfolio Summary")

        st.metric(
            "Net Profit",
            f"₹{result.portfolio.total_pnl:,.2f}",
        )

        st.metric(
            "Return",
            f"{result.portfolio.total_return_pct:.2f}%",
        )

        st.metric(
            "Trades",
            result.portfolio.total_trades,
        )

    with trades_tab:

        st.info(
            "Trade Analytics coming soon..."
        )

    with risk_tab:

        st.info(
            "Risk Analytics coming soon..."
        )