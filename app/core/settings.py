"""
Application-wide default settings.

These values are used as defaults throughout Falcon.
"""


class Settings:

    # ==============================
    # Market
    # ==============================

    DEFAULT_EXCHANGE = "NSE"

    DEFAULT_SYMBOL = "RELIANCE"

    DEFAULT_INTERVAL = "15m"

    DEFAULT_LOOKBACK_DAYS = 30

    # ==============================
    # Trading
    # ==============================

    DEFAULT_CAPITAL = 100000

    DEFAULT_BROKERAGE = 20

    DEFAULT_SLIPPAGE = 0.001

    # ==============================
    # UI
    # ==============================

    DEFAULT_THEME = "Light"

    # ==============================
    # Data
    # ==============================

    DEFAULT_DATA_PROVIDER = "Yahoo Finance"