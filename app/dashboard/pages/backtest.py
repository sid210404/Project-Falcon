from datetime import date, timedelta

import pandas as pd
import streamlit as st

from app.core.config import BacktestConfig
from app.core.constants import YAHOO_INTERVAL_LIMITS
from app.core.settings import Settings
from app.dashboard.components.candlestick_chart import render_candlestick
from app.dashboard.components.drawdown_chart import render_drawdown_curve
from app.dashboard.components.equity_chart import render_equity_curve
from app.dashboard.components.metrics import render_metrics
from app.services.falcon_service import FalconService
from app.strategy.registry import StrategyRegistry


def render():

    st.title("📈 Backtest")

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
        ).strip().upper()

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
                f"Yahoo Finance allows approximately the last "
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

        parameters = {}

        st.subheader("Parameters")

        # ------------------------------------------------------
        # FIXED PARAMETER SELECTOR
        # ------------------------------------------------------

        for parameter, metadata in strategy_class.parameter_space.items():

            values = metadata["values"]
            default = metadata["default"]

            parameters[parameter] = st.selectbox(
                label=metadata["label"],
                options=values,
                index=values.index(default),
            )

        strategy = strategy_class(**parameters)

    # ==========================================================
    # Execution
    # ==========================================================

    with st.expander("💰 Execution", expanded=True):

        capital = st.number_input(
            "Initial Capital",
            value=Settings.DEFAULT_CAPITAL,
            min_value=1000,
            step=1000,
        )

    # ==========================================================
    # Validation
    # ==========================================================

    if symbol == "":

        st.error("Please enter a stock symbol.")

        return

    if start_date > end_date:

        st.error("Start Date cannot be after End Date.")

        return

    # ==========================================================
    # Run Backtest
    # ==========================================================

    if st.button(
        "🚀 Run Backtest",
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

            with st.spinner("Running backtest..."):

                result = service.run_backtest(
                    strategy=strategy,
                    config=config,
                    generate_report=False,
                )

        except Exception as e:

            st.exception(e)

            return

        st.success("Backtest completed successfully!")
       

        summary_tab, charts_tab, trades_tab, statistics_tab = st.tabs(
            [
                "📊 Summary",
                "📈 Charts",
                "📋 Trades",
                "📑 Statistics",
            ]
        )

        # ======================================================
        # Summary
        # ======================================================

        with summary_tab:

            render_metrics(result)

        # ======================================================
        # Charts
        # ======================================================

        with charts_tab:

            render_candlestick(result)

            st.divider()

            render_equity_curve(result)

            st.divider()

            render_drawdown_curve(result)

        # ======================================================
        # Trades
        # ======================================================

        with trades_tab:

            if result.portfolio.trades:

                df = pd.DataFrame(
                    [
                        trade.__dict__
                        for trade in result.portfolio.trades
                    ]
                )

                st.dataframe(
                    df,
                    use_container_width=True,
                )

            else:

                st.info("No trades executed.")

        # ======================================================
        # Statistics
        # ======================================================

        with statistics_tab:

            st.subheader("Statistics")
            st.json(result.statistics)

            st.subheader("Performance")
            st.json(result.performance)

            st.subheader("Drawdown")
            st.json(result.drawdown)