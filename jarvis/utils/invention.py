"""
RILEY - Invention Module

This module provides advanced invention capabilities including:
- Creative problem solving
- Patent analysis
- Invention generation
- Design patterns
- Technology forecasting
- Reverse engineering analysis
"""

import logging
import random
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re
import datetime

logger = logging.getLogger(__name__)

class InventionEngine:
    """Advanced invention and creative problem-solving engine."""
    
    def __init__(self):
        """Initialize the invention engine."""
        logger.info("Initializing Invention Engine")
        self._load_design_patterns()
        self._load_technology_domains()
        self._load_innovation_principles()
    
    def _load_design_patterns(self):
        """Load design patterns database."""
        # Software design patterns
        self.software_patterns = {
            "creational": [
                {"name": "Factory Method", "description": "Defines an interface for creating an object, but lets subclasses decide which class to instantiate."},
                {"name": "Abstract Factory", "description": "Provides an interface for creating families of related or dependent objects without specifying their concrete classes."},
                {"name": "Builder", "description": "Separates the construction of a complex object from its representation, allowing the same construction process to create different representations."},
                {"name": "Prototype", "description": "Specifies the kinds of objects to create using a prototypical instance, and creates new objects by copying this prototype."},
                {"name": "Singleton", "description": "Ensures a class has only one instance, and provides a global point of access to it."},
            ],
            "structural": [
                {"name": "Adapter", "description": "Allows incompatible interfaces to work together."},
                {"name": "Bridge", "description": "Decouples an abstraction from its implementation so the two can vary independently."},
                {"name": "Composite", "description": "Composes objects into tree structures to represent part-whole hierarchies."},
                {"name": "Decorator", "description": "Attaches additional responsibilities to an object dynamically."},
                {"name": "Facade", "description": "Provides a simplified interface to a complex subsystem."},
                {"name": "Flyweight", "description": "Uses sharing to support large numbers of similar objects efficiently."},
                {"name": "Proxy", "description": "Provides a surrogate or placeholder for another object to control access to it."},
            ],
            "behavioral": [
                {"name": "Chain of Responsibility", "description": "Passes a request along a chain of handlers."},
                {"name": "Command", "description": "Encapsulates a request as an object, allowing for parameterization of clients with different requests."},
                {"name": "Interpreter", "description": "Implements a specialized language."},
                {"name": "Iterator", "description": "Accesses the elements of an aggregate object sequentially without exposing its underlying representation."},
                {"name": "Mediator", "description": "Defines an object that encapsulates how a set of objects interact."},
                {"name": "Memento", "description": "Captures and externalizes an object's internal state without violating encapsulation."},
                {"name": "Observer", "description": "Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically."},
                {"name": "State", "description": "Allows an object to alter its behavior when its internal state changes."},
                {"name": "Strategy", "description": "Defines a family of algorithms, encapsulates each one, and makes them interchangeable."},
                {"name": "Template Method", "description": "Defines the skeleton of an algorithm in a method, deferring some steps to subclasses."},
                {"name": "Visitor", "description": "Represents an operation to be performed on the elements of an object structure."},
            ]
        }
        
        # Engineering design patterns
        self.engineering_patterns = {
            "mechanical": [
                {"name": "Linkage", "description": "Systems of rigid bodies connected by joints to manage forces and movement."},
                {"name": "Ratchet and Pawl", "description": "Allows motion in one direction while preventing motion in the opposite direction."},
                {"name": "Cam and Follower", "description": "Transforms rotary motion into linear motion with a specified displacement pattern."},
                {"name": "Four-bar Linkage", "description": "A mechanism with four rigid links connected in a loop by four pin joints."},
                {"name": "Slider-Crank", "description": "Converts rotational motion to reciprocating linear motion, or vice versa."},
                {"name": "Geneva Drive", "description": "Provides intermittent rotary motion from continuous rotary motion."},
                {"name": "Compliant Mechanisms", "description": "Achieves motion through the elastic deformation of materials rather than rigid-body joints."},
            ],
            "electrical": [
                {"name": "Voltage Divider", "description": "Reduces voltage by a specified ratio using resistors."},
                {"name": "Current Mirror", "description": "Copies current from one branch to another regardless of load conditions."},
                {"name": "Wheatstone Bridge", "description": "Measures unknown electrical resistance by balancing two legs of a bridge circuit."},
                {"name": "Push-Pull Amplifier", "description": "Uses complementary transistors to improve efficiency and reduce distortion."},
                {"name": "Differential Pair", "description": "Uses matched transistors to amplify the difference between two input signals."},
                {"name": "Feedback Loop", "description": "Returns a portion of the output signal back to the input to control system performance."},
                {"name": "Phase-Locked Loop", "description": "Automatically adjusts the phase of a locally generated signal to match a reference signal."},
            ],
            "structural": [
                {"name": "Truss", "description": "Framework consisting of triangular units joined at the vertices to resist loads."},
                {"name": "Space Frame", "description": "Rigid structure made of interconnected struts in a geometric pattern."},
                {"name": "Cantilever", "description": "Structure that extends horizontally and is supported at only one end."},
                {"name": "Arch", "description": "Curved structure that spans an opening and supports load through compression."},
                {"name": "Shell Structure", "description": "Thin curved membrane that provides strength through its shape rather than mass."},
                {"name": "Honeycomb", "description": "Geometric pattern that provides high strength-to-weight ratio."},
                {"name": "Tensegrity", "description": "Structure maintained by a balance between tension and compression components."},
            ]
        }
    
    def _load_technology_domains(self):
        """Load technology domains and exemplars."""
        self.technology_domains = {
            "artificial_intelligence": {
                "name": "Artificial Intelligence",
                "subdomains": ["Machine Learning", "Natural Language Processing", "Computer Vision", "Robotics", "Knowledge Representation"],
                "exemplars": ["Neural Networks", "Deep Learning", "Reinforcement Learning", "Transformer Models", "Genetic Algorithms"],
                "trend_keywords": ["explainable AI", "federated learning", "multimodal AI", "generative AI", "edge AI", "autonomous systems"]
            },
            "biotechnology": {
                "name": "Biotechnology",
                "subdomains": ["Genetic Engineering", "Synthetic Biology", "Bioinformatics", "Tissue Engineering", "Molecular Diagnostics"],
                "exemplars": ["CRISPR", "mRNA Vaccines", "Lab-grown Organs", "Gene Therapy", "Biofabrication"],
                "trend_keywords": ["gene editing", "personalized medicine", "bioprinting", "biomaterials", "biosensors", "microbiome engineering"]
            },
            "energy": {
                "name": "Energy Technology",
                "subdomains": ["Renewable Energy", "Energy Storage", "Smart Grid", "Nuclear Energy", "Energy Efficiency"],
                "exemplars": ["Perovskite Solar Cells", "Solid-state Batteries", "Fusion Reactors", "Hydrogen Fuel Cells", "Supercapacitors"],
                "trend_keywords": ["grid-scale storage", "green hydrogen", "distributed generation", "vehicle-to-grid", "micro nuclear reactors"]
            },
            "materials_science": {
                "name": "Materials Science",
                "subdomains": ["Nanomaterials", "Smart Materials", "Biomaterials", "Composites", "Metamaterials"],
                "exemplars": ["Graphene", "Shape Memory Alloys", "Self-healing Materials", "Superconductors", "Aerogels"],
                "trend_keywords": ["2D materials", "high-entropy alloys", "programmable matter", "stimuli-responsive materials", "quantum materials"]
            },
            "robotics": {
                "name": "Robotics & Automation",
                "subdomains": ["Industrial Robotics", "Collaborative Robots", "Soft Robotics", "Swarm Robotics", "Medical Robotics"],
                "exemplars": ["Autonomous Vehicles", "Exoskeletons", "Surgical Robots", "Drone Swarms", "Humanoid Robots"],
                "trend_keywords": ["human-robot collaboration", "biomimetic robots", "self-reconfiguring robots", "micro-robotics", "sentient robots"]
            },
            "computing": {
                "name": "Advanced Computing",
                "subdomains": ["Quantum Computing", "Neuromorphic Computing", "Edge Computing", "High-Performance Computing", "Distributed Systems"],
                "exemplars": ["Quantum Supremacy", "Brain-inspired Chips", "Exascale Supercomputers", "Blockchain", "Homomorphic Encryption"],
                "trend_keywords": ["post-quantum cryptography", "quantum internet", "brain-computer interfaces", "in-memory computing", "DNA computing"]
            },
            "manufacturing": {
                "name": "Advanced Manufacturing",
                "subdomains": ["Additive Manufacturing", "Digital Manufacturing", "Nanomanufacturing", "Continuous Manufacturing", "Sustainable Manufacturing"],
                "exemplars": ["Multi-material 3D Printing", "Digital Twins", "Molecular Manufacturing", "Continuous Flow Chemistry", "Biofabrication"],
                "trend_keywords": ["mass customization", "distributed manufacturing", "circular economy", "smart factories", "generative design"]
            },
            "transportation": {
                "name": "Transportation",
                "subdomains": ["Electric Vehicles", "Autonomous Vehicles", "Urban Air Mobility", "Hyperloop", "Space Transportation"],
                "exemplars": ["Solid-state Battery EVs", "Level 5 Autonomy", "eVTOL Aircraft", "Vacuum Tube Transport", "Reusable Rockets"],
                "trend_keywords": ["shared mobility", "last-mile solutions", "mobility as a service", "intermodal transportation", "space tourism"]
            },
            "healthcare": {
                "name": "Healthcare Technology",
                "subdomains": ["Medical Devices", "Digital Health", "Drug Discovery", "Diagnostics", "Regenerative Medicine"],
                "exemplars": ["Smart Implants", "AI Diagnostics", "Precision Medicine", "Lab-on-a-chip", "Organ Regeneration"],
                "trend_keywords": ["digital therapeutics", "remote monitoring", "AI drug discovery", "in silico clinical trials", "nanomedicine"]
            },
            "environmental": {
                "name": "Environmental Technology",
                "subdomains": ["Carbon Capture", "Water Treatment", "Waste Management", "Air Purification", "Environmental Monitoring"],
                "exemplars": ["Direct Air Capture", "Advanced Membranes", "Plasma Gasification", "Atmospheric Water Generators", "Distributed Sensors"],
                "trend_keywords": ["circular economy", "ocean cleanup", "biodegradable materials", "microplastic remediation", "climate intervention"]
            }
        }
    
    def _load_innovation_principles(self):
        """Load TRIZ and other innovation principles."""
        # TRIZ (Theory of Inventive Problem Solving) principles
        self.triz_principles = [
            {"id": 1, "name": "Segmentation", "description": "Divide an object into independent parts; make an object easy to disassemble; increase the degree of fragmentation or segmentation."},
            {"id": 2, "name": "Taking Out", "description": "Separate an interfering part or property from an object, or single out the only necessary part (or property)."},
            {"id": 3, "name": "Local Quality", "description": "Change an object's structure from uniform to non-uniform; make each part of an object function in conditions most suitable for its operation."},
            {"id": 4, "name": "Asymmetry", "description": "Change the shape of an object from symmetrical to asymmetrical; if an object is asymmetrical, increase its degree of asymmetry."},
            {"id": 5, "name": "Merging", "description": "Bring closer together (or merge) identical or similar objects; assemble identical or similar parts to perform parallel operations."},
            {"id": 6, "name": "Universality", "description": "Make a part or object perform multiple functions; eliminate the need for other parts."},
            {"id": 7, "name": "Nested Doll", "description": "Place one object inside another; place each object, in turn, inside the other; make one part pass through a cavity in the other."},
            {"id": 8, "name": "Anti-Weight", "description": "To compensate for the weight of an object, merge it with other objects that provide lift; to compensate for the weight, make it interact with the environment."},
            {"id": 9, "name": "Preliminary Anti-Action", "description": "If it will be necessary to do an action with both harmful and useful effects, this action should be preceded by anti-actions to control harmful effects."},
            {"id": 10, "name": "Preliminary Action", "description": "Perform required changes of an object completely or partially before needed; pre-arrange objects such that they can come into action from the most convenient place."},
            {"id": 11, "name": "Beforehand Cushioning", "description": "Prepare emergency means beforehand to compensate for the relatively low reliability of an object."},
            {"id": 12, "name": "Equipotentiality", "description": "In a potential field, limit position changes by changing the operating condition to eliminate the need to raise or lower objects."},
            {"id": 13, "name": "The Other Way Round", "description": "Invert the action used to solve the problem; make movable parts fixed, and fixed parts movable; turn the object upside down."},
            {"id": 14, "name": "Spheroidality", "description": "Instead of using rectilinear parts, surfaces, or forms, use curvilinear ones; move from flat surfaces to spherical ones; from parts shaped as a cube to ball-shaped structures."},
            {"id": 15, "name": "Dynamics", "description": "Allow the characteristics of an object to change to be optimal; divide an object into parts capable of movement relative to each other; if an object is rigid, make it movable or adaptive."},
            {"id": 16, "name": "Partial or Excessive Actions", "description": "If 100 percent of an objective is hard to achieve, using 'slightly less' or 'slightly more' might simplify the problem."},
            {"id": 17, "name": "Another Dimension", "description": "Move an object in two or three-dimensional space; use a multi-story arrangement of objects instead of a single-story arrangement; tilt or re-orient the object."},
            {"id": 18, "name": "Mechanical Vibration", "description": "Cause an object to oscillate or vibrate; increase its frequency even to ultrasonic; use an object's resonant frequency; use piezoelectric vibrators instead of mechanical ones."},
            {"id": 19, "name": "Periodic Action", "description": "Instead of continuous action, use periodic or pulsating actions; if an action is already periodic, change the periodic magnitude or frequency."},
            {"id": 20, "name": "Continuity of Useful Action", "description": "Carry on work continuously; make all parts of an object work at full load, all the time; eliminate idle and intermediate motions."},
            {"id": 21, "name": "Skipping", "description": "Conduct a process at high speed; conduct harmful or hazardous operations at very high speed."},
            {"id": 22, "name": "Blessing in Disguise", "description": "Use harmful factors to achieve a positive effect; eliminate the primary harmful action by adding another harmful action to resolve it."},
            {"id": 23, "name": "Feedback", "description": "Introduce feedback to improve a process or action; if feedback is already used, change its magnitude or influence."},
            {"id": 24, "name": "Intermediary", "description": "Use an intermediary carrier article or intermediary process; merge one object temporarily with another that can be easily removed."},
            {"id": 25, "name": "Self-Service", "description": "Make an object serve itself by performing auxiliary helpful functions; use waste resources, energy, or substances."},
            {"id": 26, "name": "Copying", "description": "Instead of an unavailable, expensive, or fragile object, use simpler and inexpensive copies; replace an object with optical copies or images."},
            {"id": 27, "name": "Cheap Short-Living Objects", "description": "Replace an expensive object with multiple inexpensive objects, compromising certain qualities (such as service life)."},
            {"id": 28, "name": "Mechanics Substitution", "description": "Replace a mechanical system with a sensory (optical, acoustic, taste, or smell) system; use electric, magnetic, and electromagnetic fields to interact with the object."},
            {"id": 29, "name": "Pneumatics and Hydraulics", "description": "Use gas and liquid parts of an object instead of solid parts (e.g., inflatable, filled with liquids, air cushion, hydrostatic, hydro-reactive)."},
            {"id": 30, "name": "Flexible Shells and Thin Films", "description": "Use flexible shells and thin films instead of three-dimensional structures; isolate the object from the external environment using flexible shells."},
            {"id": 31, "name": "Porous Materials", "description": "Make an object porous or add porous elements; if an object is already porous, use the pores to introduce a useful substance or function."},
            {"id": 32, "name": "Color Changes", "description": "Change the color of an object or its external environment; change the transparency of an object or its external environment."},
            {"id": 33, "name": "Homogeneity", "description": "Make objects interact with a given object of the same material (or material with identical properties)."},
            {"id": 34, "name": "Discarding and Recovering", "description": "Make portions of an object that have fulfilled their functions disappear or modify them directly during operation; restore consumable parts of an object during operation."},
            {"id": 35, "name": "Parameter Changes", "description": "Change an object's physical state; change the concentration or consistency; change the degree of flexibility; change the temperature."},
            {"id": 36, "name": "Phase Transitions", "description": "Use phenomena occurring during phase transitions (e.g., volume changes, loss or absorption of heat)."},
            {"id": 37, "name": "Thermal Expansion", "description": "Use thermal expansion of materials; use multiple materials with different coefficients of thermal expansion."},
            {"id": 38, "name": "Strong Oxidants", "description": "Replace common air with oxygen-enriched air; replace enriched air with pure oxygen; expose air or oxygen to ionizing radiation; use ionized oxygen."},
            {"id": 39, "name": "Inert Atmosphere", "description": "Replace a normal environment with an inert one; add neutral parts, or inert additives to an object."},
            {"id": 40, "name": "Composite Materials", "description": "Change from uniform to composite (multiple) materials where each material is optimized to a particular functional requirement."}
        ]
        
        # Biomimicry principles (inspired by nature)
        self.biomimicry_principles = [
            {"name": "Resource Efficiency", "description": "Optimize material use through shape, hierarchical organization, or multi-functionality to achieve more with less."},
            {"name": "Cyclic Processing", "description": "Break down products into benign constituents that can become resources for something new."},
            {"name": "Solar Transformation", "description": "Collect energy using life-friendly chemistry requiring little heat to drive reactions."},
            {"name": "Dynamic Equilibrium", "description": "Maintain balance through constant monitoring and feedback loops."},
            {"name": "Evolutionary Development", "description": "Continuously incorporate iteration, testing, and adaptation."},
            {"name": "Resilience through Diversity", "description": "Incorporate multiple forms, processes, or systems to meet a functional need."},
            {"name": "Local Adaptation", "description": "Fit well within the local ecosystem by responding to specific environmental conditions."},
            {"name": "Shape Complementarity", "description": "Enhance function through structure and morphology rather than additional energy or materials."},
            {"name": "Self-Organization", "description": "Create conditions that allow components to form higher-level ordered structures without external direction."},
            {"name": "Self-Healing", "description": "Detect and respond to damage with immediate and integrated repair mechanisms."},
            {"name": "Sensing and Response", "description": "Monitor and adapt to changing environmental conditions through feedback mechanisms."},
            {"name": "Multi-Functionality", "description": "Meet multiple needs with one solution, reducing material and energy use."}
        ]
        
        # First principles thinking
        self.first_principles = [
            {"name": "Questioning Assumptions", "description": "Identify and challenge the assumptions underlying a problem or solution."},
            {"name": "Breaking Down Complexities", "description": "Decompose complex systems into fundamental components."},
            {"name": "Identifying Fundamental Truths", "description": "Identify basic truths or elements that cannot be deduced from other propositions."},
            {"name": "Reasoning from First Principles", "description": "Build up from fundamental truths rather than reasoning by analogy."},
            {"name": "Seeking Causal Relationships", "description": "Understand true cause-and-effect relationships rather than correlations."}
        ]
    
    def analyze_problem(self, problem_statement, domain=None):
        """Analyze a problem to identify patterns and potential solution approaches.
        
        Args:
            problem_statement: Description of the problem to be solved
            domain: Optional specific domain to focus analysis
            
        Returns:
            Dictionary with problem analysis
        """
        try:
            logger.info(f"Analyzing problem: {problem_statement}")
            
            # Extract keywords from problem statement
            keywords = self._extract_keywords(problem_statement)
            
            # Identify relevant domains
            if domain:
                domains = [domain]
            else:
                domains = self._identify_relevant_domains(problem_statement, keywords)
            
            # Identify contradictions or conflicts
            contradictions = self._identify_contradictions(problem_statement)
            
            # Suggest relevant TRIZ principles
            triz_suggestions = []
            if contradictions:
                for contradiction in contradictions:
                    principles = self._suggest_triz_principles(contradiction)
                    triz_suggestions.append({
                        "contradiction": contradiction,
                        "principles": principles
                    })
            else:
                # General principles that might apply
                triz_suggestions = self._suggest_general_triz_principles(problem_statement, keywords)
            
            # Suggest biomimicry principles
            biomimicry_suggestions = self._suggest_biomimicry_principles(problem_statement, keywords)
            
            # Identify first principles
            first_principles_analysis = self._apply_first_principles(problem_statement)
            
            # Generate solution directions
            solution_directions = self._generate_solution_directions(problem_statement, domains, triz_suggestions, biomimicry_suggestions)
            
            return {
                "problem_statement": problem_statement,
                "keywords": keywords,
                "relevant_domains": domains,
                "contradictions": contradictions,
                "triz_suggestions": triz_suggestions,
                "biomimicry_suggestions": biomimicry_suggestions,
                "first_principles_analysis": first_principles_analysis,
                "solution_directions": solution_directions
            }
            
        except Exception as e:
            logger.error(f"Error analyzing problem: {e}")
            return {"error": f"Could not analyze problem: {e}"}
    
    def _extract_keywords(self, text):
        """Extract key technical and conceptual keywords from text."""
        # This is a simplified keyword extraction
        # Remove common words and punctuation
        common_words = {"a", "an", "the", "in", "on", "at", "by", "for", "with", "about", "to", "of", "is", "are", "was", "were", "be", "been", "being", "and", "or", "but", "than", "that", "this", "these", "those", "then", "so", "as"}
        
        # Clean text and split into words
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter out common words and short words
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        
        # Get unique keywords with counts
        keyword_counts = {}
        for keyword in keywords:
            if keyword in keyword_counts:
                keyword_counts[keyword] += 1
            else:
                keyword_counts[keyword] = 1
        
        # Sort by count
        sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords
        return [keyword for keyword, count in sorted_keywords[:15]]
    
    def _identify_relevant_domains(self, problem_statement, keywords):
        """Identify technology domains relevant to the problem."""
        domain_matches = {}
        
        # Check each domain for keyword matches
        for domain_key, domain_info in self.technology_domains.items():
            score = 0
            
            # Check domain name
            if domain_info["name"].lower() in problem_statement.lower():
                score += 5
            
            # Check subdomains
            for subdomain in domain_info["subdomains"]:
                if subdomain.lower() in problem_statement.lower():
                    score += 3
            
            # Check exemplars
            for exemplar in domain_info["exemplars"]:
                if exemplar.lower() in problem_statement.lower():
                    score += 2
            
            # Check trend keywords
            for trend in domain_info["trend_keywords"]:
                if trend.lower() in problem_statement.lower():
                    score += 1
            
            # Check for keyword matches
            for keyword in keywords:
                # Check in domain name
                if keyword in domain_info["name"].lower():
                    score += 2
                
                # Check in subdomains
                for subdomain in domain_info["subdomains"]:
                    if keyword in subdomain.lower():
                        score += 1
                
                # Check in exemplars
                for exemplar in domain_info["exemplars"]:
                    if keyword in exemplar.lower():
                        score += 1
                
                # Check in trend keywords
                for trend in domain_info["trend_keywords"]:
                    if keyword in trend.lower():
                        score += 0.5
            
            if score > 0:
                domain_matches[domain_key] = {
                    "name": domain_info["name"],
                    "score": score
                }
        
        # Sort domains by score
        sorted_domains = sorted(domain_matches.items(), key=lambda x: x[1]["score"], reverse=True)
        
        # Return top 3 domains
        return [{"key": domain_key, "name": info["name"], "score": info["score"]} 
                for domain_key, info in sorted_domains[:3]]
    
    def _identify_contradictions(self, problem_statement):
        """Identify potential technical contradictions in the problem."""
        # Common contradiction patterns
        contradiction_patterns = [
            (r'(increase|improve|enhance|maximize).*but.*(decrease|reduce|minimize)', "Improvement vs. Reduction"),
            (r'(faster|quicker|speed).*but.*(quality|precision|accuracy)', "Speed vs. Quality"),
            (r'(stronger|durable|robust).*but.*(lighter|smaller|less)', "Strength vs. Weight"),
            (r'(simple|easy|user-friendly).*but.*(feature|function|capability)', "Simplicity vs. Functionality"),
            (r'(automated|automatic).*but.*(control|customize|flexible)', "Automation vs. Flexibility"),
            (r'(energy|power|force).*but.*(efficiency|consumption|waste)', "Power vs. Efficiency"),
            (r'(cost|price|expense).*but.*(quality|performance|durability)', "Cost vs. Quality"),
            (r'(stable|consistent|reliable).*but.*(adaptable|versatile|flexible)', "Stability vs. Adaptability"),
            (r'(production|manufacturing|output).*but.*(quality|precision|accuracy)', "Volume vs. Quality"),
            (r'(universal|general).*but.*(specific|specialized|custom)', "Universality vs. Specialization"),
        ]
        
        # Check for contradiction patterns
        contradictions = []
        for pattern, name in contradiction_patterns:
            if re.search(pattern, problem_statement, re.IGNORECASE):
                contradictions.append(name)
        
        return contradictions
    
    def _suggest_triz_principles(self, contradiction):
        """Suggest TRIZ principles for a specific contradiction."""
        # Simplified TRIZ contradiction matrix (minimal version)
        contradiction_matrix = {
            "Improvement vs. Reduction": [1, 2, 13, 15, 35],  # Segmentation, Taking Out, The Other Way Round, Dynamics, Parameter Changes
            "Speed vs. Quality": [10, 21, 28, 32, 37],  # Preliminary Action, Skipping, Mechanics Substitution, Color Changes, Thermal Expansion
            "Strength vs. Weight": [1, 8, 15, 29, 40],  # Segmentation, Anti-Weight, Dynamics, Pneumatics and Hydraulics, Composite Materials
            "Simplicity vs. Functionality": [6, 13, 15, 25, 35],  # Universality, The Other Way Round, Dynamics, Self-Service, Parameter Changes
            "Automation vs. Flexibility": [15, 17, 23, 24, 35],  # Dynamics, Another Dimension, Feedback, Intermediary, Parameter Changes
            "Power vs. Efficiency": [6, 18, 19, 36, 38],  # Universality, Mechanical Vibration, Periodic Action, Phase Transitions, Strong Oxidants
            "Cost vs. Quality": [10, 13, 27, 29, 35],  # Preliminary Action, The Other Way Round, Cheap Short-Living Objects, Pneumatics and Hydraulics, Parameter Changes
            "Stability vs. Adaptability": [3, 15, 19, 23, 40],  # Local Quality, Dynamics, Periodic Action, Feedback, Composite Materials
            "Volume vs. Quality": [5, 10, 15, 34, 35],  # Merging, Preliminary Action, Dynamics, Discarding and Recovering, Parameter Changes
            "Universality vs. Specialization": [1, 3, 6, 15, 17],  # Segmentation, Local Quality, Universality, Dynamics, Another Dimension
        }
        
        # Get principle IDs for the contradiction
        principle_ids = contradiction_matrix.get(contradiction, [])
        
        # Get principle details
        suggested_principles = []
        for principle in self.triz_principles:
            if principle["id"] in principle_ids:
                suggested_principles.append(principle)
        
        return suggested_principles
    
    def _suggest_general_triz_principles(self, problem_statement, keywords):
        """Suggest general TRIZ principles based on problem keywords."""
        # Score each principle based on keyword matches
        principle_scores = {}
        
        for principle in self.triz_principles:
            score = 0
            principle_text = principle["name"].lower() + " " + principle["description"].lower()
            
            for keyword in keywords:
                if keyword in principle_text:
                    score += 1
            
            if score > 0:
                principle_scores[principle["id"]] = score
        
        # Sort principles by score
        sorted_principles = sorted(principle_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top 5 principles
        top_principle_ids = [principle_id for principle_id, score in sorted_principles[:5]]
        
        # Get principle details
        suggested_principles = []
        for principle in self.triz_principles:
            if principle["id"] in top_principle_ids:
                suggested_principles.append(principle)
        
        return suggested_principles
    
    def _suggest_biomimicry_principles(self, problem_statement, keywords):
        """Suggest biomimicry principles based on problem keywords."""
        # Score each principle based on keyword matches
        principle_scores = {}
        
        for i, principle in enumerate(self.biomimicry_principles):
            score = 0
            principle_text = principle["name"].lower() + " " + principle["description"].lower()
            
            for keyword in keywords:
                if keyword in principle_text:
                    score += 1
            
            if score > 0:
                principle_scores[i] = score
        
        # Sort principles by score
        sorted_principles = sorted(principle_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get top 3 principles
        top_principle_indices = [index for index, score in sorted_principles[:3]]
        
        # Get principle details
        suggested_principles = []
        for i, principle in enumerate(self.biomimicry_principles):
            if i in top_principle_indices:
                suggested_principles.append(principle)
        
        # If no principles match, suggest some general ones
        if not suggested_principles:
            suggested_principles = random.sample(self.biomimicry_principles, 3)
        
        return suggested_principles
    
    def _apply_first_principles(self, problem_statement):
        """Apply first principles thinking to the problem."""
        # Create a structured analysis using first principles
        analysis = []
        
        # For each first principle, generate an analysis point
        for principle in self.first_principles:
            if principle["name"] == "Questioning Assumptions":
                analysis.append({
                    "principle": principle["name"],
                    "description": principle["description"],
                    "application": "Identify and challenge key assumptions in the problem statement.",
                    "questions": [
                        "What assumptions underlie this problem?",
                        "Which of these assumptions could be challenged?",
                        "What if the opposite of these assumptions were true?"
                    ]
                })
            elif principle["name"] == "Breaking Down Complexities":
                analysis.append({
                    "principle": principle["name"],
                    "description": principle["description"],
                    "application": "Decompose the problem into its most basic elements.",
                    "questions": [
                        "What are the fundamental components of this problem?",
                        "How do these components interact?",
                        "Which components are essential vs. incidental?"
                    ]
                })
            elif principle["name"] == "Identifying Fundamental Truths":
                analysis.append({
                    "principle": principle["name"],
                    "description": principle["description"],
                    "application": "Identify basic truths or physical laws that govern this problem.",
                    "questions": [
                        "What physical laws or fundamental truths apply here?",
                        "What are the immutable constraints?",
                        "What elements cannot be changed due to physical laws?"
                    ]
                })
            elif principle["name"] == "Reasoning from First Principles":
                analysis.append({
                    "principle": principle["name"],
                    "description": principle["description"],
                    "application": "Begin from fundamentals rather than reasoning by analogy.",
                    "questions": [
                        "How would we solve this if no previous solutions existed?",
                        "What's the most direct path from fundamentals to solution?",
                        "Can we rebuild the solution from scratch based on first principles?"
                    ]
                })
            elif principle["name"] == "Seeking Causal Relationships":
                analysis.append({
                    "principle": principle["name"],
                    "description": principle["description"],
                    "application": "Identify true cause-effect relationships in the problem.",
                    "questions": [
                        "What are the true causes of the problem?",
                        "Are there deeper causes behind the apparent ones?",
                        "Which causes would most effectively address when developing solutions?"
                    ]
                })
        
        return analysis
    
    def _generate_solution_directions(self, problem_statement, domains, triz_suggestions, biomimicry_suggestions):
        """Generate potential solution directions based on analysis."""
        solution_directions = []
        
        # Generate domain-based solutions
        for domain in domains:
            domain_info = self.technology_domains.get(domain["key"])
            if domain_info:
                # Select random exemplars and trends from the domain
                exemplars = random.sample(domain_info["exemplars"], min(2, len(domain_info["exemplars"])))
                trends = random.sample(domain_info["trend_keywords"], min(2, len(domain_info["trend_keywords"])))
                
                solution_directions.append({
                    "approach": f"{domain_info['name']} Approach",
                    "description": f"Apply advances from {domain_info['name']} to solve the problem.",
                    "examples": exemplars,
                    "trends": trends
                })
        
        # Generate TRIZ-based solutions
        if isinstance(triz_suggestions, list) and triz_suggestions:
            # Handle case when triz_suggestions is a list of dictionaries with a 'principles' key
            if "principles" in triz_suggestions[0]:
                for suggestion in triz_suggestions:
                    principles = suggestion["principles"]
                    if principles:
                        principle = principles[0]  # Take the first principle
                        solution_directions.append({
                            "approach": f"TRIZ: {principle['name']}",
                            "description": principle["description"],
                            "contradiction": suggestion.get("contradiction", "General application")
                        })
            # Handle case when triz_suggestions is a list of principles directly
            else:
                for principle in triz_suggestions[:2]:  # Take first two principles
                    solution_directions.append({
                        "approach": f"TRIZ: {principle['name']}",
                        "description": principle["description"],
                        "contradiction": "General application"
                    })
        
        # Generate biomimicry-based solutions
        for principle in biomimicry_suggestions[:2]:  # Take first two principles
            solution_directions.append({
                "approach": f"Biomimicry: {principle['name']}",
                "description": principle["description"],
                "inspiration": self._suggest_biological_example(principle["name"])
            })
        
        # Generate combined/hybrid approaches
        if len(solution_directions) >= 2:
            # Take two random solution directions and combine them
            indices = random.sample(range(len(solution_directions)), 2)
            dir1 = solution_directions[indices[0]]
            dir2 = solution_directions[indices[1]]
            
            solution_directions.append({
                "approach": f"Hybrid: {dir1['approach']} + {dir2['approach']}",
                "description": f"Combine elements from both {dir1['approach']} and {dir2['approach']} to create a novel solution.",
                "elements": [
                    f"From {dir1['approach']}: {dir1.get('description', 'Approach elements')}",
                    f"From {dir2['approach']}: {dir2.get('description', 'Approach elements')}"
                ]
            })
        
        return solution_directions
    
    def _suggest_biological_example(self, principle_name):
        """Suggest biological examples for biomimicry principles."""
        biological_examples = {
            "Resource Efficiency": [
                "Honeycomb structure in beehives optimizes material use while maximizing strength",
                "Spider silk combines extraordinary strength and elasticity with minimal material",
                "Bamboo's hollow structure provides excellent strength-to-weight ratio"
            ],
            "Cyclic Processing": [
                "Forest ecosystems where decomposing matter becomes nutrients for new growth",
                "Nitrogen fixation by leguminous plants that enrich soil for other plants",
                "Microbial communities in digestive systems breaking down complex materials"
            ],
            "Solar Transformation": [
                "Photosynthesis in plants converting sunlight to chemical energy",
                "Light-harvesting complexes in algae operating at quantum efficiency",
                "Heliotropism in sunflowers tracking the sun to maximize energy capture"
            ],
            "Dynamic Equilibrium": [
                "Thermoregulation in mammals maintaining constant body temperature",
                "Predator-prey population dynamics maintaining ecological balance",
                "Homeostasis mechanisms in biological systems"
            ],
            "Evolutionary Development": [
                "Adaptive radiation in Darwin's finches developing specialized beaks",
                "Convergent evolution of streamlined shapes in marine animals",
                "Co-evolution between flowers and pollinators"
            ],
            "Resilience through Diversity": [
                "Prairie ecosystems with diverse plant species resisting drought and disease",
                "Coral reef communities with redundant species fulfilling similar functions",
                "Human immune system with diverse antibody production capabilities"
            ],
            "Local Adaptation": [
                "Cacti with specialized water storage and reduced transpiration for desert environments",
                "Polar bears with adaptations for arctic conditions",
                "Deep sea creatures adapted to high pressure environments"
            ],
            "Shape Complementarity": [
                "Bird wing shapes optimized for different flight requirements",
                "Gecko foot structure enabling adhesion through van der Waals forces",
                "Nautilus shell logarithmic spiral providing strength and growth capability"
            ],
            "Self-Organization": [
                "Termite mounds creating sophisticated climate-controlled structures",
                "Starling murmurations forming complex coordinated patterns",
                "Cellular differentiation in embryonic development"
            ],
            "Self-Healing": [
                "Lizard tail regeneration after autotomy",
                "Plant tissue repair after damage",
                "Human skin wound healing processes"
            ],
            "Sensing and Response": [
                "Venus flytrap rapid closure mechanism triggered by touch sensors",
                "Bat echolocation for navigation and hunting",
                "Cephalopod chromatophores changing color and pattern for camouflage"
            ],
            "Multi-Functionality": [
                "Elephant trunk functioning as nose, hand, snorkel, and communication device",
                "Tree bark providing protection, transport, and sometimes photosynthesis",
                "Bird feathers providing insulation, waterproofing, display, and flight capability"
            ]
        }
        
        examples = biological_examples.get(principle_name, ["Natural systems demonstrating this principle"])
        return random.choice(examples)
    
    def generate_invention(self, problem_statement, domain=None, approach=None):
        """Generate a detailed invention concept to solve a specific problem.
        
        Args:
            problem_statement: Description of the problem to be solved
            domain: Optional specific domain for the invention
            approach: Optional specific approach or principle to apply
            
        Returns:
            Dictionary with invention details
        """
        try:
            logger.info(f"Generating invention for: {problem_statement}")
            
            # First analyze the problem
            analysis = self.analyze_problem(problem_statement, domain)
            
            # Determine the domain
            if domain:
                invention_domain = domain
            elif analysis.get("relevant_domains"):
                invention_domain = analysis["relevant_domains"][0]["name"]
            else:
                invention_domain = "General Technology"
            
            # Determine the approach
            if approach:
                invention_approach = approach
            elif analysis.get("solution_directions"):
                invention_approach = analysis["solution_directions"][0]["approach"]
            else:
                # Default approach
                rand_triz = random.choice(self.triz_principles)
                invention_approach = f"TRIZ: {rand_triz['name']}"
            
            # Generate invention components
            invention_name = self._generate_invention_name(problem_statement, invention_domain)
            invention_concept = self._generate_invention_concept(problem_statement, analysis, invention_domain, invention_approach)
            invention_components = self._generate_invention_components(invention_concept)
            invention_advantages = self._generate_invention_advantages(invention_concept, problem_statement)
            invention_limitations = self._generate_invention_limitations(invention_concept)
            implementation_challenges = self._generate_implementation_challenges(invention_concept, invention_components)
            future_improvements = self._generate_future_improvements(invention_concept, implementation_challenges)
            market_potential = self._evaluate_market_potential(invention_concept, invention_advantages)
            
            # Get current date for the invention
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Random TRL level with bias toward lower TRLs (more conceptual)
            technology_readiness_level = random.choices(
                range(1, 10),
                weights=[20, 20, 15, 15, 10, 8, 5, 4, 3],  # Higher weights for lower TRLs
                k=1
            )[0]
            
            return {
                "invention_name": invention_name,
                "problem_addressed": problem_statement,
                "domain": invention_domain,
                "approach": invention_approach,
                "concept_date": current_date,
                "technology_readiness_level": technology_readiness_level,
                "concept_description": invention_concept,
                "key_components": invention_components,
                "advantages": invention_advantages,
                "limitations": invention_limitations,
                "implementation_challenges": implementation_challenges,
                "future_improvements": future_improvements,
                "market_potential": market_potential
            }
            
        except Exception as e:
            logger.error(f"Error generating invention: {e}")
            return {"error": f"Could not generate invention: {e}"}
    
    def _generate_invention_name(self, problem_statement, domain):
        """Generate a name for the invention."""
        # Extract key terms from problem statement
        key_terms = self._extract_keywords(problem_statement)
        
        # Domain abbreviations
        domain_prefixes = {
            "Artificial Intelligence": ["AI", "Neuro", "Cognitive", "Smart", "Intelligent"],
            "Biotechnology": ["Bio", "Gen", "Cell", "Medi", "Vita"],
            "Energy Technology": ["Ener", "Power", "Volt", "Thermo", "Flux"],
            "Materials Science": ["Nano", "Poly", "Flex", "Struc", "Composite"],
            "Robotics & Automation": ["Robo", "Auto", "Mech", "Bot", "Kinetic"],
            "Advanced Computing": ["Quantum", "Compute", "Process", "Logic", "Data"],
            "Advanced Manufacturing": ["Fab", "Form", "Print", "Construct", "Build"],
            "Transportation": ["Mobil", "Trans", "Move", "Vector", "Glide"],
            "Healthcare Technology": ["Health", "Med", "Vita", "Care", "Therapy"],
            "Environmental Technology": ["Eco", "Sustain", "Enviro", "Geo", "Clean"]
        }
        
        # Get domain-specific prefixes
        prefixes = domain_prefixes.get(domain, ["Tech", "Nova", "Sys", "Pro", "Dyna"])
        
        # Generate name formats
        formats = [
            f"{random.choice(prefixes)}{random.choice(key_terms).capitalize()}",
            f"{random.choice(prefixes)}-{random.choice(key_terms).capitalize()}",
            f"{random.choice(key_terms).capitalize()}{random.choice(prefixes)}",
            f"{random.choice(prefixes)}{random.choice(key_terms).capitalize()} System",
            f"The {random.choice(key_terms).capitalize()} {random.choice(prefixes)}",
            f"{random.choice(prefixes)} {random.choice(key_terms).capitalize()}",
        ]
        
        return random.choice(formats)
    
    def _generate_invention_concept(self, problem, analysis, domain, approach):
        """Generate a concept description for the invention."""
        # Create a structured concept description
        concept = "A novel solution that "
        
        # Add problem-specific details
        if "reduce" in problem.lower() or "minimize" in problem.lower() or "decrease" in problem.lower():
            concept += f"significantly reduces the {random.choice(['challenges', 'issues', 'problems', 'limitations'])} associated with "
        elif "improve" in problem.lower() or "enhance" in problem.lower() or "increase" in problem.lower():
            concept += f"substantially improves the {random.choice(['effectiveness', 'efficiency', 'performance', 'capability'])} of "
        elif "prevent" in problem.lower() or "avoid" in problem.lower():
            concept += f"effectively prevents {random.choice(['issues', 'problems', 'failures', 'complications'])} in "
        else:
            concept += f"addresses the fundamental challenges of "
        
        # Add domain-specific terminology
        domain_terms = {
            "Artificial Intelligence": ["neural processing", "intelligent algorithms", "cognitive systems", "machine learning models", "predictive analytics"],
            "Biotechnology": ["biological processes", "cellular mechanisms", "genetic engineering", "biomolecular interactions", "enzymatic reactions"],
            "Energy Technology": ["energy conversion", "power generation", "energy storage", "thermal management", "renewable systems"],
            "Materials Science": ["material properties", "structural integrity", "molecular composition", "surface interactions", "composite structures"],
            "Robotics & Automation": ["autonomous systems", "mechanical actuation", "sensor integration", "control mechanisms", "robotic interfaces"],
            "Advanced Computing": ["computational processes", "data processing", "information systems", "quantum operations", "algorithmic functions"],
            "Advanced Manufacturing": ["fabrication methods", "production systems", "additive processes", "material forming", "assembly operations"],
            "Transportation": ["mobility systems", "propulsion mechanisms", "vehicle dynamics", "navigation methods", "transit operations"],
            "Healthcare Technology": ["medical procedures", "diagnostic methods", "treatment protocols", "patient care", "therapeutic applications"],
            "Environmental Technology": ["ecological systems", "sustainability measures", "environmental processes", "resource management", "pollution control"]
        }
        
        # Select domain terms
        selected_terms = domain_terms.get(domain, ["technological systems", "processes", "operations", "mechanisms", "functions"])
        concept += f"{random.choice(selected_terms)} "
        
        # Add approach-specific methodology
        if "TRIZ" in approach:
            # Extract the principle name
            principle_name = approach.replace("TRIZ: ", "")
            concept += f"through the application of the {principle_name} principle, which "
            
            # Add principle-specific language
            if "Segmentation" in principle_name:
                concept += "divides the system into independent functional elements that "
            elif "Taking Out" in principle_name:
                concept += "isolates essential components while removing problematic elements to "
            elif "Local Quality" in principle_name:
                concept += "creates non-uniform structures optimized for specific functions to "
            elif "Asymmetry" in principle_name:
                concept += "employs asymmetrical design elements that "
            elif "Merging" in principle_name:
                concept += "combines previously separate operations or components to "
            elif "Universality" in principle_name:
                concept += "creates multifunctional elements that "
            elif "Nested Doll" in principle_name:
                concept += "uses nested structures where components contain or pass through each other to "
            elif "Dynamics" in principle_name:
                concept += "incorporates adaptive characteristics that "
            else:
                concept += "implements innovative engineering principles that "
        elif "Biomimicry" in approach:
            # Extract the principle name
            principle_name = approach.replace("Biomimicry: ", "")
            concept += f"using biological inspiration from nature's {principle_name.lower()} strategies, which "
        elif "Hybrid" in approach:
            concept += "through a hybrid approach combining multiple methodologies that "
        else:
            concept += "using an innovative approach that "
        
        # Add key functions
        concept += f"{random.choice(['effectively', 'efficiently', 'precisely', 'elegantly', 'comprehensively'])} "
        concept += f"{random.choice(['solves', 'addresses', 'resolves', 'overcomes', 'mitigates'])} "
        concept += f"the {random.choice(['core', 'fundamental', 'central', 'key', 'essential'])} "
        concept += f"{random.choice(['challenge', 'issue', 'problem', 'limitation', 'constraint'])}."
        
        # Add secondary benefits
        secondary_benefits = [
            f"Additionally, the invention {random.choice(['provides', 'offers', 'delivers', 'enables'])} {random.choice(['improved', 'enhanced', 'superior', 'better'])} {random.choice(['efficiency', 'performance', 'reliability', 'effectiveness', 'usability'])}.",
            f"The solution also {random.choice(['reduces', 'minimizes', 'decreases', 'lowers'])} {random.choice(['costs', 'complexity', 'maintenance requirements', 'environmental impact', 'energy consumption'])}.",
            f"Furthermore, the invention {random.choice(['can be adapted for', 'is applicable to', 'can extend to', 'is suitable for'])} {random.choice(['multiple use cases', 'various applications', 'different environments', 'diverse scenarios', 'broader contexts'])}."
        ]
        
        concept += " " + random.choice(secondary_benefits)
        
        return concept
    
    def _generate_invention_components(self, invention_concept):
        """Generate key components of the invention."""
        # Extract potential component terms from the concept
        concept_words = set(re.findall(r'\b\w+\b', invention_concept.lower()))
        
        # Common component types
        component_types = [
            "System", "Module", "Interface", "Mechanism", "Processor",
            "Controller", "Sensor", "Actuator", "Framework", "Platform",
            "Network", "Algorithm", "Structure", "Layer", "Substrate",
            "Circuit", "Device", "Element", "Unit", "Array"
        ]
        
        # Common component functions
        component_functions = [
            "processing", "sensing", "monitoring", "controlling", "regulating",
            "transforming", "storing", "transmitting", "converting", "filtering",
            "analyzing", "learning", "adapting", "optimizing", "integrating",
            "coordinating", "executing", "managing", "distributing", "generating"
        ]
        
        # Common component modifiers
        component_modifiers = [
            "intelligent", "adaptive", "modular", "integrated", "advanced",
            "smart", "efficient", "high-performance", "sustainable", "scalable",
            "responsive", "distributed", "autonomous", "self-adjusting", "dynamic",
            "reconfigurable", "optimized", "enhanced", "next-generation", "innovative"
        ]
        
        # Generate components
        components = []
        used_types = set()
        used_functions = set()
        
        # Number of components to generate (3-6)
        num_components = random.randint(3, 6)
        
        for i in range(num_components):
            # Select component type (avoid repeats)
            available_types = [t for t in component_types if t not in used_types]
            if not available_types:
                available_types = component_types
            
            component_type = random.choice(available_types)
            used_types.add(component_type)
            
            # Select component function (avoid repeats)
            available_functions = [f for f in component_functions if f not in used_functions]
            if not available_functions:
                available_functions = component_functions
                
            component_function = random.choice(available_functions)
            used_functions.add(component_function)
            
            # Select modifier
            component_modifier = random.choice(component_modifiers)
            
            # Create component name
            component_name = f"{component_modifier.capitalize()} {component_function.capitalize()} {component_type}"
            
            # Create component description
            component_description = self._generate_component_description(component_type, component_function, component_modifier)
            
            # Add the component
            components.append({
                "name": component_name,
                "description": component_description,
                "key_function": f"{component_function.capitalize()}ing {random.choice(['data', 'inputs', 'signals', 'materials', 'energy', 'information'])}"
            })
        
        return components
    
    def _generate_component_description(self, component_type, component_function, component_modifier):
        """Generate a description for a component."""
        # Component purpose phrases
        purpose_phrases = [
            f"responsible for {component_function} operations",
            f"handles the {component_function} aspects of the system",
            f"manages {component_function} processes",
            f"executes {component_function} functions",
            f"performs {component_function} tasks"
        ]
        
        # Component characteristic phrases
        characteristic_phrases = [
            f"with {component_modifier} capabilities",
            f"utilizing {component_modifier} methodology",
            f"employing {component_modifier} techniques",
            f"featuring {component_modifier} design",
            f"through {component_modifier} mechanisms"
        ]
        
        # Component advantage phrases
        advantage_phrases = [
            f"to improve overall system efficiency",
            f"to enhance performance metrics",
            f"to optimize operational parameters",
            f"to maximize functional output",
            f"to reduce system constraints",
            f"to maintain operational stability",
            f"to ensure reliable functioning"
        ]
        
        # Create the description
        description = f"A {component_type.lower()} {random.choice(purpose_phrases)} {random.choice(characteristic_phrases)} {random.choice(advantage_phrases)}."
        
        return description
    
    def _generate_invention_advantages(self, invention_concept, problem_statement):
        """Generate advantages of the invention."""
        # Common advantage categories
        advantage_categories = [
            "Performance", "Efficiency", "Cost", "Usability", "Reliability",
            "Sustainability", "Adaptability", "Scalability", "Safety", "Integration"
        ]
        
        # Select a subset of categories (3-5)
        selected_categories = random.sample(advantage_categories, random.randint(3, 5))
        
        # Generate advantages for each category
        advantages = []
        
        for category in selected_categories:
            if category == "Performance":
                improvement = random.choice(["enhanced", "superior", "improved", "higher", "better"])
                metric = random.choice(["speed", "throughput", "accuracy", "precision", "output quality"])
                magnitude = random.choice(["significant", "substantial", "notable", "measurable", "marked"])
                advantage = f"{improvement.capitalize()} {metric} with {magnitude} gains over conventional solutions."
                
            elif category == "Efficiency":
                resource = random.choice(["energy", "time", "material", "computational", "operational"])
                reduction = random.choice(["reduced", "decreased", "lower", "minimized", "optimized"])
                percentage = random.randint(15, 50)
                advantage = f"{reduction.capitalize()} {resource} consumption by approximately {percentage}% compared to traditional approaches."
                
            elif category == "Cost":
                aspect = random.choice(["manufacturing", "operational", "maintenance", "implementation", "lifecycle"])
                savings = random.choice(["savings", "reduction", "efficiency", "optimization", "advantage"])
                factor = random.choice(["significantly lower", "more economical", "cost-effective", "budget-friendly", "financially optimized"])
                advantage = f"{aspect.capitalize()} cost {savings} making the solution {factor} than alternatives."
                
            elif category == "Usability":
                interface = random.choice(["user interface", "control system", "operational paradigm", "interaction model", "user experience"])
                quality = random.choice(["intuitive", "simplified", "user-friendly", "accessible", "streamlined"])
                benefit = random.choice(["reduces learning curve", "minimizes training requirements", "enhances user adoption", "improves user satisfaction", "enables broader usability"])
                advantage = f"{quality.capitalize()} {interface} that {benefit}."
                
            elif category == "Reliability":
                feature = random.choice(["design", "architecture", "operational parameters", "functional components", "system integration"])
                property = random.choice(["robust", "resilient", "fault-tolerant", "stable", "consistent"])
                condition = random.choice(["varying conditions", "edge cases", "challenging environments", "high-stress scenarios", "extended operation"])
                advantage = f"{property.capitalize()} {feature} ensuring dependable performance under {condition}."
                
            elif category == "Sustainability":
                impact = random.choice(["environmental footprint", "resource utilization", "waste generation", "emissions", "energy requirements"])
                benefit = random.choice(["reduced", "minimized", "decreased", "lowered", "optimized"])
                approach = random.choice(["eco-friendly materials", "efficient processes", "recyclable components", "renewable resources", "circular design principles"])
                advantage = f"{benefit.capitalize()} {impact} through the use of {approach}."
                
            elif category == "Adaptability":
                capability = random.choice(["configurable parameters", "modular architecture", "flexible framework", "adjustable components", "customizable settings"])
                adaptation = random.choice(["adapt to changing requirements", "accommodate various use cases", "serve diverse applications", "meet evolving needs", "function in different contexts"])
                advantage = f"{capability.capitalize()} allowing the system to {adaptation}."
                
            elif category == "Scalability":
                aspect = random.choice(["design", "architecture", "implementation", "methodology", "approach"])
                scale = random.choice(["scaled up or down", "expanded as needed", "adjusted to requirements", "sized appropriately", "optimized for different scales"])
                context = random.choice(["without performance degradation", "while maintaining efficiency", "with minimal additional resources", "preserving core functionality", "with proportional resource utilization"])
                advantage = f"Scalable {aspect} that can be {scale} {context}."
                
            elif category == "Safety":
                feature = random.choice(["protective measures", "safety protocols", "fail-safe mechanisms", "risk mitigation strategies", "security features"])
                hazard = random.choice(["accidents", "failures", "unauthorized access", "operational risks", "safety incidents"])
                advantage = f"Enhanced {feature} significantly reducing the likelihood of {hazard}."
                
            elif category == "Integration":
                compatibility = random.choice(["seamless integration", "easy interoperability", "compatible interfaces", "straightforward connectivity", "plug-and-play functionality"])
                systems = random.choice(["existing systems", "legacy infrastructure", "complementary technologies", "broader ecosystems", "related platforms"])
                advantage = f"{compatibility.capitalize()} with {systems} reducing implementation barriers."
                
            advantages.append({
                "category": category,
                "description": advantage
            })
        
        return advantages
    
    def _generate_invention_limitations(self, invention_concept):
        """Generate limitations of the invention."""
        # Common limitation categories
        limitation_categories = [
            "Technical Constraints", "Resource Requirements", "Implementation Complexity", 
            "Compatibility Issues", "Regulatory Considerations", "Performance Trade-offs"
        ]
        
        # Select a subset of categories (2-3)
        selected_categories = random.sample(limitation_categories, random.randint(2, 3))
        
        # Generate limitations for each category
        limitations = []
        
        for category in selected_categories:
            if category == "Technical Constraints":
                constraint = random.choice([
                    "May require specialized expertise for optimal configuration and tuning.",
                    "Performance may vary depending on specific operational parameters.",
                    "Current technology readiness level limits immediate widespread deployment.",
                    "Technical complexity may require additional documentation and training.",
                    "Some edge cases may not be fully addressed by the current implementation."
                ])
                
            elif category == "Resource Requirements":
                constraint = random.choice([
                    "Initial setup requires investment in supporting infrastructure.",
                    "Implementation may necessitate allocation of dedicated resources.",
                    "Optimal performance requires specific computational or material resources.",
                    "Deployment at scale may entail significant resource planning.",
                    "Maintenance and updates require ongoing resource commitment."
                ])
                
            elif category == "Implementation Complexity":
                constraint = random.choice([
                    "Integration with certain existing systems may pose challenges.",
                    "Implementation timeline depends on existing infrastructure compatibility.",
                    "Complex deployment process may require specialized expertise.",
                    "Customization for specific use cases adds implementation complexity.",
                    "Full feature utilization requires careful implementation planning."
                ])
                
            elif category == "Compatibility Issues":
                constraint = random.choice([
                    "May not be fully compatible with all legacy systems without adaptation.",
                    "Integration with certain proprietary technologies may require additional work.",
                    "Specific operational environments may require customized compatibility solutions.",
                    "Standards compliance across all potential integration points is not yet established.",
                    "Some third-party components may have limited compatibility."
                ])
                
            elif category == "Regulatory Considerations":
                constraint = random.choice([
                    "Compliance with evolving regulatory frameworks may require ongoing adjustments.",
                    "Certification processes in certain domains may extend implementation timelines.",
                    "Regulatory requirements vary by jurisdiction, potentially affecting deployment scope.",
                    "Some applications may require specific regulatory approvals or certifications.",
                    "Emerging regulatory standards may necessitate future adaptations."
                ])
                
            elif category == "Performance Trade-offs":
                constraint = random.choice([
                    "Optimizing for certain performance metrics may affect others.",
                    "Maximum efficiency may require compromises in other operational areas.",
                    "Balancing performance, cost, and complexity presents inherent trade-offs.",
                    "Certain advanced features may impact overall system simplicity.",
                    "Performance optimization for specific use cases may limit generalizability."
                ])
                
            limitations.append({
                "category": category,
                "description": constraint
            })
        
        return limitations
    
    def _generate_implementation_challenges(self, invention_concept, components):
        """Generate implementation challenges for the invention."""
        # Common challenge types
        challenge_types = [
            "Technical", "Integration", "Manufacturing", "Market", "Regulatory", "Resource"
        ]
        
        # Select a subset of types (2-4)
        selected_types = random.sample(challenge_types, random.randint(2, 4))
        
        # Generate challenges for each type
        challenges = []
        
        for challenge_type in selected_types:
            if challenge_type == "Technical":
                component = random.choice(components)["name"] if components else "System component"
                challenge = random.choice([
                    f"Optimizing the {component} for consistent performance across varied operating conditions.",
                    f"Ensuring reliability of the {component} under extended use scenarios.",
                    f"Refining the {component} to achieve target performance specifications.",
                    f"Developing robust testing methodologies for the {component}.",
                    f"Addressing technical limitations in current iterations of the {component}."
                ])
                
            elif challenge_type == "Integration":
                challenge = random.choice([
                    "Ensuring seamless integration with existing technological ecosystems.",
                    "Developing standardized interfaces for system interoperability.",
                    "Creating comprehensive documentation for integration processes.",
                    "Establishing effective communication protocols between system components.",
                    "Managing complexity in multi-system integration scenarios."
                ])
                
            elif challenge_type == "Manufacturing":
                challenge = random.choice([
                    "Scaling production processes while maintaining quality standards.",
                    "Sourcing specialized materials or components cost-effectively.",
                    "Establishing efficient assembly and quality control procedures.",
                    "Developing manufacturing partnerships for specialized components.",
                    "Optimizing production efficiency without compromising quality."
                ])
                
            elif challenge_type == "Market":
                challenge = random.choice([
                    "Communicating value proposition effectively to target market segments.",
                    "Differentiating from existing solutions in the competitive landscape.",
                    "Developing appropriate pricing strategies for market penetration.",
                    "Building awareness and acceptance among potential early adopters.",
                    "Creating effective demonstration procedures for complex functionality."
                ])
                
            elif challenge_type == "Regulatory":
                challenge = random.choice([
                    "Navigating applicable regulatory frameworks across different jurisdictions.",
                    "Obtaining necessary certifications and approvals for commercial deployment.",
                    "Maintaining compliance with evolving standards and regulations.",
                    "Documenting safety and performance characteristics for regulatory submissions.",
                    "Addressing intellectual property considerations and patent strategies."
                ])
                
            elif challenge_type == "Resource":
                challenge = random.choice([
                    "Securing necessary funding for development through commercialization phases.",
                    "Assembling team with appropriate technical and domain expertise.",
                    "Allocating resources effectively across development priorities.",
                    "Establishing partnerships for complementary capabilities or resources.",
                    "Balancing resource allocation between current development and future innovation."
                ])
                
            challenges.append({
                "type": challenge_type,
                "description": challenge
            })
        
        return challenges
    
    def _generate_future_improvements(self, invention_concept, implementation_challenges):
        """Generate potential future improvements for the invention."""
        # Common improvement categories
        improvement_categories = [
            "Performance Enhancement", "Feature Expansion", "Cost Reduction", 
            "Usability Improvement", "Integration Advancement", "Sustainability Upgrade"
        ]
        
        # Select a subset of categories (2-4)
        selected_categories = random.sample(improvement_categories, random.randint(2, 4))
        
        # Generate improvements for each category
        improvements = []
        
        for category in selected_categories:
            if category == "Performance Enhancement":
                improvement = random.choice([
                    "Optimization of core algorithms to improve processing efficiency.",
                    "Enhanced computational methods for higher accuracy and precision.",
                    "Refined materials or components to increase operational performance.",
                    "Advanced calibration techniques for improved system responsiveness.",
                    "Streamlined data processing for reduced latency and faster response times."
                ])
                
            elif category == "Feature Expansion":
                improvement = random.choice([
                    "Addition of adaptive learning capabilities for autonomous optimization.",
                    "Integration of predictive analytics for anticipatory functionality.",
                    "Expansion of compatible platforms and environments.",
                    "Development of specialized modules for niche applications.",
                    "Implementation of extended sensing or monitoring capabilities."
                ])
                
            elif category == "Cost Reduction":
                improvement = random.choice([
                    "Redesign of key components for more cost-effective manufacturing.",
                    "Material substitution with equivalent performance but lower cost.",
                    "Streamlined assembly processes to reduce production expenses.",
                    "Simplified design elements while maintaining core functionality.",
                    "Optimization of resource utilization for reduced operational costs."
                ])
                
            elif category == "Usability Improvement":
                improvement = random.choice([
                    "Enhanced user interface for more intuitive operation.",
                    "Simplified configuration and setup procedures.",
                    "Development of comprehensive user documentation and guides.",
                    "Implementation of automated calibration and self-adjustment features.",
                    "Creation of user-friendly diagnostic and maintenance tools."
                ])
                
            elif category == "Integration Advancement":
                improvement = random.choice([
                    "Development of additional connectivity options for broader compatibility.",
                    "Creation of standardized APIs for third-party integrations.",
                    "Implementation of plug-and-play functionality for easier deployment.",
                    "Enhanced interoperability with complementary systems and platforms.",
                    "Development of integration toolkits for common environments."
                ])
                
            elif category == "Sustainability Upgrade":
                improvement = random.choice([
                    "Incorporation of more environmentally friendly materials and processes.",
                    "Optimization of energy efficiency in operation and standby modes.",
                    "Implementation of recyclable or biodegradable components where possible.",
                    "Reduction of resource requirements through design optimization.",
                    "Development of extended product lifecycle through modular upgradeability."
                ])
                
            improvements.append({
                "category": category,
                "description": improvement
            })
        
        return improvements
    
    def _evaluate_market_potential(self, invention_concept, advantages):
        """Evaluate the market potential of the invention."""
        # Market sectors
        market_sectors = [
            "Industrial Manufacturing", "Healthcare", "Consumer Electronics", 
            "Transportation", "Energy", "Agriculture", "Construction", 
            "Telecommunications", "Defense", "Environmental Services"
        ]
        
        # Select primary and secondary sectors
        primary_sector = random.choice(market_sectors)
        remaining_sectors = [s for s in market_sectors if s != primary_sector]
        secondary_sectors = random.sample(remaining_sectors, random.randint(1, 3))
        
        # Adoption timeline options
        adoption_timelines = ["Near-term (1-2 years)", "Mid-term (3-5 years)", "Long-term (5+ years)"]
        adoption_timeline = random.choice(adoption_timelines)
        
        # Market size qualifiers
        market_size_qualifiers = ["emerging", "growing", "established", "substantial", "significant"]
        market_size_qualifier = random.choice(market_size_qualifiers)
        
        # Growth potential qualifiers
        growth_qualifiers = ["steady", "promising", "strong", "rapid", "exponential"]
        growth_qualifier = random.choice(growth_qualifiers)
        
        # Generate random market size figures (billions)
        starting_market = random.uniform(0.5, 10.0)
        growth_rate = random.uniform(5.0, 25.0)
        five_year_market = starting_market * (1 + growth_rate/100)**5
        
        # Create market assessment
        market_assessment = {
            "primary_sector": primary_sector,
            "secondary_sectors": secondary_sectors,
            "adoption_timeline": adoption_timeline,
            "market_description": f"The invention addresses a {market_size_qualifier} market with {growth_qualifier} growth potential.",
            "market_size": {
                "current_estimate": f"${starting_market:.1f} billion",
                "growth_rate": f"{growth_rate:.1f}% annual growth",
                "five_year_projection": f"${five_year_market:.1f} billion"
            },
            "value_proposition": self._generate_value_proposition(advantages),
            "competitive_factors": self._generate_competitive_factors()
        }
        
        return market_assessment
    
    def _generate_value_proposition(self, advantages):
        """Generate a value proposition based on the invention's advantages."""
        # Extract advantage descriptions
        advantage_descriptions = [adv["description"] for adv in advantages] if advantages else []
        
        # Value proposition statement parts
        intro_phrases = [
            "Provides significant value through",
            "Delivers compelling advantages including",
            "Offers substantial benefits with",
            "Creates measurable value by providing",
            "Presents a strong value proposition with"
        ]
        
        # Generate value statement
        if advantage_descriptions:
            # Use actual advantages if available
            selected_advantages = random.sample(advantage_descriptions, min(2, len(advantage_descriptions)))
            value_statement = f"{random.choice(intro_phrases)} {selected_advantages[0]}"
            if len(selected_advantages) > 1:
                value_statement += f" Additionally, it {selected_advantages[1].lower()}"
        else:
            # Generate generic value statement
            value_factors = [
                "improved operational efficiency",
                "reduced implementation costs",
                "enhanced performance metrics",
                "streamlined processes",
                "superior user experience",
                "increased reliability",
                "better adaptability to changing needs"
            ]
            selected_factors = random.sample(value_factors, 2)
            value_statement = f"{random.choice(intro_phrases)} {selected_factors[0]} and {selected_factors[1]}."
        
        return value_statement
    
    def _generate_competitive_factors(self):
        """Generate competitive factors for market assessment."""
        # Competitive advantage factors
        competitive_factors = [
            {
                "factor": "Technological Differentiation",
                "description": random.choice([
                    "Proprietary technology creates significant barriers to entry.",
                    "Novel approach provides clear differentiation from existing solutions.",
                    "Unique technical characteristics offer competitive advantage.",
                    "Innovative methodology distinguishes from conventional approaches.",
                    "Advanced capabilities exceed current market offerings."
                ])
            },
            {
                "factor": "Market Positioning",
                "description": random.choice([
                    "Addresses underserved market segment with specific needs.",
                    "Targets growing market sector with increasing demand.",
                    "Positioned at intersection of multiple expanding markets.",
                    "Fills significant gap in current solution landscape.",
                    "Positioned as premium offering with demonstrable advantages."
                ])
            },
            {
                "factor": "Competitive Landscape",
                "description": random.choice([
                    "Limited direct competition in the specific solution space.",
                    "Existing solutions lack key capabilities offered by this invention.",
                    "Current alternatives require significant compromises or trade-offs.",
                    "Competitors focus on different aspects of the problem space.",
                    "Established solutions use fundamentally different approaches."
                ])
            }
        ]
        
        return competitive_factors
    
    def analyze_patent_landscape(self, invention_description, domain=None):
        """Analyze the patent landscape relevant to an invention concept.
        
        Args:
            invention_description: Description of the invention concept
            domain: Optional specific domain for the invention
            
        Returns:
            Dictionary with patent landscape analysis
        """
        try:
            logger.info(f"Analyzing patent landscape for: {invention_description}")
            
            # Extract keywords from invention description
            keywords = self._extract_keywords(invention_description)
            
            # Identify relevant domains
            if domain:
                domains = [domain]
            else:
                domains = self._identify_relevant_domains(invention_description, keywords)
            
            # Generate key technology areas
            tech_areas = self._generate_technology_areas(domains, keywords)
            
            # Generate patent trends
            patent_trends = self._generate_patent_trends(tech_areas)
            
            # Generate sample representative patents
            representative_patents = self._generate_representative_patents(tech_areas)
            
            # Generate patent strategies
            patent_strategies = self._generate_patent_strategies(tech_areas, patent_trends)
            
            # Generate visualization of technology clusters
            tech_cluster_visualization = self._generate_tech_cluster_visualization(tech_areas)
            
            return {
                "invention_description": invention_description,
                "relevant_domains": domains,
                "technology_areas": tech_areas,
                "patent_trends": patent_trends,
                "representative_patents": representative_patents,
                "patent_strategies": patent_strategies,
                "tech_cluster_visualization": tech_cluster_visualization
            }
            
        except Exception as e:
            logger.error(f"Error analyzing patent landscape: {e}")
            return {"error": f"Could not analyze patent landscape: {e}"}
    
    def _generate_technology_areas(self, domains, keywords):
        """Generate key technology areas for patent landscape analysis."""
        tech_areas = []
        
        # Use domains to identify technology areas
        for domain in domains:
            domain_name = domain["name"] if isinstance(domain, dict) else domain
            
            # Check if domain exists in technology domains
            domain_key = None
            domain_info = None
            for key, info in self.technology_domains.items():
                if info["name"] == domain_name:
                    domain_key = key
                    domain_info = info
                    break
            
            if domain_info:
                # Use subdomains as technology areas
                for subdomain in domain_info["subdomains"]:
                    tech_areas.append({
                        "name": subdomain,
                        "relevance_score": random.uniform(0.6, 0.95),  # Random relevance score
                        "keywords": random.sample(keywords + domain_info["trend_keywords"], min(5, len(keywords) + len(domain_info["trend_keywords"]))),
                        "patent_activity": self._generate_patent_activity()
                    })
            else:
                # Generate generic technology areas based on keywords
                for i in range(min(3, len(keywords))):
                    tech_areas.append({
                        "name": f"{keywords[i].capitalize()} Technologies",
                        "relevance_score": random.uniform(0.5, 0.9),
                        "keywords": random.sample(keywords, min(3, len(keywords))),
                        "patent_activity": self._generate_patent_activity()
                    })
        
        # Sort by relevance score
        tech_areas.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Take top 5 areas
        return tech_areas[:5]
    
    def _generate_patent_activity(self):
        """Generate patent activity metrics for a technology area."""
        # Random starting year between 2000 and 2015
        start_year = random.randint(2000, 2015)
        
        # Generate yearly filing counts
        yearly_filings = {}
        initial_filings = random.randint(50, 500)
        growth_rate = random.uniform(1.05, 1.25)  # 5% to 25% annual growth
        
        current_filings = initial_filings
        for year in range(start_year, 2025):
            # Add some randomness to the growth rate
            year_growth = growth_rate * random.uniform(0.9, 1.1)
            yearly_filings[str(year)] = int(current_filings)
            current_filings = current_filings * year_growth
        
        # Top patent assignees
        company_prefixes = ["Tech", "Advanced", "Global", "Next", "Smart", "Precision", "Integrated", "Dynamic", "Quantum", "Nano"]
        company_suffixes = ["Systems", "Solutions", "Technologies", "Innovations", "Industries", "Corporation", "Labs", "Research", "Devices", "Applications"]
        
        assignees = []
        for i in range(5):
            company_name = f"{random.choice(company_prefixes)}{random.choice(company_suffixes)}"
            patent_count = int(sum(yearly_filings.values()) * random.uniform(0.03, 0.15))
            assignees.append({
                "name": company_name,
                "patent_count": patent_count
            })
        
        # Sort assignees by patent count
        assignees.sort(key=lambda x: x["patent_count"], reverse=True)
        
        return {
            "total_patents": sum(yearly_filings.values()),
            "active_patents": int(sum(yearly_filings.values()) * random.uniform(0.7, 0.9)),
            "growth_rate": f"{(growth_rate - 1) * 100:.1f}%",
            "yearly_filings": yearly_filings,
            "top_assignees": assignees
        }
    
    def _generate_patent_trends(self, tech_areas):
        """Generate patent trends based on technology areas."""
        # Overall filing trend
        overall_trend = random.choice([
            "Steady growth in patent filings across all relevant technology areas.",
            "Accelerating patent activity, particularly in emerging application domains.",
            "Consolidation of patent portfolios through strategic acquisitions.",
            "Increasing specialization in patent claims with narrower scope.",
            "Growing international patent coverage, especially in Asian markets."
        ])
        
        # Technology convergence trends
        convergence_trends = []
        if len(tech_areas) >= 2:
            area1 = tech_areas[0]["name"]
            area2 = tech_areas[1]["name"]
            convergence_trends.append(f"Increasing integration between {area1} and {area2} technologies.")
        
        if len(tech_areas) >= 3:
            area3 = tech_areas[2]["name"]
            convergence_trends.append(f"Emerging patent activity at the intersection of {area1} and {area3}.")
        
        # Litigation trends
        litigation_trend = random.choice([
            "Limited litigation activity suggests open innovation opportunities.",
            "Increasing litigation in mature technology segments indicates competitive market.",
            "Strategic patent licensing becoming common practice among major players.",
            "Recent landmark cases establishing clearer boundaries for patentability.",
            "Cross-licensing agreements becoming more prevalent among industry leaders."
        ])
        
        # Technology-specific trends
        tech_specific_trends = []
        for area in tech_areas[:3]:  # Top 3 technology areas
            trend = random.choice([
                f"Patent claims in {area['name']} becoming more focused on specific applications.",
                f"Increasing patent quality and specificity in {area['name']} technologies.",
                f"Growing emphasis on implementation details in {area['name']} patents.",
                f"Shift toward system-level patents incorporating {area['name']} elements.",
                f"Broader geographic coverage for {area['name']} patents, expanding beyond traditional markets."
            ])
            tech_specific_trends.append(trend)
        
        return {
            "overall_trend": overall_trend,
            "convergence_trends": convergence_trends,
            "litigation_trend": litigation_trend,
            "technology_specific_trends": tech_specific_trends
        }
    
    def _generate_representative_patents(self, tech_areas):
        """Generate sample representative patents for technology areas."""
        representative_patents = []
        
        for area in tech_areas[:3]:  # Top 3 technology areas
            # Generate 2 patents per area
            for i in range(2):
                # Generate patent title
                title_prefixes = ["Method and System for", "Apparatus for", "System and Method of", "Device for", "Process for"]
                
                # Create title from technology area and keywords
                keywords = area["keywords"]
                if keywords:
                    keyword = random.choice(keywords).capitalize()
                    title = f"{random.choice(title_prefixes)} {keyword} in {area['name']}"
                else:
                    title = f"{random.choice(title_prefixes)} {area['name']}"
                
                # Generate assignee
                top_assignees = area["patent_activity"]["top_assignees"]
                assignee = top_assignees[0]["name"] if top_assignees else "Unknown Assignee"
                
                # Generate filing year
                filing_year = random.randint(2015, 2024)
                
                # Generate patent number format
                country_codes = ["US", "EP", "WO", "CN", "JP"]
                country = random.choice(country_codes)
                
                if country == "US":
                    number = f"{random.randint(7, 11)},{random.randint(100, 999)},{random.randint(100, 999)}"
                elif country == "EP":
                    number = f"{random.randint(1, 3)},{random.randint(100, 999)},{random.randint(100, 999)}"
                elif country == "WO":
                    number = f"{filing_year}/{random.randint(10, 199)},{random.randint(100, 999)}"
                elif country == "CN":
                    number = f"{random.randint(100, 999)},{random.randint(10, 99)},{random.randint(100, 999)}"
                else:  # JP
                    number = f"{filing_year}-{random.randint(100, 999)}{random.randint(100, 999)}"
                
                patent_number = f"{country}{number}"
                
                # Generate abstract
                abstract = self._generate_patent_abstract(area["name"], keywords)
                
                # Generate key claims
                key_claims = self._generate_patent_claims(area["name"], keywords)
                
                representative_patents.append({
                    "title": title,
                    "number": patent_number,
                    "assignee": assignee,
                    "filing_year": filing_year,
                    "technology_area": area["name"],
                    "abstract": abstract,
                    "key_claims": key_claims
                })
        
        return representative_patents
    
    def _generate_patent_abstract(self, tech_area, keywords):
        """Generate a patent abstract."""
        # Introduction phrases
        intro_phrases = [
            f"A system and method for {tech_area.lower()} that",
            f"An apparatus relating to {tech_area.lower()} which",
            f"A novel approach to {tech_area.lower()} that",
            f"A {tech_area.lower()} system that",
            f"Methods and systems for {tech_area.lower()} that"
        ]
        
        # Functionality phrases
        if keywords:
            keyword = random.choice(keywords)
            functionality_phrases = [
                f"enables improved {keyword}",
                f"enhances {keyword} capabilities",
                f"optimizes {keyword} processes",
                f"provides superior {keyword} performance",
                f"addresses challenges in {keyword}"
            ]
        else:
            functionality_phrases = [
                "improves overall system performance",
                "enhances operational capabilities",
                "optimizes resource utilization",
                "provides superior results",
                "addresses existing limitations"
            ]
        
        # Advantage phrases
        advantage_phrases = [
            "while reducing computational requirements",
            "while minimizing resource consumption",
            "through an innovative architecture",
            "using a novel configuration",
            "via an optimized implementation"
        ]
        
        # Implementation phrases
        implementation_phrases = [
            "The system comprises multiple integrated components that work in concert to achieve the desired functionality.",
            "The method includes a series of steps executed in a specified order to produce optimal results.",
            "The invention utilizes a combination of hardware and software elements to implement the described capabilities.",
            "The approach incorporates specialized algorithms and data structures to enable efficient operation.",
            "The system architecture features modular components that can be configured according to specific requirements."
        ]
        
        # Combine phrases to create abstract
        abstract = f"{random.choice(intro_phrases)} {random.choice(functionality_phrases)} {random.choice(advantage_phrases)}. {random.choice(implementation_phrases)}"
        
        return abstract
    
    def _generate_patent_claims(self, tech_area, keywords):
        """Generate key patent claims."""
        # Number of claims to generate (1-3)
        num_claims = random.randint(1, 3)
        
        claims = []
        for i in range(num_claims):
            if i == 0:
                # First claim is usually a system or method claim
                claim_type = random.choice(["system", "method", "apparatus", "device", "process"])
                
                if claim_type in ["system", "apparatus", "device"]:
                    # System claim structure
                    if keywords:
                        keyword = random.choice(keywords)
                        claims.append(f"A {claim_type} for {keyword} in {tech_area.lower()}, comprising: at least one processor; and memory storing instructions that, when executed by the at least one processor, cause the {claim_type} to perform specified operations.")
                    else:
                        claims.append(f"A {claim_type} for {tech_area.lower()}, comprising: at least one processor; and memory storing instructions that, when executed by the at least one processor, cause the {claim_type} to perform specified operations.")
                else:
                    # Method claim structure
                    if keywords:
                        keyword = random.choice(keywords)
                        claims.append(f"A {claim_type} for {keyword} in {tech_area.lower()}, comprising: receiving input data; processing the input data according to specified parameters; and generating output based on the processed data.")
                    else:
                        claims.append(f"A {claim_type} for {tech_area.lower()}, comprising: receiving input data; processing the input data according to specified parameters; and generating output based on the processed data.")
            else:
                # Dependent claims
                claim_detail = random.choice([
                    f"wherein the processing includes applying a specialized algorithm to optimize performance",
                    f"further comprising a feedback mechanism that adjusts parameters based on system performance",
                    f"wherein the system adapts its operation based on environmental conditions",
                    f"further comprising a user interface for configuring operational parameters",
                    f"wherein multiple processing stages are employed for enhanced accuracy"
                ])
                
                claims.append(f"The {claim_type} of claim 1, {claim_detail}.")
        
        return claims
    
    def _generate_patent_strategies(self, tech_areas, patent_trends):
        """Generate patent strategy recommendations."""
        # Patent filing strategies
        filing_strategies = [
            random.choice([
                "Focus patent applications on core technological innovations with clear novelty.",
                "Develop a portfolio of patents covering various aspects of the invention's implementation.",
                "Emphasize patent applications in rapidly growing technology areas with limited existing coverage.",
                "Consider international filing strategy targeting key markets with strong IP protection.",
                "Pursue both broad foundational patents and specific implementation patents."
            ]),
            random.choice([
                "Structure patent claims with varying scope to provide multiple layers of protection.",
                "Include method, system, and application claims to maximize coverage.",
                "Carefully document the development process to support potential priority claims.",
                "Consider accelerated examination options for critical technology components.",
                "Balance detailed disclosure with appropriately broad claim language."
            ])
        ]
        
        # White space opportunities
        white_space = []
        for area in tech_areas[:2]:  # Top 2 technology areas
            opportunity = random.choice([
                f"Limited patent coverage at the intersection of {area['name']} and emerging application areas.",
                f"Potential for novel implementation approaches in {area['name']} that bypass existing patents.",
                f"Opportunities in specialized applications of {area['name']} technologies.",
                f"Gaps in patent coverage for specific technical challenges in {area['name']}.",
                f"Relatively sparse patent landscape for novel materials or methods in {area['name']}."
            ])
            white_space.append(opportunity)
        
        # Freedom to operate considerations
        fto_considerations = [
            "Conduct comprehensive freedom-to-operate analysis in identified core technology areas.",
            "Evaluate patents of top assignees for potential obstacles to implementation.",
            "Consider design-around strategies for potentially blocking patents.",
            "Assess the validity of key patents that might impact freedom to operate.",
            "Monitor recently published patent applications in relevant technology spaces."
        ]
        fto_considerations = random.sample(fto_considerations, 2)
        
        # Defensive strategies
        defensive_strategies = random.choice([
            "Develop a defensive publication strategy for secondary innovations.",
            "Consider cross-licensing opportunities with complementary patent holders.",
            "Maintain robust invention disclosure processes to document prior art.",
            "Establish clear boundaries between proprietary technology and open innovation.",
            "Create a strategic patent wall around core technology with multiple related patents."
        ])
        
        return {
            "filing_strategies": filing_strategies,
            "white_space_opportunities": white_space,
            "fto_considerations": fto_considerations,
            "defensive_strategies": defensive_strategies
        }
    
    def _generate_tech_cluster_visualization(self, tech_areas):
        """Generate a visualization of technology clusters."""
        try:
            # Create a network graph of technology areas
            plt.figure(figsize=(10, 8))
            
            # Generate a random graph structure
            G = nx.Graph()
            
            # Add nodes for each technology area
            for i, area in enumerate(tech_areas):
                # Use relevance score to determine node size
                node_size = 1000 * area["relevance_score"]
                G.add_node(i, name=area["name"], size=node_size)
            
            # Add some edges between related areas
            for i in range(len(tech_areas)):
                for j in range(i+1, len(tech_areas)):
                    # Random probability of connection
                    if random.random() < 0.7:  # 70% chance of connection
                        # Random edge weight (relationship strength)
                        weight = random.uniform(0.1, 1.0)
                        G.add_edge(i, j, weight=weight)
            
            # Get node positions using a spring layout
            pos = nx.spring_layout(G, seed=42)
            
            # Draw the nodes
            node_sizes = [G.nodes[i]["size"] for i in G.nodes]
            nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="skyblue", alpha=0.8)
            
            # Draw edges with weights affecting line width
            edge_widths = [G[u][v]["weight"] * 5 for u, v in G.edges]
            nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, edge_color="gray")
            
            # Draw node labels
            labels = {i: G.nodes[i]["name"] for i in G.nodes}
            nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight="bold")
            
            # Add title and styling
            plt.title("Technology Cluster Analysis", fontsize=15)
            plt.axis("off")
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format="png", dpi=300)
            plt.close()
            buffer.seek(0)
            
            # Encode the image
            visualization_data = base64.b64encode(buffer.read()).decode("utf-8")
            
            # Create visualization metadata
            visualization = {
                "data": visualization_data,
                "format": "base64_png",
                "description": "Network visualization of technology clusters with node size indicating relevance and edge thickness indicating relationship strength."
            }
            
            return visualization
            
        except Exception as e:
            logger.error(f"Error generating tech cluster visualization: {e}")
            return None
    
    def forecast_technology_trends(self, domain, timeframe="medium"):
        """Forecast technology trends in a specific domain.
        
        Args:
            domain: Domain for trend forecasting
            timeframe: Timeframe for forecasting ("short", "medium", or "long")
            
        Returns:
            Dictionary with technology trend forecasts
        """
        try:
            logger.info(f"Forecasting technology trends for domain: {domain}, timeframe: {timeframe}")
            
            # Map timeframe to years
            timeframe_years = {
                "short": "1-2 years",
                "medium": "3-5 years",
                "long": "5-10 years"
            }
            years = timeframe_years.get(timeframe, "3-5 years")
            
            # Find domain information
            domain_info = None
            domain_key = None
            for key, info in self.technology_domains.items():
                if info["name"].lower() == domain.lower() or key.lower() == domain.lower():
                    domain_info = info
                    domain_key = key
                    break
            
            if not domain_info:
                # Create generic domain info
                domain_info = {
                    "name": domain,
                    "subdomains": ["General Applications", "Core Technologies", "Integration Methods"],
                    "trend_keywords": ["innovation", "advancement", "improvement", "development", "optimization"]
                }
                domain_key = "generic"
            
            # Generate key trends
            key_trends = self._generate_key_trends(domain_info, timeframe)
            
            # Generate technology maturity assessment
            maturity_assessment = self._generate_maturity_assessment(domain_info, timeframe)
            
            # Generate market impact analysis
            market_impact = self._generate_market_impact(domain_info, timeframe)
            
            # Generate adoption forecasts
            adoption_forecasts = self._generate_adoption_forecasts(domain_info, timeframe)
            
            # Generate visualization
            visualization = self._generate_trend_visualization(domain_info, timeframe)
            
            return {
                "domain": domain_info["name"],
                "timeframe": f"{timeframe.capitalize()} term ({years})",
                "key_trends": key_trends,
                "maturity_assessment": maturity_assessment,
                "market_impact": market_impact,
                "adoption_forecasts": adoption_forecasts,
                "trend_visualization": visualization
            }
            
        except Exception as e:
            logger.error(f"Error forecasting technology trends: {e}")
            return {"error": f"Could not forecast technology trends: {e}"}
    
    def _generate_key_trends(self, domain_info, timeframe):
        """Generate key technology trends for a domain."""
        trends = []
        
        # Get trend keywords from domain info
        keywords = domain_info.get("trend_keywords", [])
        
        # If no keywords, create generic ones
        if not keywords:
            keywords = ["innovation", "advancement", "improvement", "development", "optimization"]
        
        # Create trends based on timeframe
        if timeframe == "short":
            # Short-term trends focus on incremental improvements and integration
            trend_types = [
                "Incremental improvement",
                "Integration enhancement",
                "Efficiency optimization",
                "User experience refinement",
                "Performance enhancement"
            ]
            
            magnitude_terms = [
                "notable", "measurable", "important", "significant", "valuable"
            ]
            
            impact_scope = [
                "within established applications",
                "in current implementation contexts",
                "for existing use cases",
                "within presently deployed systems",
                "in today's operational environments"
            ]
            
        elif timeframe == "long":
            # Long-term trends focus on transformative technologies and paradigm shifts
            trend_types = [
                "Paradigm shift",
                "Fundamental transformation",
                "Revolutionary approach",
                "Disruptive innovation",
                "Emergent technology"
            ]
            
            magnitude_terms = [
                "transformative", "revolutionary", "groundbreaking", "disruptive", "landmark"
            ]
            
            impact_scope = [
                "that redefines the field",
                "creating entirely new application domains",
                "fundamentally changing how systems are designed",
                "establishing new technological paradigms",
                "opening previously impossible capabilities"
            ]
            
        else:  # medium
            # Medium-term trends focus on substantial advances and new approaches
            trend_types = [
                "Significant advancement",
                "New methodology",
                "Substantial innovation",
                "Emerging capability",
                "Novel approach"
            ]
            
            magnitude_terms = [
                "substantial", "major", "considerable", "significant", "important"
            ]
            
            impact_scope = [
                "expanding current applications",
                "enabling new use cases",
                "broadening technological capabilities",
                "creating new market opportunities",
                "addressing previously difficult challenges"
            ]
        
        # Generate trends for each subdomain
        subdomains = domain_info.get("subdomains", ["General Applications", "Core Technologies", "Integration Methods"])
        
        for subdomain in subdomains[:3]:  # Limit to 3 subdomains
            # Pick random elements
            trend_type = random.choice(trend_types)
            magnitude = random.choice(magnitude_terms)
            scope = random.choice(impact_scope)
            keyword = random.choice(keywords)
            
            # Generate trend title
            trend_title = f"{trend_type} in {subdomain} {keyword}"
            
            # Generate trend description
            trend_description = f"{trend_type} delivering {magnitude} improvements in {subdomain.lower()}, {scope}."
            
            # Generate enabling factors
            enabling_factors = self._generate_enabling_factors(domain_info, subdomain, timeframe)
            
            # Generate potential impact
            impact = self._generate_potential_impact(domain_info, subdomain, timeframe)
            
            trends.append({
                "title": trend_title,
                "description": trend_description,
                "enabling_factors": enabling_factors,
                "potential_impact": impact
            })
        
        return trends
    
    def _generate_enabling_factors(self, domain_info, subdomain, timeframe):
        """Generate enabling factors for a technology trend."""
        # Common enabling factor categories
        factor_categories = [
            "Technological Advances",
            "Market Demand",
            "Infrastructure Development",
            "Regulatory Environment",
            "Research Breakthroughs",
            "Cross-domain Innovation",
            "Investment Trends"
        ]
        
        # Select 2 random categories
        selected_categories = random.sample(factor_categories, 2)
        
        # Generate factors for each category
        factors = []
        
        for category in selected_categories:
            if category == "Technological Advances":
                factor = random.choice([
                    f"Continued advancement in underlying {subdomain.lower()} technologies.",
                    f"Increasing computational capabilities supporting {subdomain.lower()} applications.",
                    f"Improved algorithms and methodologies for {subdomain.lower()}.",
                    f"Enhanced integration capabilities with complementary technologies.",
                    f"More efficient implementation approaches for {subdomain.lower()} solutions."
                ])
            
            elif category == "Market Demand":
                factor = random.choice([
                    f"Growing market demand for solutions addressing {subdomain.lower()} challenges.",
                    f"Increasing user expectations driving {subdomain.lower()} improvements.",
                    f"Expanding application domains creating new {subdomain.lower()} requirements.",
                    f"Competitive pressures accelerating {subdomain.lower()} innovation.",
                    f"Evolving consumer behavior creating new {subdomain.lower()} opportunities."
                ])
            
            elif category == "Infrastructure Development":
                factor = random.choice([
                    f"Expanding infrastructure supporting {subdomain.lower()} deployments.",
                    f"Improved networking capabilities enabling {subdomain.lower()} applications.",
                    f"More robust platforms for {subdomain.lower()} implementation.",
                    f"Enhanced data ecosystem supporting {subdomain.lower()} solutions.",
                    f"Standardization efforts facilitating {subdomain.lower()} integration."
                ])
            
            elif category == "Regulatory Environment":
                factor = random.choice([
                    f"Evolving regulatory frameworks accommodating {subdomain.lower()} innovation.",
                    f"Policy developments supporting responsible {subdomain.lower()} advancement.",
                    f"Standards development providing clarity for {subdomain.lower()} implementation.",
                    f"Regulatory certainty enabling investment in {subdomain.lower()} research.",
                    f"Compliance frameworks maturing for {subdomain.lower()} applications."
                ])
            
            elif category == "Research Breakthroughs":
                factor = random.choice([
                    f"Recent research breakthroughs in core {subdomain.lower()} technologies.",
                    f"Academic-industry collaborations accelerating {subdomain.lower()} innovation.",
                    f"Cross-disciplinary research yielding new {subdomain.lower()} approaches.",
                    f"Emergence of novel theoretical frameworks for {subdomain.lower()}.",
                    f"Publication of key findings addressing {subdomain.lower()} challenges."
                ])
            
            elif category == "Cross-domain Innovation":
                factor = random.choice([
                    f"Application of techniques from adjacent domains to {subdomain.lower()}.",
                    f"Creative combination of disparate technologies with {subdomain.lower()} approaches.",
                    f"Knowledge transfer from related fields enhancing {subdomain.lower()} capabilities.",
                    f"Interdisciplinary teams bringing fresh perspectives to {subdomain.lower()} challenges.",
                    f"Adaptation of solutions from other domains to {subdomain.lower()} applications."
                ])
            
            elif category == "Investment Trends":
                factor = random.choice([
                    f"Increasing venture capital interest in {subdomain.lower()} startups.",
                    f"Growing corporate investment in {subdomain.lower()} R&D.",
                    f"Strategic acquisitions consolidating {subdomain.lower()} expertise.",
                    f"Public funding initiatives supporting {subdomain.lower()} research.",
                    f"Long-term institutional investment in {subdomain.lower()} innovation."
                ])
            
            factors.append({
                "category": category,
                "description": factor
            })
        
        return factors
    
    def _generate_potential_impact(self, domain_info, subdomain, timeframe):
        """Generate potential impact for a technology trend."""
        # Adjust impact magnitude based on timeframe
        if timeframe == "short":
            magnitude_terms = ["modest", "incremental", "appreciable", "noticeable", "measurable"]
        elif timeframe == "long":
            magnitude_terms = ["transformative", "revolutionary", "fundamental", "paradigm-shifting", "profound"]
        else:  # medium
            magnitude_terms = ["significant", "substantial", "considerable", "important", "notable"]
        
        # Generate impact statement
        magnitude = random.choice(magnitude_terms)
        
        impact = random.choice([
            f"{magnitude.capitalize()} impact on how {subdomain.lower()} solutions are designed and implemented.",
            f"{magnitude.capitalize()} improvements in {subdomain.lower()} performance and capabilities.",
            f"{magnitude.capitalize()} changes to {subdomain.lower()} application scope and effectiveness.",
            f"{magnitude.capitalize()} shift in {subdomain.lower()} development approaches and methodologies.",
            f"{magnitude.capitalize()} enhancement of {subdomain.lower()} integration with broader systems."
        ])
        
        return impact
    
    def _generate_maturity_assessment(self, domain_info, timeframe):
        """Generate technology maturity assessment."""
        # Get subdomains
        subdomains = domain_info.get("subdomains", ["General Applications", "Core Technologies", "Integration Methods"])
        
        # Generate maturity assessment for each subdomain
        assessments = []
        
        for subdomain in subdomains[:4]:  # Limit to 4 subdomains
            # Technology Readiness Level (TRL) - adjust based on timeframe
            if timeframe == "short":
                trl_base = random.randint(6, 9)  # Higher TRL for short-term
            elif timeframe == "long":
                trl_base = random.randint(2, 5)  # Lower TRL for long-term
            else:  # medium
                trl_base = random.randint(4, 7)  # Mid-range TRL for medium-term
            
            # Current TRL
            current_trl = trl_base
            
            # Projected TRL (can only go up to 9)
            projected_trl = min(9, current_trl + random.randint(1, 3))
            
            # Development pace
            if projected_trl - current_trl >= 3:
                pace = "Accelerating"
            elif projected_trl - current_trl >= 2:
                pace = "Steady"
            else:
                pace = "Incremental"
            
            # Adoption status
            if current_trl >= 8:
                adoption = "Mainstream"
            elif current_trl >= 6:
                adoption = "Early Adopters"
            elif current_trl >= 4:
                adoption = "Innovators"
            else:
                adoption = "Research Phase"
            
            # Key challenges
            challenges = []
            if current_trl <= 3:
                challenges.append(random.choice([
                    "Fundamental research gaps",
                    "Theoretical limitations",
                    "Proof-of-concept validation",
                    "Basic science understanding",
                    "Initial feasibility demonstration"
                ]))
            elif current_trl <= 6:
                challenges.append(random.choice([
                    "Technology scaling issues",
                    "Integration complexity",
                    "Performance optimization",
                    "Reliability improvements",
                    "Prototype refinement"
                ]))
            else:
                challenges.append(random.choice([
                    "Cost reduction requirements",
                    "Manufacturing optimization",
                    "Standards compliance",
                    "Market acceptance",
                    "Competitive differentiation"
                ]))
            
            # Add a second challenge
            additional_challenges = [
                "Resource requirements",
                "Technical expertise availability",
                "Interdisciplinary collaboration needs",
                "Infrastructure dependencies",
                "Regulatory considerations"
            ]
            challenges.append(random.choice(additional_challenges))
            
            # Add the assessment
            assessments.append({
                "subdomain": subdomain,
                "current_trl": current_trl,
                "projected_trl": projected_trl,
                "development_pace": pace,
                "adoption_status": adoption,
                "key_challenges": challenges
            })
        
        return assessments
    
    def _generate_market_impact(self, domain_info, timeframe):
        """Generate market impact analysis."""
        # Growth projections - adjust based on timeframe
        if timeframe == "short":
            market_growth_min = 5
            market_growth_max = 15
            impact_scope = "Primarily within existing market segments"
        elif timeframe == "long":
            market_growth_min = 15
            market_growth_max = 40
            impact_scope = "Creating entirely new market categories"
        else:  # medium
            market_growth_min = 10
            market_growth_max = 25
            impact_scope = "Expanding beyond traditional segments"
        
        # Generate market growth rate
        market_growth = random.uniform(market_growth_min, market_growth_max)
        
        # Generate market impact assessment
        market_assessment = random.choice([
            f"Expected to drive {market_growth:.1f}% compound annual growth in related markets.",
            f"Projected to expand addressable market by approximately {market_growth:.1f}% annually.",
            f"Likely to stimulate {market_growth:.1f}% yearly growth in technology adoption.",
            f"Anticipated to create {market_growth:.1f}% annual expansion in solution deployment.",
            f"Forecasted to generate {market_growth:.1f}% growth in sector investments."
        ])
        
        # Generate industry segments affected
        industries = [
            "Manufacturing", "Healthcare", "Transportation", "Finance", 
            "Retail", "Energy", "Agriculture", "Construction", 
            "Entertainment", "Education", "Government", "Defense"
        ]
        
        # Select random industries
        num_industries = random.randint(3, 5)
        affected_industries = random.sample(industries, num_industries)
        
        # Generate impact by industry
        industry_impacts = []
        for industry in affected_industries:
            impact_level = random.choice(["High", "Medium", "Moderate", "Significant", "Transformative"])
            impact_effect = random.choice([
                "operational efficiency improvements",
                "cost structure optimization",
                "customer experience enhancement",
                "product innovation acceleration",
                "business model transformation",
                "competitive landscape changes",
                "value chain restructuring"
            ])
            
            industry_impacts.append({
                "industry": industry,
                "impact_level": impact_level,
                "impact_description": f"{impact_level} impact through {impact_effect}."
            })
        
        # Generate market disruption potential
        if timeframe == "short":
            disruption_level = random.choice(["Low", "Low to Moderate", "Moderate"])
            disruption_focus = "Incremental improvements in existing solutions"
        elif timeframe == "long":
            disruption_level = random.choice(["High", "Transformative", "Paradigm-Shifting"])
            disruption_focus = "Fundamental rethinking of industry approaches"
        else:  # medium
            disruption_level = random.choice(["Moderate", "Moderate to High", "Significant"])
            disruption_focus = "Notable changes to established business practices"
        
        disruption_potential = {
            "level": disruption_level,
            "focus": disruption_focus,
            "description": f"{disruption_level} potential for market disruption, characterized by {disruption_focus.lower()}."
        }
        
        return {
            "growth_projection": market_assessment,
            "impact_scope": impact_scope,
            "industry_impacts": industry_impacts,
            "disruption_potential": disruption_potential
        }
    
    def _generate_adoption_forecasts(self, domain_info, timeframe):
        """Generate technology adoption forecasts."""
        # Create adoption curves
        # X-axis: years
        years = np.linspace(0, 10, 50)
        
        # Create adoption curves for different adopter categories
        # Use modified logistic curves with different parameters based on timeframe
        
        # Baseline parameters
        if timeframe == "short":
            midpoint = 3  # Earlier adoption
            steepness = 1.2  # Steeper curve
        elif timeframe == "long":
            midpoint = 7  # Later adoption
            steepness = 0.7  # Flatter curve
        else:  # medium
            midpoint = 5  # Middle adoption
            steepness = 1.0  # Standard curve
        
        # Generate adoption curves
        innovators = 1 / (1 + np.exp(-steepness * (years - (midpoint - 2))))
        early_adopters = 1 / (1 + np.exp(-steepness * (years - midpoint)))
        early_majority = 1 / (1 + np.exp(-steepness * (years - (midpoint + 1))))
        late_majority = 1 / (1 + np.exp(-steepness * (years - (midpoint + 3))))
        
        # Create plot
        plt.figure(figsize=(10, 6))
        plt.plot(years, innovators, 'b-', label="Innovators (2.5%)")
        plt.plot(years, early_adopters, 'g-', label="Early Adopters (13.5%)")
        plt.plot(years, early_majority, 'y-', label="Early Majority (34%)")
        plt.plot(years, late_majority, 'r-', label="Late Majority (34%)")
        
        # Add total adoption curve
        # Weighted sum based on standard adoption percentages
        total_adoption = (0.025 * innovators + 0.135 * early_adopters + 
                          0.34 * early_majority + 0.34 * late_majority)
        plt.plot(years, total_adoption, 'k--', linewidth=2, label="Total Adoption")
        
        # Add markers for adoption milestones
        milestone_values = [0.1, 0.25, 0.5, 0.75]
        milestone_labels = ["10%", "25%", "50%", "75%"]
        
        for value, label in zip(milestone_values, milestone_labels):
            # Find year when total adoption reaches this value
            try:
                year_idx = np.where(total_adoption >= value)[0][0]
                milestone_year = years[year_idx]
                plt.plot(milestone_year, value, 'ko', markersize=8)
                plt.text(milestone_year + 0.2, value, f"{label} at year {milestone_year:.1f}", 
                         verticalalignment='center')
            except IndexError:
                # This milestone might not be reached within the time frame
                pass
        
        plt.title(f"Technology Adoption Forecast - {domain_info['name']}")
        plt.xlabel("Years")
        plt.ylabel("Adoption Rate")
        plt.grid(True)
        plt.legend()
        
        # Save visualization to base64
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format="png", dpi=300)
        plt.close()
        buffer.seek(0)
        
        # Encode the image
        adoption_curve_data = base64.b64encode(buffer.read()).decode("utf-8")
        
        # Generate adoption factors
        
        # Accelerating factors
        accelerating_factors = [
            random.choice([
                "Decreasing implementation costs over time",
                "Increasing awareness of technology benefits",
                "Growing ecosystem of complementary solutions",
                "Improving performance characteristics",
                "Expanding use case demonstrations"
            ]),
            random.choice([
                "Development of supporting infrastructure",
                "Standardization and interoperability improvements",
                "Success stories from early implementations",
                "Competitive pressure within industries",
                "Increasing technical expertise availability"
            ])
        ]
        
        # Limiting factors
        limiting_factors = [
            random.choice([
                "Initial implementation complexity",
                "Integration challenges with existing systems",
                "Required organizational changes",
                "Uncertain return on investment timeline",
                "Limited awareness in traditional sectors"
            ]),
            random.choice([
                "Regulatory compliance considerations",
                "Expertise requirements for implementation",
                "Resource allocation constraints",
                "Need for process adaptation",
                "Cultural resistance to technology change"
            ])
        ]
        
        # Generate adoption tipping points
        tipping_points = [
            random.choice([
                "Achievement of cost parity with traditional solutions",
                "Emergence of industry-specific implementation frameworks",
                "Development of simplified deployment methodologies",
                "Establishment of clear regulatory guidelines",
                "Availability of comprehensive implementation services"
            ]),
            random.choice([
                "Successful demonstrations in high-visibility applications",
                "Publication of compelling return on investment studies",
                "Incorporation into industry standards and best practices",
                "Integration with widely used technology platforms",
                "Critical mass of skilled implementation specialists"
            ])
        ]
        
        return {
            "adoption_curve": {
                "data": adoption_curve_data,
                "format": "base64_png",
                "description": "Adoption forecast showing diffusion across different adopter categories."
            },
            "accelerating_factors": accelerating_factors,
            "limiting_factors": limiting_factors,
            "tipping_points": tipping_points
        }
    
    def _generate_trend_visualization(self, domain_info, timeframe):
        """Generate visualization of technology trends."""
        try:
            # Create a radar chart showing potential impact across different dimensions
            
            # Define impact dimensions
            dimensions = [
                "Technical Performance",
                "Cost Efficiency",
                "User Experience",
                "Market Potential",
                "Sustainability",
                "Integration Ease"
            ]
            
            # Number of dimensions
            N = len(dimensions)
            
            # Generate impact scores for current and future state
            # Adjust based on timeframe
            if timeframe == "short":
                current_scores = np.random.uniform(0.4, 0.7, N)
                score_increase = np.random.uniform(0.1, 0.2, N)
            elif timeframe == "long":
                current_scores = np.random.uniform(0.2, 0.5, N)
                score_increase = np.random.uniform(0.3, 0.6, N)
            else:  # medium
                current_scores = np.random.uniform(0.3, 0.6, N)
                score_increase = np.random.uniform(0.2, 0.4, N)
            
            # Future scores (capped at 1.0)
            future_scores = np.minimum(current_scores + score_increase, 1.0)
            
            # Set up the radar chart
            angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
            
            # Close the loop
            current_scores = np.append(current_scores, current_scores[0])
            future_scores = np.append(future_scores, future_scores[0])
            angles = np.append(angles, angles[0])
            dimensions = dimensions + [dimensions[0]]
            
            # Create plot
            plt.figure(figsize=(10, 8))
            ax = plt.subplot(111, polar=True)
            
            # Plot current and future states
            ax.plot(angles, current_scores, 'b-', linewidth=2, label='Current State')
            ax.fill(angles, current_scores, 'b', alpha=0.1)
            
            ax.plot(angles, future_scores, 'r-', linewidth=2, label=f'Projected ({timeframe.capitalize()}-term)')
            ax.fill(angles, future_scores, 'r', alpha=0.1)
            
            # Set dimension labels
            plt.xticks(angles[:-1], dimensions[:-1])
            
            # Set radial ticks
            ax.set_rlabel_position(0)
            plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=8)
            plt.ylim(0, 1)
            
            # Add title and legend
            plt.title(f"Impact Assessment: {domain_info['name']}", size=15)
            plt.legend(loc='upper right')
            
            # Save visualization to base64
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format="png", dpi=300)
            plt.close()
            buffer.seek(0)
            
            # Encode the image
            radar_chart_data = base64.b64encode(buffer.read()).decode("utf-8")
            
            # Create visualization data
            visualization = {
                "data": radar_chart_data,
                "format": "base64_png",
                "description": "Radar chart visualization showing current and projected impact across key dimensions."
            }
            
            return visualization
            
        except Exception as e:
            logger.error(f"Error generating trend visualization: {e}")
            return None

# Initialize the invention engine
invention_engine = InventionEngine()

def get_invention_engine():
    """Get the global invention engine instance."""
    global invention_engine
    return invention_engine