"""
Professional Candlestick Chart
"""

import streamlit as st

from app.visualization.engine import VisualizationEngine


def render_candlestick(result):
    """
    Render Falcon Visualization Engine.
    """

    fig = VisualizationEngine.build(result)

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="falcon_chart",
    )