"""Portfolio metrics panel for paper trading."""

from __future__ import annotations

import streamlit as st

from app.paper_trading.live_session import LiveSession


def render(session: LiveSession) -> None:
    """Render metrics already calculated by the paper portfolio."""
    metrics = session.portfolio.summary()
    columns = st.columns(4)
    columns[0].metric("Current Capital", f"₹{metrics['equity']:,.2f}")
    columns[1].metric("Realized PnL", f"₹{metrics['realized_pnl']:,.2f}")
    columns[2].metric("Unrealized PnL", f"₹{metrics['unrealized_pnl']:,.2f}")
    columns[3].metric("Current Drawdown", f"{metrics['drawdown_pct']:.2f}%")
    columns = st.columns(3)
    columns[0].metric("Open Positions", metrics["open_positions"])
    columns[1].metric("Closed Trades", metrics["closed_trades"])
    columns[2].metric("Win Rate", f"{metrics['win_rate']:.2f}%")
