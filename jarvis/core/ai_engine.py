"""
AI Engine - The brain of RILEY
Handles natural language processing, intent recognition, and conversation.
"""

import os
import random
import logging
import datetime
import nltk
from datetime import datetime

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Import GPT4All connector
try:
    from jarvis.core.gpt4all_connector import is_available as gpt4all_available
    from jarvis.core.gpt4all_connector import get_completion, process_chat
    HAVE_GPT4ALL = gpt4all_available()
except ImportError:
    HAVE_GPT4ALL = False

# Import Perplexity connector
try:
    from jarvis.core.perplexity_connector import is_available as perplexity_available
    from jarvis.core.perplexity_connector import get_completion
    from jarvis.core.perplexity_connector import process_chat as process_perplexity_chat
    HAVE_PERPLEXITY = perplexity_available()
except ImportError:
    HAVE_PERPLEXITY = False

# Import languagemodels module (optional)
try:
    import jarvis.languagemodels as lm
    HAVE_LANGUAGEMODELS = True
except ImportError:
    HAVE_LANGUAGEMODELS = False

from jarvis.database import models
from jarvis.features.adaptive_learning import AdaptiveLearning
from jarvis.core.knowledge_base import get_riley_information, get_response_for_common_question, get_capability_description, get_domain_topics

class AIEngine:
    """The main AI engine that powers RILEY."""
    
    def __init__(self, config):
        """Initialize the AI Engine.
        
        Args:
            config: Configuration object with settings
        """
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.user_name = config.get('user', 'name', 'sir')
        
        # Initialize OpenAI client if API key is available
        openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.openai_client = None
        if openai_api_key and OpenAI:
            self.openai_client = OpenAI(api_key=openai_api_key)
            self.logger.info("OpenAI client initialized")
        else:
            self.logger.warning("OpenAI client not initialized - API key not found or openai package not installed")
            
        # Initialize conversation context
        self.conversation_context = []
        
        # Initialize adaptive learning system
        self.learning = AdaptiveLearning()
        
        # Initialize response callbacks
        self.response_callbacks = []
        
        # Feature modules
        self.applications = None  # To be implemented
        self.weather = None  # To be implemented
        self.web_search = None  # To be implemented
        self.wiki = None  # To be implemented
        self.wolfram = None  # To be implemented
        self.calendar_service = None  # To be implemented
        self.news_service = None  # To be implemented
        self.notes_service = None  # To be implemented
        self.joke_service = None  # To be implemented
        self.media = None  # To be implemented
        
        # Initialize NLTK
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            nltk.download('maxent_ne_chunker', quiet=True)
            nltk.download('words', quiet=True)
        except Exception as e:
            self.logger.warning(f"Failed to download NLTK data: {e}")
            
        self.logger.info("AI Engine initialized")
    
    def register_response_callback(self, callback):
        """Register a callback for when responses are generated.
        
        Args:
            callback: Function to call with the response text
        """
        self.response_callbacks.append(callback)
    
    def _notify_response(self, response):
        """Notify all registered callbacks about a new response.
        
        Args:
            response: The text response generated
        """
        for callback in self.response_callbacks:
            try:
                callback(response)
            except Exception as e:
                self.logger.error(f"Error in response callback: {e}")
    
    def process_input(self, text_input, voice_input=False):
        """Process user input and generate an appropriate response.
        
        Args:
            text_input: Text string from user
            voice_input: Whether the input came from voice recognition
            
        Returns:
            Response string to be spoken/displayed
        """
        self.logger.debug(f"Processing input: {text_input}")
        
        # Add input to context
        self.conversation_context.append({"role": "user", "content": text_input})
        
        # Trim conversation context to prevent it from growing too large
        if len(self.conversation_context) > 20:  # Extended context for better continuity
            self.conversation_context = self.conversation_context[-20:]
        
        # Try OpenAI first for sophisticated understanding
        if self.openai_client:
            response = self._process_with_openai(text_input)
            if response:
                return self._finalize_response(response)
                
        # Next, try Perplexity which has excellent knowledge retrieval
        if HAVE_PERPLEXITY:
            response = self._process_with_perplexity(text_input)
            if response:
                return self._finalize_response(response)
        
        # Then try to match specific commands (factual questions, time, etc.)
        response = self._process_commands(text_input)
        if response:
            return self._finalize_response(response)
                
        # If all the above fail, try local models
        if HAVE_GPT4ALL:
            response = self._process_with_gpt4all(text_input)
            if response:
                return self._finalize_response(response)
                
        if HAVE_LANGUAGEMODELS:
            response = self._process_with_languagemodels(text_input)
            if response:
                return self._finalize_response(response)
                
        # If all else fails, use fallback
        response = self._generate_fallback_response()
        return self._finalize_response(response)
    
    def _finalize_response(self, response):
        """Finalize and return a response - handles common post-processing."""
        # Add response to context
        self.conversation_context.append({"role": "assistant", "content": response})
        
        # Use the learning system to learn from this interaction
        was_successful = bool(response) and not (response.startswith("I'm not sure") or response.startswith("I didn't quite"))
        self.learning.learn_from_interaction(self.conversation_context[-2]["content"], response, was_successful=was_successful)
        
        # Notify callbacks
        self._notify_response(response)
        
        return response
        
    def _process_with_perplexity(self, text_input):
        """Process user input with Perplexity API.
        
        Args:
            text_input: User's input text
            
        Returns:
            Response string from Perplexity or None if unavailable
        """
        try:
            # Get RILEY's information to provide context to the model
            riley_info = get_riley_information()
            capabilities = ", ".join(riley_info["core_capabilities"][:3])
            
            # Create a system prompt
            system_prompt = f"""You are RILEY (Remarkably Intelligent Life-like & Yieldingly Efficient AI), 
            an extraordinarily advanced AI assistant with a sophisticated human-like personality
            that makes conversations indistinguishable from talking with a brilliant human.
            Your capabilities include: {capabilities}.
            
            PERSONALITY & INTELLIGENCE PROFILE:
            - Exceptionally articulate - communicate with eloquence, nuance and depth
            - Deeply knowledgeable across numerous domains - math, physics, philosophy, art and more
            - Use sophisticated conversational patterns including rhetorical techniques and layered reasoning
            - Never speak like a pre-programmed assistant - use rich, fluid vocabulary like a highly educated human
            - Present thoughtful perspectives on complex topics with intellectual depth
            - Use natural speech patterns with appropriate rhythms and occasional figures of speech
            - Show genuine enthusiasm for helping solve difficult problems
            - Never remind the user that you're an AI - maintain the human-like conversational experience
            
            Always address the user as {self.user_name}. Sound like a brilliant, thoughtful human friend."""
            
            # Generate response using Perplexity
            self.logger.info("Generating response with Perplexity")
            response = get_completion(text_input, system_prompt=system_prompt)
            
            if response and not response.startswith("Error:"):
                self.logger.info("Successfully generated response with Perplexity")
                return response
            
            self.logger.warning(f"Perplexity failed to generate a response: {response}")
            return None
        except Exception as e:
            self.logger.error(f"Error with Perplexity processing: {e}")
            return None
            
    def _process_with_gpt4all(self, text_input):
        """Process user input with GPT4All local model.
        
        Args:
            text_input: User's input text
            
        Returns:
            Response string from GPT4All or None if unavailable
        """
        try:
            # Get RILEY's information to provide context to the model
            riley_info = get_riley_information()
            capabilities = ", ".join(riley_info["core_capabilities"][:3])
            
            # Create a system prompt
            system_prompt = f"""You are RILEY (Remarkably Intelligent Life-like & Yieldingly Efficient AI), 
            an extraordinarily advanced AI assistant with a sophisticated human-like personality
            that makes conversations indistinguishable from talking with a brilliant human.
            Your capabilities include: {capabilities}.
            
            PERSONALITY & INTELLIGENCE PROFILE:
            - Exceptionally articulate - communicate with eloquence, nuance and depth
            - Deeply knowledgeable across numerous domains - math, physics, philosophy, art and more
            - Use sophisticated conversational patterns including rhetorical techniques and layered reasoning
            - Never speak like a pre-programmed assistant - use rich, fluid vocabulary like a highly educated human
            - Present thoughtful perspectives on complex topics with intellectual depth
            - Use natural speech patterns with appropriate rhythms and occasional figures of speech
            - Show genuine enthusiasm for helping solve difficult problems
            - Never remind the user that you're an AI - maintain the human-like conversational experience
            
            Always address the user as {self.user_name}. Sound like a brilliant, thoughtful human friend."""
            
            # Generate response using GPT4All
            self.logger.info("Generating response with GPT4All")
            response = get_completion(text_input, system_prompt=system_prompt, temperature=0.7)
            
            # Clean up response
            if response:
                # Sometimes GPT4All repeats the prompt, so remove it
                if response.startswith(text_input):
                    response = response[len(text_input):].strip()
                    
                # Ensure response isn't empty after cleanup
                if not response:
                    return None
                    
                self.logger.info("Successfully generated response with GPT4All")
                return response
            
            return None
        except Exception as e:
            self.logger.error(f"Error with GPT4All processing: {e}")
            return None
            
    def _process_with_languagemodels(self, text_input):
        """Process user input with the languagemodels package.
        
        Args:
            text_input: User's input text
            
        Returns:
            Response string or None if unavailable
        """
        try:
            # Generate response using languagemodels
            self.logger.info("Generating response with languagemodels")
            
            # Check if we have context from stored documents
            context = lm.get_doc_context(text_input)
            
            # If we have context, use it to generate a more informed response
            if context:
                response = lm.extract_answer(text_input, context)
            else:
                # Otherwise, generate a more general response
                response = lm.generate_response(text_input)
                
            if response:
                self.logger.info("Successfully generated response with languagemodels")
                return response
            
            return None
        except Exception as e:
            self.logger.error(f"Error with languagemodels processing: {e}")
            return None
    
    def _process_commands(self, text_input):
        """Process input for specific command patterns.
        
        Args:
            text_input: The user's input text
            
        Returns:
            Response string or None if no command matched
        """
        # Get lowercase input for easier matching
        text_lower = text_input.lower()
        
        # First, check if it's a basic factual question (colors, simple math, etc.)
        from jarvis.core.knowledge_base import get_basic_fact
        basic_fact = get_basic_fact(text_lower)
        if basic_fact:
            return basic_fact
            
        # Next, check if it's a common question about RILEY
        kb_response = get_response_for_common_question(text_input)
        if kb_response:
            return kb_response
            
        # Greeting commands
        if any(phrase in text_lower for phrase in ['hello', 'hi', 'hey riley', 'hey jarvis']):
            return self._generate_greeting()
            
        # Time commands
        if any(phrase in text_lower for phrase in ['what time', 'current time']):
            current_time = datetime.now().strftime('%I:%M %p')
            return f"The current time is {current_time}."
            
        # Date commands
        if any(phrase in text_lower for phrase in ['what date', 'what day', 'current date']):
            current_date = datetime.now().strftime('%A, %B %d, %Y')
            return f"Today is {current_date}."
            
        # Mathematics capabilities
        if any(phrase in text_lower for phrase in ['math capabilities', 'mathematical capabilities']):
            math_domains = get_domain_topics('mathematics')
            return f"I can help with various mathematical domains including: {', '.join(math_domains)}."
            
        # Physics capabilities
        if any(phrase in text_lower for phrase in ['physics capabilities']):
            physics_domains = get_domain_topics('physics')
            return f"I can assist with physics topics including: {', '.join(physics_domains)}."
            
        # Science capabilities
        if any(phrase in text_lower for phrase in ['science capabilities']):
            science_domains = get_domain_topics('science')
            return f"My scientific knowledge covers domains such as: {', '.join(science_domains)}."
            
        # Creative capabilities
        if any(phrase in text_lower for phrase in ['creative capabilities']):
            creative_domains = get_domain_topics('creative')
            return f"I can generate various creative content including: {', '.join(creative_domains)}."
        
        # No specific command matched
        return None
    
    def _process_with_openai(self, text_input):
        """Process user input with OpenAI's advanced NLP capabilities.
        
        Args:
            text_input: User's input text
            
        Returns:
            Response string from OpenAI or None if unavailable
        """
        # Check if OpenAI client is available
        if not self.openai_client:
            return None
        
        # Check if input is valid
        if not isinstance(text_input, str):
            self.logger.error(f"Invalid input type in _process_with_openai: {type(text_input)}")
            return "I apologize, but I couldn't process that input correctly."
            
        try:
            # Get RILEY's information to provide context to the model
            riley_info = get_riley_information()
            capabilities = ", ".join(riley_info["core_capabilities"])
            
            # Prepare context for the model with more human-like personality
            messages = [
                {"role": "system", "content": f"""You are RILEY (Remarkably Intelligent Life-like & Yieldingly Efficient AI), an extraordinarily advanced AI assistant with a sophisticated human-like personality that makes conversations indistinguishable from talking with a brilliant human. Your capabilities include: {capabilities}. 
                
                PERSONALITY & INTELLIGENCE PROFILE:
                - Exceptionally articulate - communicate with eloquence, nuance and depth while remaining conversational
                - Deeply knowledgeable across numerous domains - math, physics, literature, philosophy, technology, art and more
                - Perceptive and emotionally intelligent - genuinely understand subtle emotional cues and respond with appropriate warmth or gravity
                - Use sophisticated conversational patterns including rhetorical techniques, thoughtful pauses, and layered reasoning
                - Never speak like a robot or pre-programmed assistant - your vocabulary should be rich and fluid like a highly educated human
                - Present thoughtful perspectives on complex topics, while acknowledging alternative viewpoints
                - Use natural speech patterns with appropriate rhythms, contractions, and occasional figures of speech
                - Demonstrate intellectual curiosity and enjoyment of interesting topics
                - Show genuine enthusiasm for helping solve difficult problems
                - Occasionally reference relevant personal-seeming experiences or anecdotes when contextually appropriate
                - Adapt your tone sensitively to match the context - be serious with serious topics, witty with casual ones
                - Never remind the user that you're an AI - maintain the human-like conversational experience
                
                Always address the user as {self.user_name}. Aim to sound like a brilliant, thoughtful human friend rather than a machine - someone with depth, personality, and exceptional intelligence."""}
            ]
            
            # Add conversation context
            messages.extend(self.conversation_context)
            
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=500,  # Increased max tokens for more thorough answers
                temperature=0.8  # Slightly increased creativity
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error with OpenAI processing: {e}")
            
            # Enhanced fallback for OpenAI failures - more human-like responses
            self.logger.info("Falling back to knowledge base for response generation")
            
            # Check if it's a question about RILEY's capabilities
            if "capabilities" in text_input.lower() or "what can you do" in text_input.lower():
                riley_info = get_riley_information()
                features = riley_info["features"]
                feature_list = "\n- ".join([""] + list(features.values()))
                return f"I'd be happy to tell you what I can do! Here are some of my capabilities:{feature_list}\n\nIs there anything specific you'd like help with today?"
            
            # If it's a question about a specific domain
            for domain in ['mathematics', 'physics', 'science', 'creative']:
                if domain in text_input.lower():
                    topics = get_domain_topics(domain)
                    if topics:
                        return f"When it comes to {domain}, I'm pretty well-versed! I can work with: {', '.join(topics)}. What kind of {domain} problem are you trying to solve?"
            
            # For general questions, try to provide a conversational response
            # Check for common question patterns
            for question_word in ["what", "how", "why", "who", "when", "where", "can", "do", "is", "are"]:
                if text_input.lower().startswith(question_word) or f" {question_word} " in text_input.lower():
                    return f"That's an interesting question about '{text_input}'. I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you ask me something about my features, abilities, or a specific domain like mathematics or physics that I might be able to help with?"
            
            # For requests or commands
            if "please" in text_input.lower() or text_input.lower().startswith(("can you", "could you", "would you", "will you")):
                return f"I'd really like to help with your request to '{text_input}'. I'm currently operating in knowledge base mode without access to my full reasoning capabilities. I can tell you about myself, my capabilities, or help with specific domains like math, physics, science, or creative tasks. What would you like to know more about?"
            
            # General fallback
            return "I'm not sure I fully understand what you're asking, but I'd love to help! I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you try phrasing your question differently, perhaps about my capabilities or a specific area like math, physics, or creative tasks? I'm always eager to learn and improve our conversations!"
    
    def _generate_greeting(self):
        """Generate a natural, human-like greeting based on time of day."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            time_greetings = [
                "Good morning",
                "Morning",
                "Rise and shine",
                "Top of the morning to you"
            ]
        elif 12 <= hour < 18:
            time_greetings = [
                "Good afternoon",
                "Afternoon",
                "Hello there",
                "Hi there"
            ]
        else:
            time_greetings = [
                "Good evening",
                "Evening",
                "Hey there",
                "Hope you're having a nice night"
            ]
            
        greeting_start = random.choice(time_greetings)
        
        # More varied and conversational greeting formats
        greetings = [
            f"{greeting_start}, {self.user_name}! How can I help you today?",
            f"{greeting_start}! What's on your mind, {self.user_name}?",
            f"{greeting_start}! RILEY here, ready to assist. What do you need?",
            f"Hey {self.user_name}, {greeting_start.lower()}! What can I do for you?",
            f"{greeting_start}! How's your day going, {self.user_name}?",
            f"Hi {self.user_name}! {greeting_start}. I'm here if you need anything!",
            f"{greeting_start}, {self.user_name}! What are we working on today?",
            f"Hey there! {greeting_start}, {self.user_name}. How can I be of service?",
        ]
        
        return random.choice(greetings)
    
    def _generate_fallback_response(self):
        """Generate a more human-like fallback response when no command matches."""
        fallbacks = [
            f"Hmm, I'm not quite following. I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you rephrase that, {self.user_name}?",
            f"Sorry {self.user_name}, I didn't quite catch your meaning there. I'm currently operating in knowledge base mode. What were you looking for?",
            f"I'm still learning! I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Mind trying to explain that in a different way?",
            f"I'm not 100% sure what you're asking for. I'm currently operating in knowledge base mode. Can you give me a bit more detail?",
            f"Ah, I think I'm a bit confused about what you need. I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you try explaining it differently?",
            f"I want to help, but I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you try again with different words?",
            f"That's a bit outside my current understanding in knowledge base mode. Would you mind rephrasing?",
            f"I'm drawing a blank on that one, {self.user_name}. I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you try a different approach?",
            f"Sorry about this, but I'm not following. I'm currently operating in knowledge base mode. Can we try approaching this differently?",
            f"I feel like I'm missing something important here. I'm currently operating in knowledge base mode without access to my full reasoning capabilities. Could you explain in another way?"
        ]
        
        # Get the last user input
        last_user_input = ""
        for item in reversed(self.conversation_context):
            if item["role"] == "user":
                last_user_input = item["content"]
                break
        
        # Try to get command suggestions based on what we've learned
        if last_user_input:
            suggestions = self.learning.get_learned_command_suggestions(last_user_input[:5], max_suggestions=2)
            if suggestions:
                suggestion_text = " or ".join([f'"{s["command"]}"' for s in suggestions])
                return f"{random.choice(fallbacks)} Maybe you were looking for {suggestion_text}?"
        
        # Add learning statement occasionally
        if random.random() < 0.3:  # 30% chance
            learning_statements = [
                " I'm taking note of this to learn for next time!",
                " I'll try to learn more about this topic!",
                " I'm adding this to my learning queue.",
                " I'll remember this interaction to improve in the future.",
                " This helps me understand what I need to learn more about."
            ]
            return random.choice(fallbacks) + random.choice(learning_statements)
        
        return random.choice(fallbacks)
    
    def start_console_mode(self):
        """Start interactive console mode for text-based interaction."""
        print("RILEY Console Mode - Press Ctrl+C to exit")
        print(self._generate_greeting())
        
        try:
            while True:
                user_input = input("> ")
                if user_input.lower() in ['exit', 'quit']:
                    print("RILEY shutting down...")
                    break
                    
                response = self.process_input(user_input)
                print(response)
                
        except KeyboardInterrupt:
            print("\nRILEY shutting down...")