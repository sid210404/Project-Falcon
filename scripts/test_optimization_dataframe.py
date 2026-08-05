from app.data.historical_data import HistoricalData
from app.indicators.indicator_engine import IndicatorEngine
from app.optimization.dataframe import OptimizationDataFrame
from app.optimization.optimizer import Optimizer
from app.strategy.orb_strategy import ORBStrategy


symbol = "RELIANCE"

df = HistoricalData.fetch(symbol=symbol, interval="15m", days=30)
df = IndicatorEngine.apply_all(df)

optimizer = Optimizer()

results = optimizer.optimize(
    strategy_class=ORBStrategy,
    parameter_space=ORBStrategy.parameter_space,
    df=df,
    symbol=symbol,
    capital=100000,
)

df_results = OptimizationDataFrame.build(results)

print(df_results)