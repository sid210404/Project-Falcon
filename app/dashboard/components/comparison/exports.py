"""Download controls for strategy-comparison exports."""

from __future__ import annotations

import streamlit as st

from app.comparison.comparison_result import ComparisonResult
from app.reports.comparison_report import ComparisonReport


def render(results: list[ComparisonResult]) -> None:
    """Render CSV, HTML, and PDF downloads from report serializers."""
    columns = st.columns(3)
    columns[0].download_button(
        "Download CSV", ComparisonReport.dataframe(results).to_csv(index=False),
        "strategy_comparison.csv", "text/csv",
    )
    columns[1].download_button(
        "Download HTML", ComparisonReport.to_html(results),
        "strategy_comparison.html", "text/html",
    )
    columns[2].download_button(
        "Download PDF", ComparisonReport.to_pdf(results),
        "strategy_comparison.pdf", "application/pdf",
    )
