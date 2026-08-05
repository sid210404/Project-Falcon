from app.visualization.themes import dark


def configure_layout(fig):

    fig.update_layout(

        template="plotly_dark",

        height=dark.CHART_HEIGHT,

        hovermode="x unified",

        paper_bgcolor=dark.PAPER,

        plot_bgcolor=dark.BACKGROUND,

        font=dict(
            color=dark.TEXT,
        ),

        legend=dict(
            orientation="h",
            y=1.02,
            x=0,
        ),

        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20,
        ),

        xaxis_rangeslider_visible=False,
    )

    fig.update_yaxes(
        title="Price",
        row=1,
        col=1,
    )

    fig.update_yaxes(
        title="Volume",
        row=2,
        col=1,
    )