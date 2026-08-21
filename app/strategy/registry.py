"""
Strategy Registry

Central registry for all Falcon strategies.
"""

from __future__ import annotations

from app.strategy.donchian_breakout_strategy import DonchianBreakoutStrategy
from app.strategy.ema_9_21 import EMA921Strategy
from app.strategy.ema_crossover_strategy import EMACrossoverStrategy
from app.strategy.orb_strategy import ORBStrategy
from app.strategy.rsi_mean_reversion_strategy import RSIMeanReversionStrategy
from app.strategy.supertrend_strategy import SuperTrendStrategy
from app.strategy.vwap_pullback_strategy import VWAPPullbackStrategy
from app.strategy.orb_pro_strategy import ORBProStrategy
class StrategyRegistry:
    """Registry of available trading strategies."""

    _strategies = {
        "EMA 9/21 Trend": EMA921Strategy,
        "EMA Crossover": EMACrossoverStrategy,
        "RSI Mean Reversion": RSIMeanReversionStrategy,
        "Donchian Breakout": DonchianBreakoutStrategy,
        "ORB": ORBStrategy,
        "SuperTrend": SuperTrendStrategy,
        "VWAP Pullback": VWAPPullbackStrategy,
        "ORB Pro": ORBProStrategy,
    }

    @classmethod
    def names(cls) -> list[str]:
        """Return all strategy names sorted alphabetically."""
        return sorted(cls._strategies.keys())

    @classmethod
    def get(cls, name: str):
        """Return the strategy class for a given name."""
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}")
        return cls._strategies[name]

    @classmethod
    def create(cls, name: str, **kwargs):
        """Instantiate a strategy with optional parameters."""
        return cls.get(name)(**kwargs)

    @classmethod
    def register(cls, name: str, strategy_cls):
        """Register a new strategy at runtime."""
        cls._strategies[name] = strategy_cls

    @classmethod
    def unregister(cls, name: str):
        """Remove a strategy from the registry."""
        cls._strategies.pop(name, None)

    @classmethod
    def exists(cls, name: str) -> bool:
        """Check whether a strategy is registered."""
        return name in cls._strategies

    @classmethod
    def all(cls) -> dict[str, type]:
        """Return a copy of the registry."""
        return cls._strategies.copy()