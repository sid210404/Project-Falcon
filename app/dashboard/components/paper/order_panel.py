"""Manual virtual-order form."""

from __future__ import annotations

import streamlit as st

from app.paper_trading.paper_order import OrderSide, OrderType, PaperOrder


def render(symbol: str) -> PaperOrder | None:
    """Render a form and return an order request without submitting it."""
    with st.expander("Manual Order", expanded=False), st.form("paper_order_form"):
        side = OrderSide(st.selectbox("Side", [member.value for member in OrderSide]))
        order_type = OrderType(st.selectbox("Order Type", [member.value for member in OrderType]))
        quantity = st.number_input("Quantity", min_value=1, value=1, step=1)
        limit_price = st.number_input("Limit Price", min_value=0.0, value=0.0) if order_type is OrderType.LIMIT else None
        stop_price = st.number_input("Stop Price", min_value=0.0, value=0.0) if order_type is OrderType.STOP else None
        stop_loss = st.number_input("Stop Loss", min_value=0.0, value=0.0)
        target = st.number_input("Target", min_value=0.0, value=0.0)
        trailing_stop = st.number_input("Trailing Stop %", min_value=0.0, value=0.0)
        submitted = st.form_submit_button("Submit Virtual Order")
    if not submitted:
        return None
    return PaperOrder(symbol=symbol, side=side, quantity=int(quantity), order_type=order_type, limit_price=limit_price, stop_price=stop_price, stop_loss=stop_loss or None, target=target or None, trailing_stop_pct=trailing_stop or None)
