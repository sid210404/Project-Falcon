from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.strategy.orb_strategy import ORBStrategy
from app.backtesting.engine import BacktestEngine


history = HistoricalData()

df = history.fetch(
    "RELIANCE",
    interval="5m",
    days=5,
)

# Apply all indicators
df = IndicatorEngine.apply_all(df)

print("Data Columns:")
print(df.columns.tolist())

engine = BacktestEngine(
    strategy=ORBStrategy(),
    symbol="RELIANCE",
    capital=100000,
)

stats = engine.run(df)

print("\n========== STATISTICS ==========\n")

for key, value in stats.items():
    print(f"{key:20}: {value}")

print("\n========== TRADES ==========\n")

for trade in engine.portfolio.trades:
    print(trade)