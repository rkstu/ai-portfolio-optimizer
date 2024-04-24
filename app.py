import streamlit as st
from data_fetch import fetch_stock_data
from portfolio_metrics import calculate_portfolio_metrics
from portfolio_optimization import optimize_portfolio

def main():
    st.title('Portfolio Optimization App')

    # Input for list of stocks and corresponding weightage
    stocks_input = st.text_area("Enter list of stocks (comma-separated)", "AAPL, GOOGL, MSFT")
    weights_input = st.text_area("Enter corresponding weightage (comma-separated)", "0.4, 0.4, 0.2")

    # Convert input to lists
    stocks = [stock.strip() for stock in stocks_input.split(',')]
    weights = [float(weight.strip()) for weight in weights_input.split(',')]

    if st.button('Optimize Portfolio'):
        # Fetch historical stock data
        stock_data = fetch_stock_data(stocks, start_date='2023-01-01', end_date='2024-01-01')

        # Calculate current portfolio metrics
        risk, returns = calculate_portfolio_metrics(stock_data, weights)
        st.write("Current Portfolio Metrics:")
        st.write("Potential Risk:", risk)
        st.write("Potential Returns:", returns)

        # Optimize portfolio weights
        optimized_weights = optimize_portfolio(stock_data)
        st.write("Optimized Portfolio Weights:")
        st.write(optimized_weights)

if __name__ == "__main__":
    main()
