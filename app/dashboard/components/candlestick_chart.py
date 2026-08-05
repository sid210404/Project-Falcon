"""
Professional Candlestick Chart
"""

import streamlit as st

from app.visualization.engine import VisualizationEngine
from app.visualization.models.chart_settings import ChartSettings


def render_candlestick(
    result,
    settings: ChartSettings,
):
    """
    Render the Falcon Visualization Engine.
    """

    fig = VisualizationEngine.build(
        result=result,
        settings=settings,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="falcon_chart",
    )