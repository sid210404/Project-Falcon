"""
Visualization Layout

Common layout configuration for Falcon charts.
"""

from app.visualization.themes import dark


def configure_layout(fig):
    """
    Apply Falcon Dark Theme to a Plotly figure.
    """

    fig.update_layout(

        # ======================================================
        # Theme
        # ======================================================

        template=None,

        paper_bgcolor=dark.PAPER,

        plot_bgcolor=dark.BACKGROUND,

        # ======================================================
        # Size
        # ======================================================

        height=dark.CHART_HEIGHT,

        margin=dict(
            l=15,
            r=15,
            t=40,
            b=15,
        ),

        # ======================================================
        # Hover
        # ======================================================

        hovermode="x unified",

        hoverlabel=dict(
            bgcolor="#1E222D",
            bordercolor="#444",
            font=dict(
                family="Arial",
                size=12,
                color="white",
            ),
        ),

        # ======================================================
        # Legend
        # ======================================================

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.02,

            xanchor="left",

            x=0,

            bgcolor="rgba(0,0,0,0)",

            font=dict(

                color=dark.TEXT,

                size=12,

            ),

        ),

        # ======================================================
        # Font
        # ======================================================

        font=dict(

            family="Arial",

            size=12,

            color=dark.TEXT,

        ),

        # ======================================================
        # Disable Range Slider
        # ======================================================

        xaxis_rangeslider_visible=False,
    )

    # ==========================================================
    # X Axis
    # ==========================================================

    fig.update_xaxes(

        showgrid=True,

        gridcolor=dark.GRID,

        gridwidth=1,

        zeroline=False,

        showline=False,

        tickfont=dict(

            color=dark.TEXT,

            size=11,

        ),

    )

    # ==========================================================
    # Price Axis
    # ==========================================================

    fig.update_yaxes(

        title="Price",

        row=1,

        col=1,

        showgrid=True,

        gridcolor=dark.GRID,

        gridwidth=1,

        zeroline=False,

        tickfont=dict(

            color=dark.TEXT,

            size=11,

        ),

    )

    # ==========================================================
    # Volume Axis
    # ==========================================================

    fig.update_yaxes(

        title="Volume",

        row=2,

        col=1,

        showgrid=True,

        gridcolor=dark.GRID,

        gridwidth=1,

        zeroline=False,

        tickfont=dict(

            color=dark.TEXT,

            size=11,

        ),

    )