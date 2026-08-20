"""Winner callout for comparison results."""

from __future__ import annotations

import streamlit as st

from app.comparison.comparison_result import ComparisonResult


def render(results: list[ComparisonResult]) -> None:
    """Highlight the strategy with the highest net profit."""
    winner = max(results, key=lambda item: item.metrics.net_profit)
    st.success(
        f"Top strategy: {winner.strategy_name} — "
        f"₹{winner.metrics.net_profit:,.2f} net profit "
        f"({winner.metrics.return_pct:.2f}% return)."
    )
