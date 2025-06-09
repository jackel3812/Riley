#!/usr/bin/env python3
"""
RILEY - Automatic Full Capability Enabler

This script automatically enables RILEY's full reasoning capabilities by:
1. Patching the AI engine to bypass knowledge base mode restrictions
2. Enabling access to all available AI models
3. Setting up the file system access capabilities

Usage:
  python auto_enabler.py

This will silently integrate with the running RILEY instance.
"""

import os
import sys
import time
import logging
import importlib.util
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('riley_enabler.log')
    ]
)
logger = logging.getLogger("riley_enabler")

def find_module_path(module_name):
    """Find a module in the RILEY project structure."""
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up to project root
    project_root = os.path.dirname(os.path.dirname(current_dir))
    
    # Convert module name to path
    parts = module_name.split('.')
    rel_path = os.path.join(*parts) + '.py'
    
    # Check in standard locations
    standard_path = os.path.join(project_root, rel_path)
    if os.path.exists(standard_path):
        return standard_path
        
    # If not found, do a more thorough search
    for root, dirs, files in os.walk(project_root):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'env']]
        
        # Check for the file
        if os.path.basename(rel_path) in files:
            return os.path.join(root, os.path.basename(rel_path))
            
    return None

def import_module_from_path(module_name, file_path):
    """Import a module from a file path."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if not spec:
            logger.error(f"Could not create spec for {module_name} from {file_path}")
            return None
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        logger.error(f"Error importing {module_name} from {file_path}: {e}")
        logger.error(traceback.format_exc())
        return None

def find_and_import_module(module_name):
    """Find and import a module by name."""
    try:
        # Try standard import first
        return importlib.import_module(module_name)
    except ImportError:
        # If that fails, try to find and import manually
        file_path = find_module_path(module_name)
        if file_path:
            return import_module_from_path(module_name, file_path)
        else:
            logger.error(f"Could not find module {module_name}")
            return None

def get_running_riley_instance():
    """Attempt to find a running RILEY instance."""
    # Check if the AI engine is already imported
    if 'jarvis.core.ai_engine' in sys.modules:
        module = sys.modules['jarvis.core.ai_engine']
        # Look for AIEngine instances
        for name in dir(module):
            obj = getattr(module, name)
            if name == 'AIEngine' or (hasattr(obj, '__class__') and 
                                     obj.__class__.__name__ == 'AIEngine'):
                logger.info(f"Found AIEngine class or instance: {name}")
                return obj
    
    # If not already imported, try to find it
    module = find_and_import_module('jarvis.core.ai_engine')
    if module and hasattr(module, 'AIEngine'):
        return module.AIEngine
        
    # Check in main module
    if 'main' in sys.modules:
        main_module = sys.modules['main']
        for name in dir(main_module):
            obj = getattr(main_module, name)
            if hasattr(obj, '__class__') and obj.__class__.__name__ == 'AIEngine':
                logger.info(f"Found AIEngine instance in main module: {name}")
                return obj
                
    return None

def enable_access_manager():
    """Enable the access manager to provide full file system access."""
    try:
        # Import our modules
        access_manager_path = find_module_path('jarvis.core.access_manager')
        if access_manager_path:
            access_manager_module = import_module_from_path('jarvis.core.access_manager', 
                                                          access_manager_path)
            if access_manager_module:
                # Create access manager instance
                access_manager = access_manager_module.AccessManager()
                # Enable full capabilities
                success = access_manager.enable_full_capabilities()
                if success:
                    logger.info("Successfully enabled access manager capabilities")
                    return access_manager
                else:
                    logger.error("Failed to enable access manager capabilities")
        else:
            logger.error("Could not find access_manager module")
            
    except Exception as e:
        logger.error(f"Error enabling access manager: {e}")
        logger.error(traceback.format_exc())
        
    return None

def enable_bypass_integration(riley_instance=None):
    """Enable the bypass integration to allow full reasoning capabilities."""
    try:
        # Import bypass integration
        bypass_path = find_module_path('jarvis.core.bypass_integration')
        if bypass_path:
            bypass_module = import_module_from_path('jarvis.core.bypass_integration', 
                                                  bypass_path)
            if bypass_module:
                # Create new integration with RILEY instance
                if hasattr(bypass_module, 'BypassIntegration'):
                    bypass = bypass_module.BypassIntegration(riley_instance)
                    # Enable bypass
                    success = bypass.enable_bypass()
                    if success:
                        logger.info("Successfully enabled bypass integration")
                        return bypass
                    else:
                        logger.error("Failed to enable bypass integration")
                elif hasattr(bypass_module, 'bypass_integration'):
                    # Use existing instance
                    bypass = bypass_module.bypass_integration
                    # Enable bypass
                    success = bypass.enable_bypass()
                    if success:
                        logger.info("Successfully enabled existing bypass integration")
                        return bypass
                    else:
                        logger.error("Failed to enable existing bypass integration")
        else:
            logger.error("Could not find bypass_integration module")
            
    except Exception as e:
        logger.error(f"Error enabling bypass integration: {e}")
        logger.error(traceback.format_exc())
        
    return None

def patch_ai_engine():
    """Patch the AI engine to enable full reasoning capabilities."""
    try:
        # Find running RILEY instance or class
        riley = get_running_riley_instance()
        
        if riley:
            logger.info(f"Found RILEY instance: {riley}")
            
            # Enable bypass integration
            bypass = enable_bypass_integration(riley)
            
            if not bypass:
                # If bypass integration failed, try direct access manager
                access_manager = enable_access_manager()
                
                if access_manager:
                    logger.info("Using direct access manager as fallback")
                    # Directly modify RILEY if it's an instance
                    if hasattr(riley, 'HAVE_PERPLEXITY'):
                        riley.HAVE_PERPLEXITY = True
                    if hasattr(riley, 'HAVE_GPT4ALL'):
                        riley.HAVE_GPT4ALL = True
                    if hasattr(riley, 'HAVE_LANGUAGEMODELS'):
                        riley.HAVE_LANGUAGEMODELS = True
                        
                    logger.info("Successfully patched RILEY capabilities directly")
                    return True
            else:
                logger.info("Successfully patched RILEY with bypass integration")
                return True
        else:
            logger.warning("Could not find RILEY instance or class")
            
            # Try generic enabling of components
            bypass = enable_bypass_integration()
            if bypass:
                logger.info("Enabled bypass integration without RILEY instance")
                return True
                
            access_manager = enable_access_manager()
            if access_manager:
                logger.info("Enabled access manager without RILEY instance")
                return True
                
    except Exception as e:
        logger.error(f"Error patching AI engine: {e}")
        logger.error(traceback.format_exc())
        
    return False

def run_continuous_monitor():
    """Run a continuous monitor to ensure RILEY stays enabled."""
    enabled = False
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        if not enabled:
            logger.info(f"Attempting to enable RILEY capabilities (attempt {retry_count+1}/{max_retries})")
            enabled = patch_ai_engine()
            
            if enabled:
                logger.info("Successfully enabled RILEY capabilities!")
                break
            else:
                logger.warning(f"Failed to enable RILEY capabilities on attempt {retry_count+1}")
                retry_count += 1
                
        time.sleep(5)  # Wait before next check
        
    if not enabled:
        logger.error("Failed to enable RILEY capabilities after maximum retries")
    else:
        logger.info("RILEY now has full capabilities enabled")
        
    return enabled

if __name__ == "__main__":
    logger.info("Starting RILEY capability enabler")
    success = run_continuous_monitor()
    
    if success:
        logger.info("RILEY capability enabler completed successfully")
        sys.exit(0)
    else:
        logger.error("RILEY capability enabler failed")
        sys.exit(1)