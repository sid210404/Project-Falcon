"""
Reusable section headers.
"""

import streamlit as st


def render_section_header(
    title: str,
    description: str | None = None,
):
    """
    Render a standard Falcon section header.
    """

    st.subheader(title)

    if description:

        st.caption(description)

    st.divider()