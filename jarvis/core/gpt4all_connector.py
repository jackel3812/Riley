"""
RILEY - GPT4All Connector

This module provides functions to interact with the GPT4All library for local
language model inference when cloud APIs are unavailable.
"""

import os
import re
import json
import time
import logging
import tempfile
from typing import List, Dict, Optional, Union, Any, Tuple

# Configure logging
logger = logging.getLogger(__name__)

def is_available() -> bool:
    """Check if GPT4All is available for use."""
    try:
        import gpt4all
        
        # Check if models directory exists
        models_dir = os.path.expanduser("~/.cache/gpt4all")
        os.makedirs(models_dir, exist_ok=True)
        
        # Check if a model is available
        model_paths = []
        for file in os.listdir(models_dir):
            if file.endswith(".bin"):
                model_paths.append(os.path.join(models_dir, file))
        
        # Use default model if none available
        if not model_paths:
            logger.info("No GPT4All model found, will download on first use")
            
        logger.info("GPT4All is available")
        return True
        
    except ImportError:
        logger.warning("GPT4All package not installed")
        return False
    except Exception as e:
        logger.warning(f"Error checking GPT4All availability: {e}")
        return False

def get_completion(
    prompt: str, 
    system_prompt: Optional[str] = None, 
    temperature: float = 0.7,
    max_tokens: int = 500,
    top_k: int = 40,
    top_p: float = 0.9,
    repeat_penalty: float = 1.18,
    model_name: str = "orca-mini-3b-gguf2-q4_0.gguf"
) -> str:
    """Get a completion from GPT4All for a single prompt.
    
    Args:
        prompt: The user prompt to send to the model
        system_prompt: Optional system prompt to set context for the model
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        top_k: Limits token selection to top k
        top_p: Limits token selection to a cumulative probability
        repeat_penalty: Penalty for repetition
        model_name: Name of the GPT4All model to use
        
    Returns:
        Generated text response or error message
    """
    try:
        import gpt4all
        
        model_path = os.path.expanduser(f"~/.cache/gpt4all/{model_name}")
        
        # Initialize GPT4All
        logger.info(f"Initializing GPT4All with model: {model_name}")
        gpt = gpt4all.GPT4All(model_name)
        
        # Prepare the full prompt with system context if provided
        full_prompt = ""
        if system_prompt:
            full_prompt += f"System: {system_prompt}\n\n"
        full_prompt += f"User: {prompt}\n\nAssistant: "
        
        # Generate the completion
        logger.info("Generating response with GPT4All")
        start_time = time.time()
        
        response = gpt.generate(
            full_prompt,
            max_tokens=max_tokens,
            temp=temperature,
            top_k=top_k,
            top_p=top_p,
            repeat_penalty=repeat_penalty,
            streaming=False
        )
        
        elapsed_time = time.time() - start_time
        logger.info(f"GPT4All response generated in {elapsed_time:.2f} seconds")
        
        # Clean up the response text
        cleaned_response = response.strip()
        
        # Unload the model to free memory
        del gpt
        
        return cleaned_response
        
    except ImportError:
        return "Error: GPT4All package not installed"
    except Exception as e:
        error_msg = f"Error in GPT4All: {str(e)}"
        logger.error(error_msg)
        return error_msg

def process_chat(
    messages: List[Dict[str, str]], 
    temperature: float = 0.7,
    max_tokens: int = 500
) -> str:
    """Process a chat conversation through GPT4All.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        Generated text response or error message
    """
    # Extract system prompt if present
    system_prompt = None
    chat_messages = []
    
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        else:
            chat_messages.append(msg)
    
    # Convert chat format to a single prompt
    combined_prompt = ""
    for msg in chat_messages:
        role_prefix = "User: " if msg["role"] == "user" else "Assistant: "
        combined_prompt += f"{role_prefix}{msg['content']}\n\n"
    
    # Add final turn
    combined_prompt += "Assistant: "
    
    # Call the single prompt function
    return get_completion(
        prompt=combined_prompt,
        system_prompt=system_prompt,
        temperature=temperature,
        max_tokens=max_tokens
    )