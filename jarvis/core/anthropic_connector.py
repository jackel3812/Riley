"""
RILEY - Anthropic Claude API Connector

This module provides functions to interact with the Anthropic Claude API
for enhanced conversation and reasoning capabilities.
"""

import os
import json
import logging
import requests
from typing import List, Dict, Optional, Union, Any

# Configure logging
logger = logging.getLogger(__name__)

# Check if Anthropic library is available, otherwise use direct API calls
try:
    import anthropic
    from anthropic import Anthropic
    HAVE_ANTHROPIC_LIB = True
except ImportError:
    HAVE_ANTHROPIC_LIB = False

def is_available() -> bool:
    """Check if the Anthropic Claude API is available by verifying the API key."""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        logger.warning("Anthropic API key not found in environment variables")
        return False
    
    # Verify the API key with a minimal request
    try:
        if HAVE_ANTHROPIC_LIB:
            client = Anthropic(api_key=api_key)
            # Just creating the client object successfully means the API key exists
            logger.info("Anthropic API key is valid")
            return True
        else:
            # Make a minimal API request
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/complete",
                headers=headers,
                json={
                    "model": "claude-3-5-sonnet-20241022",
                    "prompt": "\n\nHuman: Test request, please respond with 'Working'.\n\nAssistant:",
                    "max_tokens_to_sample": 10,
                    "temperature": 0
                },
                timeout=5
            )
            
            if response.status_code == 200:
                logger.info("Anthropic API key is valid")
                return True
            else:
                logger.warning(f"Anthropic API key validation failed: {response.status_code} {response.text}")
                return False
    except Exception as e:
        logger.warning(f"Anthropic API check failed: {e}")
        return False

def get_completion(
    prompt: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    model: str = "claude-3-5-sonnet-20241022"
) -> str:
    """Get a completion from Claude for a single prompt.
    
    Args:
        prompt: The user prompt to send to the model
        system_prompt: Optional system prompt to set context for the model
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        model: Claude model to use (defaults to latest model)
        
    Returns:
        Generated text response or error message
    """
    # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return "Error: Anthropic API key not found"
    
    try:
        if HAVE_ANTHROPIC_LIB:
            # Use the Anthropic Python library
            client = Anthropic(api_key=api_key)
            
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = client.messages.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.content[0].text
        else:
            # Use direct API calls
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [],
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            if system_prompt:
                data["messages"].append({"role": "system", "content": system_prompt})
            
            data["messages"].append({"role": "user", "content": prompt})
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                error_msg = f"Error: Anthropic API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                return error_msg
    
    except Exception as e:
        error_msg = f"Error: Failed to get completion from Claude: {str(e)}"
        logger.error(error_msg)
        return error_msg

def process_chat(
    messages: List[Dict[str, str]],
    temperature: float = 0.7,
    max_tokens: int = 500,
    model: str = "claude-3-5-sonnet-20241022"
) -> str:
    """Process a chat conversation through Claude.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        model: Claude model to use (defaults to latest model)
        
    Returns:
        Generated text response or error message
    """
    # the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return "Error: Anthropic API key not found"
    
    # Ensure there's at least one message
    if len(messages) == 0:
        return "Error: No messages provided"
    
    try:
        if HAVE_ANTHROPIC_LIB:
            # Use the Anthropic Python library
            client = Anthropic(api_key=api_key)
            
            # Make sure the message format is correct
            valid_messages = []
            for msg in messages:
                if msg["role"] in ["user", "assistant", "system"]:
                    valid_messages.append(msg)
            
            response = client.messages.create(
                model=model,
                messages=valid_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.content[0].text
        else:
            # Use direct API calls
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            # Make sure the message format is correct
            valid_messages = []
            for msg in messages:
                if msg["role"] in ["user", "assistant", "system"]:
                    valid_messages.append(msg)
            
            data = {
                "model": model,
                "messages": valid_messages,
                "max_tokens": max_tokens,
                "temperature": temperature
            }
            
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["content"][0]["text"]
            else:
                error_msg = f"Error: Anthropic API request failed with status {response.status_code}: {response.text}"
                logger.error(error_msg)
                return error_msg
    
    except Exception as e:
        error_msg = f"Error: Failed to process chat with Claude: {str(e)}"
        logger.error(error_msg)
        return error_msg