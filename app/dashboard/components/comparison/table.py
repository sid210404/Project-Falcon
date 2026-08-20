"""Tabular rendering for strategy-comparison results."""

from __future__ import annotations

import streamlit as st

from app.comparison.comparison_result import ComparisonResult
from app.reports.comparison_report import ComparisonReport


def render(results: list[ComparisonResult]) -> None:
    """Render normalized comparison metrics without calculating them in the UI."""
    st.dataframe(ComparisonReport.dataframe(results), use_container_width=True)
