def configure_layout(fig):

    fig.update_layout(

        template="plotly_dark",

        height=900,

        hovermode="x unified",

        xaxis_rangeslider_visible=False,

        margin=dict(

            l=10,
            r=10,
            t=30,
            b=10,

        ),

        legend=dict(

            orientation="h",

            y=1.02,

            x=0,

        ),

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