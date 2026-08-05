"""
Chart Settings

Configuration for the Visualization Engine.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class ChartSettings:

    show_volume: bool = True

    show_trades: bool = True

    show_ema20: bool = True

    show_ema50: bool = True

    show_vwap: bool = True

    show_orb: bool = True