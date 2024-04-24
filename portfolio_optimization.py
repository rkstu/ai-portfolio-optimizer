import numpy as np
import cvxpy as cp

def optimize_portfolio(stock_data):
    """
    Optimize portfolio weights using quadratic optimization.

    Parameters:
    - stock_data (DataFrame): DataFrame containing historical stock prices.

    Returns:
    - optimized_weights (list): Optimized portfolio weights.
    """
    T, n = stock_data.shape
    X = stock_data.values

    # Define optimization variable
    w = cp.Variable(n)

    # Define objective function
    objective = cp.Minimize(cp.quad_form(w, np.cov(X, rowvar=False)))

    # Define constraints
    constraints = [cp.sum(w) == 1, w >= 0]

    # Solve the optimization problem
    problem = cp.Problem(objective, constraints)
    problem.solve()

    # Get optimized weights
    optimized_weights = w.value
    return optimized_weights
