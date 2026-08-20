"""Summary cards for strategy-comparison results."""

from __future__ import annotations

import streamlit as st

from app.comparison.comparison_result import ComparisonResult


def render(results: list[ComparisonResult]) -> None:
    """Render a compact KPI card for each strategy."""
    columns = st.columns(len(results))
    for column, item in zip(columns, results, strict=True):
        metrics = item.metrics
        with column:
            st.subheader(item.strategy_name)
            st.metric("Net Profit", f"₹{metrics.net_profit:,.2f}")
            st.metric("Return", f"{metrics.return_pct:.2f}%")
            st.caption(f"Sharpe {metrics.sharpe_ratio:.2f} · Drawdown {metrics.max_drawdown_pct:.2f}%")
