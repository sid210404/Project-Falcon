"""
Global theme and styling utilities for the Falcon dashboard.
"""

import streamlit as st


def apply_custom_styles():
    """Apply custom CSS styling to the entire dashboard."""
    
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Title styling */
    h1 {
        color: #0f1419;
        font-weight: 700;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #0f1419;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #31333d;
        font-weight: 600;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }
    
    /* Text styling */
    p, span {
        color: #31333d;
        line-height: 1.6;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e0e4e8;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Expander styling */
    [data-testid="stExpander"] {
        border-radius: 10px;
        border: 1px solid #e0e4e8;
        overflow: hidden;
    }
    
    [data-testid="stExpanderDetails"] {
        padding: 1.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.5rem;
        transition: all 0.3s ease;
        border: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Input field styling */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox select {
        border-radius: 8px;
        border: 1px solid #e0e4e8;
        padding: 0.6rem 1rem;
        font-size: 0.95rem;
    }
    
    .stTextInput input:focus,
    .stNumberInput input:focus,
    .stSelectbox select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background-color: rgba(102, 126, 234, 0.1);
    }
    
    /* Info/Warning/Error message styling */
    .stInfo, .stWarning, .stError, .stSuccess {
        border-radius: 8px;
        padding: 1rem 1.5rem;
        border-left: 4px solid;
    }
    
    .stInfo {
        background-color: #e7f3ff;
        border-left-color: #1890ff;
    }
    
    .stWarning {
        background-color: #fffbe6;
        border-left-color: #faad14;
    }
    
    .stError {
        background-color: #fff2f0;
        border-left-color: #ff4d4f;
    }
    
    .stSuccess {
        background-color: #f6ffed;
        border-left-color: #52c41a;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button {
        border-radius: 8px 8px 0 0;
        font-weight: 500;
    }
    
    /* Dataframe styling */
    [data-testid="stDataframe"] {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Container styling */
    [data-testid="stContainer"] {
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    /* Select box and date input styling */
    .stSelectbox > div > div,
    .stDateInput > div > div {
        border-radius: 8px;
    }
    
    /* Caption and small text */
    .stCaption {
        color: #7c8aa9;
        font-size: 0.85rem;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #e0e4e8, transparent);
    }
    
    /* Section spacing */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, icon: str = ""):
    """Render a styled page header."""
    st.markdown(
        f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin: 0;">{icon} {title}</h1>
            <div style="height: 3px; background: linear-gradient(to right, #667eea, #764ba2); width: 60px; border-radius: 2px;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_stat_row(stats: dict):
    """Render a row of statistics with modern styling."""
    cols = st.columns(len(stats))
    
    for col, (label, value) in zip(cols, stats.items()):
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 1.5rem;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #e0e4e8;
            ">
                <p style="margin: 0; color: #7c8aa9; font-size: 0.85rem; font-weight: 500;">{label}</p>
                <p style="margin: 0.5rem 0 0 0; color: #0f1419; font-size: 1.75rem; font-weight: 700;">{value}</p>
            </div>
            """, unsafe_allow_html=True)


def render_section(title: str, description: str = ""):
    """Render a styled section header."""
    st.markdown(f"""
    <div style="margin-top: 2rem; margin-bottom: 1rem;">
        <h2 style="margin: 0; margin-bottom: 0.5rem;">{title}</h2>
        {f'<p style="margin: 0; color: #7c8aa9; font-size: 0.95rem;">{description}</p>' if description else ''}
        <div style="height: 2px; background: linear-gradient(to right, #667eea, transparent); width: 40px; border-radius: 1px; margin-top: 0.75rem;"></div>
    </div>
    """, unsafe_allow_html=True)


def get_gradient_colors():
    """Return color palette for the application."""
    return {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "success": "#52c41a",
        "warning": "#faad14",
        "error": "#ff4d4f",
        "info": "#1890ff",
        "background": "#f5f7fa",
        "text": "#0f1419",
        "text_secondary": "#7c8aa9",
        "border": "#e0e4e8"
    }
