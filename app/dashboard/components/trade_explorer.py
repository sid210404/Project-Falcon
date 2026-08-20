"""
Interactive Trade Explorer
"""

import streamlit as st


def render(result):

    trades = result.portfolio.trades

    if not trades:

        st.info("No trades executed.")

        return

    options = [

        f"Trade {i+1} | "
        f"{trade.symbol} | "
        f"₹{trade.pnl:.2f}"

        for i, trade in enumerate(trades)

    ]

    selected = st.selectbox(

        "Select Trade",

        range(len(options)),

        format_func=lambda i: options[i],

    )

    trade = trades[selected]

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "PnL",

            f"₹{trade.pnl:.2f}",

        )

        st.metric(

            "Return",

            f"{trade.return_pct:.2f}%",

        )

        st.metric(

            "Holding",

            f"{trade.holding_minutes:.1f} min",

        )

    with col2:

        st.metric(

            "Entry",

            f"₹{trade.entry_price:.2f}",

        )

        st.metric(

            "Exit",

            f"₹{trade.exit_price:.2f}",

        )

        st.metric(

            "Exit Reason",

            trade.exit_reason,

        )