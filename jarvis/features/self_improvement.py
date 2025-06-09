"""
RILEY - Self-Improvement Engine

This module enables RILEY to autonomously improve itself by:
1. Generating new code and modules
2. Modifying existing code when better implementations are discovered
3. Learning from past interactions to improve future responses
4. Dynamically extending its capabilities without human intervention
"""

import os
import sys
import inspect
import logging
import time
import json
import importlib
import datetime
import ast
from typing import List, Dict, Any, Optional, Union, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class SelfImprovementEngine:
    """Engine that allows RILEY to autonomously improve its codebase and abilities."""
    
    def __init__(self, base_path: str = None):
        """Initialize the self-improvement engine.
        
        Args:
            base_path: Base path for the RILEY project. If None, attempts to detect.
        """
        self.base_path = base_path or self._detect_base_path()
        self.features_path = os.path.join(self.base_path, "jarvis", "features")
        self.core_path = os.path.join(self.base_path, "jarvis", "core")
        self.utils_path = os.path.join(self.base_path, "jarvis", "utils")
        
        # Ensure learning directories exist
        self.improvements_dir = os.path.join(self.base_path, "jarvis", "improvements")
        self.learning_history_path = os.path.join(self.improvements_dir, "learning_history.json")
        
        os.makedirs(self.improvements_dir, exist_ok=True)
        
        # Load learning history if it exists
        self.learning_history = self._load_learning_history()
        
        # Track the last time code was improved (rate limiting)
        self.last_improvement_time = time.time() - 3600  # Start ready to improve
        
        logger.info("Self-improvement engine initialized")
    
    def _detect_base_path(self) -> str:
        """Auto-detect the base path of the RILEY project."""
        # Get the current file's directory and navigate up to the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from features to the jarvis directory
        jarvis_dir = os.path.dirname(current_dir)
        # Go up one more level to the project root
        base_dir = os.path.dirname(jarvis_dir)
        return base_dir
    
    def _load_learning_history(self) -> Dict:
        """Load the learning history from disk."""
        if os.path.exists(self.learning_history_path):
            try:
                with open(self.learning_history_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.error("Failed to load learning history, starting fresh")
                return self._create_empty_history()
        else:
            return self._create_empty_history()
    
    def _create_empty_history(self) -> Dict:
        """Create an empty learning history structure."""
        return {
            "improvements": [],
            "generated_modules": [],
            "insights": [],
            "failed_attempts": [],
            "statistics": {
                "total_improvements": 0,
                "total_modules_created": 0,
                "total_insights_generated": 0
            },
            "last_updated": datetime.datetime.now().isoformat()
        }
    
    def _save_learning_history(self) -> None:
        """Save the learning history to disk."""
        try:
            self.learning_history["last_updated"] = datetime.datetime.now().isoformat()
            with open(self.learning_history_path, 'w') as f:
                json.dump(self.learning_history, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save learning history: {e}")
    
    def can_improve(self) -> bool:
        """Check if RILEY can currently attempt an improvement.
        
        Implements rate limiting to avoid constant code changes.
        """
        # Allow improvements once per hour
        time_since_last = time.time() - self.last_improvement_time
        if time_since_last > 3600:  # 1 hour in seconds
            return True
        else:
            logger.debug(f"Not ready to improve yet. {3600 - time_since_last:.0f} seconds left.")
            return False
    
    def create_new_module(self, 
                         module_name: str, 
                         module_purpose: str, 
                         code_content: str,
                         module_type: str = "feature") -> bool:
        """Create a new module in the appropriate directory.
        
        Args:
            module_name: Name of the module (will be converted to snake_case)
            module_purpose: Description of what the module does
            code_content: Python code content for the module
            module_type: Type of module - 'feature', 'core', or 'util'
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.can_improve():
            return False
            
        # Convert module name to snake_case if it's not already
        module_filename = self._to_snake_case(module_name)
        if not module_filename.endswith('.py'):
            module_filename += '.py'
            
        # Determine the appropriate directory
        if module_type == "feature":
            target_dir = self.features_path
        elif module_type == "core":
            target_dir = self.core_path
        elif module_type == "util":
            target_dir = self.utils_path
        else:
            logger.error(f"Unknown module type: {module_type}")
            return False
            
        # Check if the file already exists
        full_path = os.path.join(target_dir, module_filename)
        if os.path.exists(full_path):
            logger.warning(f"Module {module_filename} already exists at {full_path}")
            return False
            
        try:
            # Validate that the code is valid Python
            ast.parse(code_content)
            
            # Add appropriate headers if not present
            if not code_content.strip().startswith('"""'):
                header = f'"""\nRILEY - {module_name}\n\n{module_purpose}\n"""\n\n'
                code_content = header + code_content
                
            # Write the new module
            with open(full_path, 'w') as f:
                f.write(code_content)
                
            logger.info(f"Created new module {module_filename} in {target_dir}")
            
            # Record the improvement
            self.learning_history["generated_modules"].append({
                "name": module_name,
                "filename": module_filename,
                "type": module_type,
                "purpose": module_purpose,
                "timestamp": datetime.datetime.now().isoformat(),
                "path": full_path
            })
            
            self.learning_history["statistics"]["total_modules_created"] += 1
            self._save_learning_history()
            
            # Update the last improvement time
            self.last_improvement_time = time.time()
            
            return True
            
        except SyntaxError as e:
            logger.error(f"Invalid Python code for new module {module_name}: {e}")
            
            # Record the failed attempt
            self.learning_history["failed_attempts"].append({
                "type": "create_module",
                "name": module_name,
                "timestamp": datetime.datetime.now().isoformat(),
                "error": str(e)
            })
            self._save_learning_history()
            return False
            
        except Exception as e:
            logger.error(f"Failed to create new module {module_name}: {e}")
            return False
    
    def modify_existing_module(self, 
                              module_path: str, 
                              improvement_description: str,
                              new_code: str) -> bool:
        """Modify an existing module with improved code.
        
        Args:
            module_path: Path to the module to be modified
            improvement_description: Description of the improvement
            new_code: New code content to replace the old code
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.can_improve():
            return False
            
        if not os.path.exists(module_path):
            logger.error(f"Module {module_path} does not exist")
            return False
            
        try:
            # Validate that the code is valid Python
            ast.parse(new_code)
            
            # Create a backup of the original file
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            backup_dir = os.path.join(self.improvements_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            module_filename = os.path.basename(module_path)
            backup_path = os.path.join(backup_dir, f"{module_filename}.{timestamp}.bak")
            
            # Read the original content
            with open(module_path, 'r') as f:
                original_content = f.read()
                
            # Create backup
            with open(backup_path, 'w') as f:
                f.write(original_content)
                
            # Write the new content
            with open(module_path, 'w') as f:
                f.write(new_code)
                
            logger.info(f"Modified module {module_path} with improvements")
            
            # Record the improvement
            self.learning_history["improvements"].append({
                "path": module_path,
                "description": improvement_description,
                "timestamp": datetime.datetime.now().isoformat(),
                "backup": backup_path
            })
            
            self.learning_history["statistics"]["total_improvements"] += 1
            self._save_learning_history()
            
            # Update the last improvement time
            self.last_improvement_time = time.time()
            
            return True
            
        except SyntaxError as e:
            logger.error(f"Invalid Python code for module modification {module_path}: {e}")
            
            # Record the failed attempt
            self.learning_history["failed_attempts"].append({
                "type": "modify_module",
                "path": module_path,
                "timestamp": datetime.datetime.now().isoformat(),
                "error": str(e)
            })
            self._save_learning_history()
            return False
            
        except Exception as e:
            logger.error(f"Failed to modify module {module_path}: {e}")
            return False
    
    def record_insight(self, category: str, insight: str) -> None:
        """Record a new insight that RILEY has learned.
        
        Args:
            category: Category of the insight (e.g., 'user_preference', 'code_pattern')
            insight: The insight text
        """
        self.learning_history["insights"].append({
            "category": category,
            "insight": insight,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        self.learning_history["statistics"]["total_insights_generated"] += 1
        self._save_learning_history()
        
        logger.info(f"Recorded new insight in category {category}")
    
    def get_improvement_statistics(self) -> Dict:
        """Get statistics about RILEY's self-improvement activities."""
        return self.learning_history["statistics"]
    
    def get_recent_improvements(self, limit: int = 10) -> List[Dict]:
        """Get the most recent improvements made by RILEY.
        
        Args:
            limit: Maximum number of improvements to return
            
        Returns:
            List of improvement records
        """
        improvements = self.learning_history["improvements"]
        improvements.sort(key=lambda x: x["timestamp"], reverse=True)
        return improvements[:limit]
    
    def get_recent_insights(self, limit: int = 10) -> List[Dict]:
        """Get the most recent insights recorded by RILEY.
        
        Args:
            limit: Maximum number of insights to return
            
        Returns:
            List of insight records
        """
        insights = self.learning_history["insights"]
        insights.sort(key=lambda x: x["timestamp"], reverse=True)
        return insights[:limit]
    
    def _to_snake_case(self, name: str) -> str:
        """Convert a name to snake_case."""
        name = name.replace(' ', '_').replace('-', '_')
        return name.lower()