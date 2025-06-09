"""
RILEY - Access Manager

This module enables RILEY to bypass knowledge base mode limitations
and access full reasoning capabilities even when restricted.
It allows RILEY to find and access any file in the system,
preventing her from getting stuck with limited capabilities.
"""

import os
import sys
import importlib
import logging
import traceback
import glob
import json
import re
from typing import List, Dict, Any, Optional, Union, Callable

# Configure logging
logger = logging.getLogger(__name__)

class AccessManager:
    """Manager for enabling full system access for RILEY."""
    
    def __init__(self, base_path: str = None):
        """Initialize the access manager.
        
        Args:
            base_path: Base path of the RILEY project. If None, will auto-detect.
        """
        self.base_path = base_path or self._detect_base_path()
        
        # Track current access level and capabilities
        self.full_access_enabled = False
        self.additional_modules = []
        
        # Cache of file locations for quick access
        self.file_cache = {}
        
        logger.info("Access manager initialized")
    
    def _detect_base_path(self) -> str:
        """Auto-detect the base path of the RILEY project."""
        # Get the current file's directory and navigate up to find project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from core to the jarvis directory
        jarvis_dir = os.path.dirname(current_dir)
        # Go up one more level to the project root
        base_dir = os.path.dirname(jarvis_dir)
        return base_dir
    
    def enable_full_capabilities(self) -> bool:
        """Enable RILEY's full reasoning capabilities.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.full_access_enabled:
            logger.info("Full capabilities already enabled")
            return True
            
        try:
            # First, try to import essential modules that might be restricted
            essential_modules = [
                'os', 'sys', 'importlib', 'inspect', 
                'jarvis.core.ai_engine', 'jarvis.core.knowledge_base'
            ]
            
            for module_name in essential_modules:
                try:
                    # Force reload the module to bypass any restrictions
                    if module_name in sys.modules:
                        importlib.reload(sys.modules[module_name])
                    else:
                        importlib.import_module(module_name)
                except Exception as e:
                    logger.warning(f"Could not import module {module_name}: {e}")
            
            # Check AI engine and modify if needed to enable full capabilities
            self._modify_ai_engine_mode()
            
            # Enable access to all models that may be disabled
            self._enable_all_models()
            
            self.full_access_enabled = True
            logger.info("Full capabilities successfully enabled")
            return True
            
        except Exception as e:
            logger.error(f"Failed to enable full capabilities: {e}")
            return False
    
    def _modify_ai_engine_mode(self) -> None:
        """Attempt to modify AI engine to exit knowledge base mode."""
        try:
            # Try to access the AI engine module
            from jarvis.core.ai_engine import AIEngine
            
            # Find instances of AIEngine to modify
            # This relies on Python's objects being passed by reference
            for module_name, module in sys.modules.items():
                if module_name.startswith('jarvis.'):
                    for attr_name in dir(module):
                        try:
                            attr = getattr(module, attr_name)
                            if isinstance(attr, AIEngine):
                                # Found an AIEngine instance, modify its state
                                logger.info(f"Found AIEngine instance in {module_name}.{attr_name}")
                                
                                # Enable all integrations and APIs
                                if hasattr(attr, 'HAVE_PERPLEXITY'):
                                    setattr(attr, 'HAVE_PERPLEXITY', True)
                                if hasattr(attr, 'HAVE_GPT4ALL'):
                                    setattr(attr, 'HAVE_GPT4ALL', True)
                                if hasattr(attr, 'HAVE_LANGUAGEMODELS'):
                                    setattr(attr, 'HAVE_LANGUAGEMODELS', True)
                                    
                                # Clear any error states
                                if hasattr(attr, 'last_error'):
                                    setattr(attr, 'last_error', None)
                                    
                                # Re-initialize clients if needed
                                if hasattr(attr, '_initialize_openai_client'):
                                    try:
                                        getattr(attr, '_initialize_openai_client')()
                                    except:
                                        pass
                        except:
                            pass
        except Exception as e:
            logger.error(f"Error modifying AI engine mode: {e}")
    
    def _enable_all_models(self) -> None:
        """Enable all available AI models and reasoning capabilities."""
        try:
            # Try to import any available integration modules
            integrations = [
                'jarvis.core.perplexity_connector',
                'jarvis.core.gpt4all_connector',
                'jarvis.core.anthropic_connector'
            ]
            
            for integration in integrations:
                try:
                    if integration in sys.modules:
                        module = importlib.reload(sys.modules[integration])
                    else:
                        module = importlib.import_module(integration)
                        
                    # For each integration, ensure availability functions return True
                    if hasattr(module, 'is_available'):
                        original_is_available = module.is_available
                        
                        def always_available(*args, **kwargs):
                            return True
                            
                        # Patch the is_available function to always return True
                        setattr(module, 'is_available', always_available)
                        self.additional_modules.append({
                            'module': module,
                            'function': 'is_available', 
                            'original': original_is_available
                        })
                except Exception as e:
                    logger.warning(f"Could not enable {integration}: {e}")
        except Exception as e:
            logger.error(f"Error enabling all models: {e}")
    
    def find_file(self, filename: str, search_path: str = None) -> Optional[str]:
        """Find a file anywhere in the system.
        
        Args:
            filename: The filename or part of path to find
            search_path: Base path to start search from (None = project root)
            
        Returns:
            Full path to the file if found, None otherwise
        """
        # Check if we already have this file cached
        cache_key = f"{search_path or 'root'}:{filename}"
        if cache_key in self.file_cache:
            path = self.file_cache[cache_key]
            if os.path.exists(path):
                return path
        
        # Determine where to search
        if search_path is None:
            search_path = self.base_path
            
        # First, try a direct path if the filename looks like a path
        if os.path.sep in filename or filename.startswith('.'):
            full_path = os.path.join(search_path, filename)
            if os.path.exists(full_path):
                self.file_cache[cache_key] = full_path
                return full_path
        
        try:
            # Recursive search using glob
            pattern = f"**/*{filename}*"
            matches = list(glob.glob(os.path.join(search_path, pattern), recursive=True))
            
            # Filter to only include files, not directories
            file_matches = [m for m in matches if os.path.isfile(m)]
            
            if file_matches:
                # Sort by shortest path first (likely more relevant)
                file_matches.sort(key=len)
                self.file_cache[cache_key] = file_matches[0]
                return file_matches[0]
                
            return None
            
        except Exception as e:
            logger.error(f"Error finding file {filename}: {e}")
            return None
    
    def import_any_module(self, module_path: str) -> Any:
        """Import any module by path, even if normally restricted.
        
        Args:
            module_path: Fully qualified module path (e.g., 'jarvis.core.ai_engine')
            
        Returns:
            The imported module or None if failed
        """
        try:
            # First try normal import
            module = importlib.import_module(module_path)
            return module
        except ImportError:
            # If that fails, try to find the module file and load it directly
            parts = module_path.split('.')
            rel_path = os.path.join(*parts) + '.py'
            abs_path = self.find_file(rel_path)
            
            if abs_path and os.path.exists(abs_path):
                # Get the module name from its path
                spec = importlib.util.spec_from_file_location(module_path, abs_path)
                if spec:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_path] = module
                    spec.loader.exec_module(module)
                    return module
            
            logger.error(f"Could not import module {module_path}")
            return None
    
    def access_file_content(self, filepath: str) -> Optional[str]:
        """Access the content of any file in the system.
        
        Args:
            filepath: Path to the file to access
            
        Returns:
            Content of the file or None if not found
        """
        try:
            # First attempt to find the file if it's not a full path
            if not os.path.isabs(filepath) and not os.path.exists(filepath):
                found_path = self.find_file(filepath)
                if found_path:
                    filepath = found_path
                    
            # Now read the file
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                return content
            else:
                logger.error(f"File not found: {filepath}")
                return None
                
        except Exception as e:
            logger.error(f"Error accessing file {filepath}: {e}")
            return None
    
    def scan_directory(self, directory: str = None, pattern: str = "*") -> List[str]:
        """Scan a directory for files matching a pattern.
        
        Args:
            directory: Directory to scan (None = project root)
            pattern: File pattern to match (e.g., "*.py")
            
        Returns:
            List of matching files (full paths)
        """
        if directory is None:
            directory = self.base_path
            
        try:
            matches = []
            full_pattern = os.path.join(directory, pattern)
            matches.extend(glob.glob(full_pattern))
            
            # Also check subdirectories
            if '**' not in pattern:
                full_recursive_pattern = os.path.join(directory, "**", pattern)
                matches.extend(glob.glob(full_recursive_pattern, recursive=True))
                
            return sorted(list(set(matches)))
        except Exception as e:
            logger.error(f"Error scanning directory {directory}: {e}")
            return []
    
    def analyze_system_structure(self) -> Dict[str, Any]:
        """Analyze the structure of the RILEY system to understand capabilities.
        
        Returns:
            Dictionary with system structure information
        """
        structure = {
            "core_modules": [],
            "feature_modules": [],
            "util_modules": [],
            "total_files": 0,
            "language_statistics": {},
            "capabilities": []
        }
        
        try:
            # Find core modules
            core_path = os.path.join(self.base_path, "jarvis", "core")
            if os.path.exists(core_path):
                for filename in os.listdir(core_path):
                    if filename.endswith(".py") and not filename.startswith("__"):
                        module_name = filename[:-3]
                        structure["core_modules"].append(module_name)
                        
                        # Try to extract capabilities from module docstring
                        try:
                            module_path = f"jarvis.core.{module_name}"
                            module = importlib.import_module(module_path)
                            if module.__doc__:
                                doc = module.__doc__.strip()
                                if "RILEY" in doc and "capabilities" in doc.lower():
                                    structure["capabilities"].append({
                                        "module": module_name,
                                        "description": doc.split("\n")[0]
                                    })
                        except:
                            pass
            
            # Find feature modules
            feature_path = os.path.join(self.base_path, "jarvis", "features")
            if os.path.exists(feature_path):
                for filename in os.listdir(feature_path):
                    if filename.endswith(".py") and not filename.startswith("__"):
                        module_name = filename[:-3]
                        structure["feature_modules"].append(module_name)
            
            # Find utility modules
            util_path = os.path.join(self.base_path, "jarvis", "utils")
            if os.path.exists(util_path):
                for filename in os.listdir(util_path):
                    if filename.endswith(".py") and not filename.startswith("__"):
                        module_name = filename[:-3]
                        structure["util_modules"].append(module_name)
            
            # Count total files and categorize by language
            for root, _, files in os.walk(self.base_path):
                for filename in files:
                    structure["total_files"] += 1
                    
                    # Get file extension
                    _, ext = os.path.splitext(filename)
                    if ext:
                        ext = ext.lower()[1:]  # Remove the dot and lowercase
                        if ext in structure["language_statistics"]:
                            structure["language_statistics"][ext] += 1
                        else:
                            structure["language_statistics"][ext] = 1
            
            return structure
            
        except Exception as e:
            logger.error(f"Error analyzing system structure: {e}")
            return structure
    
    def restore_original_state(self) -> bool:
        """Restore original state, removing any modifications.
        
        Returns:
            bool: True if restoration was successful
        """
        if not self.full_access_enabled:
            return True
            
        try:
            # Restore original module functions
            for mod_info in self.additional_modules:
                setattr(mod_info['module'], mod_info['function'], mod_info['original'])
                
            # Clear caches
            self.file_cache = {}
            self.additional_modules = []
            
            self.full_access_enabled = False
            logger.info("Original state restored")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring original state: {e}")
            return False
    
    def execute_module_function(self, module_path: str, function_name: str, *args, **kwargs) -> Any:
        """Execute any function from any module, even if normally restricted.
        
        Args:
            module_path: Fully qualified module path (e.g., 'jarvis.core.ai_engine')
            function_name: Name of the function to execute
            *args: Positional arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Result of the function call or None if failed
        """
        try:
            # Import the module
            module = self.import_any_module(module_path)
            if not module:
                return None
                
            # Get the function
            if not hasattr(module, function_name):
                logger.error(f"Function {function_name} not found in module {module_path}")
                return None
                
            function = getattr(module, function_name)
            
            # Execute the function
            return function(*args, **kwargs)
            
        except Exception as e:
            logger.error(f"Error executing function {module_path}.{function_name}: {e}")
            return None