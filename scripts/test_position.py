from datetime import datetime

from app.backtesting.position import Position

position = Position(

    symbol="RELIANCE",

    direction="LONG",

    quantity=100,

    entry_price=1000,

    entry_time=datetime.now(),

    stop_loss=990,

    target=1020,
)

print("Open Position")
print(position)

print()

print("Current PnL @1015")

print(position.current_pnl(1015))

print()

position.close(

    exit_price=1018,

    exit_time=datetime.now(),
)

print(position)

print()

print("Realized PnL")

print(position.realized_pnl)