from app.backtesting.position import Position
from app.backtesting.trade import Trade


class ExecutionEngine:

    def __init__(self, brokerage=20, slippage=0.001):
        self.brokerage = brokerage
        self.slippage = slippage

    def open_position(
        self,
        symbol,
        direction,
        quantity,
        price,
        entry_time,
        stop_loss,
        target,
    ):

        if direction == "LONG":
            execution_price = price * (1 + self.slippage)
        else:
            execution_price = price * (1 - self.slippage)

        return Position(
            symbol=symbol,
            direction=direction,
            quantity=quantity,
            entry_price=execution_price,
            entry_time=entry_time,
            stop_loss=stop_loss,
            target=target,
        )

    def close_position(
        self,
        position,
        price,
        exit_time,
        exit_reason="UNKNOWN",
    ):

        # Apply exit slippage
        if position.direction == "LONG":
            execution_price = price * (1 - self.slippage)
        else:
            execution_price = price * (1 + self.slippage)

        # Close the position
        position.close(
            execution_price,
            exit_time,
        )

        gross_pnl = position.realized_pnl
        net_pnl = gross_pnl - self.brokerage

        # Slippage calculations
        if position.direction == "LONG":
            original_entry = position.entry_price / (1 + self.slippage)
        else:
            original_entry = position.entry_price / (1 - self.slippage)

        entry_slippage = abs(position.entry_price - original_entry)
        exit_slippage = abs(price - execution_price)

        total_slippage = entry_slippage + exit_slippage

        invested_amount = position.entry_price * position.quantity

        return_pct = (
            (net_pnl / invested_amount) * 100
            if invested_amount > 0
            else 0
        )

        risk_amount = abs(
            position.entry_price - position.stop_loss
        ) * position.quantity

        reward_amount = net_pnl

        risk_reward = (
            reward_amount / risk_amount
            if risk_amount > 0
            else 0
        )

        return Trade(
            symbol=position.symbol,
            direction=position.direction,
            quantity=position.quantity,

            entry_time=position.entry_time,
            entry_price=position.entry_price,

            exit_time=position.exit_time,
            exit_price=position.exit_price,
            exit_reason=exit_reason,

            pnl=net_pnl,
            return_pct=return_pct,

            risk_amount=risk_amount,
            reward_amount=reward_amount,
            risk_reward=risk_reward,

            brokerage=self.brokerage,
            slippage=total_slippage,

            capital_after_trade=0.0,   # Updated by Portfolio
        )