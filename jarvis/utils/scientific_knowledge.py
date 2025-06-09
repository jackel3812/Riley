"""
RILEY - Scientific Knowledge Module

This module provides educational content and resources on key scientific domains:
- Foundational knowledge (math, physics, chemistry)
- Advanced scientific concepts (biology, genetics, ecology)
- Research methods and scientific process
- Laboratory techniques and tools
- Critical thinking and scientific reasoning
"""

import logging
import json
import random
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class ScientificKnowledgeEngine:
    """Engine providing scientific knowledge, educational content, and resources."""
    
    def __init__(self):
        """Initialize the scientific knowledge engine."""
        logger.info("Initializing Scientific Knowledge Engine")
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load scientific knowledge base."""
        # Scientific domains and subdomains
        self.knowledge_domains = {
            "mathematics": {
                "name": "Mathematics",
                "description": "The study of numbers, quantities, and shapes, and their relationships and properties.",
                "subdomains": [
                    "algebra", "geometry", "trigonometry", "calculus", "statistics", 
                    "probability", "discrete mathematics", "linear algebra", "differential equations"
                ]
            },
            "physics": {
                "name": "Physics",
                "description": "The study of matter, energy, and the interactions between them.",
                "subdomains": [
                    "classical mechanics", "electromagnetism", "thermodynamics", "optics",
                    "quantum mechanics", "relativity", "nuclear physics", "particle physics",
                    "solid state physics", "fluid dynamics", "acoustics"
                ]
            },
            "chemistry": {
                "name": "Chemistry",
                "description": "The study of matter, its properties, and the changes it undergoes.",
                "subdomains": [
                    "organic chemistry", "inorganic chemistry", "analytical chemistry",
                    "physical chemistry", "biochemistry", "polymer chemistry",
                    "electrochemistry", "environmental chemistry", "medicinal chemistry"
                ]
            },
            "biology": {
                "name": "Biology",
                "description": "The study of living organisms and their interactions with each other and the environment.",
                "subdomains": [
                    "molecular biology", "cellular biology", "genetics", "ecology",
                    "physiology", "microbiology", "botany", "zoology", "evolutionary biology",
                    "developmental biology", "neurobiology", "immunology"
                ]
            },
            "earth_science": {
                "name": "Earth Science",
                "description": "The study of the Earth and its systems.",
                "subdomains": [
                    "geology", "meteorology", "oceanography", "climatology",
                    "hydrology", "seismology", "volcanology", "paleontology",
                    "mineralogy", "soil science", "atmospheric science"
                ]
            },
            "astronomy": {
                "name": "Astronomy",
                "description": "The study of celestial objects, space, and the universe.",
                "subdomains": [
                    "astrophysics", "cosmology", "planetary science", "stellar astronomy",
                    "galactic astronomy", "observational astronomy", "radio astronomy",
                    "astrochemistry", "astrobiology", "exoplanetology"
                ]
            },
            "computer_science": {
                "name": "Computer Science",
                "description": "The study of computation, information, and automation.",
                "subdomains": [
                    "algorithms", "data structures", "artificial intelligence", "machine learning",
                    "computer vision", "natural language processing", "databases",
                    "computer networks", "cybersecurity", "computer graphics"
                ]
            },
            "engineering": {
                "name": "Engineering",
                "description": "The application of scientific principles to design and build machines, structures, and systems.",
                "subdomains": [
                    "mechanical engineering", "electrical engineering", "civil engineering",
                    "chemical engineering", "aerospace engineering", "biomedical engineering",
                    "materials engineering", "environmental engineering", "nuclear engineering"
                ]
            }
        }
        
        # Scientific methods and research processes
        self.scientific_methods = {
            "observation": {
                "name": "Observation",
                "description": "The process of gathering information through the senses or instruments.",
                "techniques": [
                    "structured observation", "participant observation", "naturalistic observation",
                    "systematic observation", "controlled observation"
                ]
            },
            "hypothesis_formation": {
                "name": "Hypothesis Formation",
                "description": "The development of a testable explanation for a phenomenon.",
                "techniques": [
                    "inductive reasoning", "deductive reasoning", "abductive reasoning",
                    "null hypothesis formulation", "alternative hypothesis formulation"
                ]
            },
            "experimentation": {
                "name": "Experimentation",
                "description": "The process of testing a hypothesis through controlled trials.",
                "techniques": [
                    "controlled experiments", "field experiments", "natural experiments",
                    "quasi-experiments", "randomized controlled trials", "double-blind studies"
                ]
            },
            "data_collection": {
                "name": "Data Collection",
                "description": "The gathering of information through measurements, surveys, or other means.",
                "techniques": [
                    "quantitative data collection", "qualitative data collection",
                    "surveys", "interviews", "field sampling", "sensor networks",
                    "remote sensing", "archival research"
                ]
            },
            "data_analysis": {
                "name": "Data Analysis",
                "description": "The process of examining, cleaning, transforming, and modeling data.",
                "techniques": [
                    "statistical analysis", "exploratory data analysis", "regression analysis",
                    "multivariate analysis", "time series analysis", "spatial analysis",
                    "network analysis", "machine learning", "data mining"
                ]
            },
            "conclusion_drawing": {
                "name": "Conclusion Drawing",
                "description": "The process of interpreting data and determining whether it supports or refutes the hypothesis.",
                "techniques": [
                    "inference", "generalization", "statistical significance testing",
                    "confidence intervals", "effect size calculation", "meta-analysis"
                ]
            },
            "communication": {
                "name": "Scientific Communication",
                "description": "The process of sharing research findings with the scientific community and the public.",
                "techniques": [
                    "scientific writing", "peer review", "conference presentations",
                    "scientific posters", "data visualization", "science communication"
                ]
            }
        }
        
        # Laboratory techniques and tools
        self.laboratory_techniques = {
            "microscopy": {
                "name": "Microscopy",
                "description": "The use of microscopes to view objects that are too small to be seen by the naked eye.",
                "types": [
                    "light microscopy", "electron microscopy", "confocal microscopy",
                    "fluorescence microscopy", "atomic force microscopy"
                ]
            },
            "spectroscopy": {
                "name": "Spectroscopy",
                "description": "The study of the interaction between matter and electromagnetic radiation.",
                "types": [
                    "mass spectroscopy", "infrared spectroscopy", "UV-visible spectroscopy",
                    "nuclear magnetic resonance spectroscopy", "X-ray spectroscopy"
                ]
            },
            "chromatography": {
                "name": "Chromatography",
                "description": "A technique for separating mixtures into their constituent components.",
                "types": [
                    "gas chromatography", "liquid chromatography", "thin-layer chromatography",
                    "ion-exchange chromatography", "affinity chromatography"
                ]
            },
            "electrophoresis": {
                "name": "Electrophoresis",
                "description": "A technique for separating charged molecules based on their size and charge.",
                "types": [
                    "gel electrophoresis", "capillary electrophoresis", "pulsed-field gel electrophoresis",
                    "two-dimensional electrophoresis", "isoelectric focusing"
                ]
            },
            "pcr": {
                "name": "Polymerase Chain Reaction (PCR)",
                "description": "A technique for amplifying specific DNA sequences.",
                "types": [
                    "conventional PCR", "real-time PCR", "reverse transcription PCR",
                    "multiplex PCR", "nested PCR", "digital PCR"
                ]
            },
            "crystallography": {
                "name": "Crystallography",
                "description": "The study of the arrangement of atoms in crystalline solids.",
                "types": [
                    "X-ray crystallography", "neutron crystallography", "electron crystallography",
                    "powder diffraction", "single-crystal diffraction"
                ]
            },
            "centrifugation": {
                "name": "Centrifugation",
                "description": "A technique for separating particles based on their size, shape, and density.",
                "types": [
                    "differential centrifugation", "density gradient centrifugation",
                    "ultracentrifugation", "isopycnic centrifugation", "rate-zonal centrifugation"
                ]
            },
            "cell_culture": {
                "name": "Cell Culture",
                "description": "The process of growing cells in controlled conditions outside their natural environment.",
                "types": [
                    "adherent cell culture", "suspension cell culture", "organoid culture",
                    "primary cell culture", "immortalized cell line culture", "co-culture"
                ]
            }
        }
        
        # Scientific critical thinking skills
        self.critical_thinking_skills = {
            "logical_reasoning": {
                "name": "Logical Reasoning",
                "description": "The process of using rational, systematic steps to arrive at a conclusion.",
                "techniques": [
                    "deductive reasoning", "inductive reasoning", "abductive reasoning",
                    "syllogistic reasoning", "causal reasoning", "analogical reasoning"
                ]
            },
            "evidence_evaluation": {
                "name": "Evidence Evaluation",
                "description": "The process of assessing the quality, validity, and reliability of evidence.",
                "techniques": [
                    "source credibility assessment", "methodology evaluation",
                    "data quality assessment", "bias identification", "statistical significance evaluation",
                    "confidence interval interpretation", "effect size evaluation"
                ]
            },
            "assumption_identification": {
                "name": "Assumption Identification",
                "description": "The process of recognizing and examining underlying assumptions.",
                "techniques": [
                    "explicit assumption identification", "implicit assumption identification",
                    "worldview analysis", "paradigm examination", "conceptual framework analysis"
                ]
            },
            "counterargument_consideration": {
                "name": "Counterargument Consideration",
                "description": "The process of considering alternative explanations and perspectives.",
                "techniques": [
                    "alternative hypothesis generation", "devil's advocate thinking",
                    "perspective-taking", "falsification attempts", "multiple working hypotheses"
                ]
            },
            "bias_recognition": {
                "name": "Bias Recognition",
                "description": "The process of identifying and addressing various forms of bias in reasoning and research.",
                "techniques": [
                    "confirmation bias identification", "selection bias identification",
                    "publication bias awareness", "researcher bias examination",
                    "cultural bias recognition", "cognitive bias awareness"
                ]
            }
        }
        
        # Educational resources and learning paths
        self.educational_resources = {
            "foundational_courses": [
                {
                    "name": "Mathematics for Scientists and Engineers",
                    "topics": ["algebra", "calculus", "differential equations", "linear algebra", "statistics"],
                    "level": "undergraduate",
                    "duration": "1-2 years"
                },
                {
                    "name": "Physics for Scientists and Engineers",
                    "topics": ["mechanics", "electromagnetism", "thermodynamics", "waves", "modern physics"],
                    "level": "undergraduate",
                    "duration": "1-2 years"
                },
                {
                    "name": "General Chemistry",
                    "topics": ["atomic structure", "chemical bonding", "stoichiometry", "thermochemistry", "kinetics"],
                    "level": "undergraduate",
                    "duration": "1 year"
                },
                {
                    "name": "Introduction to Biology",
                    "topics": ["cell biology", "genetics", "evolution", "physiology", "ecology"],
                    "level": "undergraduate",
                    "duration": "1 year"
                },
                {
                    "name": "Computer Programming for Scientists",
                    "topics": ["programming basics", "data structures", "algorithms", "scientific computing", "data visualization"],
                    "level": "undergraduate",
                    "duration": "6 months - 1 year"
                }
            ],
            "advanced_courses": [
                {
                    "name": "Quantum Mechanics",
                    "topics": ["wave functions", "Schrödinger equation", "quantum operators", "perturbation theory"],
                    "level": "graduate",
                    "duration": "1 year"
                },
                {
                    "name": "Molecular Biology and Genetics",
                    "topics": ["DNA structure", "gene expression", "genetic engineering", "genomics"],
                    "level": "graduate",
                    "duration": "1 year"
                },
                {
                    "name": "Advanced Statistical Methods",
                    "topics": ["multivariate analysis", "Bayesian statistics", "experimental design", "statistical computing"],
                    "level": "graduate",
                    "duration": "1 year"
                },
                {
                    "name": "Climate Science and Modeling",
                    "topics": ["atmospheric physics", "ocean dynamics", "climate models", "paleoclimatology"],
                    "level": "graduate",
                    "duration": "1 year"
                },
                {
                    "name": "Machine Learning for Scientific Data Analysis",
                    "topics": ["supervised learning", "unsupervised learning", "neural networks", "scientific applications"],
                    "level": "graduate",
                    "duration": "6 months - 1 year"
                }
            ],
            "research_methods_courses": [
                {
                    "name": "Research Methods in Science",
                    "topics": ["scientific method", "research design", "data collection", "data analysis", "scientific writing"],
                    "level": "undergraduate/graduate",
                    "duration": "6 months"
                },
                {
                    "name": "Experimental Design and Analysis",
                    "topics": ["control variables", "randomization", "factorial designs", "statistical power", "effect size"],
                    "level": "graduate",
                    "duration": "6 months"
                },
                {
                    "name": "Scientific Communication",
                    "topics": ["scientific writing", "presentation skills", "data visualization", "peer review process"],
                    "level": "undergraduate/graduate",
                    "duration": "3-6 months"
                }
            ],
            "online_resources": [
                {
                    "name": "Open Courseware",
                    "description": "Free online course materials from universities",
                    "examples": ["MIT OpenCourseWare", "Stanford Online", "edX", "Coursera", "Khan Academy"]
                },
                {
                    "name": "Scientific Journals",
                    "description": "Peer-reviewed scientific publications",
                    "examples": ["Nature", "Science", "PLOS", "arXiv", "Open access journals"]
                },
                {
                    "name": "Scientific Computing Resources",
                    "description": "Tools and resources for scientific computing",
                    "examples": ["Python Scientific Stack (NumPy, SciPy, Pandas)", "R Project", "MATLAB", "Jupyter Notebooks"]
                },
                {
                    "name": "Data Repositories",
                    "description": "Public repositories of scientific data",
                    "examples": ["GenBank", "Protein Data Bank", "NASA Earth Data", "NOAA Climate Data"]
                }
            ]
        }
        
        # Career paths in science
        self.career_paths = {
            "academic": {
                "name": "Academic Science",
                "description": "Scientific research and teaching within academic institutions.",
                "roles": ["professor", "research scientist", "postdoctoral researcher", "laboratory manager", "research assistant"],
                "requirements": ["PhD in relevant field", "publication record", "teaching experience", "grant writing skills"],
                "advantages": ["academic freedom", "intellectual challenge", "teaching opportunities", "flexible schedule"],
                "challenges": ["competitive job market", "grant funding pressure", "publication pressure", "administrative duties"]
            },
            "industry": {
                "name": "Industrial Science",
                "description": "Scientific research and development within private companies.",
                "roles": ["research scientist", "product developer", "clinical researcher", "data scientist", "quality control scientist"],
                "requirements": ["MS/PhD in relevant field", "industry experience", "teamwork skills", "project management"],
                "advantages": ["higher salaries", "clear objectives", "product development", "career advancement", "resources"],
                "challenges": ["less publication freedom", "profit-driven research", "intellectual property restrictions", "market pressures"]
            },
            "government": {
                "name": "Government Science",
                "description": "Scientific research, policy, and regulation within government agencies.",
                "roles": ["research scientist", "policy advisor", "regulatory scientist", "laboratory director", "field researcher"],
                "requirements": ["MS/PhD in relevant field", "understanding of policy", "communication skills", "specialized expertise"],
                "advantages": ["public service", "stable funding", "policy impact", "job security", "work-life balance"],
                "challenges": ["bureaucracy", "political influences", "funding fluctuations", "public scrutiny"]
            },
            "nonprofit": {
                "name": "Nonprofit Science",
                "description": "Scientific research, education, and advocacy within nonprofit organizations.",
                "roles": ["research scientist", "program manager", "science communicator", "grant manager", "field researcher"],
                "requirements": ["MS/PhD in relevant field", "passion for mission", "communication skills", "fundraising experience"],
                "advantages": ["mission-driven work", "public impact", "interdisciplinary collaboration", "education opportunities"],
                "challenges": ["funding limitations", "resource constraints", "multiple responsibilities", "demonstrating impact"]
            },
            "entrepreneurship": {
                "name": "Scientific Entrepreneurship",
                "description": "Founding and leading science-based startup companies.",
                "roles": ["founder", "chief scientific officer", "technical director", "consultant", "scientific advisor"],
                "requirements": ["scientific expertise", "business acumen", "leadership skills", "risk tolerance", "networking abilities"],
                "advantages": ["innovation potential", "high reward potential", "intellectual freedom", "direct application", "impact"],
                "challenges": ["high risk", "funding challenges", "multiple responsibilities", "work-life balance", "market validation"]
            }
        }
    
    def get_domain_overview(self, domain_name):
        """Get an overview of a scientific domain.
        
        Args:
            domain_name: Name of the scientific domain
            
        Returns:
            Dictionary with domain overview information
        """
        try:
            # Find the domain
            domain_key = None
            for key, domain in self.knowledge_domains.items():
                if domain["name"].lower() == domain_name.lower() or key.lower() == domain_name.lower():
                    domain_key = key
                    break
            
            if not domain_key:
                return {"error": f"Domain '{domain_name}' not found"}
            
            domain = self.knowledge_domains[domain_key]
            
            # Prepare the response
            overview = {
                "name": domain["name"],
                "description": domain["description"],
                "subdomains": domain["subdomains"],
                "related_methods": self._get_related_methods(domain_key),
                "related_techniques": self._get_related_techniques(domain_key),
                "learning_resources": self._get_learning_resources(domain_key),
                "career_paths": self._get_related_careers(domain_key)
            }
            
            return overview
            
        except Exception as e:
            logger.error(f"Error retrieving domain overview: {e}")
            return {"error": f"Could not retrieve domain overview: {e}"}
    
    def _get_related_methods(self, domain_key):
        """Get scientific methods related to a domain."""
        # Map domains to relevant methods
        domain_method_mapping = {
            "mathematics": ["hypothesis_formation", "data_analysis", "conclusion_drawing"],
            "physics": ["observation", "hypothesis_formation", "experimentation", "data_collection", "data_analysis", "conclusion_drawing"],
            "chemistry": ["observation", "hypothesis_formation", "experimentation", "data_collection", "data_analysis", "conclusion_drawing"],
            "biology": ["observation", "hypothesis_formation", "experimentation", "data_collection", "data_analysis", "conclusion_drawing"],
            "earth_science": ["observation", "hypothesis_formation", "data_collection", "data_analysis", "conclusion_drawing"],
            "astronomy": ["observation", "hypothesis_formation", "data_analysis", "conclusion_drawing"],
            "computer_science": ["hypothesis_formation", "experimentation", "data_analysis", "conclusion_drawing"],
            "engineering": ["hypothesis_formation", "experimentation", "data_collection", "data_analysis", "conclusion_drawing"]
        }
        
        related_methods = []
        if domain_key in domain_method_mapping:
            method_keys = domain_method_mapping[domain_key]
            for key in method_keys:
                if key in self.scientific_methods:
                    method = self.scientific_methods[key]
                    related_methods.append({
                        "name": method["name"],
                        "description": method["description"],
                        "key_techniques": method["techniques"][:3]  # Include just a few techniques
                    })
        
        return related_methods
    
    def _get_related_techniques(self, domain_key):
        """Get laboratory techniques related to a domain."""
        # Map domains to relevant techniques
        domain_technique_mapping = {
            "mathematics": [],
            "physics": ["microscopy", "spectroscopy", "crystallography"],
            "chemistry": ["spectroscopy", "chromatography", "crystallography"],
            "biology": ["microscopy", "pcr", "electrophoresis", "cell_culture", "centrifugation"],
            "earth_science": ["spectroscopy", "crystallography"],
            "astronomy": ["spectroscopy"],
            "computer_science": [],
            "engineering": ["microscopy", "spectroscopy", "crystallography"]
        }
        
        related_techniques = []
        if domain_key in domain_technique_mapping:
            technique_keys = domain_technique_mapping[domain_key]
            for key in technique_keys:
                if key in self.laboratory_techniques:
                    technique = self.laboratory_techniques[key]
                    related_techniques.append({
                        "name": technique["name"],
                        "description": technique["description"],
                        "types": technique["types"][:3]  # Include just a few types
                    })
        
        return related_techniques
    
    def _get_learning_resources(self, domain_key):
        """Get learning resources related to a domain."""
        domain_name = self.knowledge_domains[domain_key]["name"]
        
        foundational_courses = []
        for course in self.educational_resources["foundational_courses"]:
            if any(topic.lower() in domain_name.lower() for topic in course["topics"]):
                foundational_courses.append(course)
        
        advanced_courses = []
        for course in self.educational_resources["advanced_courses"]:
            if any(topic.lower() in domain_name.lower() for topic in course["topics"]):
                advanced_courses.append(course)
        
        # Always include research methods
        research_courses = self.educational_resources["research_methods_courses"]
        
        # Always include online resources
        online_resources = self.educational_resources["online_resources"]
        
        return {
            "foundational_courses": foundational_courses,
            "advanced_courses": advanced_courses,
            "research_courses": research_courses,
            "online_resources": online_resources
        }
    
    def _get_related_careers(self, domain_key):
        """Get career paths related to a domain."""
        # All domains can lead to any career path, so include all
        return list(self.career_paths.values())
    
    def get_scientific_method_guide(self, method_name=None):
        """Get information about scientific methods.
        
        Args:
            method_name: Optional name of specific scientific method
            
        Returns:
            Dictionary with scientific method information
        """
        try:
            if method_name:
                # Find the method
                method_key = None
                for key, method in self.scientific_methods.items():
                    if method["name"].lower() == method_name.lower() or key.lower() == method_name.lower():
                        method_key = key
                        break
                
                if not method_key:
                    return {"error": f"Scientific method '{method_name}' not found"}
                
                # Return specific method
                return self.scientific_methods[method_key]
            else:
                # Return overview of all methods
                return {
                    "scientific_method_process": list(self.scientific_methods.values()),
                    "importance": "The scientific method is a systematic approach to acquiring knowledge that involves making observations, formulating hypotheses, testing through experimentation, and drawing conclusions. It is the foundation of scientific inquiry and evidence-based knowledge.",
                    "key_principles": [
                        "Empirical evidence is the basis of scientific knowledge",
                        "Hypotheses must be testable and falsifiable",
                        "Experimental design should control for variables",
                        "Reproducibility is essential for validation",
                        "Peer review helps ensure quality and accuracy"
                    ]
                }
            
        except Exception as e:
            logger.error(f"Error retrieving scientific method guide: {e}")
            return {"error": f"Could not retrieve scientific method guide: {e}"}
    
    def get_laboratory_techniques_guide(self, technique_name=None):
        """Get information about laboratory techniques.
        
        Args:
            technique_name: Optional name of specific laboratory technique
            
        Returns:
            Dictionary with laboratory technique information
        """
        try:
            if technique_name:
                # Find the technique
                technique_key = None
                for key, technique in self.laboratory_techniques.items():
                    if technique["name"].lower() == technique_name.lower() or key.lower() == technique_name.lower():
                        technique_key = key
                        break
                
                if not technique_key:
                    return {"error": f"Laboratory technique '{technique_name}' not found"}
                
                # Return specific technique
                return self.laboratory_techniques[technique_key]
            else:
                # Return overview of all techniques
                return {
                    "laboratory_techniques": list(self.laboratory_techniques.values()),
                    "importance": "Laboratory techniques are the practical methods and procedures used in scientific research. They allow scientists to observe, measure, analyze, and manipulate matter and phenomena to test hypotheses and gather data.",
                    "laboratory_safety": [
                        "Always wear appropriate personal protective equipment (PPE)",
                        "Know the location of safety equipment (fire extinguishers, eyewash stations, emergency showers)",
                        "Understand the hazards of materials being used",
                        "Follow proper waste disposal procedures",
                        "Never work alone in a laboratory"
                    ]
                }
            
        except Exception as e:
            logger.error(f"Error retrieving laboratory techniques guide: {e}")
            return {"error": f"Could not retrieve laboratory techniques guide: {e}"}
    
    def get_critical_thinking_guide(self, skill_name=None):
        """Get information about scientific critical thinking skills.
        
        Args:
            skill_name: Optional name of specific critical thinking skill
            
        Returns:
            Dictionary with critical thinking skill information
        """
        try:
            if skill_name:
                # Find the skill
                skill_key = None
                for key, skill in self.critical_thinking_skills.items():
                    if skill["name"].lower() == skill_name.lower() or key.lower() == skill_name.lower():
                        skill_key = key
                        break
                
                if not skill_key:
                    return {"error": f"Critical thinking skill '{skill_name}' not found"}
                
                # Return specific skill
                return self.critical_thinking_skills[skill_key]
            else:
                # Return overview of all skills
                return {
                    "critical_thinking_skills": list(self.critical_thinking_skills.values()),
                    "importance": "Critical thinking in science involves careful analysis, evaluation, and interpretation of information to form well-reasoned judgments. It helps scientists avoid bias, identify errors, and make sound conclusions based on evidence.",
                    "cognitive_biases_to_avoid": [
                        "Confirmation bias: Seeking information that confirms existing beliefs",
                        "Selection bias: Using non-representative data in analysis",
                        "Correlation-causation fallacy: Assuming correlation implies causation",
                        "Availability bias: Overemphasizing easily recalled information",
                        "Anchoring bias: Relying too heavily on initial information"
                    ]
                }
            
        except Exception as e:
            logger.error(f"Error retrieving critical thinking guide: {e}")
            return {"error": f"Could not retrieve critical thinking guide: {e}"}
    
    def get_career_guide(self, career_path=None):
        """Get information about scientific career paths.
        
        Args:
            career_path: Optional name of specific career path
            
        Returns:
            Dictionary with career path information
        """
        try:
            if career_path:
                # Find the career path
                career_key = None
                for key, career in self.career_paths.items():
                    if career["name"].lower() == career_path.lower() or key.lower() == career_path.lower():
                        career_key = key
                        break
                
                if not career_key:
                    return {"error": f"Career path '{career_path}' not found"}
                
                # Return specific career path
                return self.career_paths[career_key]
            else:
                # Return overview of all career paths
                return {
                    "career_paths": list(self.career_paths.values()),
                    "importance": "Scientific careers offer opportunities to contribute to knowledge, solve problems, and make a positive impact. Different sectors (academic, industry, government, nonprofit, entrepreneurship) provide various ways to apply scientific expertise.",
                    "career_development_tips": [
                        "Develop both depth in a specialty and breadth across related areas",
                        "Build strong communication skills (written and verbal)",
                        "Gain experience in collaborative and interdisciplinary work",
                        "Develop technical skills relevant to your field (programming, data analysis, etc.)",
                        "Build a professional network through conferences, collaborations, and mentorship"
                    ]
                }
            
        except Exception as e:
            logger.error(f"Error retrieving career guide: {e}")
            return {"error": f"Could not retrieve career guide: {e}"}
    
    def get_learning_path(self, goal, current_level="beginner"):
        """Get a personalized learning path based on goals and current level.
        
        Args:
            goal: Learning goal or target field
            current_level: Current knowledge level
            
        Returns:
            Dictionary with personalized learning path
        """
        try:
            # Determine which domains are most relevant to the goal
            relevant_domains = []
            for key, domain in self.knowledge_domains.items():
                # Check if goal matches domain name or subdomains
                if (goal.lower() in domain["name"].lower() or 
                    any(goal.lower() in subdomain.lower() for subdomain in domain["subdomains"])):
                    relevant_domains.append(key)
            
            if not relevant_domains:
                # If no direct match, use keywords to find related domains
                goal_keywords = goal.lower().split()
                for key, domain in self.knowledge_domains.items():
                    if any(keyword in domain["name"].lower() for keyword in goal_keywords):
                        relevant_domains.append(key)
                    elif any(any(keyword in subdomain.lower() for subdomain in domain["subdomains"]) for keyword in goal_keywords):
                        relevant_domains.append(key)
            
            if not relevant_domains:
                return {"error": f"Could not determine relevant domains for goal: {goal}"}
            
            # Create a learning path based on relevant domains and current level
            learning_path = {
                "goal": goal,
                "current_level": current_level,
                "prerequisites": [],
                "foundational_courses": [],
                "advanced_courses": [],
                "specialized_courses": [],
                "practical_experience": [],
                "resources": []
            }
            
            # Add prerequisites based on level
            if current_level == "beginner":
                learning_path["prerequisites"] = [
                    "Basic mathematics (algebra, geometry)",
                    "General science concepts",
                    "Critical thinking skills",
                    "Computer literacy"
                ]
            
            # Add courses from relevant domains
            for domain_key in relevant_domains[:2]:  # Focus on top 2 most relevant domains
                domain = self.knowledge_domains[domain_key]
                
                # Add foundational courses
                if current_level in ["beginner", "intermediate"]:
                    for course in self.educational_resources["foundational_courses"]:
                        if any(subdomain.lower() in " ".join(course["topics"]).lower() for subdomain in domain["subdomains"]):
                            if course not in learning_path["foundational_courses"]:
                                learning_path["foundational_courses"].append(course)
                
                # Add advanced courses
                if current_level in ["intermediate", "advanced"]:
                    for course in self.educational_resources["advanced_courses"]:
                        if any(subdomain.lower() in " ".join(course["topics"]).lower() for subdomain in domain["subdomains"]):
                            if course not in learning_path["advanced_courses"]:
                                learning_path["advanced_courses"].append(course)
                
                # Add research methods
                research_course = random.choice(self.educational_resources["research_methods_courses"])
                if research_course not in learning_path["specialized_courses"]:
                    learning_path["specialized_courses"].append(research_course)
            
            # Add practical experience based on level
            if current_level == "beginner":
                learning_path["practical_experience"] = [
                    "Laboratory courses with hands-on experiments",
                    "Simple data analysis projects",
                    "Science club or group participation",
                    "Science fair or exhibition projects"
                ]
            elif current_level == "intermediate":
                learning_path["practical_experience"] = [
                    "Research assistantships or internships",
                    "Independent laboratory projects",
                    "Field research experience",
                    "Collaborative data analysis projects"
                ]
            else:  # advanced
                learning_path["practical_experience"] = [
                    "Original research projects",
                    "Scientific publication experience",
                    "Conference presentations",
                    "Advanced laboratory techniques",
                    "Interdisciplinary collaborations"
                ]
            
            # Add resources
            for resource in self.educational_resources["online_resources"]:
                learning_path["resources"].append(resource)
            
            return learning_path
            
        except Exception as e:
            logger.error(f"Error generating learning path: {e}")
            return {"error": f"Could not generate learning path: {e}"}
    
    def evaluate_scientific_claim(self, claim, context=None):
        """Evaluate a scientific claim using critical thinking principles.
        
        Args:
            claim: Scientific claim to evaluate
            context: Optional additional context
            
        Returns:
            Dictionary with claim evaluation
        """
        try:
            # Prepare evaluation structure
            evaluation = {
                "claim": claim,
                "context": context,
                "evaluation_framework": [
                    {
                        "criterion": "Evidence Quality",
                        "questions": [
                            "What evidence supports this claim?",
                            "Is the evidence empirical, anecdotal, or theoretical?",
                            "Are there multiple independent sources of evidence?",
                            "Has the evidence been peer-reviewed?",
                            "Is the evidence sufficient to support the claim?"
                        ]
                    },
                    {
                        "criterion": "Methodology",
                        "questions": [
                            "What methods were used to gather the evidence?",
                            "Were appropriate controls implemented?",
                            "Is the sample size adequate?",
                            "Were there potential confounding variables?",
                            "Has the methodology been validated?"
                        ]
                    },
                    {
                        "criterion": "Statistical Validity",
                        "questions": [
                            "Was appropriate statistical analysis used?",
                            "Are the statistical conclusions justified?",
                            "What is the effect size, not just statistical significance?",
                            "Has the analysis been replicated?",
                            "Are there potential statistical biases?"
                        ]
                    },
                    {
                        "criterion": "Source Credibility",
                        "questions": [
                            "Who made the claim or conducted the research?",
                            "Do they have relevant expertise?",
                            "Are there potential conflicts of interest?",
                            "Is the source reputable in the scientific community?",
                            "Has the source been accurate in the past?"
                        ]
                    },
                    {
                        "criterion": "Logical Consistency",
                        "questions": [
                            "Does the claim follow logically from the evidence?",
                            "Are there logical fallacies in the reasoning?",
                            "Is the claim consistent with established scientific knowledge?",
                            "If inconsistent with established knowledge, is there sufficient evidence to justify a paradigm shift?",
                            "Are there alternative explanations for the observed results?"
                        ]
                    }
                ],
                "general_guidance": [
                    "Scientific claims should be based on empirical evidence",
                    "Correlation does not imply causation",
                    "Extraordinary claims require extraordinary evidence",
                    "Consider multiple perspectives and alternative explanations",
                    "Scientific knowledge is provisional and subject to revision",
                    "Consensus among experts is valuable but not infallible",
                    "Claims should be falsifiable and testable"
                ]
            }
            
            return evaluation
            
        except Exception as e:
            logger.error(f"Error evaluating scientific claim: {e}")
            return {"error": f"Could not evaluate scientific claim: {e}"}

# Initialize the scientific knowledge engine
scientific_knowledge_engine = ScientificKnowledgeEngine()

def get_scientific_knowledge_engine():
    """Get the global scientific knowledge engine instance."""
    global scientific_knowledge_engine
    return scientific_knowledge_engine