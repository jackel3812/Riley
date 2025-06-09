"""
Web Search - Provides web search functionality.
"""

import logging
import webbrowser
import urllib.parse

class WebSearch:
    """Handles web searches through various search engines."""
    
    def __init__(self):
        """Initialize the Web Search feature."""
        self.logger = logging.getLogger(__name__)
        
        # Search engine URLs
        self.search_engines = {
            'google': 'https://www.google.com/search?q={}',
            'bing': 'https://www.bing.com/search?q={}',
            'duckduckgo': 'https://duckduckgo.com/?q={}',
            'youtube': 'https://www.youtube.com/results?search_query={}'
        }
        
        # Default search engine
        self.default_engine = 'google'
        
        self.logger.info("Web Search initialized")
    
    def search(self, query, engine=None):
        """Perform a web search with the specified query.
        
        Args:
            query: Search query string
            engine: Search engine to use (default is Google)
            
        Returns:
            True if successful, False otherwise
        """
        if not query:
            self.logger.warning("Empty search query")
            return False
        
        self.logger.debug(f"Searching for '{query}' using {engine or self.default_engine}")
        
        # Use specified engine or default
        engine = engine.lower() if engine else self.default_engine
        
        # Check if the engine is supported
        if engine not in self.search_engines:
            self.logger.warning(f"Unsupported search engine: {engine}, using {self.default_engine}")
            engine = self.default_engine
        
        # Encode the query for URL
        encoded_query = urllib.parse.quote_plus(query)
        
        # Build the search URL
        url = self.search_engines[engine].format(encoded_query)
        
        try:
            # Open the URL in the default browser
            webbrowser.open(url)
            return True
        except Exception as e:
            self.logger.error(f"Error opening search URL: {e}")
            return False
    
    def youtube_search(self, query):
        """Search for videos on YouTube.
        
        Args:
            query: Search query string
            
        Returns:
            True if successful, False otherwise
        """
        return self.search(query, engine='youtube')
    
    def image_search(self, query):
        """Search for images.
        
        Args:
            query: Search query string
            
        Returns:
            True if successful, False otherwise
        """
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={encoded_query}&tbm=isch"
        
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            self.logger.error(f"Error opening image search URL: {e}")
            return False
    
    def maps_search(self, query):
        """Search for locations on Google Maps.
        
        Args:
            query: Location to search for
            
        Returns:
            True if successful, False otherwise
        """
        encoded_query = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/maps/search/{encoded_query}"
        
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            self.logger.error(f"Error opening maps search URL: {e}")
            return False
