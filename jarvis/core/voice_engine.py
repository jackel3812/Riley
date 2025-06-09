"""
Voice Engine - Handles speech recognition and text-to-speech functionality.
"""

import os
import queue
import logging
import threading
import tempfile
from datetime import datetime

# Try importing speech recognition libraries
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

# Try importing text-to-speech libraries
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

class VoiceEngine:
    """Handles voice recognition and speech synthesis."""
    
    def __init__(self, config):
        """Initialize the Voice Engine.
        
        Args:
            config: Configuration object with settings
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.recognizer = None
        self.tts_engine = None
        self.listening = False
        self.speech_queue = queue.Queue()
        self.wake_word = config.get('voice', 'wake_word', default='jarvis')
        self.voice_type = config.get('voice', 'type', default='pyttsx3')  # pyttsx3 or gtts
        self.voice_rate = config.get('voice', 'rate', default=150)
        self.voice_volume = config.get('voice', 'volume', default=1.0)
        
        # Event callbacks
        self.on_speech_recognition_callbacks = []
        
        # Initialize speech recognition if available
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            self.logger.info("Speech recognition initialized")
        else:
            self.logger.warning("Speech recognition not available. Install SpeechRecognition package.")
        
        # Initialize text-to-speech
        self._initialize_tts()
        
        # Initialize audio playback if using gTTS
        if self.voice_type == 'gtts' and PYGAME_AVAILABLE:
            pygame.mixer.init()
    
    def _initialize_tts(self):
        """Initialize the text-to-speech engine based on configuration."""
        if self.voice_type == 'pyttsx3' and PYTTSX3_AVAILABLE:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', self.voice_rate)
            self.tts_engine.setProperty('volume', self.voice_volume)
            
            # Try to set a more natural voice if available
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                # Try to find a male voice for J.A.R.V.I.S.
                if "male" in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.logger.info("pyttsx3 text-to-speech initialized")
        elif self.voice_type == 'gtts' and GTTS_AVAILABLE:
            self.logger.info("gTTS text-to-speech initialized")
        else:
            self.logger.warning("Text-to-speech not available. Install pyttsx3 or gTTS package.")
    
    def register_speech_callback(self, callback):
        """Register a callback for when speech is recognized.
        
        Args:
            callback: Function to call with the recognized text
        """
        self.on_speech_recognition_callbacks.append(callback)
    
    def _notify_speech_recognition(self, text):
        """Notify all registered callbacks about recognized speech.
        
        Args:
            text: The recognized speech text
        """
        for callback in self.on_speech_recognition_callbacks:
            try:
                callback(text)
            except Exception as e:
                self.logger.error(f"Error in speech recognition callback: {e}")
    
    def speak(self, text):
        """Convert text to speech.
        
        Args:
            text: Text to be spoken
        """
        if not text:
            return
            
        self.logger.debug(f"Speaking: {text}")
        
        # Add to speech queue to avoid multiple simultaneous speeches
        self.speech_queue.put(text)
        
        # Start a new thread for TTS if not already processing
        if self.speech_queue.qsize() == 1:
            threading.Thread(target=self._process_speech_queue, daemon=True).start()
    
    def _process_speech_queue(self):
        """Process the speech queue in a separate thread."""
        while not self.speech_queue.empty():
            text = self.speech_queue.get()
            
            if self.voice_type == 'pyttsx3' and PYTTSX3_AVAILABLE:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            elif self.voice_type == 'gtts' and GTTS_AVAILABLE:
                try:
                    # Create a temporary file for the speech audio
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                        temp_filename = tmp_file.name
                    
                    # Generate speech with gTTS
                    tts = gTTS(text=text, lang='en', slow=False)
                    tts.save(temp_filename)
                    
                    # Play the speech if pygame is available
                    if PYGAME_AVAILABLE:
                        pygame.mixer.music.load(temp_filename)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            pygame.time.Clock().tick(10)
                    
                    # Clean up the temporary file
                    os.remove(temp_filename)
                except Exception as e:
                    self.logger.error(f"Error with gTTS: {e}")
            else:
                self.logger.warning("No text-to-speech engine available")
    
    def start_listening(self):
        """Start listening for voice commands in the background."""
        if not SPEECH_RECOGNITION_AVAILABLE or not self.recognizer:
            self.logger.error("Speech recognition is not available")
            return
        
        self.listening = True
        self.logger.info("Starting voice recognition")
        
        # Use a thread to continuously listen for commands
        try:
            while self.listening:
                self._listen_for_commands()
        except Exception as e:
            self.logger.error(f"Error in voice recognition: {e}")
            self.listening = False
    
    def stop_listening(self):
        """Stop listening for voice commands."""
        self.listening = False
        self.logger.info("Stopped voice recognition")
    
    def _listen_for_commands(self):
        """Listen for a single voice command and process it."""
        if not SPEECH_RECOGNITION_AVAILABLE or not self.recognizer:
            return
            
        try:
            with sr.Microphone() as source:
                self.logger.debug("Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                self.logger.debug("Processing speech...")
                
                # Try to recognize the speech
                text = self.recognizer.recognize_google(audio).lower()
                
                self.logger.debug(f"Recognized: {text}")
                
                # Check for wake word if enabled
                if self.wake_word and not text.startswith(self.wake_word):
                    return
                
                # Remove wake word from command
                if self.wake_word and text.startswith(self.wake_word):
                    text = text[len(self.wake_word):].strip()
                
                # Only process if there's text after removing the wake word
                if text:
                    self._notify_speech_recognition(text)
                
        except sr.WaitTimeoutError:
            pass  # No speech detected, continue listening
        except sr.UnknownValueError:
            self.logger.debug("Could not understand audio")
        except sr.RequestError as e:
            self.logger.error(f"Could not request results; {e}")
        except Exception as e:
            self.logger.error(f"Error in speech recognition: {e}")
