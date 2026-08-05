from pathlib import Path
import pandas as pd

df = pd.read_csv(Path("data") / "instruments.csv")

symbol = input("Enter symbol: ").strip().upper()

result = df[df["tradingsymbol"] == symbol]

if result.empty:
    print("Symbol not found.")
else:
    print(result[[
        "tradingsymbol",
        "instrument_token",
        "exchange",
        "segment",
        "name"
    ]])