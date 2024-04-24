import yfinance as yf

def fetch_stock_data(stocks, start_date, end_date):
    """
    Fetch historical stock prices for the given stocks from Yahoo Finance.

    Parameters:
    - stocks (list): List of stock symbols.
    - start_date (str): Start date for historical data in 'YYYY-MM-DD' format.
    - end_date (str): End date for historical data in 'YYYY-MM-DD' format.

    Returns:
    - stock_data (DataFrame): DataFrame containing historical stock prices.
    """
    stock_data = yf.download(stocks, start=start_date, end=end_date)['Adj Close']
    return stock_data
