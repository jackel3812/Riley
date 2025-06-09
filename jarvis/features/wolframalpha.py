"""
Wolfram Alpha - Provides information and calculations using Wolfram Alpha.
"""

import os
import logging
import re

# Try importing Wolfram Alpha library
try:
    import wolframalpha
    WOLFRAMALPHA_AVAILABLE = True
except ImportError:
    WOLFRAMALPHA_AVAILABLE = False

class WolframAlpha:
    """Handles queries to the Wolfram Alpha API."""
    
    def __init__(self):
        """Initialize the Wolfram Alpha feature."""
        self.logger = logging.getLogger(__name__)
        self.app_id = os.environ.get("WOLFRAMALPHA_APP_ID", "")
        self.client = None
        
        if not self.app_id:
            self.logger.warning("Wolfram Alpha App ID not found in environment variables")
        elif WOLFRAMALPHA_AVAILABLE:
            try:
                self.client = wolframalpha.Client(self.app_id)
                self.logger.info("Wolfram Alpha client initialized")
            except Exception as e:
                self.logger.error(f"Error initializing Wolfram Alpha client: {e}")
        else:
            self.logger.warning("Wolfram Alpha library not available. Install the 'wolframalpha' package.")
    
    def query(self, query_str, include_pods=None):
        """Send a query to Wolfram Alpha and get the result.
        
        Args:
            query_str: The query string to send
            include_pods: List of pod IDs to include in the result
            
        Returns:
            String with query result or None if error
        """
        if not WOLFRAMALPHA_AVAILABLE or not self.client:
            self.logger.warning("Wolfram Alpha service not available")
            return None
        
        self.logger.debug(f"Querying Wolfram Alpha with '{query_str}'")
        
        try:
            # Check if it's a math expression that can be evaluated directly
            if self._is_math_expression(query_str):
                query_str = f"calculate {query_str}"
            
            # Send the query to Wolfram Alpha
            res = self.client.query(query_str)
            
            # Check if we got an answer
            if not hasattr(res, 'pods') or len(res.pods) == 0:
                return None
            
            # Default to more concise answer
            primary_pod = None
            
            # Try to get the Result pod first
            for pod in res.pods:
                if pod.id in ('Result', 'Solution'):
                    primary_pod = pod
                    break
            
            # If no Result pod, try other useful pods
            if not primary_pod:
                for pod in res.pods:
                    if pod.id in ('DecimalApproximation', 'Definition', 'Value', 'BasicInformation'):
                        primary_pod = pod
                        break
            
            # If still no pod, use the first non-input pod
            if not primary_pod:
                for pod in res.pods:
                    if pod.id != 'Input':
                        primary_pod = pod
                        break
            
            # If we found a suitable pod, extract the text
            if primary_pod and hasattr(primary_pod, 'text') and primary_pod.text:
                return primary_pod.text
            
            # If we reach here, try to extract any text from the response
            all_results = []
            
            for pod in res.pods:
                if pod.id != 'Input' and hasattr(pod, 'text') and pod.text:
                    all_results.append(f"{pod.title}: {pod.text}")
            
            if all_results:
                return '\n'.join(all_results[:3])  # Limit to first 3 results
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error querying Wolfram Alpha: {e}")
            return None
    
    def _is_math_expression(self, text):
        """Check if the text is likely a mathematical expression.
        
        Args:
            text: Text to check
            
        Returns:
            True if likely a math expression, False otherwise
        """
        # Remove common phrase prefixes
        text = re.sub(r'^(calculate|compute|what is|solve|evaluate)\s+', '', text, flags=re.IGNORECASE)
        
        # Check if the remaining text contains math operators and digits
        math_pattern = r'[-+*/^()=<>√∛∜π]|\d+(\.\d+)?'
        matches = re.findall(math_pattern, text)
        
        return len(matches) > 0 and any(c.isdigit() for c in text)
    
    def convert_units(self, value, from_unit, to_unit):
        """Convert between different units.
        
        Args:
            value: Numeric value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            String with conversion result or None if error
        """
        query_str = f"convert {value} {from_unit} to {to_unit}"
        return self.query(query_str)
    
    def get_weather_forecast(self, location):
        """Get weather forecast for a location.
        
        Args:
            location: Location to get forecast for
            
        Returns:
            String with weather forecast or None if error
        """
        query_str = f"weather forecast {location}"
        return self.query(query_str)
    
    def solve_equation(self, equation):
        """Solve a mathematical equation.
        
        Args:
            equation: Equation to solve
            
        Returns:
            String with solution or None if error
        """
        query_str = f"solve {equation}"
        return self.query(query_str)
    
    def calculate_expression(self, expression):
        """Calculate a mathematical expression.
        
        Args:
            expression: Expression to calculate
            
        Returns:
            String with calculation result or None if error
        """
        query_str = f"calculate {expression}"
        return self.query(query_str)
