import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from backtest import dynamic_backtesting  
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
from matplotlib.lines import Line2D
import plotly.express as px


list_strategy = ['Minimum Variance', 'Omega Ratio', 'Semivariance',# 'Martingale', 
                 'Roy Safety First Ratio', 'Sortino Ratio', 'Fama French', 'CVaR', 
                 'HRP', 'Sharpe Ratio', 'Black Litterman', 'Total Return']

def show_basic():
    st.title('Backtesting Page')
    st.write("Welcome to the QAA Strategy Backtesting.")

    with st.form("input_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            tickers = st.text_input("Enter tickers separated by commas", "ABBV, MET, OXY, PERI")
            start_date_data = st.text_input("Start date for historical data", "2020-01-02")
            start_backtesting = st.text_input("Start date for backtesting", "2023-01-23")
            end_date = st.text_input("End date for backtesting", "2024-01-23")
        with col2:
            rebalance_frequency_months = st.slider("Rebalance frequency in months", 1, 12, 6)
            rf = st.number_input("Enter the risk-free rate", value=0.02)
        with col3:
            initial_portfolio_value = st.number_input("Initial portfolio value", value=1000000)
            commission = st.number_input("Transaction commission", value=0.0025)

        submitted = st.form_submit_button("Run Backtesting")

        if submitted:
            progress_text = st.empty()  # Placeholder for dynamic text
            progress_bar = st.progress(0)
            strategy_results = {}
            num_strategies = len(list_strategy)
            for i, strategy in enumerate(list_strategy):
                tickers_list = [ticker.strip() for ticker in tickers.split(',')]
                resultados_backtesting, daily_data, portfolio_values = dynamic_backtesting(
                    tickers=tickers_list,
                    start_date_data=start_date_data,
                    start_backtesting=start_backtesting,
                    end_date=end_date,
                    rebalance_frequency_months=rebalance_frequency_months, 
                    rf=rf, 
                    optimization_strategy=strategy, 
                    optimization_model='SLSQP',
                    initial_portfolio_value=initial_portfolio_value,
                    commission=commission
                )
                strategy_results[strategy] = (daily_data, portfolio_values)
                current_progress = (i + 1) / num_strategies
                progress_bar.progress(current_progress)
                progress_text.text(f"Processing: {int(current_progress * 100)}% Complete")  # Update text
                
            progress_text.text("All strategies have been processed. Displaying results...")

            # Display the resulting DataFrame
            for strategy, (result_df, _, _) in strategy_results.items():
                st.write(f"Results for {strategy}:")
                st.dataframe(result_df)

            # Plot the portfolio values for all strategies
            plot_all_strategies(strategy_results)

def plot_all_strategies(strategy_results):
    fig = px.line()
    for strategy, (daily_data, portfolio_values) in strategy_results.items():
        fig.add_scatter(x=daily_data.index, y=portfolio_values, mode='lines', name=strategy)
    fig.update_layout(title="Portfolio Value Over Time by Strategy",
                      xaxis_title='Date',
                      yaxis_title='Portfolio Value ($)',
                      legend_title='Strategy')
    st.plotly_chart(fig, use_container_width=True)
