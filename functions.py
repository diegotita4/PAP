
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Quantitative Asset Allocation (QAA)                                                        -- #
# -- script: main.py - Python script with the main functionality                                         -- #
# -- authors: diegotita4 - Antonio-IF - JoAlfonso - J3SVS - Oscar148                                     -- #
# -- license: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007                                       -- #
# -- repository: https://github.com/diegotita4/PAP                                                       -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ----------------------------------------------------------------------------------------------------

# LIBRARIES / WARNINGS
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.optimize import minimize
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
import optuna
import warnings
import logging
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.efficient_frontier import EfficientCVaR
import yfinance as yf
optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings('ignore', message='A new study created in memory with name:')
warnings.filterwarnings('ignore', message='Method COBYLA cannot handle bounds.')

# ----------------------------------------------------------------------------------------------------


"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Quantitative Asset Allocation (QAA)                                                        -- #
# -- script: main.py - Python script with the main functionality                                         -- #
# -- authors: diegotita4 - Antonio-IF - JoAlfonso - J3SVS - Oscar148                                     -- #
# -- license: GNU GENERAL PUBLIC LICENSE - Version 3, 29 June 2007                                       -- #
# -- repository: https://github.com/diegotita4/PAP                                                       -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# ----------------------------------------------------------------------------------------------------

# LIBRARIES / WARNINGS
import yfinance as yf
import numpy as np
from scipy.optimize import minimize
import optuna
import warnings
import logging
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.efficient_frontier import EfficientCVaR
import yfinance as yf
optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings('ignore', message='A new study created in memory with name:')
warnings.filterwarnings('ignore', message='Method COBYLA cannot handle bounds.')

# ----------------------------------------------------------------------------------------------------

# CLASS DEFINITION
class QAA:
    """
    Class OptimizedStrategy: Quantitative Asset Allocation.

    This class provides functionalities for conducting quantitative analysis and asset allocation.

    Attributes:
    - tickers (list): List of asset tickers.
    - benchmark_ticker (str): Ticker of the benchmark asset.
    - rf (float): Risk-free rate.
    - lower_bound (float): Lower bound for asset weights.
    - higher_bound (float): Higher bound for asset weights.
    - start_date (str): Start date for data retrieval.
    - end_date (str): End date for data retrieval.
    - optimization_strategy (str): Selected optimization strategy.
    - optimization_model (str): Selected optimization model.

    Methods:
    - __init__: Constructor of the OptimizedStrategy class.
    - set_optimization_strategy: Sets the optimization strategy.
    - set_optimization_model: Sets the optimization model.
    - load_data: Loads historical data for the assets.
    - calculate_returns: Calculates daily returns for the assets.
    - validate_returns_empyrical: Validates the returns of each ticker using empyrical.
    - optimize_slsqp: Optimizes the objective function using the SLSQP method.
    - optimize_montecarlo: Optimizes the objective function using the Montecarlo method.
    - optimize_cobyla: Optimizes the objective function using the COBYLA method.
    - minimum_variance: Calculates the portfolio with the minimum variance.
    - omega_ratio: Calculates the portfolio with the Omega ratio.
    - semivariance: Calculates the portfolio with the Semivariance.
    - martingale: Calculates the portfolio with the Martingale strategy.
    - roy_safety_first_ratio: Calculates the portfolio with the Roy Safety First Ratio.
    - optimize: Executes the selected optimization strategy and model.
    """

    def __init__(self, tickers=None, benchmark_ticker='SPY', rf=None, lower_bound=0.10, higher_bound=0.99, start_date=None, end_date=None):
            """
            Initializes the QAA class.

            Parameters:
            - tickers (list, optional): List of asset tickers.
            - benchmark_ticker (str, optional): Ticker of the benchmark asset. Defaults to 'SPY'.
            - rf (float, optional): Risk-free rate. Defaults to None.
            - lower_bound (float, optional): Lower bound for asset weights. Defaults to 0.10.
            - higher_bound (float, optional): Higher bound for asset weights. Defaults to 0.99.
            - start_date (str, optional): Start date for data retrieval. Defaults to None.
            - end_date (str, optional): End date for data retrieval. Defaults to None.
            """
            self.tickers = tickers
            self.benchmark_ticker = benchmark_ticker
            self.rf = rf
            self.lower_bound = lower_bound
            self.higher_bound = higher_bound
            self.start_date = start_date
            self.end_date = end_date
            self.data, self.benchmark_data = self.load_data()
            self.returns = self.calculate_returns()
            self.benchmark_returns = self.calculate_benchmark_returns()
            self.optimal_weights = None
            self.optimization_strategy = None
            self.optimization_model = None

    def calculate_benchmark_returns(self):
        """Calculates daily returns for the benchmark asset."""
        if self.benchmark_data is not None:
            return self.benchmark_data.pct_change().dropna()
        else:
            raise ValueError("Benchmark data not found.")

    def set_optimization_strategy(self, strategy):
        """Sets the optimization strategy."""
        self.optimization_strategy = strategy

    def set_optimization_model(self, model):
        """Sets the optimization model."""
        self.optimization_model = model

    def load_data(self):
        """Loads historical data for the assets and benchmark."""
        if not self.tickers or self.benchmark_ticker is None:
            raise ValueError("You must provide a list of tickers and a benchmark ticker.")
        tickers_with_benchmark = self.tickers + [self.benchmark_ticker] if self.benchmark_ticker not in self.tickers else self.tickers
        data = yf.download(tickers_with_benchmark, start=self.start_date, end=self.end_date)['Adj Close']
        benchmark_data = data.pop(self.benchmark_ticker) if self.benchmark_ticker in data else None
        return data, benchmark_data

    def calculate_returns(self):
        """Calculates daily returns for the assets."""
        return self.data.pct_change().dropna()

    def validate_returns_empyrical(self):
        """Validates the returns of each ticker using empyrical."""
        results = {}

        for ticker in self.tickers:
            # Assuming self.data already has the adjusted closing prices of each ticker
            prices = self.data[ticker]

            # Calculate daily returns
            daily_returns = prices.pct_change().dropna()

            # Calculate annualized return and Sharpe ratio
            annualized_return = empyrical.annual_return(daily_returns)
            sharpe_ratio = empyrical.sharpe_ratio(daily_returns, risk_free=self.rf / 252)

            # Store the results
            results[ticker] = {
                'Annualized Return': annualized_return,
                'Sharpe Ratio': sharpe_ratio
            }

        return results
# ----------------------------------------------------------------------------------------------------

    # OPTIMIZATION MODEL SELECTION
     # 1ST OPTIMIZE MODEL: "SLSQP"
    def optimize_slsqp(self):
        """Optimizes the objective function using the SLSQP method."""
        if self.optimization_strategy == 'Minimum Variance':
            objective = self.minimum_variance
        elif self.optimization_strategy == 'Omega Ratio':
            objective = lambda weights: -self.omega_ratio(weights, self.rf)
        elif self.optimization_strategy == 'Semivariance':
            objective = self.semivariance()
        elif self.optimization_strategy == 'Martingale':
            objective = self.martingale
        elif self.optimization_strategy == 'Roy Safety First Ratio':
             objective = self.roy_safety_first_ratio
        else:
            raise ValueError("Invalid optimization strategy.")

        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = [(self.lower_bound, self.higher_bound) for _ in self.tickers]

        result = minimize(objective, np.ones(len(self.tickers)) / len(self.tickers), method='SLSQP', bounds=bounds, constraints=constraints)
        self.optimal_weights = result.x if result.success else None
# ----------------------------------------------------------------------------------------------------

     # 2ND OPTIMIZE MODEL: "MONTECARLO (w/optuna)"

    def optimize_montecarlo(self):
        """Optimizes the objective function using the Montecarlo method."""
        def objective(trial):
            # Suppress specific warnings from Optuna about suggest_uniform
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=FutureWarning)

                # Generate tentative weights with suggest_float
                weights = np.array([trial.suggest_float(f"weight_{i}", 0, 1) for i in range(len(self.tickers))])

            # Normalize the weights to sum to 1
            weights /= np.sum(weights)

            # Apply a penalty if the weights do not respect the lower bound
            penalty = 0
            for weight in weights:
                if weight < self.lower_bound:
                    penalty += 1e6 * (self.lower_bound - weight) ** 2

            # Calculate the objective value based on the selected strategy, including the penalty
            if self.optimization_strategy == 'Minimum Variance':
                objective_value = self.minimum_variance(weights) + penalty
            elif self.optimization_strategy == 'Omega Ratio':
                objective_value = -self.omega_ratio(weights, self.rf) + penalty
            elif self.optimization_strategy == 'Semivariance':
                objective_function = self.semivariance()  # Get the lambda function
                objective_value = objective_function(weights) + penalty  # Invoke it with the weights
            elif self.optimization_strategy == 'Martingale':
                objective_value = self.martingale(weights) + penalty
            elif self.optimization_strategy == 'Roy Safety First Ratio':
                objective_value = self.roy_safety_first_ratio(weights) + penalty
            else:
                raise ValueError("Invalid optimization strategy.")

            return objective_value

        # Create an Optuna study and find the optimal weights
        study = optuna.create_study(sampler=optuna.samplers.TPESampler(), direction='minimize')

        num_trials = 500  # Adjust the number of trials as necessary
        study.optimize(objective, n_trials=num_trials, n_jobs=-1)  # n_jobs=-1 uses all available cores

        # Get and save the optimal weights
        optimal_weights = np.array([study.best_params[f"weight_{i}"] for i in range(len(self.tickers))])
        optimal_weights /= np.sum(optimal_weights)  # Normalize the weights to sum to 1
        self.optimal_weights = optimal_weights

    # ----------------------------------------------------------------------------------------------------

     # 3RD OPTIMIZE MODEL: "COBYLA"

    def optimize_cobyla(self):
        """Optimizes the objective function using the COBYLA method."""
        if self.optimization_strategy == 'Minimum Variance':
            objective = self.minimum_variance
        elif self.optimization_strategy == 'Omega Ratio':
            objective = lambda weights: -self.omega_ratio(weights, self.rf)
        elif self.optimization_strategy == 'Semivariance':
            objective = self.semivariance()
        elif self.optimization_strategy == 'Martingale':
            objective = self.martingale
        elif self.optimization_strategy == 'Roy Safety First Ratio':
            objective = self.roy_safety_first_ratio
        else:
            raise ValueError("Invalid optimization strategy.")

        initial_weights = np.ones(len(self.tickers)) / len(self.tickers)

        # Define inequality constraints
        constraints = [{'type': 'ineq', 'fun': lambda weights, i=i: weights[i] - 0.10} for i in range(len(self.tickers))]
        constraints += [{'type': 'ineq', 'fun': lambda weights: 1 - np.sum(weights)},
                        {'type': 'ineq', 'fun': lambda weights: np.sum(weights) - 0.99}]  # Ensure sum close to 1

        result = minimize(objective, initial_weights, method='COBYLA', constraints=constraints, options={'maxiter': 10000, 'tol': 0.0001})
        if result.success:
            self.optimal_weights = result.x / np.sum(result.x)
        else:
            self.optimal_weights = None
    # ----------------------------------------------------------------------------------------------------  

    # 1ST QAA STRATEGY: "MIN VARIANCE"
    def minimum_variance(self, weights):
        """Minimum variance strategy."""
        return np.dot(weights.T, np.dot(self.returns.cov() * 252, weights))
    
    # ----------------------------------------------------------------------------------------------------  

    # 2ND QAA STRATEGY: "OMEGA"
    def omega_ratio(self, weights, threshold=0.0):
        """Strategy based on the Omega Ratio."""
        portfolio_returns = np.dot(self.returns, weights)
        excess_returns = portfolio_returns - threshold

        gain = np.sum(excess_returns[excess_returns > 0])
        loss = -np.sum(excess_returns[excess_returns < 0])

        if loss == 0:
            return np.inf  # Avoid division by zero
        return gain / loss
    # ----------------------------------------------------------------------------------------------------  

    # 3RD QAA STRATEGY: "SEMIVARIANCE"
    def semivariance(self):
        diff = self.returns.subtract(self.benchmark_returns, axis=0)
        negative_diff = diff.copy()
        negative_diff[negative_diff > 0] = 0
        downside_risk = negative_diff.std()

        downside_risk_df = downside_risk.to_frame()
        downside_risk_transposed = downside_risk_df.T
        mmult = np.dot(downside_risk_df, downside_risk_transposed)
        correlation = self.returns.corr()
        semi_var_matrix = (mmult * correlation) * 100

        # Define the objective function to minimize the total semivariance of the portfolio
        semivariance = lambda w: np.dot(w.T, np.dot(semi_var_matrix, w))

        return semivariance
    # ----------------------------------------------------------------------------------------------------  

    # 4TH QAA STRATEGY: "MARTINGALE "
    def martingale(self, weights):
        """Martingale strategy."""
        past_returns = self.returns.iloc[-1]  # Last returns
        adjustment = 1 - past_returns / past_returns.mean()  # Adjust based on relative performance
        adjusted_weights = weights * adjustment
        return np.dot(adjusted_weights.T, np.dot(self.returns.cov() * 252, adjusted_weights))
    
    # ----------------------------------------------------------------------------------------------------  

    # 5TH QAA STRATEGY: "ROY SAFETY FIRST RATIO"
    def roy_safety_first_ratio(self, weights):
        """Roy's Safety-First Ratio strategy."""
        expected_return = np.dot(self.returns.mean() * 252, weights)
        volatility = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov() * 252, weights)))
        return -(expected_return - self.rf) / volatility
    # ----------------------------------------------------------------------------------------------------  

    # ----------------------------------------------------------------------------------------------------  

    # 6TH QAA STRATEGY: ""

    # ----------------------------------------------------------------------------------------------------  

    # 7TH QAA STRATEGY: ""

    # ---------------------------------------------------------------------------------------------------- 

    # 8TH QAA STRATEGY: ""

    # ----------------------------------------------------------------------------------------------------  

    # 9TH QAA STRATEGY: ""

    # ----------------------------------------------------------------------------------------------------  

    # 10TH QAA STRATEGY: ""

    # ----------------------------------------------------------------------------------------------------  

    # 11TH QAA STRATEGY: ""

    # ----------------------------------------------------------------------------------------------------  


    # FINAL OPTIMIZE FUNCTION
    def optimize(self):
        """Executes the selected optimization strategy and model."""
        # Define the objective function based on the chosen strategy
        if self.optimization_strategy == 'Minimum Variance':
            self.objective_function = self.minimum_variance
        elif self.optimization_strategy == 'Omega Ratio':
            # Here it is assumed that Omega Ratio is maximized, so we minimize its negative
            self.objective_function = lambda weights: -self.omega_ratio(weights, self.rf)
        elif self.optimization_strategy == 'Semivariance':
            self.objective_function = self.semivariance()
        elif self.optimization_strategy == 'Martingale':
            self.objective_function = self.martingale
        elif self.optimization_strategy == 'Roy Safety First Ratio':
            self.objective_function = self.roy_safety_first_ratio
        else:
            raise ValueError("Invalid optimization strategy.")

        # Execute the selected optimization model
        if self.optimization_model == 'SLSQP':
            self.optimize_slsqp()
        elif self.optimization_model == 'Monte Carlo':
            self.optimize_montecarlo()
        elif self.optimization_model == 'COBYLA':
            self.optimize_cobyla()
        else:
            raise ValueError("Invalid optimization model.")