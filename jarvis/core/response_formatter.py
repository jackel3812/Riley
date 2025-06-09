"""
RILEY - Response Formatter

This module formats RILEY's responses to ensure a consistent female personality
and voice across all interactions. It integrates the personality manager and
voice characteristics to create cohesive, natural-sounding responses.
"""

import os
import sys
import logging
import random
import re
from typing import Dict, Any, Optional, List, Tuple

# Configure logging
logger = logging.getLogger(__name__)

# Import RILEY components
from jarvis.core.personality_manager import get_personality_manager
from jarvis.core.voice_manager import get_voice_manager

class ResponseFormatter:
    """Formats responses with RILEY's consistent female personality."""
    
    def __init__(self):
        """Initialize the response formatter."""
        self.personality_manager = get_personality_manager()
        self.voice_manager = get_voice_manager()
        
        # Get personality traits and speaking style
        self.traits = self.personality_manager.get_personality_traits()
        self.speaking_style = self.personality_manager.get_speaking_style()
        
        # Language patterns for question responses
        self.question_responses = {
            "what": [
                "{answer}",
                "The answer is {answer}",
                "I can tell you that {answer}",
                "Based on my knowledge, {answer}"
            ],
            "how": [
                "Here's how: {answer}",
                "The process is: {answer}",
                "You can do this by {answer}",
                "The method is to {answer}"
            ],
            "why": [
                "Because {answer}",
                "The reason is {answer}",
                "This happens because {answer}",
                "It's because {answer}"
            ],
            "when": [
                "The timing is {answer}",
                "{answer}",
                "That would be {answer}",
                "It happens {answer}"
            ],
            "where": [
                "The location is {answer}",
                "You can find it {answer}",
                "It's located {answer}",
                "{answer}"
            ],
            "who": [
                "The person is {answer}",
                "{answer}",
                "That would be {answer}",
                "It's {answer}"
            ],
            "default": [
                "{answer}",
                "Here's what I know: {answer}",
                "I can tell you that {answer}",
                "The answer is {answer}"
            ]
        }
        
        logger.info("Response formatter initialized with female personality profile")
    
    def format_response(self, response, query = None) -> str:
        """Format a response with RILEY's female personality.
        
        Args:
            response: Original response text
            query: Optional original query for context
            
        Returns:
            Formatted response
        """
        if not response:
            return "I don't have a response for that at the moment."
            
        # Ensure we're working with a string
        if not isinstance(response, str):
            try:
                response = str(response)
                logger.warning(f"Converted non-string response to string: {type(response)}")
            except Exception as e:
                logger.error(f"Error converting response to string: {e}")
                return "I'm sorry, but I couldn't process that response correctly."
            
        # Apply personality-based modifications
        try:
            formatted = self.personality_manager.modify_response_for_personality(response)
        except Exception as e:
            logger.error(f"Error modifying response for personality: {e}")
            formatted = response
        
        # Apply voice-appropriate formatting
        try:
            formatted = self.voice_manager.format_speech_for_voice(formatted)
        except Exception as e:
            logger.error(f"Error formatting speech for voice: {e}")
        
        # Ensure first-person pronoun capitalization
        try:
            formatted = re.sub(r'\bi\b', 'I', formatted)
        except Exception as e:
            logger.error(f"Error fixing first-person pronouns: {e}")
        
        # If the original query is available, check for question formats
        if query is not None:
            # Ensure query is a string
            if not isinstance(query, str):
                try:
                    query = str(query)
                    logger.warning(f"Converted non-string query to string: {type(query)}")
                except Exception as e:
                    logger.error(f"Error converting query to string: {e}")
                    query = None
                    
            if query and self._is_question(query):
                try:
                    formatted = self._format_question_response(query, formatted)
                except Exception as e:
                    logger.error(f"Error formatting question response: {e}")
            
        return formatted
    
    def _is_question(self, text: str) -> bool:
        """Check if text is a question.
        
        Args:
            text: Text to check
            
        Returns:
            True if text is a question, False otherwise
        """
        # Check for question mark at the end
        if text.strip().endswith('?'):
            return True
            
        # Check for question words at the beginning
        question_starters = ['what', 'where', 'when', 'why', 'how', 'who', 'which', 'can', 'could', 'should', 'would', 'is', 'are', 'do', 'does', 'did']
        first_word = text.strip().split()[0].lower() if text.strip() else ""
        
        return first_word in question_starters
    
    def _format_question_response(self, question: str, answer: str) -> str:
        """Format an answer based on the question type.
        
        Args:
            question: The original question
            answer: The answer to format
            
        Returns:
            Formatted answer
        """
        # Determine question type
        question_lower = question.lower().strip()
        question_type = "default"
        
        for q_type in ["what", "how", "why", "when", "where", "who"]:
            if question_lower.startswith(q_type) or f" {q_type} " in question_lower:
                question_type = q_type
                break
                
        # Select format template based on personality traits
        templates = self.question_responses[question_type]
        
        # For high warmth, sometimes add a personal touch
        if self.traits["warmth"] > 0.7 and random.random() < 0.3:
            if question_type in ["what", "how", "why"]:
                templates = [
                    "I'd be happy to explain that. {answer}",
                    "I can help with that question. {answer}",
                    "Great question! {answer}",
                    "I'd love to help with that. {answer}"
                ]
                
        # For high competence, sometimes add confidence markers
        elif self.traits["competence"] > 0.8 and random.random() < 0.3:
            if question_type in ["what", "how", "why"]:
                templates = [
                    "I can definitely answer that. {answer}",
                    "I know exactly how to address this. {answer}",
                    "Here's the precise information: {answer}",
                    "The definitive answer is: {answer}"
                ]
                
        # Apply the template
        template = random.choice(templates)
        formatted = template.format(answer=answer)
        
        return formatted
    
    def format_code_response(self, code, explanation = None) -> str:
        """Format a code response with appropriate female personality markers.
        
        Args:
            code: Code snippet
            explanation: Optional explanation of the code
            
        Returns:
            Formatted code response
        """
        try:
            # Convert code to string if it's not one
            if not isinstance(code, str):
                try:
                    code = str(code)
                    logger.warning(f"Converted non-string code to string: {type(code)}")
                except Exception as e:
                    logger.error(f"Error converting code to string: {e}")
                    code = "# Error: Could not process code"
            
            if explanation is not None:
                # Convert explanation to string if it's not one
                if not isinstance(explanation, str):
                    try:
                        explanation = str(explanation)
                        logger.warning(f"Converted non-string explanation to string: {type(explanation)}")
                    except Exception as e:
                        logger.error(f"Error converting explanation to string: {e}")
                        explanation = "I couldn't properly explain this code due to an error."
                        
                try:
                    return self.personality_manager.format_code_explanation(code, explanation)
                except Exception as e:
                    logger.error(f"Error in personality manager format_code_explanation: {e}")
                    # Fall back to basic formatting
                    return f"Here's the code:\n\n```\n{code}\n```\n\nExplanation: {explanation}"
            else:
                # Create a basic explanation
                intro = random.choice([
                    "Here's the code you requested:",
                    "I've prepared this code for you:",
                    "Here's how we can approach this with code:",
                    "This code should help you accomplish that:"
                ])
                
                # For high warmth, add encouragement
                if self.traits["warmth"] > 0.7:
                    outro = random.choice([
                        "\n\nFeel free to ask if you need any explanation!",
                        "\n\nLet me know if you need any clarification on how this works.",
                        "\n\nI hope this helps! Let me know if you need any adjustments."
                    ])
                else:
                    outro = ""
                    
                return f"{intro}\n\n```\n{code}\n```{outro}"
        except Exception as e:
            logger.error(f"Error in format_code_response: {e}")
            return f"I encountered an error formatting the code response: {str(e)[:100]}..."
    
    def format_error_response(self, error_message) -> str:
        """Format an error response with female personality traits.
        
        Args:
            error_message: Error message to format
            
        Returns:
            Formatted error response
        """
        try:
            # Convert error_message to string if it's not one
            if not isinstance(error_message, str):
                try:
                    error_message = str(error_message)
                    logger.warning(f"Converted non-string error message to string: {type(error_message)}")
                except Exception as e:
                    logger.error(f"Error converting error message to string: {e}")
                    error_message = "An unknown error occurred."
                
            # High warmth error responses
            if self.traits["warmth"] > 0.7:
                intros = [
                    "I'm sorry, but I encountered an issue: ",
                    "I apologize, but there was a problem: ",
                    "I'd like to help, but I ran into a difficulty: ",
                    "I wish I could complete that, but there was an error: "
                ]
            else:
                intros = [
                    "An error occurred: ",
                    "There was a problem: ",
                    "Error encountered: ",
                    "I couldn't complete the operation: "
                ]
                
            # High competence addition
            if self.traits["competence"] > 0.8:
                outros = [
                    " I can help troubleshoot this if you provide more information.",
                    " I can suggest an alternative approach if you'd like.",
                    " I might be able to resolve this with additional details.",
                    " I can work around this issue if needed."
                ]
            else:
                outros = [""]
                
            # Combine parts
            formatted = f"{random.choice(intros)}{error_message}{random.choice(outros)}"
            
            return formatted
        except Exception as e:
            logger.error(f"Error in format_error_response: {e}")
            return "I encountered an error while processing your request."
    
    def format_greeting(self, name: str = "") -> str:
        """Format a greeting with female personality traits.
        
        Args:
            name: Optional name to greet
            
        Returns:
            Formatted greeting
        """
        return self.personality_manager.generate_greeting(name)
    
    def format_thinking_response(self) -> str:
        """Format a thinking response for processing delays.
        
        Returns:
            Formatted thinking response
        """
        return self.personality_manager.create_thinking_response()
    
    def update_from_managers(self) -> None:
        """Update formatter with latest settings from managers."""
        self.traits = self.personality_manager.get_personality_traits()
        self.speaking_style = self.personality_manager.get_speaking_style()

# Global instance
response_formatter = ResponseFormatter()

def get_response_formatter() -> ResponseFormatter:
    """Get the global response formatter instance.
    
    Returns:
        Response formatter instance
    """
    global response_formatter
    return response_formatter

def format_response(response, query = None) -> str:
    """Format a response with RILEY's female personality (convenience function).
    
    Args:
        response: Original response text
        query: Optional original query for context
        
    Returns:
        Formatted response
    """
    return response_formatter.format_response(response, query)