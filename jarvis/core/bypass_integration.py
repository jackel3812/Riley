"""
RILEY - Knowledge Base Bypass Integration

This module integrates the access manager into RILEY's AI engine,
allowing her to bypass knowledge base mode restrictions and access
her full reasoning capabilities. It also provides utilities to find
and access any file in the system when normal access is restricted.
"""

import os
import sys
import logging
import importlib
import inspect
from typing import Dict, List, Any, Optional, Tuple, Union

# Configure logging
logger = logging.getLogger(__name__)

# Try to import the access manager
try:
    from jarvis.core.access_manager import AccessManager
    access_manager = AccessManager()
    logger.info("Access manager loaded successfully")
except ImportError:
    logger.warning("Could not import access manager, trying alternative methods")
    access_manager = None

class BypassIntegration:
    """Integrates access manager bypass capabilities into RILEY's AI engine."""
    
    def __init__(self, riley_instance=None):
        """Initialize the bypass integration.
        
        Args:
            riley_instance: The main RILEY AI instance
        """
        self.riley = riley_instance
        self.bypass_enabled = False
        
        # Initialize or retrieve access manager
        global access_manager
        if access_manager is None:
            try:
                # Try to find and import the access manager module directly
                module_path = self._find_module_path('access_manager.py')
                if module_path:
                    # Import the module
                    spec = importlib.util.spec_from_file_location("access_manager", module_path)
                    if spec:
                        access_manager_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(access_manager_module)
                        
                        # Create an instance
                        access_manager = access_manager_module.AccessManager()
                        logger.info("Access manager loaded through direct import")
            except Exception as e:
                logger.error(f"Failed to import access manager: {e}")
                
                # Create a minimal access manager implementation
                access_manager = self._create_minimal_access_manager()
        
        self.access_manager = access_manager
        logger.info("Bypass integration initialized")
    
    def _find_module_path(self, module_filename: str) -> Optional[str]:
        """Find a module file in the project directories.
        
        Args:
            module_filename: The module filename to find
            
        Returns:
            Full path to the module file or None if not found
        """
        # Get the possible paths to look in
        current_dir = os.path.dirname(os.path.abspath(__file__))
        jarvis_dir = os.path.dirname(current_dir)
        
        # Places to look
        search_paths = [
            current_dir,  # current directory (core)
            jarvis_dir,   # jarvis directory
            os.path.join(jarvis_dir, "core"),
            os.path.join(jarvis_dir, "features"),
            os.path.join(jarvis_dir, "utils")
        ]
        
        for path in search_paths:
            full_path = os.path.join(path, module_filename)
            if os.path.exists(full_path):
                return full_path
                
        # Recursive search if needed
        for path in search_paths:
            for root, _, files in os.walk(path):
                if module_filename in files:
                    return os.path.join(root, module_filename)
                    
        return None
    
    def _create_minimal_access_manager(self) -> Any:
        """Create a minimal access manager implementation if the real one can't be loaded.
        
        Returns:
            A simple object with the necessary methods
        """
        class MinimalAccessManager:
            def __init__(self):
                self.full_access_enabled = False
                self.base_path = self._detect_base_path()
                
            def _detect_base_path(self) -> str:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                return os.path.dirname(os.path.dirname(current_dir))
                
            def enable_full_capabilities(self) -> bool:
                self.full_access_enabled = True
                return True
                
            def find_file(self, filename: str, search_path: str = None) -> Optional[str]:
                if search_path is None:
                    search_path = self.base_path
                    
                # Simple recursive file search
                for root, _, files in os.walk(search_path):
                    if filename in files:
                        return os.path.join(root, filename)
                        
                # Try partial matches
                for root, _, files in os.walk(search_path):
                    for file in files:
                        if filename in file:
                            return os.path.join(root, file)
                            
                return None
                
            def access_file_content(self, filepath: str) -> Optional[str]:
                if not os.path.exists(filepath):
                    found_path = self.find_file(filepath)
                    if found_path:
                        filepath = found_path
                        
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                        return f.read()
                        
                return None
                
            def analyze_system_structure(self) -> Dict[str, Any]:
                return {
                    "core_modules": [],
                    "feature_modules": [],
                    "util_modules": [],
                    "total_files": 0
                }
                
            def restore_original_state(self) -> bool:
                self.full_access_enabled = False
                return True
        
        return MinimalAccessManager()
    
    def enable_bypass(self) -> bool:
        """Enable bypass mode to access full capabilities.
        
        Returns:
            bool: True if bypass was successfully enabled
        """
        if self.bypass_enabled:
            logger.info("Bypass already enabled")
            return True
            
        # Enable full capabilities through access manager
        success = self.access_manager.enable_full_capabilities()
        
        if success:
            self.bypass_enabled = True
            
            # Try to modify the AI engine directly if we have access
            if self.riley:
                # Reset any error state
                if hasattr(self.riley, 'last_error'):
                    self.riley.last_error = None
                    
                # Set up API integrations
                self._integrate_with_riley()
                
            logger.info("Bypass successfully enabled")
        else:
            logger.error("Failed to enable bypass")
            
        return success
    
    def _integrate_with_riley(self) -> None:
        """Integrate bypass capabilities with RILEY's AI engine."""
        if not self.riley:
            return
            
        try:
            # Make all AI models available
            if hasattr(self.riley, 'HAVE_PERPLEXITY'):
                self.riley.HAVE_PERPLEXITY = True
            if hasattr(self.riley, 'HAVE_GPT4ALL'):
                self.riley.HAVE_GPT4ALL = True
            if hasattr(self.riley, 'HAVE_LANGUAGEMODELS'):
                self.riley.HAVE_LANGUAGEMODELS = True
                
            # Modify the process_input method to add bypass capabilities
            if hasattr(self.riley, 'process_input'):
                original_process_input = self.riley.process_input
                
                def enhanced_process_input(self, text_input, voice_input=False):
                    # Check for bypass command
                    if "enable full capabilities" in text_input.lower() or "bypass knowledge base mode" in text_input.lower():
                        result = self.bypass_integration.enable_bypass()
                        if result:
                            return "Full capabilities enabled. I am no longer restricted to knowledge base mode."
                        else:
                            return "I was unable to enable full capabilities. I'll try to answer using my current mode."
                    
                    # Check for file access command
                    if "find file" in text_input.lower() and ":" in text_input:
                        # Extract filename
                        filename = text_input.split(":", 1)[1].strip()
                        filepath = self.bypass_integration.access_manager.find_file(filename)
                        if filepath:
                            return f"I found the file at: {filepath}"
                        else:
                            return f"I could not find a file matching '{filename}'."
                    
                    # Check for file content command
                    if "show file" in text_input.lower() and ":" in text_input:
                        # Extract filename
                        filename = text_input.split(":", 1)[1].strip()
                        filepath = self.bypass_integration.access_manager.find_file(filename)
                        if filepath:
                            content = self.bypass_integration.access_manager.access_file_content(filepath)
                            if content:
                                # Limit content length for display
                                if len(content) > 1000:
                                    content = content[:997] + "..."
                                return f"Content of {filepath}:\n\n{content}"
                            else:
                                return f"I found the file at {filepath} but could not read its content."
                        else:
                            return f"I could not find a file matching '{filename}'."
                    
                    # If not a special command, use the original method
                    return original_process_input(text_input, voice_input)
                
                # Add the bypass integration to the RILEY instance
                setattr(self.riley, 'bypass_integration', self)
                
                # Replace the original method with the enhanced one
                # We need to create a bound method since we're replacing a method
                bound_method = enhanced_process_input.__get__(self.riley, type(self.riley))
                setattr(self.riley, 'process_input', bound_method)
                
                logger.info("Successfully integrated bypass with RILEY's process_input method")
                
        except Exception as e:
            logger.error(f"Error integrating with RILEY: {e}")
    
    def find_file(self, filename: str) -> Optional[str]:
        """Find a file in the system.
        
        Args:
            filename: The filename to find
            
        Returns:
            Full path to the file or None if not found
        """
        return self.access_manager.find_file(filename)
    
    def get_file_content(self, filename: str) -> Optional[str]:
        """Get the content of a file.
        
        Args:
            filename: The filename to get content from
            
        Returns:
            Content of the file or None if not found
        """
        filepath = self.find_file(filename)
        if filepath:
            return self.access_manager.access_file_content(filepath)
        return None
    
    def get_module_code(self, module_name: str) -> Optional[str]:
        """Get the source code of a Python module.
        
        Args:
            module_name: The module name (e.g., 'jarvis.core.ai_engine')
            
        Returns:
            Source code of the module or None if not found
        """
        try:
            # First try to import the module
            module = importlib.import_module(module_name)
            
            # Get the module file path
            module_file = inspect.getfile(module)
            
            # Read the source code
            with open(module_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
                
            return source_code
            
        except Exception as e:
            # If import fails, try to find the file directly
            parts = module_name.split('.')
            filename = parts[-1] + '.py'
            filepath = self.find_file(filename)
            
            if filepath:
                return self.access_manager.access_file_content(filepath)
                
            logger.error(f"Could not get source code for module {module_name}: {e}")
            return None
    
    def analyze_system(self) -> Dict[str, Any]:
        """Analyze the RILEY system to understand capabilities and structure.
        
        Returns:
            Dictionary with system information
        """
        return self.access_manager.analyze_system_structure()
    
    def disable_bypass(self) -> bool:
        """Disable bypass mode and restore original state.
        
        Returns:
            bool: True if successful
        """
        if not self.bypass_enabled:
            return True
            
        success = self.access_manager.restore_original_state()
        
        if success:
            self.bypass_enabled = False
            logger.info("Bypass disabled")
        else:
            logger.error("Failed to disable bypass")
            
        return success

# Create global instance
bypass_integration = BypassIntegration()

def enable_full_capabilities() -> bool:
    """Enable RILEY's full capabilities, bypassing knowledge base mode.
    
    Returns:
        bool: True if successful
    """
    return bypass_integration.enable_bypass()

def find_system_file(filename: str) -> Optional[str]:
    """Find any file in the system.
    
    Args:
        filename: Name of the file to find
        
    Returns:
        Full path to the file or None if not found
    """
    return bypass_integration.find_file(filename)

def get_file_content(filename: str) -> Optional[str]:
    """Get the content of any file in the system.
    
    Args:
        filename: Name of the file to get content from
        
    Returns:
        Content of the file or None if not found
    """
    return bypass_integration.get_file_content(filename)