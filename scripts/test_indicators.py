from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine

history = HistoricalData()

engine = IndicatorEngine()

df = history.fetch(
    symbol="RELIANCE",
    interval="5m",
    days=5,
)

df = engine.ema(df, 20)
df = engine.sma(df, 20)
df = engine.rsi(df, 14)
df = engine.atr(df, 14)
df = engine.vwap(df)
df = engine.bollinger(df)
df = engine.macd(df)

print(df.tail())

print("\nColumns:")
print(df.columns.tolist())