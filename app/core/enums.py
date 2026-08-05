from enum import Enum


class Exchange(str, Enum):

    NSE = "NSE"

    BSE = "BSE"


class DataProvider(str, Enum):

    YAHOO = "Yahoo Finance"

    ZERODHA = "Zerodha"


class Theme(str, Enum):

    LIGHT = "Light"

    DARK = "Dark"