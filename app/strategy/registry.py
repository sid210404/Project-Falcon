"""
Strategy Registry

Keeps track of all available strategies.
"""

from app.strategy.orb_strategy import ORBStrategy
from app.strategy.ema_crossover_strategy import EMACrossoverStrategy
from app.strategy.rsi_mean_reversion_strategy import RSIMeanReversionStrategy
from app.strategy.donchian_breakout_strategy import DonchianBreakoutStrategy


class StrategyRegistry:

    _strategies = {
        "Donchian Breakout": DonchianBreakoutStrategy,
        "EMA Crossover": EMACrossoverStrategy,
        "ORB": ORBStrategy,
        "RSI Mean Reversion": RSIMeanReversionStrategy,
    }

    @classmethod
    def names(cls):
        return sorted(cls._strategies.keys())

    @classmethod
    def get(cls, name):
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}")

        return cls._strategies[name]
