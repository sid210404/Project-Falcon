"""Live virtual trading dashboard; orchestration only."""

from __future__ import annotations

import streamlit as st

from app.dashboard.components.paper import controls, live_chart, order_panel, portfolio_panel
from app.services.paper_trading_service import PaperTradingService
from app.strategy.registry import StrategyRegistry


_SESSION_KEY = "paper_trading_session"
_SERVICE_KEY = "paper_trading_service"


def render() -> None:
    """Orchestrate the paper-trading service and presentation components."""
    st.title("Live Paper Trading")
    inputs, action = controls.render()
    service = st.session_state.setdefault(_SERVICE_KEY, PaperTradingService())
    session = st.session_state.get(_SESSION_KEY)
    if action == "reset":
        st.session_state.pop(_SESSION_KEY, None)
        session = None
    elif action == "start":
        if session is None:
            strategy = StrategyRegistry.get(inputs.strategy_name)()
            try:
                session = service.create_session(inputs.symbol, inputs.exchange, inputs.interval, strategy, inputs.capital)
                st.session_state[_SESSION_KEY] = session
            except Exception as error:
                st.exception(error)
                return
        service.start(session)
    elif action == "pause" and session is not None:
        service.pause(session)
    elif action == "stop" and session is not None:
        service.stop(session)

    if session is None:
        st.info("Start a session to load live Yahoo Finance candles. All orders are virtual.")
        return
    try:
        service.poll(session)
    except Exception as error:
        st.warning(f"Live data poll failed: {error}")
    st.caption(f"Status: {session.status} · {session.symbol} · {session.interval} · {session.strategy.name}")
    portfolio_panel.render(session)
    order = order_panel.render(session.symbol)
    if order is not None:
        try:
            service.submit_order(session, order)
        except ValueError as error:
            st.error(str(error))
    live_chart.render(session)
    st.subheader("Open Position")
    st.write(session.portfolio.open_position or "No open position")
    st.subheader("Trade History")
    st.dataframe([item.to_dict() for item in session.portfolio.closed_trades], use_container_width=True)
    st.subheader("Order Log")
    st.dataframe([order.__dict__ for order in session.order_log], use_container_width=True)
    st.subheader("Notifications")
    for event in session.notifications[-8:][::-1]:
        st.caption(f"{event.timestamp:%H:%M:%S} — {event.message}")
