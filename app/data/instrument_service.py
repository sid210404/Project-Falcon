from pathlib import Path

import pandas as pd


class InstrumentService:
    def __init__(self):
        self.file = Path("data") / "instruments.csv"

        if not self.file.exists():
            raise FileNotFoundError(
                "Instrument list not found. Run download_instruments.py first."
            )

        self.df = pd.read_csv(self.file)

    def get_token(self, symbol: str):
        symbol = symbol.upper()

        result = self.df[
            (self.df["tradingsymbol"] == symbol)
            & (self.df["segment"] == "NSE")
        ]

        if result.empty:
            raise ValueError(f"{symbol} not found")

        return int(result.iloc[0]["instrument_token"])

    def get_details(self, symbol: str):
        symbol = symbol.upper()

        result = self.df[
            (self.df["tradingsymbol"] == symbol)
            & (self.df["segment"] == "NSE")
        ]

        if result.empty:
            raise ValueError(f"{symbol} not found")

        return result.iloc[0]