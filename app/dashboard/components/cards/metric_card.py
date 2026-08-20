"""
Falcon Metric Card
"""

import streamlit as st


def render_metric_card(
    title: str,
    value,
    delta=None,
    icon="📊",
    help_text=None,
):

    with st.container(border=True):

        st.caption(f"{icon} {title}")

        st.metric(
            label="",
            value=value,
            delta=delta,
            help=help_text,
        )