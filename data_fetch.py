# data_fetch.py
import yfinance as yf

def fetch_stock_data(tickers, start_date=None):
    """
    Fetch historical stock data for the given tickers and start date.
    
    Args:
        tickers (list): List of stock tickers.
        start_date (str): Start date for data fetching.
        
    Returns:
        tuple: Historical stock prices and index values.
    """
    if start_date is None:
        start_date = "2018-01-01"
    stock_data = yf.download(tickers, start=start_date, end=None)
    stock_prices = stock_data['Adj Close']
    index_data = yf.download("^GSPC", start=start_date, end=None)
    index_values = index_data['Adj Close']
    return stock_prices, index_values
