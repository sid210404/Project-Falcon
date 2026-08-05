from datetime import datetime

from app.backtesting.execution import ExecutionEngine

engine = ExecutionEngine()

position = engine.open_position(
    symbol="RELIANCE",
    direction="LONG",
    quantity=100,
    price=1000,
    time=datetime.now(),
    stop_loss=990,
    target=1020,
)

print("Position Opened")
print(position)

trade = engine.close_position(
    position,
    exit_price=1015,
    exit_time=datetime.now(),
)

print("\nTrade Executed")
print(trade)