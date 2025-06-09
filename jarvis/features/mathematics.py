"""
RILEY - Mathematics Module

This module provides advanced mathematical capabilities including:
- Symbolic mathematics (equation solving, calculus, linear algebra)
- Numerical analysis
- Statistical analysis
- Plotting and visualization
- Mathematical proofs and theory
"""

import logging
import re
import numpy as np
import sympy as sp
from sympy import symbols, solve, integrate, diff, Matrix, simplify, factor, expand
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
from io import BytesIO
import base64

logger = logging.getLogger(__name__)

class MathematicsEngine:
    """Advanced mathematical analysis and problem-solving engine."""
    
    def __init__(self):
        """Initialize the mathematics engine."""
        logger.info("Initializing Mathematics Engine")
        self.initialize_symbols()
        
    def initialize_symbols(self):
        """Initialize common mathematical symbols."""
        # Common variables
        self.x, self.y, self.z = symbols('x y z')
        self.a, self.b, self.c = symbols('a b c')
        self.n, self.m = symbols('n m', integer=True)
        self.t = symbols('t')
        
        # Greek letters commonly used in math
        self.alpha, self.beta, self.gamma = symbols('alpha beta gamma')
        self.theta, self.phi = symbols('theta phi')
        
        # Constants
        self.pi = sp.pi
        self.e = sp.E
        self.infinity = sp.oo
        
    def parse_expression(self, expr_str):
        """Parse a mathematical expression string into a SymPy expression.
        
        Args:
            expr_str: String representation of mathematical expression
            
        Returns:
            SymPy expression
        """
        try:
            # Clean up the expression
            expr_str = expr_str.replace('^', '**')
            
            # Handle special functions
            expr_str = expr_str.replace('sin(', 'sp.sin(')
            expr_str = expr_str.replace('cos(', 'sp.cos(')
            expr_str = expr_str.replace('tan(', 'sp.tan(')
            expr_str = expr_str.replace('log(', 'sp.log(')
            expr_str = expr_str.replace('exp(', 'sp.exp(')
            expr_str = expr_str.replace('sqrt(', 'sp.sqrt(')
            
            # Parse the expression
            return parse_expr(expr_str)
        except Exception as e:
            logger.error(f"Error parsing expression '{expr_str}': {e}")
            raise ValueError(f"Could not parse the expression: {expr_str}. Error: {e}")
            
    def solve_equation(self, equation_str, variable=None):
        """Solve a mathematical equation or system of equations.
        
        Args:
            equation_str: String representation of equation(s)
            variable: Variable to solve for (optional)
            
        Returns:
            Dictionary with solution information
        """
        try:
            logger.info(f"Solving equation: {equation_str}")
            
            # Extract left and right side if '=' is present
            if '=' in equation_str:
                left_side, right_side = equation_str.split('=')
                left_expr = self.parse_expression(left_side.strip())
                right_expr = self.parse_expression(right_side.strip())
                equation = sp.Eq(left_expr, right_expr)
            else:
                # If no equals sign, assume it's an expression equal to 0
                equation = sp.Eq(self.parse_expression(equation_str), 0)
            
            # Determine the variable to solve for if not specified
            if variable is None:
                # Extract all symbols from the equation
                all_symbols = list(equation.free_symbols)
                
                if not all_symbols:
                    return {"error": "No variables found in the equation"}
                
                # Use x, y, or z if present, otherwise use the first symbol
                for var in [self.x, self.y, self.z]:
                    if var in all_symbols:
                        variable = var
                        break
                else:
                    variable = all_symbols[0]
            else:
                variable = self.parse_expression(variable)
            
            # Solve the equation
            solution = solve(equation, variable)
            
            # Format the solution
            if isinstance(solution, list):
                solution_strs = [str(sol) for sol in solution]
                solution_latex = [sp.latex(sol) for sol in solution]
            else:
                solution_strs = [str(solution)]
                solution_latex = [sp.latex(solution)]
            
            return {
                "equation": str(equation),
                "variable": str(variable),
                "solutions": solution_strs,
                "solutions_latex": solution_latex,
                "count": len(solution_strs)
            }
            
        except Exception as e:
            logger.error(f"Error solving equation '{equation_str}': {e}")
            return {"error": f"Could not solve the equation: {e}"}
    
    def calculate_derivative(self, expr_str, variable=None, order=1):
        """Calculate the derivative of an expression.
        
        Args:
            expr_str: String representation of the expression
            variable: Variable to differentiate with respect to (default: x)
            order: Order of the derivative (default: 1)
            
        Returns:
            Dictionary with derivative information
        """
        try:
            logger.info(f"Calculating derivative of {expr_str} with respect to {variable}, order {order}")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Determine the variable if not specified
            if variable is None:
                # If x is in the expression, use it, otherwise use the first symbol
                all_symbols = list(expr.free_symbols)
                if self.x in all_symbols:
                    variable = self.x
                elif not all_symbols:
                    return {"error": "No variables found in the expression"}
                else:
                    variable = all_symbols[0]
            else:
                variable = self.parse_expression(variable)
            
            # Calculate the derivative
            derivative = diff(expr, variable, order)
            
            # Simplify the result
            derivative_simplified = simplify(derivative)
            
            return {
                "expression": str(expr),
                "variable": str(variable),
                "order": order,
                "derivative": str(derivative),
                "derivative_simplified": str(derivative_simplified),
                "derivative_latex": sp.latex(derivative_simplified)
            }
            
        except Exception as e:
            logger.error(f"Error calculating derivative of '{expr_str}': {e}")
            return {"error": f"Could not calculate the derivative: {e}"}
    
    def calculate_integral(self, expr_str, variable=None, lower_bound=None, upper_bound=None):
        """Calculate the integral of an expression.
        
        Args:
            expr_str: String representation of the expression
            variable: Variable to integrate with respect to (default: x)
            lower_bound: Lower bound for definite integral (optional)
            upper_bound: Upper bound for definite integral (optional)
            
        Returns:
            Dictionary with integral information
        """
        try:
            logger.info(f"Calculating integral of {expr_str}")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Determine the variable if not specified
            if variable is None:
                # If x is in the expression, use it, otherwise use the first symbol
                all_symbols = list(expr.free_symbols)
                if self.x in all_symbols:
                    variable = self.x
                elif not all_symbols:
                    return {"error": "No variables found in the expression"}
                else:
                    variable = all_symbols[0]
            else:
                variable = self.parse_expression(variable)
            
            # Calculate the indefinite integral
            indefinite_integral = integrate(expr, variable)
            
            # Calculate the definite integral if bounds are provided
            definite_integral = None
            if lower_bound is not None and upper_bound is not None:
                lower = self.parse_expression(str(lower_bound))
                upper = self.parse_expression(str(upper_bound))
                definite_integral = integrate(expr, (variable, lower, upper))
            
            result = {
                "expression": str(expr),
                "variable": str(variable),
                "indefinite_integral": str(indefinite_integral),
                "indefinite_integral_latex": sp.latex(indefinite_integral)
            }
            
            if definite_integral is not None:
                result.update({
                    "lower_bound": str(lower_bound),
                    "upper_bound": str(upper_bound),
                    "definite_integral": str(definite_integral),
                    "definite_integral_latex": sp.latex(definite_integral)
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating integral of '{expr_str}': {e}")
            return {"error": f"Could not calculate the integral: {e}"}
    
    def solve_system_of_equations(self, equations_list):
        """Solve a system of equations.
        
        Args:
            equations_list: List of equation strings
            
        Returns:
            Dictionary with solution information
        """
        try:
            logger.info(f"Solving system of equations: {equations_list}")
            
            equations = []
            all_symbols = set()
            
            # Parse each equation
            for eq_str in equations_list:
                if '=' in eq_str:
                    left_side, right_side = eq_str.split('=')
                    left_expr = self.parse_expression(left_side.strip())
                    right_expr = self.parse_expression(right_side.strip())
                    equation = sp.Eq(left_expr, right_expr)
                else:
                    # If no equals sign, assume it's an expression equal to 0
                    equation = sp.Eq(self.parse_expression(eq_str), 0)
                
                equations.append(equation)
                all_symbols.update(equation.free_symbols)
            
            # Convert to list and sort for consistent results
            all_symbols = sorted(list(all_symbols), key=str)
            
            # Solve the system
            solution = solve(equations, all_symbols)
            
            # Format the solution
            if isinstance(solution, dict):
                # Format each variable's solution
                formatted_solution = {}
                for var, sol in solution.items():
                    formatted_solution[str(var)] = {
                        "value": str(sol),
                        "latex": sp.latex(sol)
                    }
                
                return {
                    "equations": [str(eq) for eq in equations],
                    "variables": [str(var) for var in all_symbols],
                    "solution": formatted_solution
                }
            elif isinstance(solution, list):
                # Multiple solution sets (e.g., for non-linear systems)
                formatted_solutions = []
                for sol_set in solution:
                    if isinstance(sol_set, tuple):
                        formatted_sol = {str(all_symbols[i]): {"value": str(val), "latex": sp.latex(val)} 
                                        for i, val in enumerate(sol_set)}
                        formatted_solutions.append(formatted_sol)
                    else:
                        # Handle unexpected solution format
                        formatted_solutions.append({"raw_solution": str(sol_set)})
                
                return {
                    "equations": [str(eq) for eq in equations],
                    "variables": [str(var) for var in all_symbols],
                    "solutions": formatted_solutions,
                    "count": len(formatted_solutions)
                }
            else:
                # Handle unexpected solution format
                return {
                    "equations": [str(eq) for eq in equations],
                    "variables": [str(var) for var in all_symbols],
                    "raw_solution": str(solution)
                }
            
        except Exception as e:
            logger.error(f"Error solving system of equations: {e}")
            return {"error": f"Could not solve the system of equations: {e}"}
    
    def factor_expression(self, expr_str):
        """Factor a mathematical expression.
        
        Args:
            expr_str: String representation of the expression
            
        Returns:
            Dictionary with factorization information
        """
        try:
            logger.info(f"Factoring expression: {expr_str}")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Factor the expression
            factored = factor(expr)
            
            return {
                "expression": str(expr),
                "factored": str(factored),
                "factored_latex": sp.latex(factored)
            }
            
        except Exception as e:
            logger.error(f"Error factoring expression '{expr_str}': {e}")
            return {"error": f"Could not factor the expression: {e}"}
    
    def expand_expression(self, expr_str):
        """Expand a mathematical expression.
        
        Args:
            expr_str: String representation of the expression
            
        Returns:
            Dictionary with expansion information
        """
        try:
            logger.info(f"Expanding expression: {expr_str}")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Expand the expression
            expanded = expand(expr)
            
            return {
                "expression": str(expr),
                "expanded": str(expanded),
                "expanded_latex": sp.latex(expanded)
            }
            
        except Exception as e:
            logger.error(f"Error expanding expression '{expr_str}': {e}")
            return {"error": f"Could not expand the expression: {e}"}
    
    def calculate_limit(self, expr_str, variable=None, approach=None):
        """Calculate the limit of an expression.
        
        Args:
            expr_str: String representation of the expression
            variable: Variable for the limit (default: x)
            approach: Value the variable approaches (default: 0)
            
        Returns:
            Dictionary with limit information
        """
        try:
            logger.info(f"Calculating limit of {expr_str}")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Determine the variable if not specified
            if variable is None:
                # If x is in the expression, use it, otherwise use the first symbol
                all_symbols = list(expr.free_symbols)
                if self.x in all_symbols:
                    variable = self.x
                elif not all_symbols:
                    return {"error": "No variables found in the expression"}
                else:
                    variable = all_symbols[0]
            else:
                variable = self.parse_expression(variable)
            
            # Set default approach value if not specified
            if approach is None:
                approach = 0
            else:
                approach = self.parse_expression(str(approach))
            
            # Calculate the limit
            limit_result = sp.limit(expr, variable, approach)
            
            return {
                "expression": str(expr),
                "variable": str(variable),
                "approach": str(approach),
                "limit": str(limit_result),
                "limit_latex": sp.latex(limit_result)
            }
            
        except Exception as e:
            logger.error(f"Error calculating limit of '{expr_str}': {e}")
            return {"error": f"Could not calculate the limit: {e}"}
    
    def analyze_function(self, expr_str, variable=None, domain=(-10, 10)):
        """Comprehensive analysis of a mathematical function.
        
        Args:
            expr_str: String representation of the function
            variable: Variable of the function (default: x)
            domain: Domain range for analysis (default: [-10, 10])
            
        Returns:
            Dictionary with function analysis information
        """
        try:
            logger.info(f"Analyzing function: {expr_str}")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Determine the variable if not specified
            if variable is None:
                # If x is in the expression, use it, otherwise use the first symbol
                all_symbols = list(expr.free_symbols)
                if self.x in all_symbols:
                    variable = self.x
                elif not all_symbols:
                    return {"error": "No variables found in the expression"}
                else:
                    variable = all_symbols[0]
            else:
                variable = self.parse_expression(variable)
            
            # Calculate the derivative
            derivative = diff(expr, variable)
            derivative_simplified = simplify(derivative)
            
            # Calculate the second derivative
            second_derivative = diff(expr, variable, 2)
            second_derivative_simplified = simplify(second_derivative)
            
            # Calculate critical points (where derivative = 0)
            critical_points_eq = sp.Eq(derivative, 0)
            critical_points = solve(critical_points_eq, variable)
            
            # Identify potential maxima, minima, and inflection points
            maxima = []
            minima = []
            inflection_points = []
            
            for point in critical_points:
                try:
                    # Check if the point is a maximum or minimum
                    second_deriv_value = second_derivative.subs(variable, point)
                    
                    if second_deriv_value < 0:
                        maxima.append(point)
                    elif second_deriv_value > 0:
                        minima.append(point)
                    
                    # Inflection points (where second derivative = 0)
                    inflection_eq = sp.Eq(second_derivative, 0)
                    inflection_candidates = solve(inflection_eq, variable)
                    
                    for inf_point in inflection_candidates:
                        inflection_points.append(inf_point)
                except Exception as e:
                    logger.warning(f"Error analyzing critical point {point}: {e}")
                    continue
            
            # Calculate the indefinite integral (antiderivative)
            antiderivative = integrate(expr, variable)
            
            # Generate plot data for visualization
            try:
                domain_min, domain_max = domain
                x_values = np.linspace(float(domain_min), float(domain_max), 100)
                y_values = []
                
                for x_val in x_values:
                    try:
                        y_val = float(expr.subs(variable, x_val))
                        y_values.append(y_val)
                    except:
                        y_values.append(np.nan)  # Use NaN for undefined points
                
                plt.figure(figsize=(10, 6))
                plt.plot(x_values, y_values)
                plt.title(f"Plot of f({variable}) = {expr}")
                plt.xlabel(str(variable))
                plt.ylabel(f"f({variable})")
                plt.grid(True)
                
                # Mark critical points
                for point in critical_points:
                    try:
                        x_val = float(point)
                        if domain_min <= x_val <= domain_max:
                            y_val = float(expr.subs(variable, x_val))
                            plt.plot(x_val, y_val, 'ro')
                    except:
                        continue
                
                # Save plot to base64 for display
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close()
                buffer.seek(0)
                plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            except Exception as e:
                logger.warning(f"Error generating plot: {e}")
                plot_data = None
            
            # Compile the analysis results
            analysis = {
                "function": str(expr),
                "function_latex": sp.latex(expr),
                "variable": str(variable),
                "derivative": {
                    "expression": str(derivative_simplified),
                    "latex": sp.latex(derivative_simplified)
                },
                "second_derivative": {
                    "expression": str(second_derivative_simplified),
                    "latex": sp.latex(second_derivative_simplified)
                },
                "critical_points": [str(point) for point in critical_points],
                "maxima": [str(point) for point in maxima],
                "minima": [str(point) for point in minima],
                "inflection_points": [str(point) for point in inflection_points],
                "antiderivative": {
                    "expression": str(antiderivative),
                    "latex": sp.latex(antiderivative)
                }
            }
            
            if plot_data:
                analysis["plot"] = {
                    "data": plot_data,
                    "format": "base64_png"
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing function '{expr_str}': {e}")
            return {"error": f"Could not analyze the function: {e}"}
    
    def perform_calculus_of_variations(self, functional_str, function_symbol='y', variable='x', boundary_conditions=None):
        """Perform calculus of variations to find the function that extremizes a functional.
        
        Args:
            functional_str: String representation of the functional
            function_symbol: Symbol for the function (default: 'y')
            variable: Independent variable (default: 'x')
            boundary_conditions: Dictionary of boundary conditions (optional)
            
        Returns:
            Dictionary with calculus of variations results
        """
        try:
            logger.info(f"Performing calculus of variations on: {functional_str}")
            
            # Parse the functional
            functional = self.parse_expression(functional_str)
            
            # Set up the symbols
            x = self.parse_expression(variable)
            y = sp.Function(function_symbol)(x)
            y_prime = y.diff(x)
            
            # Apply the Euler-Lagrange equation
            euler_lagrange = functional.diff(y) - sp.diff(functional.diff(y_prime), x)
            
            # Try to solve the Euler-Lagrange equation
            solution = sp.dsolve(euler_lagrange, y)
            
            # Format the results
            result = {
                "functional": str(functional),
                "functional_latex": sp.latex(functional),
                "function_symbol": function_symbol,
                "variable": str(variable),
                "euler_lagrange_equation": str(euler_lagrange),
                "euler_lagrange_equation_latex": sp.latex(euler_lagrange),
                "general_solution": str(solution),
                "general_solution_latex": sp.latex(solution)
            }
            
            # Apply boundary conditions if provided
            if boundary_conditions:
                # TODO: Implement application of boundary conditions
                result["boundary_conditions"] = boundary_conditions
                # This is a complex process requiring solving for constants of integration
                
            return result
            
        except Exception as e:
            logger.error(f"Error in calculus of variations for '{functional_str}': {e}")
            return {"error": f"Could not perform calculus of variations: {e}"}
    
    def compute_statistics(self, data, stats_type="basic"):
        """Compute statistical measures for a dataset.
        
        Args:
            data: List of numerical values
            stats_type: Type of statistics to compute ("basic", "descriptive", or "all")
            
        Returns:
            Dictionary with statistical measures
        """
        try:
            logger.info(f"Computing {stats_type} statistics for dataset of size {len(data)}")
            
            # Convert data to numpy array
            data_array = np.array(data, dtype=float)
            
            # Basic statistics
            basic_stats = {
                "count": len(data_array),
                "min": float(np.min(data_array)),
                "max": float(np.max(data_array)),
                "range": float(np.max(data_array) - np.min(data_array)),
                "sum": float(np.sum(data_array)),
                "mean": float(np.mean(data_array)),
                "median": float(np.median(data_array)),
                "mode": float(sp.stats.mode(data_array)[0]),
            }
            
            if stats_type == "basic":
                return basic_stats
            
            # Descriptive statistics
            descriptive_stats = {
                "variance": float(np.var(data_array)),
                "std_dev": float(np.std(data_array)),
                "skewness": float(sp.stats.skew(data_array)),
                "kurtosis": float(sp.stats.kurtosis(data_array))
            }
            
            # Combine based on requested stats type
            if stats_type == "descriptive":
                return {**basic_stats, **descriptive_stats}
            
            # Advanced statistics
            percentiles = {
                f"percentile_{p}": float(np.percentile(data_array, p))
                for p in [25, 50, 75, 90, 95, 99]
            }
            
            # Generate histogram data
            hist, bins = np.histogram(data_array, bins='auto')
            histogram_data = {
                "bin_counts": hist.tolist(),
                "bin_edges": bins.tolist()
            }
            
            # Create a distribution plot
            plt.figure(figsize=(10, 6))
            plt.hist(data_array, bins='auto', alpha=0.7)
            plt.title("Data Distribution")
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.grid(True)
            
            # Save plot to base64 for display
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            plt.close()
            buffer.seek(0)
            plot_data = base64.b64encode(buffer.read()).decode('utf-8')
            
            # Combine all statistics
            all_stats = {
                **basic_stats,
                **descriptive_stats,
                "percentiles": percentiles,
                "histogram": histogram_data,
                "distribution_plot": {
                    "data": plot_data,
                    "format": "base64_png"
                }
            }
            
            return all_stats
            
        except Exception as e:
            logger.error(f"Error computing statistics: {e}")
            return {"error": f"Could not compute statistics: {e}"}
    
    def solve_optimization_problem(self, objective_str, constraints=None, variables=None, maximize=False):
        """Solve mathematical optimization problems.
        
        Args:
            objective_str: String representation of the objective function
            constraints: List of constraint strings (optional)
            variables: List of variable strings (optional)
            maximize: Whether to maximize (True) or minimize (False) the objective
            
        Returns:
            Dictionary with optimization results
        """
        try:
            logger.info(f"Solving optimization problem: {'maximize' if maximize else 'minimize'} {objective_str}")
            
            # Parse the objective function
            objective = self.parse_expression(objective_str)
            
            # Determine the variables if not specified
            if variables is None:
                all_symbols = list(objective.free_symbols)
                variables = all_symbols
            else:
                variables = [self.parse_expression(var) for var in variables]
            
            # Parse constraints if provided
            parsed_constraints = []
            if constraints:
                for constraint_str in constraints:
                    if '=' in constraint_str:
                        left_side, right_side = constraint_str.split('=')
                        left_expr = self.parse_expression(left_side.strip())
                        right_expr = self.parse_expression(right_side.strip())
                        
                        if '≤' in constraint_str or '<=' in constraint_str:
                            parsed_constraints.append(sp.LessThan(left_expr, right_expr))
                        elif '≥' in constraint_str or '>=' in constraint_str:
                            parsed_constraints.append(sp.GreaterThan(left_expr, right_expr))
                        else:
                            parsed_constraints.append(sp.Eq(left_expr, right_expr))
                    else:
                        # If no equals sign, assume it's an expression equal to 0
                        parsed_constraints.append(sp.Eq(self.parse_expression(constraint_str), 0))
            
            # For unconstrained optimization with one or two variables
            if not constraints and len(variables) <= 2:
                # Find critical points by taking partial derivatives
                critical_points_eqs = [sp.Eq(objective.diff(var), 0) for var in variables]
                critical_points = sp.solve(critical_points_eqs, variables)
                
                # Evaluate objective at critical points
                optimal_value = None
                optimal_point = None
                
                if isinstance(critical_points, list):
                    for point in critical_points:
                        # Substitute values into objective
                        value = objective
                        for i, var in enumerate(variables):
                            value = value.subs(var, point[i])
                        
                        # Update optimal value (maximize or minimize)
                        if optimal_value is None or (maximize and value > optimal_value) or (not maximize and value < optimal_value):
                            optimal_value = value
                            optimal_point = point
                elif isinstance(critical_points, dict):
                    # Substitute values into objective
                    value = objective
                    for var, val in critical_points.items():
                        value = value.subs(var, val)
                    
                    optimal_value = value
                    optimal_point = [critical_points[var] for var in variables]
                
                # Format the result
                result = {
                    "objective": str(objective),
                    "objective_latex": sp.latex(objective),
                    "operation": "maximize" if maximize else "minimize",
                    "variables": [str(var) for var in variables],
                    "critical_points": [str(point) for point in critical_points],
                    "optimal_point": [str(val) for val in optimal_point] if optimal_point else None,
                    "optimal_value": str(optimal_value) if optimal_value else None
                }
                
                return result
            
            # For constrained optimization or many variables, provide a symbolic answer
            # (Full implementation would require numerical optimization)
            return {
                "objective": str(objective),
                "objective_latex": sp.latex(objective),
                "operation": "maximize" if maximize else "minimize",
                "variables": [str(var) for var in variables],
                "constraints": [str(constraint) for constraint in parsed_constraints],
                "note": "For complex constrained optimization problems, numerical methods are required."
            }
            
        except Exception as e:
            logger.error(f"Error solving optimization problem: {e}")
            return {"error": f"Could not solve the optimization problem: {e}"}
    
    def compute_taylor_series(self, expr_str, variable=None, around_point=0, num_terms=5):
        """Compute the Taylor series expansion of a function.
        
        Args:
            expr_str: String representation of the function
            variable: Variable for expansion (default: x)
            around_point: Point around which to expand (default: 0)
            num_terms: Number of terms in the expansion (default: 5)
            
        Returns:
            Dictionary with Taylor series information
        """
        try:
            logger.info(f"Computing Taylor series for {expr_str} around {around_point} with {num_terms} terms")
            
            # Parse the expression
            expr = self.parse_expression(expr_str)
            
            # Determine the variable if not specified
            if variable is None:
                # If x is in the expression, use it, otherwise use the first symbol
                all_symbols = list(expr.free_symbols)
                if self.x in all_symbols:
                    variable = self.x
                elif not all_symbols:
                    return {"error": "No variables found in the expression"}
                else:
                    variable = all_symbols[0]
            else:
                variable = self.parse_expression(variable)
            
            # Compute the Taylor series
            taylor_series = expr.series(variable, around_point, num_terms).removeO()
            
            # Compute individual terms for explanation
            terms = []
            for n in range(num_terms):
                term = sp.diff(expr, variable, n).subs(variable, around_point) * (variable - around_point)**n / sp.factorial(n)
                terms.append({
                    "order": n,
                    "term": str(term),
                    "term_latex": sp.latex(term)
                })
            
            return {
                "function": str(expr),
                "function_latex": sp.latex(expr),
                "variable": str(variable),
                "around_point": str(around_point),
                "num_terms": num_terms,
                "taylor_series": str(taylor_series),
                "taylor_series_latex": sp.latex(taylor_series),
                "terms": terms
            }
            
        except Exception as e:
            logger.error(f"Error computing Taylor series for '{expr_str}': {e}")
            return {"error": f"Could not compute the Taylor series: {e}"}

    def analyze_linear_system(self, matrix_str, augmented=False):
        """Analyze a system of linear equations using matrix methods.
        
        Args:
            matrix_str: String representation of the coefficient matrix
            augmented: Whether the matrix is augmented with constants (default: False)
            
        Returns:
            Dictionary with linear system analysis
        """
        try:
            logger.info(f"Analyzing linear system with matrix: {matrix_str}")
            
            # Parse the matrix
            if isinstance(matrix_str, str):
                # Clean up the matrix string
                matrix_str = matrix_str.replace('[', '').replace(']', '')
                
                # Split into rows
                rows = matrix_str.strip().split(';')
                matrix_data = []
                
                for row in rows:
                    # Split the row into elements
                    elements = row.strip().split()
                    row_data = [self.parse_expression(elem) for elem in elements]
                    matrix_data.append(row_data)
                
                matrix = Matrix(matrix_data)
            else:
                # Assume it's already a matrix
                matrix = Matrix(matrix_str)
            
            # Dimensions of the matrix
            m, n = matrix.shape
            
            # If augmented, separate the coefficient matrix and constants
            if augmented:
                coeff_matrix = matrix[:, :-1]
                constants = matrix[:, -1]
                n = n - 1  # Adjust the number of variables
            else:
                coeff_matrix = matrix
                constants = None
            
            # Compute rank
            rank_coeff = coeff_matrix.rank()
            
            # Compute determinant if square
            determinant = None
            if coeff_matrix.is_square:
                determinant = coeff_matrix.det()
            
            # Compute reduced row echelon form
            rref_matrix, pivots = coeff_matrix.rref()
            
            # Determine solution type
            solution_type = None
            if augmented:
                # Compute rank of augmented matrix
                rank_aug = matrix.rank()
                
                if rank_coeff < rank_aug:
                    solution_type = "inconsistent"
                elif rank_coeff == rank_aug:
                    if rank_coeff == n:
                        solution_type = "unique"
                    else:
                        solution_type = f"infinite ({n - rank_coeff} parameter(s))"
            else:
                if coeff_matrix.is_square and determinant != 0:
                    solution_type = "unique"
                elif rank_coeff < n:
                    solution_type = f"infinite ({n - rank_coeff} parameter(s))"
                else:
                    solution_type = "undetermined without constants"
            
            # Calculate eigenvalues and eigenvectors if square
            eigenvalues = None
            eigenvectors = None
            if coeff_matrix.is_square:
                eigenvalues = coeff_matrix.eigenvals()
                eigenvectors = coeff_matrix.eigenvects()
            
            # Solve the system if augmented
            solution = None
            if augmented and solution_type != "inconsistent":
                try:
                    # Create variable symbols
                    variables = [sp.Symbol(f'x{i+1}') for i in range(n)]
                    
                    # Set up the system
                    system = []
                    for i in range(m):
                        equation = sum(coeff_matrix[i, j] * variables[j] for j in range(n)) - constants[i]
                        system.append(equation)
                    
                    # Solve the system
                    solution = sp.solve(system, variables)
                except Exception as e:
                    logger.warning(f"Error solving the system: {e}")
                    solution = None
            
            # Format the results
            result = {
                "matrix": str(matrix),
                "matrix_latex": sp.latex(matrix),
                "dimensions": {
                    "rows": m,
                    "columns": n if not augmented else n + 1
                },
                "coefficient_matrix": {
                    "matrix": str(coeff_matrix),
                    "matrix_latex": sp.latex(coeff_matrix),
                    "rank": rank_coeff,
                },
                "rref": {
                    "matrix": str(rref_matrix),
                    "matrix_latex": sp.latex(rref_matrix),
                    "pivots": list(pivots)
                }
            }
            
            if determinant is not None:
                result["determinant"] = {
                    "value": str(determinant),
                    "latex": sp.latex(determinant)
                }
            
            if eigenvalues is not None:
                result["eigenvalues"] = {
                    "values": [{"value": str(val), "multiplicity": mult} 
                               for val, mult in eigenvalues.items()]
                }
            
            if solution_type is not None:
                result["solution_type"] = solution_type
            
            if augmented:
                result["constants"] = {
                    "vector": str(constants),
                    "vector_latex": sp.latex(constants)
                }
                
                if solution is not None:
                    result["solution"] = str(solution)
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing linear system: {e}")
            return {"error": f"Could not analyze the linear system: {e}"}

# Initialize the mathematics engine
math_engine = MathematicsEngine()

def get_mathematics_engine():
    """Get the global mathematics engine instance."""
    global math_engine
    return math_engine