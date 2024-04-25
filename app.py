# app.py
import streamlit as st
import numpy as np
import datetime
from data_fetch import fetch_stock_data
from portfolio_optimization import solve_quadratic_optimization_cvxpy, solve_quadratic_optimization_scipy
import portfolio_metrics as pm
import matplotlib.pyplot as plt

def main():
    st.title("Optimization")
    
    # User input
    tickers = st.text_input("Stock tickers (comma-separated)", value="AAPL,MSFT,GOOGL", help="Example: AAPL, MSFT, GOOGL")
    weights = st.text_input("Weights (comma-separated)", value="0.3,0.4,0.3", help="Example: 0.3, 0.4, 0.3")
    start_date = st.date_input("Start Date", value=datetime.date(2018, 1, 1), min_value=None, max_value=None, help="Select the start date for data fetching")
    
    # Button to trigger optimization
    if st.button("Optimize Portfolio"):
        tickers = tickers.split(',')
        weights = [float(w) for w in weights.split(',')]
        weights = np.array(weights)

        # Fetch data
        stock_prices, index_values = fetch_stock_data(tickers, start_date)

        # Perform optimization using cvxpy
        optimized_weights_cvxpy = solve_quadratic_optimization_cvxpy(stock_prices.values, index_values.values)

        # Perform optimization using scipy
        optimized_weights_scipy = solve_quadratic_optimization_scipy(stock_prices.values, index_values.values)

        # Calculate metrics for user's initial portfolio
        user_metrics = pm.calculate_portfolio_metrics(stock_prices, weights)
        user_returns, user_volatility, user_var = user_metrics

        # Calculate metrics for optimized portfolios
        optimized_metrics_cvxpy = pm.calculate_portfolio_metrics(stock_prices, optimized_weights_cvxpy)
        optimized_metrics_scipy = pm.calculate_portfolio_metrics(stock_prices, optimized_weights_scipy)

        # Display results for initial and optimized portfolios
        pm.display_results(user_metrics, optimized_metrics_cvxpy)
        pm.display_results(user_metrics, optimized_metrics_scipy)

        # Plot risk-return profiles for initial and optimized portfolios
        pm.plot_risk_return_profile(user_volatility, user_returns, optimized_metrics_cvxpy[1], optimized_metrics_cvxpy[0], optimized_metrics_scipy[1], optimized_metrics_scipy[0])

if __name__ == "__main__":
    main()
