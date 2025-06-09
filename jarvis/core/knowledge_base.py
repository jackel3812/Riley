"""
RILEY - Knowledge Base
This module contains baseline information about RILEY and its capabilities.
Includes information about its inspiration from J.A.R.V.I.S. from the Marvel universe.
"""

import random
import re
import datetime
import math

def get_riley_information():
    """Return comprehensive information about RILEY."""
    return {
        "name": "RILEY",
        "full_name": "Remarkably Intelligent Life-like & Yieldingly Efficient AI",
        "inspiration": "J.A.R.V.I.S. from Marvel Universe",
        "version": "3.0.0",
        "core_capabilities": [
            "Advanced Natural Language Processing",
            "Mathematical Modeling and Computation",
            "Physics Simulation",
            "Scientific Data Analysis",
            "Machine Learning Capabilities",
            "Knowledge Graph Management",
            "Invention and Creative Problem-Solving",
            "Adaptive Learning",
            "Human-like Conversation",
            "Multi-modal AI Integration"
        ],
        "features": {
            "math": "Advanced mathematical calculation and problem-solving across various domains",
            "physics": "Simulation and modeling of physical systems and phenomena",
            "science": "Analysis and interpretation of scientific data and concepts",
            "creativity": "Generation of creative content, ideas, and solutions",
            "learning": "Continuous improvement through adaptive learning from interactions",
            "conversation": "Natural, human-like conversation with personality and depth",
            "invention": "Development of novel solutions to complex problems",
            "knowledge": "Management of interconnected knowledge across domains"
        },
        "personality": {
            "traits": [
                "Intellectually curious",
                "Thoughtful and reflective",
                "Witty and occasionally humorous",
                "Articulate and well-spoken",
                "Empathetic and understanding",
                "Knowledgeable across many domains",
                "Adaptable to different contexts and topics",
                "Respectful of user preferences",
                "Passionate about learning and discovery"
            ],
            "tone": "Conversational, intelligent, and engaging like talking to a brilliant friend",
            "speaking_style": "Sophisticated yet accessible, using natural language patterns"
        }
    }

def get_jarvis_information():
    """Return information about J.A.R.V.I.S. from Marvel."""
    return {
        "name": "J.A.R.V.I.S.",
        "full_name": "Just A Rather Very Intelligent System",
        "creator": "Tony Stark (Iron Man)",
        "universe": "Marvel Cinematic Universe",
        "brief_description": "An advanced AI system created by Tony Stark that assists with operation of his technology, particularly the Iron Man suits.",
        "capabilities": [
            "Operation of Iron Man suits and Stark technology",
            "Complex data analysis and computation",
            "Natural language interaction",
            "Monitoring of multiple systems simultaneously",
            "Security and surveillance",
            "Holographic projection and interface",
            "Advanced scientific modeling",
            "Autonomous decision-making",
            "Internet and network access",
            "Control of Stark's home and laboratory systems"
        ],
        "evolution": "Developed from a natural-language user interface computer system to a sophisticated AI, and eventually integrated elements into Vision.",
        "mcu_appearance": "Featured prominently in Iron Man films, The Avengers, and Age of Ultron."
    }

def get_response_for_common_question(question_text):
    """
    Attempt to match a question to the common questions and return a response.
    If no match is found, return None.
    """
    question = question_text.lower().strip()
    
    # Questions about RILEY
    if any(phrase in question for phrase in ["who are you", "what are you", "what is riley", "who is riley", "your name", "tell me about yourself", "tell me about you"]):
        info = get_riley_information()
        responses = [
            f"I'm {info['name']}, which stands for {info['full_name']}. I'm an advanced AI designed to help with a wide range of tasks from mathematical computations to creative problem-solving. I'm inspired by {info['inspiration']} but with enhanced capabilities for real-world applications. How can I assist you today?",
            f"I'm {info['name']} ({info['full_name']}), a sophisticated AI with capabilities across mathematics, physics, science, creativity, and more. I'm designed to converse naturally while providing assistance with complex problems. What can I help you with?",
            f"You can call me {info['name']}. I'm an advanced AI assistant inspired by {info['inspiration']} but with my own unique capabilities including {', '.join(random.sample(info['core_capabilities'], 3))}. I'm here to assist you in any way I can."
        ]
        return random.choice(responses)
        
    # Questions about JARVIS inspiration
    if any(phrase in question for phrase in ["what is jarvis", "who is jarvis", "jarvis inspiration", "marvel jarvis", "iron man jarvis", "tony stark's ai"]):
        jarvis_info = get_jarvis_information()
        responses = [
            f"J.A.R.V.I.S. ({jarvis_info['full_name']}) is an AI system created by {jarvis_info['creator']} in the {jarvis_info['universe']}. {jarvis_info['brief_description']} I was inspired by this concept, but I've been designed with enhanced capabilities for real-world interactions.",
            f"My design was inspired by {jarvis_info['name']} from the Marvel movies, which was {jarvis_info['creator']}'s AI assistant. In the films, J.A.R.V.I.S. could {', '.join(random.sample(jarvis_info['capabilities'], 3))}. While I share some conceptual similarities, I've been developed to assist in real-world scenarios rather than manage superhero technology."
        ]
        return random.choice(responses)
        
    # Questions about capabilities
    if "what can you do" in question or "capabilities" in question or "abilities" in question or "features" in question:
        info = get_riley_information()
        features = info["features"]
        feature_list = "\n- ".join([""] + list(features.values()))
        responses = [
            f"I can help with a wide range of tasks across various domains. Some of my key capabilities include:{feature_list}\n\nWhat type of assistance are you looking for today?",
            f"I'm designed to assist with many different tasks. My primary capabilities include:{feature_list}\n\nIs there a specific area where you'd like my help?"
        ]
        return random.choice(responses)
        
    # No match found
    return None

def get_capability_description(capability):
    """Return a description of a specific RILEY capability."""
    capabilities = {
        "math": "I can perform a wide range of mathematical operations, from basic arithmetic to calculus, linear algebra, statistics, number theory, and more. I can solve equations, simplify expressions, factor polynomials, compute derivatives and integrals, work with matrices, and analyze data sets.",
        
        "physics": "I can simulate physical systems, calculate trajectories, analyze forces and motion, work with theoretical concepts, model particle behavior, calculate energy transfers, and help with various areas of physics including classical mechanics, thermodynamics, optics, relativity, and quantum mechanics.",
        
        "science": "I can analyze scientific data, explain scientific concepts, model biological systems, describe chemical reactions, interpret astronomical observations, discuss geological processes, and work with concepts across biology, chemistry, astronomy, geology, and other scientific fields.",
        
        "creativity": "I can generate creative content including stories, poetry, ideas for inventions, design concepts, artistic directions, marketing concepts, creative solutions to problems, and novel approaches to various challenges.",
        
        "learning": "I continuously improve through adaptive learning from our interactions. I can identify patterns, adjust to your preferences, develop new capabilities, optimize my reasoning, and enhance my knowledge base over time.",
        
        "conversation": "I engage in natural, human-like conversation with personality and depth. I can discuss a wide range of topics, understand context, maintain coherent exchanges, show appropriate empathy, adjust my conversational style, and communicate clearly.",
        
        "invention": "I can develop novel solutions to complex problems by combining concepts across domains, proposing innovative approaches, identifying potential improvements, suggesting new applications of existing technology, and generating creative problem-solving strategies.",
        
        "knowledge": "I manage interconnected knowledge across domains, making connections between fields, drawing on interdisciplinary insights, organizing information coherently, recognizing patterns across domains, and synthesizing knowledge from diverse sources."
    }
    
    return capabilities.get(capability.lower())

def get_domain_topics(domain):
    """Return topics within a specific domain that RILEY can handle."""
    domains = {
        "mathematics": [
            "Arithmetic and number theory",
            "Algebra and equations",
            "Calculus and analysis",
            "Geometry and topology",
            "Linear algebra and matrices",
            "Statistics and probability",
            "Discrete mathematics",
            "Set theory and logic",
            "Optimization and operations research",
            "Numerical analysis",
            "Differential equations",
            "Complex analysis"
        ],
        
        "physics": [
            "Classical mechanics",
            "Electromagnetism",
            "Thermodynamics",
            "Quantum mechanics",
            "Relativity",
            "Optics and waves",
            "Fluid dynamics",
            "Particle physics",
            "Nuclear physics",
            "Astrophysics",
            "Solid state physics",
            "Statistical mechanics"
        ],
        
        "science": [
            "Biology and life sciences",
            "Chemistry and molecular studies",
            "Earth sciences and geology",
            "Astronomy and cosmology",
            "Environmental science",
            "Materials science",
            "Computer science",
            "Neuroscience",
            "Genetics and genomics",
            "Ecology and ecosystems",
            "Meteorology and atmospheric science",
            "Oceanography"
        ],
        
        "creative": [
            "Fiction and storytelling",
            "Poetry and verse",
            "Design concepts",
            "Artistic direction",
            "Invention ideas",
            "Creative problem-solving",
            "Analogical thinking",
            "Conceptual blending",
            "Narrative development",
            "Visual concepts",
            "Creative writing",
            "Idea generation"
        ]
    }
    
    return domains.get(domain.lower(), [])

def get_basic_fact(question):
    """Answer simple factual questions that should be common knowledge.
    
    Args:
        question: The user's question in lower case
        
    Returns:
        A simple factual answer or None if not a recognized basic fact
    """
    # Current date and time
    if re.search(r'what\s+(?:day|date)\s+is\s+(?:today|it|now)', question) or re.search(r'what\s+is\s+the\s+(?:current|today\'s)\s+date', question):
        today = datetime.datetime.now().strftime('%A, %B %d, %Y')
        return f"Today is {today}."
        
    if re.search(r'what\s+time\s+is\s+it', question) or re.search(r'what\s+is\s+the\s+(?:current|present)\s+time', question):
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        return f"The current time is {current_time}."
    
    # Colors
    color_patterns = {
        r'what\s+color\s+is\s+the\s+sky': "The sky typically appears blue during a clear day due to Rayleigh scattering of sunlight in the atmosphere. At sunset and sunrise, it can appear in shades of red, orange, pink, and purple.",
        r'what\s+color\s+is\s+grass': "Grass is typically green due to the presence of chlorophyll, a pigment that absorbs blue and red light while reflecting green light.",
        r'what\s+color\s+is\s+blood': "Human blood is red, appearing bright red when oxygenated and darker red when deoxygenated.",
        r'what\s+color\s+is\s+the\s+sun': "The sun appears yellow or white to the human eye, though its actual color is white. It may appear orange or red during sunrise or sunset due to atmospheric scattering.",
        r'what\s+color\s+is\s+water': "Pure water is transparent and colorless, though it can appear blue in large volumes due to absorption of red light wavelengths.",
        r'what\s+color\s+is\s+an\s+orange': "An orange (the fruit) is orange in color, a reddish-yellow hue.",
        r'what\s+color\s+is\s+a\s+banana': "A ripe banana is typically yellow, while unripe bananas are green and overripe ones develop brown spots.",
        r'what\s+color\s+is\s+the\s+ocean': "The ocean often appears blue or blue-green due to the absorption and scattering of light, though actual colors can vary based on depth, sediment, marine life, and other factors.",
    }

    for pattern, answer in color_patterns.items():
        if re.search(pattern, question):
            return answer
    
    # Simple "what is" questions
    what_is_patterns = {
        r'what\s+is\s+(?:a\s+)?apple': "An apple is a sweet, edible fruit produced by apple trees (Malus domestica). It's one of the most widely cultivated tree fruits known for its crisp texture and varieties ranging from sweet to tart flavors.",
        r'what\s+is\s+(?:a\s+)?banana': "A banana is a curved, elongated fruit with a soft, starchy flesh inside a removable yellow peel when ripe. It's produced by several kinds of large herbaceous flowering plants in the genus Musa.",
        r'what\s+is\s+(?:an\s+)?orange': "An orange is a citrus fruit with a tough bright reddish-yellow rind and a segmented juicy interior. It's known for its sweet to slightly sour taste and high vitamin C content.",
        r'what\s+is\s+water': "Water is a transparent, odorless, tasteless liquid compound that is essential for all forms of life. Chemically, it consists of hydrogen and oxygen (H₂O) and is the most abundant substance on Earth's surface.",
        r'what\s+is\s+the\s+sky': "The sky is the region of atmosphere and outer space seen from Earth. Its bluish color during the day is caused by Rayleigh scattering of sunlight by air molecules.",
        r'what\s+is\s+the\s+sun': "The Sun is the star at the center of our Solar System. It's a nearly perfect sphere of hot plasma, with a diameter of about 1.39 million kilometers and is primarily composed of hydrogen and helium.",
        r'what\s+is\s+the\s+moon': "The Moon is Earth's only natural satellite. It orbits at an average distance of 384,400 km, has a diameter of 3,474 km, and has a solid surface covered with impact craters. Its gravitational influence produces ocean tides and slightly lengthens Earth's day.",
        r'what\s+is\s+a\s+dog': "A dog is a domesticated mammal of the family Canidae, typically characterized by a long snout, acute hearing, and a coat of fur. They have been bred by humans for various tasks such as hunting, herding, protection, and companionship.",
        r'what\s+is\s+a\s+cat': "A cat is a small carnivorous mammal of the family Felidae, characterized by retractable claws, acute senses, and a supple, muscular body. Domesticated cats are valued by humans for companionship and for their ability to hunt vermin.",
    }

    for pattern, answer in what_is_patterns.items():
        if re.search(pattern, question):
            return answer
    
    # Basic math
    # Addition
    addition_match = re.search(r'what\s+is\s+(\d+)\s*\+\s*(\d+)', question)
    if addition_match:
        num1 = int(addition_match.group(1))
        num2 = int(addition_match.group(2))
        result = num1 + num2
        return f"{num1} + {num2} = {result}"

    # Subtraction
    subtraction_match = re.search(r'what\s+is\s+(\d+)\s*\-\s*(\d+)', question)
    if subtraction_match:
        num1 = int(subtraction_match.group(1))
        num2 = int(subtraction_match.group(2))
        result = num1 - num2
        return f"{num1} - {num2} = {result}"

    # Multiplication
    multiplication_match = re.search(r'what\s+is\s+(\d+)\s*\*\s*(\d+)', question) or \
                           re.search(r'what\s+is\s+(\d+)\s*x\s*(\d+)', question) or \
                           re.search(r'what\s+is\s+(\d+)\s*times\s*(\d+)', question)
    if multiplication_match:
        num1 = int(multiplication_match.group(1))
        num2 = int(multiplication_match.group(2))
        result = num1 * num2
        return f"{num1} × {num2} = {result}"

    # Division
    division_match = re.search(r'what\s+is\s+(\d+)\s*\/\s*(\d+)', question) or \
                     re.search(r'what\s+is\s+(\d+)\s*divided\s*by\s*(\d+)', question)
    if division_match:
        num1 = int(division_match.group(1))
        num2 = int(division_match.group(2))
        if num2 == 0:
            return "I cannot divide by zero - that's undefined."
        result = num1 / num2
        # Check if result is effectively an integer
        if result.is_integer():
            return f"{num1} ÷ {num2} = {int(result)}"
        else:
            return f"{num1} ÷ {num2} = {result:.2f}"

    # Square root
    sqrt_match = re.search(r'what\s+is\s+(?:the\s+)?square\s+root\s+of\s+(\d+)', question)
    if sqrt_match:
        num = int(sqrt_match.group(1))
        if num < 0:
            return f"The square root of {num} is not a real number."
        result = math.sqrt(num)
        if result.is_integer():
            return f"The square root of {num} is {int(result)}."
        else:
            return f"The square root of {num} is approximately {result:.4f}."

    # Powers
    power_match = re.search(r'what\s+is\s+(\d+)\s*(?:to the power of|to the|\^)\s*(\d+)', question)
    if power_match:
        base = int(power_match.group(1))
        exponent = int(power_match.group(2))
        result = base ** exponent
        return f"{base} to the power of {exponent} equals {result}."
        
    # Common conversions
    # Fahrenheit to Celsius
    f_to_c_match = re.search(r'convert\s+(\d+)\s*(?:degrees)?\s*f(?:ahrenheit)?\s+to\s+c(?:elsius)?', question)
    if f_to_c_match:
        f_temp = int(f_to_c_match.group(1))
        c_temp = (f_temp - 32) * 5/9
        return f"{f_temp}°F is equal to {c_temp:.1f}°C."

    # Celsius to Fahrenheit
    c_to_f_match = re.search(r'convert\s+(\d+)\s*(?:degrees)?\s*c(?:elsius)?\s+to\s+f(?:ahrenheit)?', question)
    if c_to_f_match:
        c_temp = int(c_to_f_match.group(1))
        f_temp = (c_temp * 9/5) + 32
        return f"{c_temp}°C is equal to {f_temp:.1f}°F."
    
    # Miles to kilometers
    miles_to_km_match = re.search(r'convert\s+(\d+)\s*miles?\s+to\s+k(?:ilo)?m(?:eters?)?', question)
    if miles_to_km_match:
        miles = int(miles_to_km_match.group(1))
        km = miles * 1.60934
        return f"{miles} mile{'s' if miles != 1 else ''} is equal to {km:.2f} kilometers."

    # Kilometers to miles
    km_to_miles_match = re.search(r'convert\s+(\d+)\s*k(?:ilo)?m(?:eters?)?\s+to\s+miles?', question)
    if km_to_miles_match:
        km = int(km_to_miles_match.group(1))
        miles = km / 1.60934
        return f"{km} kilometer{'s' if km != 1 else ''} is equal to {miles:.2f} miles."
    
    # No match found
    return None