"""
Wikipedia Search - Provides information from Wikipedia.
"""

import logging
import textwrap

# Try importing Wikipedia library
try:
    import wikipedia
    WIKIPEDIA_AVAILABLE = True
except ImportError:
    WIKIPEDIA_AVAILABLE = False

class WikipediaSearch:
    """Handles searching and retrieving information from Wikipedia."""
    
    def __init__(self):
        """Initialize the Wikipedia Search feature."""
        self.logger = logging.getLogger(__name__)
        
        if not WIKIPEDIA_AVAILABLE:
            self.logger.warning("Wikipedia library not available. Install the 'wikipedia' package.")
        
        self.logger.info("Wikipedia Search initialized")
    
    def search(self, query, sentences=2, detailed=False):
        """Search for information on Wikipedia.
        
        Args:
            query: Search query string
            sentences: Number of sentences to include in summary
            detailed: Whether to provide a more detailed result
            
        Returns:
            String with search results or error message
        """
        if not WIKIPEDIA_AVAILABLE:
            return "I'm sorry, but I can't search Wikipedia right now. The required library is not installed."
        
        if not query:
            return "Please provide a search query."
        
        self.logger.debug(f"Searching Wikipedia for '{query}'")
        
        try:
            # Try to get a summary of the page
            # This will automatically handle disambiguation
            summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
            
            if detailed:
                # Get more information about the page
                page = wikipedia.page(query, auto_suggest=True)
                
                # Format the result with title, summary, and URL
                result = f"# {page.title}\n\n{summary}\n\nRead more: {page.url}"
                
                # Add categories if available
                if page.categories:
                    categories = ', '.join(page.categories[:5])  # Limit to first 5 categories
                    result += f"\n\nCategories: {categories}"
            else:
                # Just return the summary
                result = summary
            
            return result
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages
            options = e.options[:5]  # Limit to first 5 options
            result = f"'{query}' may refer to multiple topics. Here are some options:\n"
            for option in options:
                result += f"- {option}\n"
            result += "\nPlease try a more specific query."
            return result
            
        except wikipedia.exceptions.PageError:
            # Handle page not found
            return f"I couldn't find information about '{query}' on Wikipedia. Try a different search."
            
        except Exception as e:
            self.logger.error(f"Error searching Wikipedia: {e}")
            return f"I encountered an error while searching for '{query}'. Please try again later."
    
    def get_summary(self, query, sentences=2):
        """Get a concise summary from Wikipedia.
        
        Args:
            query: Search query string
            sentences: Number of sentences to include
            
        Returns:
            String with summary or error message
        """
        return self.search(query, sentences=sentences, detailed=False)
    
    def get_detailed_info(self, query):
        """Get detailed information from Wikipedia.
        
        Args:
            query: Search query string
            
        Returns:
            String with detailed information or error message
        """
        return self.search(query, sentences=5, detailed=True)
    
    def suggest(self, query):
        """Get Wikipedia suggestions for a partial query.
        
        Args:
            query: Partial search query
            
        Returns:
            List of suggestion strings or empty list if error
        """
        if not WIKIPEDIA_AVAILABLE or not query:
            return []
        
        try:
            suggestions = wikipedia.search(query, results=5)
            return suggestions
        except Exception as e:
            self.logger.error(f"Error getting Wikipedia suggestions: {e}")
            return []
