import numpy as np

def calculate_portfolio_metrics(stock_data, weights):
    """
    Calculate portfolio metrics: risk and returns.

    Parameters:
    - stock_data (DataFrame): DataFrame containing historical stock prices.
    - weights (list): List of weights for the portfolio.

    Returns:
    - risk (float): Portfolio risk.
    - returns (float): Portfolio returns.
    """
    daily_returns = stock_data.pct_change()
    portfolio_daily_returns = daily_returns.dot(weights)
    risk = np.std(portfolio_daily_returns) * np.sqrt(252)  # Assuming 252 trading days in a year
    returns = np.mean(portfolio_daily_returns) * 252  # Annualized returns
    return risk, returns
