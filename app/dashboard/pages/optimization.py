from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from app.core.config import BacktestConfig
from app.core.constants import YAHOO_INTERVAL_LIMITS
from app.core.settings import Settings
from app.services.falcon_service import FalconService
from app.strategy.registry import StrategyRegistry


def render():

    st.title("⚙ Strategy Optimization")

    # ==========================================================
    # Market Data
    # ==========================================================

    with st.expander("📊 Market Data", expanded=True):

        exchange = st.selectbox(
            "Exchange",
            ["NSE", "BSE"],
            index=0,
        )

        symbol = st.text_input(
            "Symbol",
            value=Settings.DEFAULT_SYMBOL,
        )

        interval = st.selectbox(
            "Timeframe",
            list(YAHOO_INTERVAL_LIMITS.keys()),
            index=3,
        )

        today = date.today()

        max_days = YAHOO_INTERVAL_LIMITS[interval]

        if max_days is None:

            min_date = date(2000, 1, 1)

            default_start = today - timedelta(days=180)

        else:

            min_date = today - timedelta(days=max_days)

            default_start = today - timedelta(
                days=min(max_days, 30)
            )

        col1, col2 = st.columns(2)

        with col1:

            start_date = st.date_input(
                "Start Date",
                value=default_start,
                min_value=min_date,
                max_value=today,
            )

        with col2:

            end_date = st.date_input(
                "End Date",
                value=today,
                min_value=min_date,
                max_value=today,
            )

        if max_days:

            st.info(
                f"Yahoo allows approximately the last "
                f"{max_days} days for {interval} data."
            )

    # ==========================================================
    # Strategy
    # ==========================================================

    with st.expander("⚙ Strategy", expanded=True):

        strategy_name = st.selectbox(
            "Strategy",
            StrategyRegistry.names(),
        )

        strategy_class = StrategyRegistry.get(strategy_name)

        st.subheader("Parameter Space")

        for parameter, metadata in strategy_class.parameter_space.items():

            st.markdown(
                f"**{metadata['label']}**"
            )

            st.caption(
                "Values: "
                + ", ".join(
                    map(str, metadata["values"])
                )
            )

            st.caption(
                f"Default: {metadata['default']}"
            )

    # ==========================================================
    # Execution
    # ==========================================================

    with st.expander("💰 Execution", expanded=True):

        capital = st.number_input(
            "Capital",
            value=Settings.DEFAULT_CAPITAL,
            min_value=1000,
            step=1000,
        )

    # ==========================================================
    # Validation
    # ==========================================================

    if start_date > end_date:

        st.error("Start Date cannot be after End Date.")

        return

    # ==========================================================
    # Run
    # ==========================================================

    if st.button(
        "🚀 Run Optimization",
        type="primary",
        use_container_width=True,
    ):

        config = BacktestConfig(
            exchange=exchange,
            symbol=symbol,
            interval=interval,
            start_date=start_date,
            end_date=end_date,
            capital=capital,
        )

        service = FalconService()

        try:

            with st.spinner("Running optimization..."):

                results = service.run_optimization(
                    strategy_class=strategy_class,
                    config=config,
                )

        except Exception as e:

            st.error(str(e))
            return

        if not results:

            st.warning("No optimization results.")
            return

        # ======================================================
        # DataFrame
        # ======================================================

        rows = []

        for result in results:

            row = {}

            row.update(result.parameters)

            row["Net Profit"] = result.net_profit
            row["Return %"] = result.return_pct
            row["Win Rate"] = result.win_rate
            row["Profit Factor"] = result.profit_factor
            row["Sharpe"] = result.sharpe_ratio
            row["Max Drawdown"] = result.max_drawdown
            row["Trades"] = result.total_trades

            rows.append(row)

        df = pd.DataFrame(rows)

        # ======================================================
        # Best Result
        # ======================================================

        best = df.loc[df["Net Profit"].idxmax()]

        st.success("Optimization completed successfully!")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Best Profit",
                f"₹{best['Net Profit']:,.2f}",
            )

        with col2:

            st.metric(
                "Best Win Rate",
                f"{best['Win Rate']:.2f}%",
            )

        with col3:

            st.metric(
                "Best Sharpe",
                f"{best['Sharpe']:.2f}",
            )

        st.subheader("Best Parameters")

        parameter_names = strategy_class.parameter_space.keys()

        st.json(
            {
                key: best[key]
                for key in parameter_names
            }
        )

        # ======================================================
        # Results Table
        # ======================================================

        st.subheader("Results")

        st.dataframe(
            df,
            use_container_width=True,
        )

        # ======================================================
        # Profit Chart
        # ======================================================

        parameter = list(parameter_names)[0]

        fig = px.bar(
            df,
            x=parameter,
            y="Net Profit",
            title="Net Profit",
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

        # ======================================================
        # CSV
        # ======================================================

        st.download_button(
            "📥 Download Results",
            df.to_csv(index=False),
            file_name="optimization_results.csv",
            mime="text/csv",
        )