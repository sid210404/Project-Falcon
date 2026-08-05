"""
Strategy Registry

Keeps track of all available strategies.
"""

from app.strategy.orb_strategy import ORBStrategy


class StrategyRegistry:

    _strategies = {
        "ORB": ORBStrategy,
    }

    @classmethod
    def names(cls):
        return sorted(cls._strategies.keys())

    @classmethod
    def get(cls, name):
        if name not in cls._strategies:
            raise ValueError(f"Unknown strategy: {name}")

        return cls._strategies[name]