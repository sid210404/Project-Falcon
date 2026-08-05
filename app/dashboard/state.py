import streamlit as st

from app.core.settings import Settings


def initialize():

    defaults = {

        "exchange": Settings.DEFAULT_EXCHANGE,

        "symbol": Settings.DEFAULT_SYMBOL,

        "interval": Settings.DEFAULT_INTERVAL,

        "capital": Settings.DEFAULT_CAPITAL,

        "strategy": "ORB",

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value