"""Live candlestick and trade-marker presentation."""

from __future__ import annotations

import plotly.graph_objects as go
import streamlit as st

from app.paper_trading.live_session import LiveSession


def render(session: LiveSession) -> None:
    """Render the session history and completed virtual trade markers."""
    frame = session.candle_history
    if frame.empty:
        st.info("Waiting for market data.")
        return
    figure = go.Figure(go.Candlestick(x=frame["datetime"], open=frame["open"], high=frame["high"], low=frame["low"], close=frame["close"], name="Price"))
    trades = [item.trade for item in session.portfolio.closed_trades]
    if trades:
        figure.add_trace(go.Scatter(x=[trade.entry_time for trade in trades], y=[trade.entry_price for trade in trades], mode="markers", marker_symbol="triangle-up", marker_color="#26A69A", name="Entries"))
        figure.add_trace(go.Scatter(x=[trade.exit_time for trade in trades], y=[trade.exit_price for trade in trades], mode="markers", marker_symbol="triangle-down", marker_color="#EF5350", name="Exits"))
    figure.update_layout(template="plotly_dark", height=550, xaxis_rangeslider_visible=False, title="Live Paper Chart")
    st.plotly_chart(figure, use_container_width=True)
