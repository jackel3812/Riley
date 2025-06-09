"""
RILEY - Voice & Personality Integration

This module integrates the female voice and personality system with RILEY's
AI engine, ensuring consistent behavior across all interactions. It provides
the necessary hooks for the AI engine to use the voice and personality systems.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List, Callable

# Configure logging
logger = logging.getLogger(__name__)

# Import RILEY components
from jarvis.core.personality_manager import get_personality_manager
from jarvis.core.voice_manager import get_voice_manager
from jarvis.core.response_formatter import get_response_formatter
from jarvis.features.voice_synthesis import get_voice_synthesizer

class VoiceIntegration:
    """Integrates voice and personality systems with the AI engine."""
    
    def __init__(self, ai_engine=None):
        """Initialize the voice integration.
        
        Args:
            ai_engine: Optional AI engine instance
        """
        self.ai_engine = ai_engine
        
        # Get component managers
        self.personality_manager = get_personality_manager()
        self.voice_manager = get_voice_manager()
        self.response_formatter = get_response_formatter()
        self.voice_synthesizer = get_voice_synthesizer()
        
        # Track registered callbacks
        self.callbacks = {
            "response": [],
            "thinking": [],
            "error": []
        }
        
        logger.info("Voice integration initialized")
    
    def register_with_ai_engine(self, ai_engine) -> None:
        """Register with an AI engine instance.
        
        Args:
            ai_engine: AI engine instance
        """
        if not ai_engine:
            logger.warning("Cannot register with AI engine: None provided")
            return
            
        self.ai_engine = ai_engine
        
        # Register response callback with AI engine if supported
        if hasattr(ai_engine, 'register_response_callback'):
            ai_engine.register_response_callback(self.process_response)
            logger.info("Registered response callback with AI engine")
            
        # Try to patch the AI engine to use female voice consistently
        self._patch_ai_engine()
        
        logger.info("Registered with AI engine")
    
    def _patch_ai_engine(self) -> None:
        """Patch the AI engine to use female voice consistently."""
        if not self.ai_engine:
            return
            
        try:
            # Try to patch the process_input method
            if hasattr(self.ai_engine, 'process_input'):
                original_process_input = self.ai_engine.process_input
                
                def enhanced_process_input(text_input, voice_input=False):
                    # First notify thinking callbacks
                    for callback in self.callbacks["thinking"]:
                        callback(self.response_formatter.format_thinking_response())
                    
                    # Check if input is valid before proceeding
                    if not isinstance(text_input, str):
                        try:
                            text_input = str(text_input)
                            logger.warning(f"Converted input from {type(text_input)} to string")
                        except Exception as e:
                            logger.error(f"Invalid input type: {type(text_input)}. Expected string. Error: {e}")
                            return "I'm sorry, but I couldn't process that input correctly."
                        
                    # Call original method
                    response = original_process_input(text_input, voice_input)
                    
                    # Format the response with female personality
                    try:
                        formatted_response = self.response_formatter.format_response(response, text_input)
                    except Exception as e:
                        logger.error(f"Error formatting response: {e}")
                        formatted_response = response if isinstance(response, str) else "I encountered an error while processing your request."
                    
                    # If voice synthesis is enabled and it's a voice input, speak the response
                    if voice_input and self.ai_engine is not None and hasattr(self.ai_engine, 'voice_enabled') and self.ai_engine.voice_enabled:
                        try:
                            if isinstance(formatted_response, str):
                                self.voice_synthesizer.speak(formatted_response)
                            else:
                                logger.warning(f"Cannot speak non-string response of type {type(formatted_response)}")
                        except Exception as e:
                            logger.error(f"Error in voice synthesis: {e}")
                        
                    return formatted_response
                
                # Replace the method
                bound_method = enhanced_process_input.__get__(self.ai_engine, type(self.ai_engine))
                setattr(self.ai_engine, 'process_input', bound_method)
                
                logger.info("Successfully patched AI engine process_input method")
                
            # Patch the _finalize_response method if it exists
            if hasattr(self.ai_engine, '_finalize_response'):
                original_finalize = self.ai_engine._finalize_response
                
                # Add better error checking to the original _finalize_response method
                original_finalize_method = original_finalize
                
                def safe_original_finalize(response):
                    """Safely call the original finalize method with better error handling."""
                    if not isinstance(response, str) and response is not None:
                        try:
                            response = str(response)
                            logger.warning(f"Converted response from {type(response)} to string")
                        except Exception as e:
                            logger.error(f"Invalid response type: {type(response)}. Error: {e}")
                            return "I'm sorry, but I couldn't process that correctly."
                    
                    try:
                        return original_finalize_method(response)
                    except Exception as e:
                        logger.error(f"Error in original_finalize: {e}")
                        return response or "I'm having trouble processing your request."
                
                # Replace the original method with our safe version
                self.ai_engine._finalize_response = safe_original_finalize
                logger.info("Successfully enhanced AI engine _finalize_response method")
                
            # Set voice attributes
            setattr(self.ai_engine, 'voice_gender', 'female')
            if not hasattr(self.ai_engine, 'voice_enabled'):
                setattr(self.ai_engine, 'voice_enabled', True)
                
        except Exception as e:
            logger.error(f"Error patching AI engine: {e}")
    
    def register_callback(self, event_type: str, callback: Callable) -> bool:
        """Register a callback for voice and personality events.
        
        Args:
            event_type: Event type ('response', 'thinking', or 'error')
            callback: Callback function
            
        Returns:
            True if registration was successful, False otherwise
        """
        if event_type not in self.callbacks:
            logger.warning(f"Unknown event type: {event_type}")
            return False
            
        self.callbacks[event_type].append(callback)
        logger.info(f"Registered callback for event type: {event_type}")
        return True
    
    def process_response(self, response, query = None) -> str:
        """Process an AI response to apply female voice and personality.
        
        Args:
            response: Original response text
            query: Optional original query for context
            
        Returns:
            Processed response
        """
        try:
            # Convert response to string if it's not one
            if not isinstance(response, str):
                try:
                    response = str(response)
                    logging.warning(f"Converted non-string response to string: {type(response)}")
                except Exception as e:
                    logging.error(f"Error converting response to string: {e}")
                    response = "I'm sorry, but I couldn't process that correctly."
                    
            # Convert query to string if it's not None and not a string
            if query is not None and not isinstance(query, str):
                try:
                    query = str(query)
                    logging.warning(f"Converted non-string query to string: {type(query)}")
                except Exception as e:
                    logging.error(f"Error converting query to string: {e}")
                    query = None
                
            # Format response with female personality
            formatted = self.response_formatter.format_response(response, query)
            
            # Notify response callbacks
            for callback in self.callbacks["response"]:
                callback(formatted)
                
            return formatted
        except Exception as e:
            logging.error(f"Error in process_response: {e}")
            return "I encountered an error while processing your request."
    
    def speak_response(self, response: str) -> None:
        """Speak a response with RILEY's female voice.
        
        Args:
            response: Response to speak
        """
        self.voice_synthesizer.speak(response)
    
    def process_error(self, error_message) -> str:
        """Process an error message with female personality traits.
        
        Args:
            error_message: Error message to process
            
        Returns:
            Processed error message
        """
        try:
            # Convert error_message to string if it's not one
            if not isinstance(error_message, str):
                try:
                    error_message = str(error_message)
                    logging.warning(f"Converted non-string error message to string: {type(error_message)}")
                except Exception as e:
                    logging.error(f"Error converting error message to string: {e}")
                    error_message = "An unknown error occurred."
                    
            # Format error with female personality
            formatted = self.response_formatter.format_error_response(error_message)
            
            # Notify error callbacks
            for callback in self.callbacks["error"]:
                callback(formatted)
                
            return formatted
        except Exception as e:
            logging.error(f"Error in process_error: {e}")
            return "I encountered an error while processing your request."
    
    def generate_greeting(self, name: str = "") -> str:
        """Generate a greeting with female personality.
        
        Args:
            name: Optional name to greet
            
        Returns:
            Greeting message
        """
        return self.response_formatter.format_greeting(name)

# Global instance
voice_integration = None

def get_voice_integration(ai_engine=None) -> VoiceIntegration:
    """Get the global voice integration instance.
    
    Args:
        ai_engine: Optional AI engine instance to register with
        
    Returns:
        Voice integration instance
    """
    global voice_integration
    
    if voice_integration is None:
        voice_integration = VoiceIntegration(ai_engine)
    elif ai_engine is not None and voice_integration.ai_engine is None:
        voice_integration.register_with_ai_engine(ai_engine)
        
    return voice_integration

def integrate_with_ai_engine(ai_engine) -> VoiceIntegration:
    """Integrate voice and personality systems with an AI engine.
    
    Args:
        ai_engine: AI engine instance
        
    Returns:
        Voice integration instance
    """
    integration = get_voice_integration(ai_engine)
    
    # Ensure we're registered with this engine
    integration.register_with_ai_engine(ai_engine)
    
    return integration