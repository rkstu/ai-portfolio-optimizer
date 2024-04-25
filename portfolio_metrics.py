# portfolio_metrics.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_portfolio_metrics(stock_prices, weights):
    """
    Calculate portfolio metrics based on given stock prices and weights.
    
    Args:
        stock_prices (DataFrame): Historical stock prices.
        weights (array): Portfolio weights.
        
    Returns:
        tuple: Returns, volatility, and Value at Risk (VaR) of the portfolio.
    """
    stock_prices_cleaned = stock_prices.dropna()  # Remove rows with missing values
    if stock_prices_cleaned.empty:  # Check if DataFrame is empty after removing NaN values
        return 0, 0, 0  # Return zeros if DataFrame is empty
    
    pct_change_data = stock_prices_cleaned.pct_change()
    pct_change_data.fillna(0, inplace=True)  # Replace NoneType values with zeros
    
    print("Mean:", pct_change_data.mean())
    print("Weights:", weights)
    
    # Check if pct_change_data.mean() and weights are not None
    if pct_change_data.mean() is not None and weights is not None:
        # Check if pct_change_data.mean() contains any missing values
        if np.isnan(pct_change_data.mean().values).any() or np.isnan(weights).any():
            return 0, 0, 0  # Return zeros if mean or weights contain missing values
    
    returns = np.sum(pct_change_data.mean() * weights) * 252
    volatility = np.sqrt(np.dot(weights.T, np.dot(pct_change_data.cov() * 252, weights)))
    var = volatility * np.percentile(returns, 5)
    
    return returns, volatility, var


def format_metrics(returns, volatility, var):
    """
    Format portfolio metrics for display.
    
    Args:
        returns (float): Expected returns of the portfolio.
        volatility (float): Portfolio volatility.
        var (float): Value at Risk (VaR) of the portfolio.
        
    Returns:
        tuple: Formatted returns, volatility, and VaR.
    """
    returns_pct = returns * 100
    volatility_pct = volatility * 100
    var_pct = var * 100
    return returns_pct, volatility_pct, var_pct

def display_results(user_metrics, optimized_metrics):
    """
    Display portfolio metrics.
    
    Args:
        user_metrics (tuple): User's portfolio metrics.
        optimized_metrics (tuple): Optimized portfolio metrics.
    """
    user_returns, user_volatility, user_var = user_metrics
    user_returns_pct, user_volatility_pct, user_var_pct = format_metrics(user_returns, user_volatility, user_var)

    optimized_returns, optimized_volatility, optimized_var = optimized_metrics
    optimized_returns_pct, optimized_volatility_pct, optimized_var_pct = format_metrics(optimized_returns, optimized_volatility, optimized_var)

    st.write("Current Portfolio Metrics:")
    st.write(f"Expected Returns: {user_returns_pct:.2f}%")
    st.write(f"Portfolio Volatility: {user_volatility_pct:.2f}%")
    st.write(f"Portfolio Value at Risk (VaR): {user_var_pct:.2f}%")

    st.write("Optimized Portfolio Metrics:")
    st.write(f"Expected Returns: {optimized_returns_pct:.2f}%")
    st.write(f"Portfolio Volatility: {optimized_volatility_pct:.2f}%")
    st.write(f"Portfolio Value at Risk (VaR): {optimized_var_pct:.2f}%")

def plot_risk_return_profile(user_volatility, user_returns, optimized_volatility, optimized_returns):
    """
    Plot risk-return profiles for initial and optimized portfolios.
    
    Args:
        user_volatility (float): Volatility of the initial portfolio.
        user_returns (float): Returns of the initial portfolio.
        optimized_volatility (float): Volatility of the optimized portfolio.
        optimized_returns (float): Returns of the optimized portfolio.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(user_volatility, user_returns, label='Current Portfolio', color='blue')
    ax.scatter(optimized_volatility, optimized_returns, label='Optimized Portfolio', color='red')
    ax.set_title('Risk-Return Profile')
    ax.set_xlabel('Portfolio Volatility')
    ax.set_ylabel('Expected Returns')
    ax.legend()
    st.pyplot(fig)
