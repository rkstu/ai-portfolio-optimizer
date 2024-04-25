# portfolio_optimization.py
import numpy as np
from scipy.optimize import minimize
import cvxpy as cp 

def objective_function(w, X, y):
    """
    Objective function for the optimization problem.

    Parameters:
    - w (ndarray): Weight vector.
    - X (ndarray): Design matrix.
    - y (ndarray): Target vector.

    Returns:
    - float: Value of the objective function.
    """
    # Expanded form of the squared 2-norm objective function
    return np.dot(w.T, np.dot(X.T, X) @ w) - 2 * np.dot((X.T @ y).T, w) + np.dot(y.T, y)

def solve_quadratic_optimization_cvxpy(X, y):
    """
    Solves the quadratic optimization problem using cvxpy to find the optimal weights for index replication.

    Parameters:
    - X (ndarray): Design matrix representing historical data of shape (T, n), where T is the number of time points
      and n is the number of assets (stocks).
    - y (ndarray): Target vector representing the returns of the index to be replicated, of length T.

    Returns:
    - w_star (ndarray): Optimal solution vector representing the weights of the portfolio,
      such that the portfolio mimics the index as closely as possible.
    """
    T, n = X.shape

    # Define the optimization variable representing the portfolio weights
    w = cp.Variable(n)

    # Define the objective function to minimize the squared error between replicated and actual index returns
    objective = cp.Minimize((1/T) * cp.norm(X @ w - y)**2)

    # Define the constraints:
    # - Non-negativity constraint on the weights
    # - Constraint to ensure the weights sum up to 1 (standard simplex constraint)
    constraints = [w >= 0, cp.sum(w) == 1]

    # Formulate the quadratic optimization problem
    problem = cp.Problem(objective, constraints)

    # Solve the optimization problem
    problem.solve()

    # Get the optimal solution (portfolio weights)
    w_star = w.value

    return w_star

def solve_quadratic_optimization_scipy(X, y):
    """
    Solves the quadratic optimization problem using scipy to find the optimal weights for index replication.

    Parameters:
    - X (ndarray): Design matrix representing historical data of shape (T, n), where T is the number of time points
      and n is the number of assets (stocks).
    - y (ndarray): Target vector representing the returns of the index to be replicated, of length T.

    Returns:
    - w_star (ndarray): Optimal solution vector representing the weights of the portfolio,
      such that the portfolio mimics the index as closely as possible.
    """
    n = X.shape[1]  # Number of assets

    # Initial guess for the weights (equal weights for all assets)
    w0 = np.ones(n) / n

    # Define the bounds for each weight (non-negative constraint)
    bounds = [(0, None)] * n

    # Define the equality constraint (sum of weights equals 1)
    cons = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}

    # Minimize the objective function subject to the equality constraint
    result = minimize(objective_function, w0, args=(X, y), bounds=bounds, constraints=cons)

    # Extract the optimal solution (portfolio weights)
    w_star = result.x

    return w_star
