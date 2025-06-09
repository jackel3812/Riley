"""
RILEY - Web Learning Module

This module enables RILEY to learn from any website, including:
1. Extracting structured knowledge from Wikipedia
2. Learning from technical documentation 
3. Gathering code examples and patterns from developer sites
4. Building a continuously expanding knowledge base
5. Generating new capabilities based on web-extracted knowledge
"""

import os
import sys
import json
import time
import logging
import requests
import re
import traceback
from typing import Dict, List, Any, Optional, Union, Tuple
from urllib.parse import urlparse
from datetime import datetime

# Try to import trafilatura for web scraping
try:
    import trafilatura
    HAVE_TRAFILATURA = True
except ImportError:
    HAVE_TRAFILATURA = False

# Configure logging
logger = logging.getLogger(__name__)

class WebLearner:
    """System for RILEY to learn from websites and expand her capabilities."""
    
    def __init__(self, knowledge_base_dir: str = None):
        """Initialize the web learning system.
        
        Args:
            knowledge_base_dir: Directory to store learned knowledge. If None, uses default.
        """
        # Set up knowledge base storage
        self.base_path = self._detect_base_path()
        self.knowledge_base_dir = knowledge_base_dir or os.path.join(self.base_path, "jarvis", "knowledge")
        
        # Create knowledge directories if needed
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_dir, "websites"), exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_dir, "code"), exist_ok=True)
        os.makedirs(os.path.join(self.knowledge_base_dir, "topics"), exist_ok=True)
        
        # User agent for web requests
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        
        # Track learning statistics
        self.learning_stats = {
            "sites_learned": 0,
            "code_examples_extracted": 0,
            "topics_learned": 0,
            "last_learned_site": None,
            "bytes_of_knowledge": 0
        }
        
        # Session for web requests
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        
        logger.info("Web learning system initialized")
    
    def _detect_base_path(self) -> str:
        """Auto-detect the base path of the RILEY project."""
        # Get the current file's directory and navigate up to find project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from features to the jarvis directory
        jarvis_dir = os.path.dirname(current_dir)
        # Go up one more level to the project root
        base_dir = os.path.dirname(jarvis_dir)
        return base_dir
    
    def extract_content_from_url(self, url: str, include_comments: bool = True) -> Optional[str]:
        """Extract the main content from a URL.
        
        Args:
            url: The URL to extract content from
            include_comments: Whether to include comments in the extraction
            
        Returns:
            Extracted text content or None if failed
        """
        if not HAVE_TRAFILATURA:
            logger.error("Trafilatura is required for content extraction. Please install it.")
            return None
            
        try:
            # Download the document with appropriate headers
            downloaded = trafilatura.fetch_url(url, headers={"User-Agent": self.user_agent})
            
            if not downloaded:
                logger.error(f"Failed to download content from {url}")
                return None
                
            # Extract the main content
            extracted_text = trafilatura.extract(
                downloaded,
                include_comments=include_comments,
                include_tables=True,
                include_images=True,
                include_links=True,
                output_format="text"
            )
            
            if not extracted_text:
                logger.error(f"Failed to extract content from {url}")
                return None
                
            return extracted_text
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return None
    
    def learn_from_website(self, url: str, topic: Optional[str] = None) -> Dict[str, Any]:
        """Learn from a website and store the knowledge.
        
        Args:
            url: URL to learn from
            topic: Optional topic label for the content
            
        Returns:
            Dictionary with learning results and status
        """
        # Parse URL to get domain and path
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Generate filename for storage
            filename_base = domain.replace(".", "_")
            if parsed_url.path and parsed_url.path not in ["/", ""]:
                path_part = parsed_url.path.strip("/").replace("/", "_")
                filename_base += "_" + path_part
                
            # Further clean the filename
            filename_base = re.sub(r'[^\w\-_\.]', '_', filename_base)
            
            # Extract content
            content = self.extract_content_from_url(url)
            
            if not content:
                return {
                    "status": "error",
                    "message": f"Failed to extract content from {url}",
                    "url": url
                }
                
            # Create a knowledge entry
            timestamp = datetime.now().isoformat()
            
            knowledge_entry = {
                "url": url,
                "domain": domain,
                "topic": topic,
                "timestamp": timestamp,
                "content_length": len(content),
                "extracted_by": "trafilatura"
            }
            
            # Store the content
            content_file = os.path.join(
                self.knowledge_base_dir, 
                "websites", 
                f"{filename_base}.txt"
            )
            
            with open(content_file, "w", encoding="utf-8") as f:
                f.write(content)
                
            # Store metadata
            metadata_file = os.path.join(
                self.knowledge_base_dir, 
                "websites",
                f"{filename_base}.json"
            )
            
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(knowledge_entry, f, indent=2)
                
            # Update learning stats
            self.learning_stats["sites_learned"] += 1
            self.learning_stats["last_learned_site"] = url
            self.learning_stats["bytes_of_knowledge"] += len(content)
            
            # Store by topic if provided
            if topic:
                topic_dir = os.path.join(self.knowledge_base_dir, "topics", topic)
                os.makedirs(topic_dir, exist_ok=True)
                
                # Create a symlink or copy to the topic directory
                topic_link = os.path.join(topic_dir, f"{filename_base}.txt")
                
                try:
                    # Try symlink first (more efficient)
                    if os.path.exists(topic_link):
                        os.remove(topic_link)
                    os.symlink(content_file, topic_link)
                except:
                    # Fall back to copying if symlink fails
                    with open(topic_link, "w", encoding="utf-8") as f:
                        f.write(content)
                        
                self.learning_stats["topics_learned"] += 1
                
            # Extract code examples if present
            code_examples = self._extract_code_from_text(content)
            
            if code_examples:
                self._store_code_examples(code_examples, domain, topic)
                self.learning_stats["code_examples_extracted"] += len(code_examples)
                
            return {
                "status": "success",
                "message": f"Successfully learned from {url}",
                "url": url,
                "content_length": len(content),
                "code_examples": len(code_examples) if code_examples else 0,
                "topic": topic,
                "files": {
                    "content": content_file,
                    "metadata": metadata_file
                }
            }
            
        except Exception as e:
            logger.error(f"Error learning from {url}: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error learning from {url}: {str(e)}",
                "url": url
            }
    
    def learn_from_wikipedia(self, topic: str) -> Dict[str, Any]:
        """Learn about a specific topic from Wikipedia.
        
        Args:
            topic: The topic to learn about
            
        Returns:
            Dictionary with learning results and status
        """
        # Format the Wikipedia URL
        url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        
        # Use the general website learning function
        result = self.learn_from_website(url, topic)
        
        # Add Wikipedia-specific metadata
        if result["status"] == "success":
            result["source"] = "wikipedia"
            
        return result
    
    def _extract_code_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract code examples from text content.
        
        Args:
            text: Text content to extract code from
            
        Returns:
            List of dictionaries with code examples and metadata
        """
        code_examples = []
        
        # Pattern for code blocks in markdown and similar formats
        # Match both ```language and ```
        code_block_pattern = r"```(?:\w+)?\s*\n(.*?)\n```"
        code_blocks = re.findall(code_block_pattern, text, re.DOTALL)
        
        for i, code in enumerate(code_blocks):
            # Try to determine the language
            language = self._detect_code_language(code)
            
            code_examples.append({
                "code": code,
                "language": language,
                "source": "code_block",
                "index": i
            })
            
        # Look for HTML <pre> and <code> tags
        pre_pattern = r"<pre(?:\s+.*?)?>(.*?)</pre>"
        pre_blocks = re.findall(pre_pattern, text, re.DOTALL)
        
        for i, code in enumerate(pre_blocks):
            # Clean HTML entities
            code = re.sub(r"&lt;", "<", code)
            code = re.sub(r"&gt;", ">", code)
            code = re.sub(r"&amp;", "&", code)
            
            language = self._detect_code_language(code)
            
            code_examples.append({
                "code": code,
                "language": language,
                "source": "pre_tag",
                "index": i
            })
            
        # Filter out very short "code" that's probably not actual code
        code_examples = [ex for ex in code_examples if len(ex["code"].strip()) > 10]
        
        return code_examples
    
    def _detect_code_language(self, code: str) -> str:
        """Attempt to detect the programming language of a code sample.
        
        Args:
            code: The code sample to analyze
            
        Returns:
            Detected language or "unknown"
        """
        # Simple language detection heuristics
        code = code.strip()
        
        # Check for language indicators
        if code.startswith("import ") or code.startswith("from ") or "def " in code or "class " in code:
            return "python"
        elif "{" in code and "function" in code:
            return "javascript"
        elif "public class" in code or "private class" in code or "public static void" in code:
            return "java"
        elif "<?" in code and "<?php" in code:
            return "php"
        elif "#include" in code and ("{" in code or "int main" in code):
            return "c" if "int main" in code else "cpp"
        elif "using namespace" in code or "::" in code:
            return "cpp"
        elif "<html" in code.lower() or "<!doctype html" in code.lower():
            return "html"
        elif "@import" in code or "{" in code and (":" in code and ";" in code):
            return "css"
        elif "SELECT" in code.upper() and "FROM" in code.upper():
            return "sql"
        elif "function" in code and "{" in code:
            return "javascript"
        
        return "unknown"
    
    def _store_code_examples(self, code_examples: List[Dict[str, Any]], domain: str, topic: Optional[str] = None) -> None:
        """Store extracted code examples.
        
        Args:
            code_examples: List of code examples to store
            domain: Source domain of the code
            topic: Optional topic label
        """
        # Make sure the code directory exists
        code_dir = os.path.join(self.knowledge_base_dir, "code")
        os.makedirs(code_dir, exist_ok=True)
        
        # Create a domain-specific directory
        domain_dir = os.path.join(code_dir, domain.replace(".", "_"))
        os.makedirs(domain_dir, exist_ok=True)
        
        # Store each code example
        for i, example in enumerate(code_examples):
            language = example["language"]
            
            # Choose appropriate file extension
            ext = ".txt"
            if language == "python":
                ext = ".py"
            elif language == "javascript":
                ext = ".js"
            elif language == "java":
                ext = ".java"
            elif language == "cpp":
                ext = ".cpp"
            elif language == "c":
                ext = ".c"
            elif language == "html":
                ext = ".html"
            elif language == "css":
                ext = ".css"
            elif language == "sql":
                ext = ".sql"
            elif language == "php":
                ext = ".php"
                
            # Create filename with topic if available
            if topic:
                filename = f"{topic}_{i+1}{ext}"
            else:
                filename = f"example_{i+1}{ext}"
                
            # Store the code
            with open(os.path.join(domain_dir, filename), "w", encoding="utf-8") as f:
                f.write(example["code"])
                
            # Create a metadata file
            metadata = {
                "language": language,
                "source": example["source"],
                "domain": domain,
                "topic": topic,
                "timestamp": datetime.now().isoformat()
            }
            
            with open(os.path.join(domain_dir, f"{filename}.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
    
    def search_knowledge_base(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information.
        
        Args:
            query: Search query
            limit: Maximum number of results to return
            
        Returns:
            List of matching knowledge items
        """
        results = []
        
        try:
            # Convert query to lowercase for case-insensitive matching
            query_lower = query.lower()
            
            # Search website content
            websites_dir = os.path.join(self.knowledge_base_dir, "websites")
            
            if os.path.exists(websites_dir):
                for filename in os.listdir(websites_dir):
                    if filename.endswith(".txt"):
                        filepath = os.path.join(websites_dir, filename)
                        
                        # Check if this content contains the query
                        try:
                            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                                content = f.read()
                                
                                if query_lower in content.lower():
                                    # Find the corresponding metadata file
                                    metadata_file = filepath[:-4] + ".json"
                                    metadata = {}
                                    
                                    if os.path.exists(metadata_file):
                                        with open(metadata_file, "r", encoding="utf-8") as mf:
                                            metadata = json.load(mf)
                                            
                                    # Find the relevant context around the query
                                    context = self._extract_context(content, query_lower)
                                    
                                    results.append({
                                        "type": "website",
                                        "file": filepath,
                                        "metadata": metadata,
                                        "context": context,
                                        "relevance": len(context)  # Simple relevance score
                                    })
                        except Exception as e:
                            logger.error(f"Error reading file {filepath}: {e}")
            
            # Search code examples
            code_dir = os.path.join(self.knowledge_base_dir, "code")
            
            if os.path.exists(code_dir):
                for domain_dir in os.listdir(code_dir):
                    domain_path = os.path.join(code_dir, domain_dir)
                    
                    if os.path.isdir(domain_path):
                        for filename in os.listdir(domain_path):
                            if not filename.endswith(".json"):  # Skip metadata files
                                filepath = os.path.join(domain_path, filename)
                                
                                # Check if this code contains the query
                                try:
                                    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                                        content = f.read()
                                        
                                        if query_lower in content.lower():
                                            # Find the corresponding metadata file
                                            metadata_file = filepath + ".json"
                                            metadata = {}
                                            
                                            if os.path.exists(metadata_file):
                                                with open(metadata_file, "r", encoding="utf-8") as mf:
                                                    metadata = json.load(mf)
                                                    
                                            results.append({
                                                "type": "code",
                                                "file": filepath,
                                                "content": content,
                                                "metadata": metadata,
                                                "relevance": 2 if query_lower in content.lower() else 1
                                            })
                                except Exception as e:
                                    logger.error(f"Error reading file {filepath}: {e}")
            
            # Sort by relevance and limit results
            results.sort(key=lambda x: x["relevance"], reverse=True)
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def _extract_context(self, content: str, query: str, context_size: int = 200) -> str:
        """Extract relevant context around a query match.
        
        Args:
            content: The full content text
            query: The search query
            context_size: Number of characters to include before and after the match
            
        Returns:
            Extracted context string
        """
        # Find the position of the match
        pos = content.lower().find(query)
        
        if pos == -1:
            return ""
            
        # Calculate start and end positions
        start = max(0, pos - context_size)
        end = min(len(content), pos + len(query) + context_size)
        
        # Extract the context
        context = content[start:end]
        
        # Add ellipsis if needed
        if start > 0:
            context = "..." + context
        if end < len(content):
            context = context + "..."
            
        return context
    
    def learn_and_generate_code(self, topic: str, language: str = "python") -> Dict[str, Any]:
        """Learn about a topic and generate relevant code.
        
        Args:
            topic: The topic to learn about
            language: The programming language to generate code in
            
        Returns:
            Dictionary with learning results and generated code
        """
        try:
            # First learn from Wikipedia
            wiki_result = self.learn_from_wikipedia(topic)
            
            # Try to learn from additional sources
            additional_sources = [
                f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}",
                f"https://github.com/topics/{topic.replace(' ', '-')}",
                f"https://stackoverflow.com/questions/tagged/{topic.replace(' ', '-')}"
            ]
            
            source_results = []
            for url in additional_sources:
                try:
                    result = self.learn_from_website(url, topic)
                    if result["status"] == "success":
                        source_results.append(result)
                except:
                    pass
            
            # Search our knowledge base for this topic
            knowledge = self.search_knowledge_base(topic)
            
            # Extract code examples
            code_examples = []
            for item in knowledge:
                if item["type"] == "code":
                    code_examples.append(item["content"])
            
            # Generate a code template
            code_template = self._generate_code_template(topic, language, code_examples)
            
            return {
                "status": "success",
                "topic": topic,
                "language": language,
                "wikipedia_result": wiki_result,
                "additional_sources": source_results,
                "knowledge_items": len(knowledge),
                "code_examples": len(code_examples),
                "generated_code": code_template
            }
            
        except Exception as e:
            logger.error(f"Error learning and generating code for {topic}: {e}")
            return {
                "status": "error",
                "message": f"Error learning about {topic}: {str(e)}",
                "topic": topic
            }
    
    def _generate_code_template(self, topic: str, language: str, examples: List[str]) -> str:
        """Generate a code template based on examples and topic.
        
        Args:
            topic: The topic for the code
            language: The programming language
            examples: List of code examples
            
        Returns:
            Generated code template
        """
        if language == "python":
            # Generate a Python module
            template = f'''"""
{topic.title()} - Module generated by RILEY
This module provides functionality related to {topic}.
"""

import os
import sys
import logging

# Configure logging
logger = logging.getLogger(__name__)

class {topic.title().replace(" ", "")}:
    """Class for handling {topic} functionality."""
    
    def __init__(self):
        """Initialize the {topic} handler."""
        self.name = "{topic}"
        logger.info(f"{topic.title()} module initialized")
    
    def process(self, data):
        """Process data related to {topic}.
        
        Args:
            data: The data to process
            
        Returns:
            Processed result
        """
        # TODO: Implement processing logic
        return f"Processed {data} with {topic} handler"
        
# Example usage
if __name__ == "__main__":
    handler = {topic.title().replace(" ", "")}()
    result = handler.process("sample data")
    print(result)
'''
        elif language == "javascript":
            # Generate a JavaScript module
            template = f'''/**
 * {topic.title()} - Module generated by RILEY
 * This module provides functionality related to {topic}.
 */

class {topic.title().replace(" ", "")} {{
    /**
     * Initialize the {topic} handler
     */
    constructor() {{
        this.name = "{topic}";
        console.log(`{topic.title()} module initialized`);
    }}
    
    /**
     * Process data related to {topic}
     * @param {{any}} data - The data to process
     * @returns {{string}} - Processed result
     */
    process(data) {{
        // TODO: Implement processing logic
        return `Processed ${{data}} with {topic} handler`;
    }}
}}

// Example usage
if (require.main === module) {{
    const handler = new {topic.title().replace(" ", "")}();
    const result = handler.process("sample data");
    console.log(result);
}}

module.exports = {topic.title().replace(" ", "")};
'''
        else:
            # Generic template for unsupported languages
            template = f"""
/* {topic.title()} - Code generated by RILEY */
/* This code provides functionality related to {topic}. */

// TODO: Implement {topic} functionality in {language}
"""
        
        return template
    
    def generate_new_module(self, topic: str, module_type: str = "feature") -> Dict[str, Any]:
        """Generate a new module for RILEY based on learning.
        
        Args:
            topic: The topic to create a module for
            module_type: Type of module ('feature', 'core', or 'util')
            
        Returns:
            Dictionary with generation results
        """
        try:
            # First learn about the topic
            learn_result = self.learn_and_generate_code(topic, "python")
            
            # Determine file path
            if module_type == "feature":
                module_dir = os.path.join(self.base_path, "jarvis", "features")
            elif module_type == "core":
                module_dir = os.path.join(self.base_path, "jarvis", "core")
            elif module_type == "util":
                module_dir = os.path.join(self.base_path, "jarvis", "utils")
            else:
                return {
                    "status": "error",
                    "message": f"Invalid module type: {module_type}",
                    "topic": topic
                }
                
            # Generate a snake_case filename
            filename = topic.lower().replace(" ", "_") + ".py"
            filepath = os.path.join(module_dir, filename)
            
            # Check if module already exists
            if os.path.exists(filepath):
                return {
                    "status": "error",
                    "message": f"Module {filename} already exists at {filepath}",
                    "topic": topic,
                    "path": filepath
                }
                
            # Generate module code
            module_code = self._generate_module_code(topic, module_type)
            
            # Write the module file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(module_code)
                
            return {
                "status": "success",
                "message": f"Successfully generated {module_type} module for {topic}",
                "topic": topic,
                "path": filepath,
                "module_type": module_type,
                "learn_result": learn_result
            }
            
        except Exception as e:
            logger.error(f"Error generating new module for {topic}: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error generating module for {topic}: {str(e)}",
                "topic": topic
            }
    
    def _generate_module_code(self, topic: str, module_type: str) -> str:
        """Generate Python code for a new module.
        
        Args:
            topic: The module topic
            module_type: Type of module ('feature', 'core', or 'util')
            
        Returns:
            Generated Python code
        """
        # Format the class name in CamelCase
        class_name = "".join(word.capitalize() for word in topic.split())
        
        if module_type == "feature":
            # Feature module template
            return f'''"""
RILEY - {topic.title()} Feature Module

This module provides {topic} functionality for RILEY, enabling:
1. Processing {topic} requests
2. Generating {topic} content
3. Analyzing {topic} data
4. Integrating with external {topic} resources
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional

# Configure logging
logger = logging.getLogger(__name__)

class {class_name}Manager:
    """Manager for {topic} functionality."""
    
    def __init__(self):
        """Initialize the {topic} manager."""
        self.name = "{topic}"
        logger.info(f"{topic.title()} manager initialized")
    
    def process_{topic.lower().replace(" ", "_")}_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a {topic} request.
        
        Args:
            request: The request parameters
            
        Returns:
            Response with processed results
        """
        logger.info(f"Processing {topic} request: {{request}}")
        
        # TODO: Implement {topic} processing logic
        
        return {{
            "status": "success",
            "message": f"Processed {topic} request",
            "result": request
        }}
    
    def generate_{topic.lower().replace(" ", "_")}_content(self, parameters: Dict[str, Any]) -> str:
        """Generate {topic} content.
        
        Args:
            parameters: Content generation parameters
            
        Returns:
            Generated content
        """
        logger.info(f"Generating {topic} content with parameters: {{parameters}}")
        
        # TODO: Implement {topic} content generation
        
        return f"Generated {topic} content based on {{parameters}}"
    
    def analyze_{topic.lower().replace(" ", "_")}_data(self, data: Any) -> Dict[str, Any]:
        """Analyze {topic} data.
        
        Args:
            data: The data to analyze
            
        Returns:
            Analysis results
        """
        logger.info(f"Analyzing {topic} data")
        
        # TODO: Implement {topic} data analysis
        
        return {{
            "status": "success",
            "message": f"Analyzed {topic} data",
            "analysis": {{
                "type": "{topic}",
                "summary": "Data analysis complete"
            }}
        }}
'''
        elif module_type == "core":
            # Core module template
            return f'''"""
RILEY - {topic.title()} Core System

This core module provides essential {topic} functionality for RILEY:
1. Low-level {topic} operations
2. System integration with {topic} subsystems
3. Core services for {topic} processing
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

# Configure logging
logger = logging.getLogger(__name__)

class {class_name}System:
    """Core system for {topic} functionality."""
    
    def __init__(self):
        """Initialize the {topic} system."""
        self.initialized = False
        self.system_name = "{topic.lower().replace(' ', '_')}_system"
        
        # Initialize components
        self._initialize_components()
        
        logger.info(f"{topic.title()} system initialized")
    
    def _initialize_components(self) -> None:
        """Initialize system components."""
        try:
            # TODO: Initialize {topic} components
            self.initialized = True
        except Exception as e:
            logger.error(f"Error initializing {topic} system: {{e}}")
            self.initialized = False
    
    def perform_{topic.lower().replace(" ", "_")}_operation(self, operation: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a {topic} operation.
        
        Args:
            operation: The operation to perform
            parameters: Operation parameters
            
        Returns:
            Operation result
        """
        if not self.initialized:
            return {{
                "status": "error",
                "message": f"{topic.title()} system not initialized"
            }}
            
        logger.info(f"Performing {topic} operation: {{operation}}")
        
        # TODO: Implement {topic} operations
        
        return {{
            "status": "success",
            "operation": operation,
            "result": f"Completed {topic} operation: {{operation}}"
        }}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get the current status of the {topic} system.
        
        Returns:
            System status information
        """
        return {{
            "system": self.system_name,
            "initialized": self.initialized,
            "status": "operational" if self.initialized else "offline"
        }}
'''
        else:  # util module
            # Utility module template
            return f'''"""
RILEY - {topic.title()} Utilities

This utility module provides helper functions for {topic} operations:
1. Common {topic} functions
2. Data conversion for {topic} formats
3. Helper utilities for {topic} processing
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional, Union

# Configure logging
logger = logging.getLogger(__name__)

def process_{topic.lower().replace(" ", "_")}(data: Any) -> Any:
    """Process {topic} data.
    
    Args:
        data: The data to process
        
    Returns:
        Processed data
    """
    logger.debug(f"Processing {topic} data")
    
    # TODO: Implement {topic} processing
    
    return data

def convert_{topic.lower().replace(" ", "_")}_format(data: Any, target_format: str) -> Any:
    """Convert {topic} data to a different format.
    
    Args:
        data: The data to convert
        target_format: Target format identifier
        
    Returns:
        Converted data
    """
    logger.debug(f"Converting {topic} data to {{target_format}}")
    
    # TODO: Implement format conversion
    
    return data

def validate_{topic.lower().replace(" ", "_")}(data: Any) -> Tuple[bool, Optional[str]]:
    """Validate {topic} data.
    
    Args:
        data: The data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    logger.debug(f"Validating {topic} data")
    
    # TODO: Implement validation logic
    
    return True, None

class {class_name}Helper:
    """Helper class for {topic} operations."""
    
    @staticmethod
    def format_{topic.lower().replace(" ", "_")}(data: Any) -> str:
        """Format {topic} data as a string.
        
        Args:
            data: The data to format
            
        Returns:
            Formatted string
        """
        # TODO: Implement formatting logic
        
        return f"{topic.title()} data: {{data}}"
    
    @staticmethod
    def parse_{topic.lower().replace(" ", "_")}(text: str) -> Optional[Any]:
        """Parse {topic} data from text.
        
        Args:
            text: Text to parse
            
        Returns:
            Parsed data or None if parsing failed
        """
        logger.debug(f"Parsing {topic} data from text")
        
        # TODO: Implement parsing logic
        
        return {{
            "type": "{topic}",
            "source": text,
            "parsed": True
        }}
'''
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get statistics about web learning activities.
        
        Returns:
            Dictionary with learning statistics
        """
        # Calculate total size of knowledge base
        total_bytes = 0
        num_files = 0
        
        try:
            for root, _, files in os.walk(self.knowledge_base_dir):
                for file in files:
                    try:
                        filepath = os.path.join(root, file)
                        total_bytes += os.path.getsize(filepath)
                        num_files += 1
                    except:
                        pass
        except:
            pass
            
        # Update stats
        self.learning_stats["bytes_of_knowledge"] = total_bytes
        
        # Add additional stats
        stats = self.learning_stats.copy()
        stats["knowledge_base_size_bytes"] = total_bytes
        stats["knowledge_base_size_mb"] = round(total_bytes / (1024 * 1024), 2)
        stats["total_files"] = num_files
        
        return stats