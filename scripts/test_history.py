from app.data.historical_data import HistoricalData

history = HistoricalData()

df = history.fetch(
    "RELIANCE",
    interval="5m",
    days=5
)

print(df.head())
print()
print(df.tail())
print()
print(df.shape)