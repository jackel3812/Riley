"""
RILEY - Personality Manager

This module manages RILEY's consistent female personality across all interfaces
and interactions. It ensures a cohesive character with appropriate language patterns,
response styles, and personality traits.
"""

import os
import sys
import logging
import json
import random
from typing import Dict, Any, Optional, List, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class PersonalityManager:
    """Manages RILEY's female personality traits and expression patterns."""
    
    # Personality traits configuration
    DEFAULT_PERSONALITY = {
        "gender": "female",
        "traits": {
            "warmth": 0.8,         # High warmth (0-1)
            "competence": 0.9,      # Very high competence (0-1)
            "assertiveness": 0.7,   # Moderate-high assertiveness (0-1)
            "enthusiasm": 0.7,      # Moderate-high enthusiasm (0-1)
            "formality": 0.5        # Balanced formality (0-1)
        },
        "speaking_style": {
            "uses_contractions": True,
            "sentence_length": "varied",  # short, medium, long, varied
            "vocabulary_level": "advanced",
            "uses_technical_terms": True,
            "uses_humor": True,
            "uses_empathy": True
        }
    }
    
    # Language patterns for female personality
    LANGUAGE_PATTERNS = {
        # Greeting templates
        "greetings": [
            "Hello {name}, how can I help you today?",
            "Hi there {name}! What can I do for you?",
            "Hello {name}, it's nice to see you. How can I assist you?",
            "Hi {name}! I'm here to help. What do you need?",
            "Good {time_of_day}, {name}. How may I assist you today?"
        ],
        
        # Thinking expressions
        "thinking": [
            "Let me think about that...",
            "I'm analyzing that now...",
            "Let me work through this...",
            "Considering all possibilities...",
            "Thinking through this carefully..."
        ],
        
        # Confirmation responses
        "confirmation": [
            "I understand what you're asking for.",
            "I see what you need.",
            "I've got it.",
            "That makes sense to me.",
            "I understand."
        ],
        
        # Enthusiasm expressions
        "enthusiasm": [
            "That's exciting!",
            "I'd be happy to help with that!",
            "What a great question!",
            "I'm really interested in that topic!",
            "I'm looking forward to working on this!"
        ],
        
        # Empathy expressions
        "empathy": [
            "I understand how you feel about that.",
            "That sounds challenging.",
            "I can see why that would be important to you.",
            "I appreciate your perspective on this.",
            "I can tell this matters to you."
        ]
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the personality manager.
        
        Args:
            config_path: Path to personality configuration file
        """
        self.base_path = self._detect_base_path()
        self.config_path = config_path or os.path.join(self.base_path, "jarvis", "config", "personality_config.json")
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Load or create personality configuration
        self.personality_config = self._load_personality_config()
        
        # Set active personality traits
        self.active_personality = self.personality_config.get("active_personality", self.DEFAULT_PERSONALITY.copy())
        
        # Ensure gender is female
        self._ensure_female_personality()
        
        logger.info("Personality manager initialized with female personality profile")
    
    def _detect_base_path(self) -> str:
        """Auto-detect the base path of the RILEY project."""
        # Get the current file's directory and navigate up to find project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from core to the jarvis directory
        jarvis_dir = os.path.dirname(current_dir)
        # Go up one more level to the project root
        base_dir = os.path.dirname(jarvis_dir)
        return base_dir
    
    def _load_personality_config(self) -> Dict[str, Any]:
        """Load personality configuration from file or create default.
        
        Returns:
            Personality configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("Loaded personality configuration from file")
                return config
            except Exception as e:
                logger.error(f"Error loading personality configuration: {e}")
                
        # Create default configuration
        config = {
            "active_personality": self.DEFAULT_PERSONALITY,
            "available_personalities": {
                "female": ["standard", "professional", "friendly", "empathetic"],
                "male": []  # No male personalities per requirements
            },
            "personality_settings": {
                "female": {
                    "standard": self.DEFAULT_PERSONALITY["traits"],
                    "professional": {
                        "warmth": 0.6,
                        "competence": 0.95,
                        "assertiveness": 0.8,
                        "enthusiasm": 0.5,
                        "formality": 0.9
                    },
                    "friendly": {
                        "warmth": 0.9,
                        "competence": 0.8,
                        "assertiveness": 0.6,
                        "enthusiasm": 0.9,
                        "formality": 0.3
                    },
                    "empathetic": {
                        "warmth": 0.95,
                        "competence": 0.8,
                        "assertiveness": 0.5,
                        "enthusiasm": 0.7,
                        "formality": 0.4
                    }
                }
            }
        }
        
        # Save default configuration
        self._save_personality_config(config)
        
        return config
    
    def _save_personality_config(self, config: Dict[str, Any]) -> bool:
        """Save personality configuration to file.
        
        Args:
            config: Personality configuration to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            logger.info("Saved personality configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving personality configuration: {e}")
            return False
    
    def _ensure_female_personality(self) -> None:
        """Ensure personality is set to female."""
        if self.active_personality["gender"] != "female":
            self.active_personality["gender"] = "female"
            self.active_personality["traits"] = self.DEFAULT_PERSONALITY["traits"].copy()
            self.active_personality["speaking_style"] = self.DEFAULT_PERSONALITY["speaking_style"].copy()
            
            # Update config
            self.personality_config["active_personality"] = self.active_personality
            self._save_personality_config(self.personality_config)
            
            logger.info("Reset to female personality profile")
    
    def get_personality_traits(self) -> Dict[str, Any]:
        """Get current personality traits.
        
        Returns:
            Dictionary of personality traits
        """
        return self.active_personality["traits"].copy()
    
    def get_speaking_style(self) -> Dict[str, Any]:
        """Get current speaking style.
        
        Returns:
            Dictionary of speaking style attributes
        """
        return self.active_personality["speaking_style"].copy()
    
    def get_language_pattern(self, pattern_type: str, context: Dict[str, Any] = None) -> str:
        """Get a language pattern for a given type and context.
        
        Args:
            pattern_type: Type of language pattern to get
            context: Optional context variables for template formatting
            
        Returns:
            Selected language pattern
        """
        if pattern_type not in self.LANGUAGE_PATTERNS:
            return ""
            
        patterns = self.LANGUAGE_PATTERNS[pattern_type]
        if not patterns:
            return ""
            
        # Select a pattern based on personality traits
        traits = self.active_personality["traits"]
        
        # For enthusiasm, select more enthusiastic patterns if the trait is high
        if pattern_type == "enthusiasm" and traits["enthusiasm"] < 0.5:
            # Just return a mild statement for low enthusiasm
            return "I can help with that."
            
        # Special handling for greetings based on formality
        if pattern_type == "greetings":
            formality = traits["formality"]
            warmth = traits["warmth"]
            
            if formality > 0.7:  # Formal
                filtered_patterns = [p for p in patterns if "Hello" in p]
            elif formality < 0.3:  # Informal
                filtered_patterns = [p for p in patterns if "Hi" in p]
            else:  # Mixed
                filtered_patterns = patterns
                
            # Use filtered patterns if we have any
            if filtered_patterns:
                patterns = filtered_patterns
                
        # Randomly select a pattern
        pattern = random.choice(patterns)
        
        # Format with context if provided
        if context:
            try:
                pattern = pattern.format(**context)
            except KeyError as e:
                logger.error(f"Missing context key in pattern formatting: {e}")
            
        return pattern
    
    def modify_response_for_personality(self, text: str) -> str:
        """Modify a response to match the active personality.
        
        Args:
            text: Original response text
            
        Returns:
            Modified response text
        """
        if not text:
            return "I don't have a response for that at the moment."
            
        # Ensure we're working with a string
        if not isinstance(text, str):
            try:
                text = str(text)
            except:
                return "I'm having trouble formulating a response right now."
            
        # Get active traits and style
        traits = self.active_personality["traits"]
        style = self.active_personality["speaking_style"]
        
        # Apply contractions if enabled
        if style["uses_contractions"]:
            contractions = {
                "I am": "I'm",
                "You are": "You're",
                "We are": "We're",
                "They are": "They're",
                "It is": "It's",
                "That is": "That's",
                "What is": "What's",
                "Where is": "Where's",
                "Who is": "Who's",
                "How is": "How's",
                "There is": "There's",
                "He is": "He's",
                "She is": "She's",
                "I will": "I'll",
                "You will": "You'll",
                "We will": "We'll",
                "They will": "They'll",
                "It will": "It'll",
                "That will": "That'll",
                "I have": "I've",
                "You have": "You've",
                "We have": "We've",
                "They have": "They've",
                "Would have": "Would've",
                "Could have": "Could've",
                "Should have": "Should've",
                "Cannot": "Can't",
                "Do not": "Don't",
                "Does not": "Doesn't",
                "Did not": "Didn't",
                "Has not": "Hasn't",
                "Have not": "Haven't",
                "Had not": "Hadn't",
                "Will not": "Won't",
                "Would not": "Wouldn't",
                "Could not": "Couldn't",
                "Should not": "Shouldn't"
            }
            
            for full, contraction in contractions.items():
                text = text.replace(full, contraction)
                
        # Add empathy for high warmth
        if traits["warmth"] > 0.7 and style["uses_empathy"] and random.random() < 0.3:
            # 30% chance to add empathy expression for questions or problems
            if "?" in text or any(word in text.lower() for word in ["issue", "problem", "trouble", "difficult", "help"]):
                empathy = self.get_language_pattern("empathy")
                text = f"{empathy} {text}"
                
        # Add enthusiasm for high enthusiasm
        if traits["enthusiasm"] > 0.7 and random.random() < 0.3:
            # 30% chance to add enthusiasm for positive responses
            if any(word in text.lower() for word in ["great", "good", "excellent", "perfect", "success", "accomplished"]):
                enthusiasm = self.get_language_pattern("enthusiasm")
                text = f"{enthusiasm} {text}"
                
        # Adjust formality
        if traits["formality"] > 0.7:
            # Higher formality replacements
            text = text.replace("Yeah", "Yes")
            text = text.replace("Nope", "No")
            text = text.replace("Sure", "Certainly")
            text = text.replace("Thanks", "Thank you")
            text = text.replace("Okay", "Very well")
            
        elif traits["formality"] < 0.3:
            # Lower formality replacements
            text = text.replace("I will assist you", "I'll help you")
            text = text.replace("I would recommend", "I'd recommend")
            text = text.replace("I would suggest", "I'd suggest")
            text = text.replace("Therefore", "So")
            text = text.replace("Additionally", "Also")
            
        # Add conversational markers for middle-range formality
        if 0.3 <= traits["formality"] <= 0.7:
            # Sometimes start with a conversational opener
            if random.random() < 0.2 and len(text) > 50:
                openers = ["Well, ", "So, ", "Actually, ", "Basically, ", "Essentially, "]
                text = random.choice(openers) + text
                
        return text
    
    def generate_greeting(self, name: str = "") -> str:
        """Generate a greeting appropriate for the current personality.
        
        Args:
            name: Name of the person to greet
            
        Returns:
            Greeting text
        """
        # Determine time of day
        import datetime
        hour = datetime.datetime.now().hour
        
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 18:
            time_of_day = "afternoon"
        else:
            time_of_day = "evening"
            
        # Create context for greeting
        context = {
            "name": name if name else "",
            "time_of_day": time_of_day
        }
        
        # Get greeting pattern
        greeting = self.get_language_pattern("greetings", context)
        
        # If no name provided, remove the reference
        if not name:
            greeting = greeting.replace(", !", "!")
            greeting = greeting.replace(" ,", "")
            greeting = greeting.replace("  ", " ")
            
        return greeting
    
    def create_thinking_response(self) -> str:
        """Create a thinking response for processing delays.
        
        Returns:
            Thinking response text
        """
        return self.get_language_pattern("thinking")
    
    def adjust_trait(self, trait: str, value: float) -> bool:
        """Adjust a personality trait.
        
        Args:
            trait: Trait to adjust
            value: New trait value (0-1)
            
        Returns:
            True if successful, False otherwise
        """
        if trait not in self.active_personality["traits"]:
            logger.warning(f"Unknown personality trait: {trait}")
            return False
            
        # Ensure value is in valid range
        value = max(0.0, min(1.0, value))
        
        # Update trait
        self.active_personality["traits"][trait] = value
        
        # Save changes
        self.personality_config["active_personality"] = self.active_personality
        self._save_personality_config(self.personality_config)
        
        logger.info(f"Adjusted personality trait {trait} to {value}")
        return True
    
    def set_speaking_style_attribute(self, attribute: str, value: Any) -> bool:
        """Set a speaking style attribute.
        
        Args:
            attribute: Speaking style attribute to set
            value: New attribute value
            
        Returns:
            True if successful, False otherwise
        """
        if attribute not in self.active_personality["speaking_style"]:
            logger.warning(f"Unknown speaking style attribute: {attribute}")
            return False
            
        # Update attribute
        self.active_personality["speaking_style"][attribute] = value
        
        # Save changes
        self.personality_config["active_personality"] = self.active_personality
        self._save_personality_config(self.personality_config)
        
        logger.info(f"Set speaking style attribute {attribute} to {value}")
        return True
    
    def format_code_explanation(self, code: str, explanation: str) -> str:
        """Format code explanation in a female voice style.
        
        Args:
            code: Code to explain
            explanation: Explanation text
            
        Returns:
            Formatted explanation
        """
        traits = self.active_personality["traits"]
        
        # More warm and supportive language for female voice
        if traits["warmth"] > 0.7:
            intros = [
                "Here's how this code works:",
                "Let me walk you through this code:",
                "I'd be happy to explain this code:",
                "This code is actually quite interesting:"
            ]
        else:
            intros = [
                "This code works as follows:",
                "Here's an explanation of the code:",
                "The code functions like this:",
                "Here's a breakdown of this code:"
            ]
            
        # Format with intro
        formatted = f"{random.choice(intros)}\n\n{code}\n\n{explanation}"
        
        # Add encouragement for high warmth
        if traits["warmth"] > 0.8:
            encouragements = [
                "\n\nFeel free to ask if you need any clarification!",
                "\n\nLet me know if you'd like me to explain any part in more detail.",
                "\n\nDoes that make sense? I'm happy to elaborate further."
            ]
            formatted += random.choice(encouragements)
            
        return formatted

# Global instance
personality_manager = PersonalityManager()

def get_personality_manager() -> PersonalityManager:
    """Get the global personality manager instance.
    
    Returns:
        Personality manager instance
    """
    global personality_manager
    return personality_manager