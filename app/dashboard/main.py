import streamlit as st

from app.dashboard.state import initialize
from app.dashboard.components.sidebar import render_sidebar
from app.dashboard.pages import (
    analytics,
    backtest,
    home,
    optimization,
    paper_trading,
    reports,
    settings,
    strategy_comparison,
)

PAGES = {
    "🏠 Home": home.render,
    "📈 Backtest": backtest.render,
    "📊 Analytics": analytics.render,
    "📡 Live Paper Trading": paper_trading.render,
    "⚔️ Strategy Comparison": strategy_comparison.render,
    "⚙ Optimization": optimization.render,
    "📄 Reports": reports.render,
    "⚙ Settings": settings.render,
}


def run_dashboard():

    st.set_page_config(
        page_title="Project Falcon",
        page_icon="🦅",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply global theme and styling
    
    page = render_sidebar()

    PAGES[page]()


if __name__ == "__main__":
    run_dashboard()