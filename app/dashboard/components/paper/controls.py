"""Controls for paper-trading session orchestration."""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from app.core.settings import Settings
from app.strategy.registry import StrategyRegistry


@dataclass(frozen=True, slots=True)
class PaperTradingInputs:
    """User-selected configuration returned to the page orchestrator."""
    symbol: str
    exchange: str
    interval: str
    strategy_name: str
    capital: float


def render() -> tuple[PaperTradingInputs, str | None]:
    """Render controls and return the requested action without executing it."""
    with st.expander("Paper Trading Controls", expanded=True):
        symbol = st.text_input("Symbol", Settings.DEFAULT_SYMBOL, key="paper_symbol").strip().upper()
        exchange = st.selectbox("Exchange", ["NSE", "BSE"], key="paper_exchange")
        interval = st.selectbox("Timeframe", ["1m", "2m", "5m", "15m", "30m", "60m", "1d"], index=3, key="paper_interval")
        strategy_name = st.selectbox("Strategy", StrategyRegistry.names(), key="paper_strategy")
        capital = st.number_input("Virtual Capital", min_value=1000, value=Settings.DEFAULT_CAPITAL, step=1000, key="paper_capital")
        columns = st.columns(4)
        actions = {"start": columns[0].button("Start / Resume"), "pause": columns[1].button("Pause"), "stop": columns[2].button("Stop"), "reset": columns[3].button("Reset")}
    action = next((name for name, clicked in actions.items() if clicked), None)
    return PaperTradingInputs(symbol, exchange, interval, strategy_name, capital), action
