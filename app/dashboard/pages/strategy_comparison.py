"""Strategy-comparison dashboard page."""

from __future__ import annotations

from datetime import date, timedelta

import streamlit as st

from app.comparison.comparison_service import ComparisonService
from app.core.config import BacktestConfig
from app.core.constants import YAHOO_INTERVAL_LIMITS
from app.core.settings import Settings
from app.dashboard.components.comparison import equity_chart, exports, summary, table, winner
from app.strategy.registry import StrategyRegistry


def render() -> None:
    """Orchestrate execution and presentation of selected strategies."""
    st.title("Strategy Comparison")
    strategy_names = StrategyRegistry.names()

    with st.expander("Market Data", expanded=True):
        exchange = st.selectbox("Exchange", ["NSE", "BSE"], key="comparison_exchange")
        symbol = st.text_input("Symbol", Settings.DEFAULT_SYMBOL, key="comparison_symbol").strip().upper()
        interval = st.selectbox("Timeframe", list(YAHOO_INTERVAL_LIMITS), index=3, key="comparison_interval")
        today = date.today()
        maximum_days = YAHOO_INTERVAL_LIMITS[interval]
        minimum_date = date(2000, 1, 1) if maximum_days is None else today - timedelta(days=maximum_days)
        default_start = today - timedelta(days=180 if maximum_days is None else min(maximum_days, 30))
        left, right = st.columns(2)
        start_date = left.date_input("Start Date", default_start, minimum_date, today, key="comparison_start")
        end_date = right.date_input("End Date", today, minimum_date, today, key="comparison_end")
        capital = st.number_input("Initial Capital", min_value=1000, value=Settings.DEFAULT_CAPITAL, step=1000, key="comparison_capital")

    selected_names = st.multiselect(
        "Strategies", strategy_names, default=strategy_names[:2],
        help="Each strategy is evaluated against the same downloaded candles.",
    )
    if not symbol:
        st.error("Please enter a symbol.")
        return
    if start_date > end_date:
        st.error("Start Date cannot be after End Date.")
        return

    if st.button("Run Comparison", type="primary", use_container_width=True):
        if len(selected_names) < 2:
            st.warning("Select at least two strategies.")
        else:
            config = BacktestConfig(exchange=exchange, symbol=symbol, interval=interval, start_date=start_date, end_date=end_date, capital=capital)
            classes = [StrategyRegistry.get(name) for name in selected_names]
            try:
                with st.spinner("Running strategy comparison..."):
                    st.session_state.comparison_results = ComparisonService().compare(classes, config)
            except Exception as error:
                st.exception(error)
                return

    results = st.session_state.get("comparison_results")
    if not results:
        st.info("Choose at least two strategies and run a comparison.")
        return

    winner.render(results)
    summary.render(results)
    st.subheader("Comparison Metrics")
    table.render(results)
    st.subheader("Equity Curve Overlay")
    equity_chart.render(results)
    st.subheader("Exports")
    exports.render(results)
