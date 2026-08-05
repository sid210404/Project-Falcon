from app.backtesting.backtest_runner import BacktestRunner
from app.optimization.models import OptimizationResult
from app.optimization.parameter_grid import ParameterGrid


class Optimizer:
    """
    Runs parameter optimization for any strategy.
    """

    def optimize(
        self,
        strategy_class,
        df,
        symbol,
        capital,
    ):

        results = []

        grid = ParameterGrid.generate(
            strategy_class.parameter_space
        )

        total = len(grid)

        print(f"\nRunning {total} optimization combinations...\n")

        for i, params in enumerate(grid, start=1):

            print(f"[{i}/{total}] Testing {params}")

            strategy = strategy_class(**params)

            result = BacktestRunner.run(
                strategy=strategy,
                symbol=symbol,
                df=df,
                capital=capital,
            )

            results.append(
                OptimizationResult(
                    parameters=params,
                    net_profit=result.portfolio.total_pnl,
                    return_pct=result.portfolio.total_return_pct,
                    win_rate=result.portfolio.win_rate,
                    profit_factor=result.portfolio.profit_factor,
                    sharpe_ratio=result.performance["sharpe_ratio"],
                    max_drawdown=result.drawdown["max_drawdown_pct"],
                    total_trades=result.portfolio.total_trades,
                )
            )

        return results