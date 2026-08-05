from app.backtesting.risk_manager import (
    RiskManager,
    RiskConfig,
)

config = RiskConfig(
    risk_per_trade=0.01,
    risk_reward_ratio=2,
)

risk = RiskManager(config)

capital = 100000

entry = 1000

atr = 10

stop = risk.calculate_stop_loss(
    entry,
    atr,
    "LONG",
)

target = risk.calculate_target(
    entry,
    stop,
    "LONG",
)

qty = risk.calculate_position_size(
    capital,
    entry,
    stop,
)

print(f"Capital : {capital}")
print(f"Entry   : {entry}")
print(f"ATR     : {atr}")
print(f"Stop    : {stop}")
print(f"Target  : {target}")
print(f"Qty     : {qty}")