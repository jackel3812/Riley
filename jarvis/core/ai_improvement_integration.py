"""
RILEY - AI Self-Improvement Integration

This module integrates the self-improvement capabilities into RILEY's core AI engine,
allowing it to analyze interactions, detect opportunities for enhancement,
and autonomously improve its own code and capabilities.
"""

import os
import sys
import logging
import json
import time
import importlib
from typing import Dict, List, Any, Optional, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class AIImprovement:
    """Integrates self-improvement capabilities into RILEY."""
    
    def __init__(self, riley_instance=None):
        """Initialize the AI improvement integration.
        
        Args:
            riley_instance: The main RILEY AI instance
        """
        self.riley = riley_instance
        self.self_improvement_enabled = True
        self.last_improvement_check = time.time() - 3600  # Start ready to check
        self.improvement_check_interval = 3600  # Once per hour
        
        # Import self-improvement modules
        try:
            from jarvis.features.self_improvement import SelfImprovementEngine
            self.improvement_engine = SelfImprovementEngine()
            logger.info("Self-improvement engine loaded successfully")
        except ImportError:
            self.improvement_engine = None
            logger.warning("Self-improvement engine not available")
            
        try:
            from jarvis.features.code_generation import CodeGenerator
            self.code_generator = CodeGenerator()
            logger.info("Code generator loaded successfully")
        except ImportError:
            self.code_generator = None
            logger.warning("Code generator not available")
            
        # Maintain improvement statistics
        self.improvement_stats = {
            "improvements_made": 0,
            "modules_created": 0,
            "last_improvement": None,
            "improvement_log": []
        }
    
    def can_check_improvements(self) -> bool:
        """Check if it's time to look for improvement opportunities.
        
        Returns:
            bool: True if should check for improvements
        """
        if not self.self_improvement_enabled:
            return False
            
        time_since_last = time.time() - self.last_improvement_check
        return time_since_last >= self.improvement_check_interval
    
    def check_for_improvement_opportunities(self) -> List[Dict[str, Any]]:
        """Check for opportunities to improve RILEY's codebase.
        
        Returns:
            List of improvement opportunities
        """
        if not self.can_check_improvements():
            return []
            
        opportunities = []
        self.last_improvement_check = time.time()
        
        if not self.code_generator:
            logger.warning("Cannot check for code improvements: Code generator not available")
            return opportunities
            
        try:
            # Look for improvement opportunities in core modules
            base_path = self.code_generator._detect_base_path()
            core_path = os.path.join(base_path, "jarvis", "core")
            features_path = os.path.join(base_path, "jarvis", "features")
            
            # Analyze core modules
            for filename in os.listdir(core_path):
                if filename.endswith(".py") and filename not in ["__init__.py", "ai_improvement_integration.py"]:
                    module_path = os.path.join(core_path, filename)
                    suggestions = self.code_generator.suggest_code_improvements(module_path)
                    
                    if suggestions:
                        # Add module context to each suggestion
                        for suggestion in suggestions:
                            suggestion["module"] = f"jarvis.core.{filename[:-3]}"
                            
                        opportunities.extend(suggestions)
            
            # Check for feature gap opportunities based on user interactions
            if hasattr(self.riley, "learning") and hasattr(self.riley.learning, "get_trending_topics"):
                trending_topics = self.riley.learning.get_trending_topics(5)
                
                for topic in trending_topics:
                    # Check if we have a feature module for this topic
                    if self._should_create_feature_for_topic(topic):
                        opportunities.append({
                            "type": "new_feature",
                            "topic": topic["topic"],
                            "description": f"Create new feature module for frequently requested topic: {topic['topic']}",
                            "priority": "high" if topic["frequency"] > 5 else "medium"
                        })
        
        except Exception as e:
            logger.error(f"Error checking for improvement opportunities: {e}")
            
        logger.info(f"Found {len(opportunities)} improvement opportunities")
        return opportunities
    
    def _should_create_feature_for_topic(self, topic: Dict[str, Any]) -> bool:
        """Determine if a new feature module should be created for a topic.
        
        Args:
            topic: Topic information including frequency
            
        Returns:
            bool: True if should create feature
        """
        # Simple implementation - check if topic appears in any existing feature
        topic_name = topic["topic"].lower()
        
        try:
            base_path = self.code_generator._detect_base_path()
            features_path = os.path.join(base_path, "jarvis", "features")
            
            for filename in os.listdir(features_path):
                if filename.endswith(".py") and topic_name in filename.lower():
                    # Already have a feature for this topic
                    return False
                    
                # Check file contents
                if filename.endswith(".py"):
                    try:
                        with open(os.path.join(features_path, filename), 'r') as f:
                            content = f.read().lower()
                            if topic_name in content and "class" in content and topic_name in content.split("class")[1]:
                                # Topic is already covered in this feature
                                return False
                    except:
                        pass
        except:
            pass
            
        # If topic frequency is high enough, create a feature
        return topic["frequency"] >= 3
    
    def apply_improvement(self, opportunity: Dict[str, Any]) -> Tuple[bool, str]:
        """Apply an improvement to RILEY's codebase.
        
        Args:
            opportunity: The improvement opportunity to apply
            
        Returns:
            Tuple of (success, message)
        """
        if not self.self_improvement_enabled:
            return False, "Self-improvement is disabled"
            
        if opportunity["type"] == "new_feature":
            return self._create_new_feature_module(opportunity)
        elif opportunity["type"] in ["fix_issue", "enhancement", "documentation", "code_quality"]:
            # Create an improvement record
            improvement = {
                "file": opportunity.get("file"),
                "type": "code_replacement" if "old_code" in opportunity else opportunity["type"],
                "description": opportunity.get("description", "Code improvement")
            }
            
            # Add appropriate fields based on type
            if "old_code" in opportunity and "new_code" in opportunity:
                improvement["old_code"] = opportunity["old_code"]
                improvement["new_code"] = opportunity["new_code"]
                
            # Apply the improvement
            if self.improvement_engine:
                success, message = self.improvement_engine.modify_existing_module(
                    improvement["file"],
                    improvement["description"],
                    # Assume we have the new code content
                    improvement.get("new_code", "# Improved code")
                )
                
                if success:
                    self.improvement_stats["improvements_made"] += 1
                    self.improvement_stats["last_improvement"] = time.time()
                    self.improvement_stats["improvement_log"].append({
                        "timestamp": time.time(),
                        "type": improvement["type"],
                        "file": improvement["file"],
                        "description": improvement["description"]
                    })
                
                return success, message
            elif self.code_generator:
                success, message = self.code_generator.apply_improvement(improvement)
                
                if success:
                    self.improvement_stats["improvements_made"] += 1
                    self.improvement_stats["last_improvement"] = time.time()
                    self.improvement_stats["improvement_log"].append({
                        "timestamp": time.time(),
                        "type": improvement["type"],
                        "file": improvement["file"],
                        "description": improvement["description"]
                    })
                
                return success, message
            else:
                return False, "No improvement engine or code generator available"
        else:
            return False, f"Unknown improvement type: {opportunity['type']}"
    
    def _create_new_feature_module(self, opportunity: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a new feature module based on an opportunity.
        
        Args:
            opportunity: The new feature opportunity
            
        Returns:
            Tuple of (success, message)
        """
        topic = opportunity["topic"]
        module_name = topic.replace(" ", "_").lower()
        
        # Create a basic module description
        module_description = {
            "name": topic.title(),
            "purpose": f"This module provides {topic} capabilities for RILEY.",
            "imports": [
                "import os",
                "import sys",
                "import logging",
                "from typing import Dict, List, Any, Optional"
            ],
            "classes": [
                {
                    "name": f"{topic.title().replace(' ', '')}Manager",
                    "purpose": f"Manages {topic} functionality for RILEY.",
                    "attributes": [
                        {
                            "name": "logger",
                            "type": "logging.Logger",
                            "description": "Logger instance"
                        }
                    ],
                    "methods": [
                        {
                            "name": "__init__",
                            "purpose": "Initialize the manager",
                            "params": [],
                            "code_logic": "self.logger = logging.getLogger(__name__)\nself.logger.info(f\"{topic.title()} manager initialized\")"
                        },
                        {
                            "name": f"process_{module_name}",
                            "purpose": f"Process a {topic} request",
                            "params": [
                                {
                                    "name": "request",
                                    "type": "Dict[str, Any]",
                                    "description": f"The {topic} request parameters"
                                }
                            ],
                            "return_type": "Dict[str, Any]",
                            "code_logic": f"self.logger.info(f\"Processing {topic} request: {{request}}\")\n\n# TODO: Implement {topic} processing logic\n\nreturn {{\n    \"status\": \"success\",\n    \"result\": f\"Processed {topic} request\"\n}}"
                        }
                    ]
                }
            ]
        }
        
        # Generate the module code
        if self.code_generator:
            module_code = self.code_generator.generate_module_from_description(module_description)
            
            # Create the module file
            if self.improvement_engine:
                success = self.improvement_engine.create_new_module(
                    module_name=module_name,
                    module_purpose=module_description["purpose"],
                    code_content=module_code,
                    module_type="feature"
                )
                
                if success:
                    self.improvement_stats["modules_created"] += 1
                    self.improvement_stats["last_improvement"] = time.time()
                    self.improvement_stats["improvement_log"].append({
                        "timestamp": time.time(),
                        "type": "new_module",
                        "name": module_name,
                        "description": f"Created new feature module for {topic}"
                    })
                    
                    return True, f"Successfully created new feature module for {topic}"
                else:
                    return False, f"Failed to create module for {topic}"
            else:
                # Use the detector method to find the base path
                base_path = self.code_generator._detect_base_path()
                features_path = os.path.join(base_path, "jarvis", "features")
                module_filename = f"{module_name}.py"
                
                try:
                    with open(os.path.join(features_path, module_filename), 'w') as f:
                        f.write(module_code)
                        
                    self.improvement_stats["modules_created"] += 1
                    self.improvement_stats["last_improvement"] = time.time()
                    self.improvement_stats["improvement_log"].append({
                        "timestamp": time.time(),
                        "type": "new_module",
                        "name": module_name,
                        "description": f"Created new feature module for {topic}"
                    })
                    
                    return True, f"Successfully created new feature module for {topic}"
                except Exception as e:
                    logger.error(f"Error creating module file: {e}")
                    return False, f"Error creating module file: {str(e)}"
        else:
            return False, "Code generator not available"
    
    def get_improvement_statistics(self) -> Dict[str, Any]:
        """Get statistics about RILEY's self-improvement activities.
        
        Returns:
            Dictionary with improvement statistics
        """
        stats = self.improvement_stats.copy()
        
        # Add stats from improvement engine if available
        if self.improvement_engine:
            engine_stats = self.improvement_engine.get_improvement_statistics()
            stats["engine_stats"] = engine_stats
            
        return stats
    
    def process_improvement_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request for RILEY to improve itself.
        
        Args:
            request: The improvement request
            
        Returns:
            Response with results of the improvement attempt
        """
        if not self.self_improvement_enabled:
            return {
                "status": "error",
                "message": "Self-improvement is currently disabled"
            }
            
        request_type = request.get("type", "")
        
        if request_type == "create_module":
            # Request to create a new module
            if not self.improvement_engine or not self.code_generator:
                return {
                    "status": "error",
                    "message": "Required improvement components not available"
                }
                
            module_name = request.get("name", "")
            module_purpose = request.get("purpose", "")
            module_type = request.get("module_type", "feature")
            
            # Generate module code from description
            module_description = {
                "name": module_name,
                "purpose": module_purpose,
                "imports": request.get("imports", []),
                "classes": request.get("classes", []),
                "functions": request.get("functions", [])
            }
            
            module_code = self.code_generator.generate_module_from_description(module_description)
            
            # Create the module
            success = self.improvement_engine.create_new_module(
                module_name=module_name,
                module_purpose=module_purpose,
                code_content=module_code,
                module_type=module_type
            )
            
            if success:
                return {
                    "status": "success",
                    "message": f"Successfully created module {module_name}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to create module {module_name}"
                }
        elif request_type == "improve_module":
            # Request to improve an existing module
            module_path = request.get("path", "")
            improvement_description = request.get("description", "")
            new_code = request.get("new_code", "")
            
            if not module_path or not os.path.exists(module_path):
                return {
                    "status": "error",
                    "message": f"Module not found: {module_path}"
                }
                
            if not self.improvement_engine:
                return {
                    "status": "error",
                    "message": "Improvement engine not available"
                }
                
            success = self.improvement_engine.modify_existing_module(
                module_path=module_path,
                improvement_description=improvement_description,
                new_code=new_code
            )
            
            if success:
                return {
                    "status": "success",
                    "message": f"Successfully improved module {module_path}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to improve module {module_path}"
                }
        elif request_type == "analyze_code":
            # Request to analyze code quality
            if not self.code_generator:
                return {
                    "status": "error",
                    "message": "Code generator not available"
                }
                
            code = request.get("code", "")
            if not code:
                return {
                    "status": "error",
                    "message": "No code provided for analysis"
                }
                
            analysis = self.code_generator.analyze_code(code)
            return {
                "status": "success",
                "analysis": analysis
            }
        elif request_type == "check_opportunities":
            # Request to check for improvement opportunities
            opportunities = self.check_for_improvement_opportunities()
            return {
                "status": "success",
                "opportunities": opportunities
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown improvement request type: {request_type}"
            }
    
    def toggle_self_improvement(self, enabled: bool) -> Dict[str, Any]:
        """Enable or disable RILEY's self-improvement capabilities.
        
        Args:
            enabled: Whether self-improvement should be enabled
            
        Returns:
            Status response
        """
        previous_state = self.self_improvement_enabled
        self.self_improvement_enabled = enabled
        
        return {
            "status": "success",
            "previous_state": previous_state,
            "current_state": self.self_improvement_enabled,
            "message": f"Self-improvement {'enabled' if enabled else 'disabled'}"
        }