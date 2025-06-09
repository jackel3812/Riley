"""
RILEY - Perplexity API Connector

This module provides functions to interact with the Perplexity API for enhanced
question answering capabilities.
"""

import os
import json
import logging
import requests
from typing import List, Dict, Optional, Union, Any

# Configure logging
logger = logging.getLogger(__name__)

def is_available() -> bool:
    """Check if the Perplexity API is available by verifying the API key."""
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    if not api_key:
        logger.warning("Perplexity API key not found in environment variables")
        return False
    
    # Verify the API key with a minimal request
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple test request
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json={
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant."
                    },
                    {
                        "role": "user", 
                        "content": "Test request, please respond with 'Working'."
                    }
                ],
                "max_tokens": 10,
                "temperature": 0.2,
                "stream": False
            },
            timeout=5  # Set a timeout to avoid hanging
        )
        
        if response.status_code == 200:
            logger.info("Perplexity API key is valid")
            return True
        else:
            logger.warning(f"Perplexity API key validation failed: {response.status_code} {response.text}")
            return False
            
    except Exception as e:
        logger.warning(f"Perplexity API check failed: {e}")
        return False

def get_completion(
    prompt: str, 
    system_prompt: Optional[str] = None, 
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    search_recency_filter: str = "month"
) -> str:
    """Get a response from the Perplexity API for a single prompt.
    
    Args:
        prompt: The user prompt to send to the API
        system_prompt: Optional system prompt to set context for the AI
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate (optional)
        search_recency_filter: Time filter for search results
        
    Returns:
        The generated text response or an error message
    """
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    if not api_key:
        return "Error: Perplexity API key not found"
        
    # Prepare the messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Prepare the request payload
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",  # Most reliable model
        "messages": messages,
        "temperature": temperature,
        "top_p": 0.9,
        "search_recency_filter": search_recency_filter,
        "return_images": False,
        "return_related_questions": False,
        "stream": False,
        "frequency_penalty": 1  # Reduces repetition
    }
    
    # Add max_tokens if specified
    if max_tokens:
        payload["max_tokens"] = max_tokens
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the API request
        logger.info("Sending request to Perplexity API")
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30  # Increased timeout for more complex queries
        )
        
        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            logger.info("Successfully received response from Perplexity API")
            
            # Extract and return the generated text
            generated_text = result["choices"][0]["message"]["content"]
            
            # Log a sample of the response to debug
            text_sample = generated_text[:100] + "..." if len(generated_text) > 100 else generated_text
            logger.debug(f"Perplexity response: {text_sample}")
            
            return generated_text
        else:
            error_msg = f"Error: Perplexity API request failed with status {response.status_code}: {response.text}"
            logger.error(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Error: Failed to get completion from Perplexity: {str(e)}"
        logger.error(error_msg)
        return error_msg

def process_chat(
    messages: List[Dict[str, str]], 
    temperature: float = 0.2,
    max_tokens: Optional[int] = None
) -> str:
    """Process a chat conversation with the Perplexity API.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate (optional)
        
    Returns:
        The generated text response or an error message
    """
    api_key = os.environ.get('PERPLEXITY_API_KEY')
    if not api_key:
        return "Error: Perplexity API key not found"
    
    # Ensure the messages alternate properly and end with a user message
    if len(messages) == 0:
        return "Error: No messages provided"
    
    if messages[-1]["role"] != "user":
        return "Error: The last message must be from the user"
    
    # Prepare the request payload
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": messages,
        "temperature": temperature,
        "top_p": 0.9,
        "return_images": False,
        "return_related_questions": False,
        "stream": False,
        "frequency_penalty": 1
    }
    
    # Add max_tokens if specified
    if max_tokens:
        payload["max_tokens"] = max_tokens
    
    # Prepare headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the API request
        logger.info("Sending chat request to Perplexity API")
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            logger.info("Successfully received chat response from Perplexity API")
            
            # Extract and return the generated text
            generated_text = result["choices"][0]["message"]["content"]
            
            # Get citations if available
            citations = result.get("citations", [])
            if citations:
                citation_text = "\n\nSources:\n" + "\n".join([f"- {cite}" for cite in citations[:5]])
                generated_text += citation_text
            
            return generated_text
        else:
            error_msg = f"Error: Perplexity API chat request failed with status {response.status_code}: {response.text}"
            logger.error(error_msg)
            return error_msg
            
    except Exception as e:
        error_msg = f"Error: Failed to process chat with Perplexity: {str(e)}"
        logger.error(error_msg)
        return error_msg