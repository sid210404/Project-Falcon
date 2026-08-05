from app.data.historical_data import HistoricalData
from app.strategy.orb_strategy import ORBStrategy
from app.backtesting.engine import BacktestEngine

history = HistoricalData()

df = history.fetch(
    symbol="RELIANCE",
    interval="5m",
    days=5,
)

strategy = ORBStrategy()

engine = BacktestEngine(
    strategy=strategy,
    capital=100000,
)

results = engine.run(df)

print(results)