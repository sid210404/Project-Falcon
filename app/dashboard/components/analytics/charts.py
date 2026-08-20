"""
Analytics Charts
"""

from app.dashboard.components.analytics import pnl_distribution


def render(result):

    pnl_distribution.render(result)