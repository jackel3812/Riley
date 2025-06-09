"""
RILEY - Voice Management System

This module ensures RILEY maintains a consistent female voice across all interfaces
and interactions. It provides unified voice settings, voice synthesis configuration,
and a central point for managing voice-related features.
"""

import os
import sys
import logging
import json
from typing import Dict, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

class VoiceManager:
    """Manages RILEY's voice settings and characteristics."""
    
    # Default voice settings
    DEFAULT_VOICE = {
        "gender": "female",
        "name": "riley",
        "pitch": 1.0,  # Normal pitch
        "rate": 1.0,   # Normal speech rate
        "volume": 1.0  # Full volume
    }
    
    # Voice characteristics
    VOICE_CHARACTERISTICS = {
        "female": {
            "riley": {
                "description": "RILEY's primary female voice - warm, friendly and confident",
                "pitch_range": (0.9, 1.1),
                "tone": "warm",
                "personality": "friendly, confident, intelligent"
            }
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the voice manager.
        
        Args:
            config_path: Path to voice configuration file
        """
        self.base_path = self._detect_base_path()
        self.config_path = config_path or os.path.join(self.base_path, "jarvis", "config", "voice_config.json")
        
        # Ensure config directory exists
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        # Load or create voice configuration
        self.voice_config = self._load_voice_config()
        
        # Set active voice
        self.active_voice = self.voice_config.get("active_voice", self.DEFAULT_VOICE.copy())
        
        logger.info(f"Voice manager initialized with {self.active_voice['gender']} voice '{self.active_voice['name']}'")
    
    def _detect_base_path(self) -> str:
        """Auto-detect the base path of the RILEY project."""
        # Get the current file's directory and navigate up to find project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from core to the jarvis directory
        jarvis_dir = os.path.dirname(current_dir)
        # Go up one more level to the project root
        base_dir = os.path.dirname(jarvis_dir)
        return base_dir
    
    def _load_voice_config(self) -> Dict[str, Any]:
        """Load voice configuration from file or create default.
        
        Returns:
            Voice configuration dictionary
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info("Loaded voice configuration from file")
                return config
            except Exception as e:
                logger.error(f"Error loading voice configuration: {e}")
                
        # Create default configuration
        config = {
            "active_voice": self.DEFAULT_VOICE,
            "available_voices": {
                "female": ["riley", "sophia", "emma"],
                "male": []  # No male voices available by default
            },
            "voice_settings": {
                "female": {
                    "riley": {
                        "pitch": 1.0,
                        "rate": 1.0,
                        "volume": 1.0
                    }
                }
            }
        }
        
        # Save default configuration
        self._save_voice_config(config)
        
        return config
    
    def _save_voice_config(self, config: Dict[str, Any]) -> bool:
        """Save voice configuration to file.
        
        Args:
            config: Voice configuration to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            logger.info("Saved voice configuration to file")
            return True
        except Exception as e:
            logger.error(f"Error saving voice configuration: {e}")
            return False
    
    def set_voice_gender(self, gender: str = "female") -> bool:
        """Set the voice gender (locked to female by default).
        
        Args:
            gender: Voice gender to set (only 'female' is allowed)
            
        Returns:
            True if successful, False otherwise
        """
        # Only allow female voice per requirements
        if gender.lower() != "female":
            logger.warning(f"Attempted to set non-female voice gender: {gender}")
            return False
            
        if self.active_voice["gender"] != "female":
            self.active_voice["gender"] = "female"
            
            # Get the first available female voice
            available_female_voices = self.voice_config["available_voices"]["female"]
            if available_female_voices:
                self.active_voice["name"] = available_female_voices[0]
                
            # Update config
            self.voice_config["active_voice"] = self.active_voice
            self._save_voice_config(self.voice_config)
            
            logger.info(f"Voice gender set to female: {self.active_voice['name']}")
            
        return True
    
    def set_voice_name(self, name: str) -> bool:
        """Set the voice name within available female voices.
        
        Args:
            name: Voice name to set
            
        Returns:
            True if successful, False otherwise
        """
        name = name.lower()
        available_female_voices = self.voice_config["available_voices"]["female"]
        
        if name in available_female_voices:
            self.active_voice["name"] = name
            
            # Update config
            self.voice_config["active_voice"] = self.active_voice
            self._save_voice_config(self.voice_config)
            
            logger.info(f"Voice name set to: {name}")
            return True
        else:
            logger.warning(f"Voice name not available: {name}")
            return False
    
    def adjust_voice_parameter(self, parameter: str, value: float) -> bool:
        """Adjust a voice parameter (pitch, rate, volume).
        
        Args:
            parameter: Parameter to adjust ('pitch', 'rate', or 'volume')
            value: New parameter value
            
        Returns:
            True if successful, False otherwise
        """
        if parameter not in ["pitch", "rate", "volume"]:
            logger.warning(f"Invalid voice parameter: {parameter}")
            return False
            
        # Validate parameter value
        if parameter == "pitch":
            # Keep pitch in female range
            value = max(0.8, min(1.2, value))
        elif parameter == "rate":
            value = max(0.5, min(1.5, value))
        elif parameter == "volume":
            value = max(0.1, min(1.0, value))
            
        # Update active voice
        self.active_voice[parameter] = value
        
        # Update settings for this voice
        gender = self.active_voice["gender"]
        name = self.active_voice["name"]
        
        if gender not in self.voice_config["voice_settings"]:
            self.voice_config["voice_settings"][gender] = {}
            
        if name not in self.voice_config["voice_settings"][gender]:
            self.voice_config["voice_settings"][gender][name] = {}
            
        self.voice_config["voice_settings"][gender][name][parameter] = value
        
        # Update active voice in config
        self.voice_config["active_voice"] = self.active_voice
        
        # Save changes
        self._save_voice_config(self.voice_config)
        
        logger.info(f"Adjusted voice {parameter} to {value}")
        return True
    
    def get_active_voice(self) -> Dict[str, Any]:
        """Get the current active voice settings.
        
        Returns:
            Dictionary with active voice settings
        """
        return self.active_voice.copy()
    
    def get_voice_characteristics(self) -> Dict[str, Any]:
        """Get characteristics of the active voice.
        
        Returns:
            Dictionary with voice characteristics
        """
        gender = self.active_voice["gender"]
        name = self.active_voice["name"]
        
        if gender in self.VOICE_CHARACTERISTICS and name in self.VOICE_CHARACTERISTICS[gender]:
            return self.VOICE_CHARACTERISTICS[gender][name].copy()
        else:
            return {
                "description": "Standard female voice",
                "pitch_range": (0.9, 1.1),
                "tone": "neutral",
                "personality": "helpful, friendly"
            }
    
    def reset_to_default(self) -> bool:
        """Reset voice settings to default female voice.
        
        Returns:
            True if successful
        """
        self.active_voice = self.DEFAULT_VOICE.copy()
        self.voice_config["active_voice"] = self.active_voice
        self._save_voice_config(self.voice_config)
        
        logger.info("Reset voice to default female voice")
        return True
    
    def format_speech_for_voice(self, text: str) -> str:
        """Format text for speech synthesis based on voice characteristics.
        
        Args:
            text: Text to format
            
        Returns:
            Formatted text
        """
        # Apply voice-specific formatting
        # This could include adding pauses, emphasis, or modifying text
        # to better match the voice's personality
        
        # For now, just return the original text
        return text

# Global instance
voice_manager = VoiceManager()

def get_voice_manager() -> VoiceManager:
    """Get the global voice manager instance.
    
    Returns:
        Voice manager instance
    """
    global voice_manager
    return voice_manager