"""
Falcon Visualization Engine

Builds reusable Plotly charts using independent layers.
"""

from plotly.subplots import make_subplots

from app.visualization.layers.price_layer import add_price_layer
from app.visualization.layers.volume_layer import add_volume_layer
from app.visualization.layers.indicator_layer import add_indicator_layer
from app.visualization.layers.trade_layer import add_trade_layer
from app.visualization.utils.layout import configure_layout


class VisualizationEngine:
    """
    Central visualization engine for Falcon.
    """

    @staticmethod
    def build(result):

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.75, 0.25],
        )

        df = result.dataframe

        add_price_layer(fig, df)

        add_volume_layer(fig, df)

        add_indicator_layer(fig, df)

        add_trade_layer(fig, result)

        configure_layout(fig)

        return fig