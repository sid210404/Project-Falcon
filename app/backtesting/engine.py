from app.backtesting.portfolio import Portfolio
from app.backtesting.statistics import Statistics
from app.backtesting.execution import ExecutionEngine
from app.backtesting.risk_manager import RiskManager
from app.backtesting.exit_manager import ExitManager


class BacktestEngine:

    def __init__(
        self,
        strategy,
        symbol,
        capital=100000,
        brokerage=20,
        slippage=0.001,
    ):

        self.strategy = strategy
        self.symbol = symbol

        self.portfolio = Portfolio(capital)

        self.execution = ExecutionEngine(
            brokerage=brokerage,
            slippage=slippage,
        )

        self.risk = RiskManager()

        self.exit_manager = ExitManager()

    def run(self, df):

        # Generate strategy signals
        df = self.strategy.generate_signals(df)

        current_position = None

        for _, row in df.iterrows():

            ########################################################
            # ENTRY
            ########################################################

            if current_position is None:

                if row.signal == 1:

                    atr = row.ATR_14

                    stop_loss = self.risk.calculate_stop_loss(
                        entry_price=row.close,
                        atr=atr,
                        direction="LONG",
                    )

                    target = self.risk.calculate_target(
                        entry_price=row.close,
                        stop_loss=stop_loss,
                        direction="LONG",
                    )

                    quantity = self.risk.calculate_position_size(
                        capital=self.portfolio.capital,
                        entry_price=row.close,
                        stop_loss=stop_loss,
                    )

                    current_position = self.execution.open_position(
                        symbol=self.symbol,
                        direction="LONG",
                        quantity=quantity,
                        price=row.close,
                        entry_time=row.datetime,
                        stop_loss=stop_loss,
                        target=target,
                    )

                continue

            ########################################################
            # EXIT
            ########################################################

            should_exit, exit_price, reason = self.exit_manager.should_exit(
                current_position,
                row,
            )

            if should_exit:

                trade = self.execution.close_position(
                    position=current_position,
                    price=exit_price,
                    exit_time=row.datetime,
                )

                self.portfolio.add_trade(trade)

                current_position = None

        ########################################################
        # FORCE EXIT ON LAST CANDLE
        ########################################################

        if current_position is not None:

            last_row = df.iloc[-1]

            trade = self.execution.close_position(
                position=current_position,
                price=last_row.close,
                exit_time=last_row.datetime,
                exit_reason="END_OF_DATA",
            )

            self.portfolio.add_trade(trade)

        return self.portfolio