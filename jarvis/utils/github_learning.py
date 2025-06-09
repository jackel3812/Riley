"""
RILEY - GitHub Learning System

This module enables RILEY to learn from GitHub repositories by:
1. Cloning and analyzing repositories
2. Extracting code patterns and solutions
3. Learning from documentation and examples
4. Building specialized knowledge in various programming domains
5. Automatically generating new capabilities based on discovered code
"""

import os
import sys
import json
import time
import logging
import requests
import re
import tempfile
import traceback
import subprocess
import shutil
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
from urllib.parse import urlparse, quote_plus

# Configure logging
logger = logging.getLogger(__name__)

class GitHubLearner:
    """System for RILEY to learn from GitHub repositories and source code."""
    
    def __init__(self, knowledge_base_dir: str = None, github_token: str = None):
        """Initialize the GitHub learning system.
        
        Args:
            knowledge_base_dir: Directory to store learned knowledge. If None, uses default.
            github_token: Optional GitHub API token for increased rate limits
        """
        # Set up knowledge base storage
        self.base_path = self._detect_base_path()
        self.knowledge_base_dir = knowledge_base_dir or os.path.join(self.base_path, "jarvis", "knowledge")
        
        # Create knowledge directories if needed
        os.makedirs(self.knowledge_base_dir, exist_ok=True)
        github_knowledge_dir = os.path.join(self.knowledge_base_dir, "github")
        os.makedirs(github_knowledge_dir, exist_ok=True)
        os.makedirs(os.path.join(github_knowledge_dir, "repositories"), exist_ok=True)
        os.makedirs(os.path.join(github_knowledge_dir, "code_snippets"), exist_ok=True)
        
        # GitHub API configuration
        self.github_api_url = "https://api.github.com"
        self.github_token = github_token
        
        # Set up headers for GitHub API
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "RILEY-AI-Assistant"
        }
        
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
        
        # Learning statistics
        self.learning_stats = {
            "repositories_analyzed": 0,
            "files_processed": 0,
            "code_snippets_learned": 0,
            "languages_encountered": {},
            "last_repository": None,
            "bytes_processed": 0,
            "api_calls": 0
        }
        
        # Temporary directory for repository clones
        self.temp_dir = os.path.join(tempfile.gettempdir(), "riley_github_learning")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        logger.info("GitHub learning system initialized")
    
    def _detect_base_path(self) -> str:
        """Auto-detect the base path of the RILEY project."""
        # Get the current file's directory and navigate up to find project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up one level from features to the jarvis directory
        jarvis_dir = os.path.dirname(current_dir)
        # Go up one more level to the project root
        base_dir = os.path.dirname(jarvis_dir)
        return base_dir
    
    def _make_github_api_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Make a request to the GitHub API.
        
        Args:
            endpoint: API endpoint to call
            params: Optional query parameters
            
        Returns:
            Response JSON or error dictionary
        """
        url = f"{self.github_api_url}{endpoint}"
        
        try:
            self.learning_stats["api_calls"] += 1
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403 and "rate limit exceeded" in response.text.lower():
                logger.warning("GitHub API rate limit exceeded")
                return {"error": "Rate limit exceeded", "status_code": 403}
            else:
                logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                return {"error": f"API error: {response.status_code}", "status_code": response.status_code}
                
        except Exception as e:
            logger.error(f"Error making GitHub API request: {e}")
            return {"error": str(e)}
    
    def search_repositories(self, query: str, language: Optional[str] = None, 
                           sort: str = "stars", max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for GitHub repositories matching a query.
        
        Args:
            query: Search query
            language: Optional language filter (e.g., "python")
            sort: How to sort results ("stars", "forks", "updated")
            max_results: Maximum number of results to return
            
        Returns:
            List of repository information dictionaries
        """
        # Construct the search query
        search_query = query
        if language:
            search_query += f" language:{language}"
            
        params = {
            "q": search_query,
            "sort": sort,
            "order": "desc",
            "per_page": min(max_results, 100)  # GitHub API limit
        }
        
        results = self._make_github_api_request("/search/repositories", params)
        
        if "error" in results:
            logger.error(f"Error searching repositories: {results['error']}")
            return []
            
        repositories = []
        for repo in results.get("items", []):
            repositories.append({
                "name": repo["name"],
                "full_name": repo["full_name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "api_url": repo["url"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "language": repo["language"],
                "last_updated": repo["updated_at"]
            })
            
        return repositories[:max_results]
    
    def get_repository_info(self, repo_name: str) -> Dict[str, Any]:
        """Get detailed information about a repository.
        
        Args:
            repo_name: Repository name with owner (e.g., "owner/repo")
            
        Returns:
            Repository information or error
        """
        endpoint = f"/repos/{repo_name}"
        return self._make_github_api_request(endpoint)
    
    def get_repository_contents(self, repo_name: str, path: str = "") -> List[Dict[str, Any]]:
        """Get the contents of a directory in a repository.
        
        Args:
            repo_name: Repository name with owner (e.g., "owner/repo")
            path: Path within the repository
            
        Returns:
            List of content items or empty list if error
        """
        endpoint = f"/repos/{repo_name}/contents/{path}"
        result = self._make_github_api_request(endpoint)
        
        if isinstance(result, list):
            return result
        elif "error" in result:
            logger.error(f"Error getting repository contents: {result['error']}")
            return []
        else:
            # This might be a single file
            return [result]
    
    def get_file_content(self, repo_name: str, file_path: str) -> Optional[str]:
        """Get the content of a file from a repository.
        
        Args:
            repo_name: Repository name with owner (e.g., "owner/repo")
            file_path: Path to the file within the repository
            
        Returns:
            File content or None if error
        """
        endpoint = f"/repos/{repo_name}/contents/{file_path}"
        result = self._make_github_api_request(endpoint)
        
        if "error" in result:
            logger.error(f"Error getting file content: {result['error']}")
            return None
            
        if result.get("type") != "file" or "content" not in result:
            logger.error(f"Not a file or no content available: {file_path}")
            return None
            
        # Decode base64 content
        import base64
        try:
            content = base64.b64decode(result["content"]).decode("utf-8")
            return content
        except Exception as e:
            logger.error(f"Error decoding file content: {e}")
            return None
    
    def clone_repository(self, repo_url: str, branch: str = "main") -> Optional[str]:
        """Clone a GitHub repository to a temporary directory.
        
        Args:
            repo_url: URL of the repository to clone
            branch: Branch to clone (default: main)
            
        Returns:
            Path to the cloned repository or None if failed
        """
        try:
            # Extract repository name from URL
            parsed_url = urlparse(repo_url)
            path_parts = parsed_url.path.strip("/").split("/")
            
            if len(path_parts) < 2:
                logger.error(f"Invalid repository URL: {repo_url}")
                return None
                
            repo_owner = path_parts[0]
            repo_name = path_parts[1]
            
            # Create a unique directory for this repository
            repo_dir = os.path.join(self.temp_dir, f"{repo_owner}_{repo_name}_{int(time.time())}")
            
            # Clone the repository
            logger.info(f"Cloning repository {repo_url} to {repo_dir}")
            result = subprocess.run(
                ["git", "clone", "--branch", branch, "--single-branch", "--depth", "1", repo_url, repo_dir],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                logger.error(f"Error cloning repository: {result.stderr}")
                
                # Try again with the default branch if specified branch failed
                if branch != "main" and branch != "master":
                    logger.info(f"Trying to clone default branch instead of {branch}")
                    return self.clone_repository(repo_url, "main")
                elif branch == "main":
                    logger.info("Trying to clone 'master' branch instead")
                    return self.clone_repository(repo_url, "master")
                else:
                    return None
                    
            logger.info(f"Successfully cloned repository to {repo_dir}")
            return repo_dir
            
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            logger.error(traceback.format_exc())
            return None
    
    def analyze_repository(self, repo_url: str, depth: int = 3, 
                          file_types: List[str] = None) -> Dict[str, Any]:
        """Analyze a GitHub repository and learn from its code.
        
        Args:
            repo_url: URL of the repository to analyze
            depth: Maximum directory depth to analyze
            file_types: List of file extensions to analyze (e.g., [".py", ".js"])
            
        Returns:
            Analysis results
        """
        if file_types is None:
            file_types = [".py", ".js", ".java", ".cpp", ".c", ".h", ".rb", ".go", ".ts", ".php"]
            
        try:
            # Clone the repository
            repo_dir = self.clone_repository(repo_url)
            
            if not repo_dir:
                return {
                    "status": "error",
                    "message": f"Failed to clone repository: {repo_url}",
                    "url": repo_url
                }
                
            # Extract repository name from URL for storage
            parsed_url = urlparse(repo_url)
            path_parts = parsed_url.path.strip("/").split("/")
            repo_owner = path_parts[0]
            repo_name = path_parts[1]
            
            # Analyze the repository structure
            structure = self._analyze_repository_structure(repo_dir, depth, file_types)
            
            # Process and learn from important files
            learned_files = self._process_repository_files(repo_dir, structure["files"], repo_owner, repo_name)
            
            # Update learning statistics
            self.learning_stats["repositories_analyzed"] += 1
            self.learning_stats["files_processed"] += len(learned_files)
            self.learning_stats["last_repository"] = repo_url
            
            # Record language statistics
            for lang, count in structure["language_counts"].items():
                if lang in self.learning_stats["languages_encountered"]:
                    self.learning_stats["languages_encountered"][lang] += count
                else:
                    self.learning_stats["languages_encountered"][lang] = count
            
            # Store repository metadata
            metadata = {
                "url": repo_url,
                "owner": repo_owner,
                "name": repo_name,
                "analyzed_at": datetime.now().isoformat(),
                "file_count": len(structure["files"]),
                "directory_count": len(structure["directories"]),
                "languages": structure["language_counts"],
                "learned_files": len(learned_files),
                "size_bytes": structure["total_size"]
            }
            
            # Store metadata in knowledge base
            metadata_file = os.path.join(
                self.knowledge_base_dir,
                "github",
                "repositories",
                f"{repo_owner}_{repo_name}_metadata.json"
            )
            
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
                
            # Clean up temporary repository
            try:
                shutil.rmtree(repo_dir)
            except:
                logger.warning(f"Failed to remove temporary repository directory: {repo_dir}")
                
            return {
                "status": "success",
                "message": f"Successfully analyzed repository: {repo_url}",
                "url": repo_url,
                "files_processed": len(learned_files),
                "languages": structure["language_counts"],
                "size_bytes": structure["total_size"],
                "metadata_file": metadata_file
            }
            
        except Exception as e:
            logger.error(f"Error analyzing repository: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error analyzing repository: {str(e)}",
                "url": repo_url
            }
    
    def _analyze_repository_structure(self, repo_dir: str, max_depth: int, 
                                     file_types: List[str]) -> Dict[str, Any]:
        """Analyze the structure of a repository.
        
        Args:
            repo_dir: Path to the cloned repository
            max_depth: Maximum directory depth to analyze
            file_types: List of file extensions to analyze
            
        Returns:
            Dictionary with repository structure information
        """
        structure = {
            "directories": [],
            "files": [],
            "language_counts": {},
            "total_size": 0
        }
        
        for root, dirs, files in os.walk(repo_dir):
            # Calculate current depth
            current_depth = root[len(repo_dir):].count(os.sep)
            
            # Skip if we've exceeded max depth
            if current_depth > max_depth:
                del dirs[:]  # Clear dirs to prevent further recursion
                continue
                
            # Skip hidden directories and common directories to ignore
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", "venv", "env", "build", "dist", "__pycache__"]]
            
            # Record this directory
            rel_path = os.path.relpath(root, repo_dir)
            if rel_path != ".":  # Skip the root directory
                structure["directories"].append(rel_path)
                
            # Process files
            for file in files:
                # Skip hidden files and certain file types
                if file.startswith(".") or file.endswith((".pyc", ".pyo", ".o", ".obj", ".exe")):
                    continue
                    
                file_path = os.path.join(root, file)
                rel_file_path = os.path.relpath(file_path, repo_dir)
                
                # Get file extension
                _, ext = os.path.splitext(file)
                ext = ext.lower()
                
                # Only process file types we're interested in
                if file_types and ext not in file_types:
                    continue
                    
                # Get file size
                try:
                    size = os.path.getsize(file_path)
                    structure["total_size"] += size
                except:
                    size = 0
                    
                # Record language statistics
                lang = ext[1:] if ext.startswith(".") else ext
                if lang:
                    if lang in structure["language_counts"]:
                        structure["language_counts"][lang] += 1
                    else:
                        structure["language_counts"][lang] = 1
                        
                # Add file to structure
                structure["files"].append({
                    "path": rel_file_path,
                    "size": size,
                    "language": lang
                })
                
        return structure
    
    def _process_repository_files(self, repo_dir: str, files: List[Dict[str, Any]], 
                                 repo_owner: str, repo_name: str) -> List[Dict[str, Any]]:
        """Process and learn from files in a repository.
        
        Args:
            repo_dir: Path to the cloned repository
            files: List of file information from structure analysis
            repo_owner: Owner of the repository
            repo_name: Name of the repository
            
        Returns:
            List of processed file information
        """
        processed_files = []
        
        # Sort files by size (smallest first) to avoid processing huge files
        files.sort(key=lambda x: x["size"])
        
        # Set a reasonable size limit (10MB)
        max_file_size = 10 * 1024 * 1024
        
        for file_info in files:
            if file_info["size"] > max_file_size:
                logger.info(f"Skipping large file: {file_info['path']} ({file_info['size']} bytes)")
                continue
                
            file_path = os.path.join(repo_dir, file_info["path"])
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    
                # Store this file in the knowledge base
                storage_dir = os.path.join(
                    self.knowledge_base_dir,
                    "github",
                    "repositories",
                    f"{repo_owner}_{repo_name}"
                )
                
                os.makedirs(storage_dir, exist_ok=True)
                
                # Create a clean filename
                clean_path = file_info["path"].replace("/", "_").replace("\\", "_")
                storage_path = os.path.join(storage_dir, clean_path)
                
                with open(storage_path, "w", encoding="utf-8") as f:
                    f.write(content)
                    
                # Extract code patterns from the file
                code_snippets = self._extract_code_patterns(content, file_info["language"])
                
                if code_snippets:
                    # Store valuable code snippets
                    for i, snippet in enumerate(code_snippets):
                        snippet_dir = os.path.join(
                            self.knowledge_base_dir,
                            "github",
                            "code_snippets",
                            file_info["language"]
                        )
                        
                        os.makedirs(snippet_dir, exist_ok=True)
                        
                        # Create a filename based on the repository and pattern type
                        snippet_file = os.path.join(
                            snippet_dir,
                            f"{repo_owner}_{repo_name}_{clean_path}_snippet_{i+1}.{file_info['language']}"
                        )
                        
                        with open(snippet_file, "w", encoding="utf-8") as f:
                            f.write(snippet["code"])
                            
                        # Create metadata
                        metadata = {
                            "language": file_info["language"],
                            "repository": f"{repo_owner}/{repo_name}",
                            "file": file_info["path"],
                            "pattern_type": snippet["type"],
                            "extracted_at": datetime.now().isoformat()
                        }
                        
                        with open(f"{snippet_file}.json", "w", encoding="utf-8") as f:
                            json.dump(metadata, f, indent=2)
                            
                    self.learning_stats["code_snippets_learned"] += len(code_snippets)
                    
                # Record this processed file
                processed_files.append({
                    "path": file_info["path"],
                    "language": file_info["language"],
                    "size": file_info["size"],
                    "stored_at": storage_path,
                    "snippets_extracted": len(code_snippets) if code_snippets else 0
                })
                
                # Update byte count
                self.learning_stats["bytes_processed"] += file_info["size"]
                
            except Exception as e:
                logger.error(f"Error processing file {file_info['path']}: {e}")
                
        return processed_files
    
    def _extract_code_patterns(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Extract useful code patterns from content.
        
        Args:
            content: File content
            language: Programming language
            
        Returns:
            List of extracted code patterns
        """
        patterns = []
        
        # Skip empty or tiny files
        if not content or len(content) < 10:
            return patterns
            
        if language == "py":
            # Extract Python functions (basic approach)
            function_pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)(?:\s*->.*?)?:\s*(?:(?:\s*'''[\s\S]*?''')|(?:\s*\"\"\"[\s\S]*?\"\"\"))?\s*((?:(?:\s+)[^\n]+\n?)+)"
            for match in re.finditer(function_pattern, content, re.MULTILINE):
                func_name = match.group(1)
                func_args = match.group(2)
                func_body = match.group(3)
                
                # Combine the function signature and body
                function_code = f"def {func_name}({func_args}):\n{func_body}"
                
                patterns.append({
                    "type": "function",
                    "name": func_name,
                    "code": function_code
                })
                
            # Extract Python classes
            class_pattern = r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\([^)]*\))?:\s*(?:(?:\s*'''[\s\S]*?''')|(?:\s*\"\"\"[\s\S]*?\"\"\"))?((?:(?:[^\n])+\n?)+)"
            for match in re.finditer(class_pattern, content, re.MULTILINE):
                class_name = match.group(1)
                class_body = match.group(2)
                
                # Find the full class definition by counting indentation
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if f"class {class_name}" in line:
                        # Found the class definition
                        class_code = [line]
                        j = i + 1
                        
                        # Continue until we find a line with the same or less indentation
                        while j < len(lines):
                            if lines[j].strip() and not lines[j].startswith(' '):
                                break
                            class_code.append(lines[j])
                            j += 1
                            
                        patterns.append({
                            "type": "class",
                            "name": class_name,
                            "code": "\n".join(class_code)
                        })
                        break
                        
        elif language in ["js", "ts"]:
            # Extract JavaScript/TypeScript functions
            function_pattern = r"(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>)\s*{((?:(?:[^\n])+\n?)+)}"
            for match in re.finditer(function_pattern, content, re.MULTILINE):
                func_name = match.group(1) or match.group(3)
                func_args = match.group(2) or match.group(4)
                func_body = match.group(5)
                
                if match.group(1):  # Standard function
                    function_code = f"function {func_name}({func_args}) {{\n{func_body}\n}}"
                else:  # Arrow function
                    function_code = f"const {func_name} = ({func_args}) => {{\n{func_body}\n}};"
                    
                patterns.append({
                    "type": "function",
                    "name": func_name,
                    "code": function_code
                })
                
            # Extract JavaScript/TypeScript classes
            class_pattern = r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)(?:\s+extends\s+([a-zA-Z_][a-zA-Z0-9_.]*))?(?:\s+implements\s+([a-zA-Z_][a-zA-Z0-9_.]*))?\s*{((?:(?:[^\n])+\n?)+)}"
            for match in re.finditer(class_pattern, content, re.MULTILINE):
                class_name = match.group(1)
                extends = match.group(2)
                implements = match.group(3)
                class_body = match.group(4)
                
                class_code = f"class {class_name}"
                if extends:
                    class_code += f" extends {extends}"
                if implements:
                    class_code += f" implements {implements}"
                    
                class_code += f" {{\n{class_body}\n}}"
                
                patterns.append({
                    "type": "class",
                    "name": class_name,
                    "code": class_code
                })
                
        # Extract utility patterns for any language
        # 1. Find common algorithmic patterns (like sorting, searching)
        if "sort" in content.lower() and (
            "array" in content.lower() or 
            "list" in content.lower() or 
            "[" in content):
            
            # Try to extract a sorting algorithm implementation
            patterns.append({
                "type": "algorithm",
                "name": "sorting",
                "code": content
            })
            
        # 2. Data structure implementations
        if (
            "class" in content and
            any(ds in content.lower() for ds in ["tree", "stack", "queue", "list", "map", "dict"])
        ):
            patterns.append({
                "type": "data_structure",
                "name": "data_structure",
                "code": content
            })
            
        return patterns
    
    def learn_from_github_topic(self, topic: str, max_repos: int = 5) -> Dict[str, Any]:
        """Learn from repositories related to a specific topic.
        
        Args:
            topic: GitHub topic to learn from
            max_repos: Maximum number of repositories to analyze
            
        Returns:
            Learning results
        """
        try:
            # Search for repositories with this topic
            repos = self.search_repositories(f"topic:{topic}", max_results=max_repos)
            
            if not repos:
                return {
                    "status": "error",
                    "message": f"No repositories found for topic: {topic}",
                    "topic": topic
                }
                
            # Analyze each repository
            analysis_results = []
            for repo in repos:
                result = self.analyze_repository(repo["url"])
                analysis_results.append(result)
                
            # Generate a topic summary
            topic_dir = os.path.join(
                self.knowledge_base_dir,
                "github",
                "topics",
                topic.replace(" ", "_")
            )
            
            os.makedirs(topic_dir, exist_ok=True)
            
            # Create a summary file
            summary = {
                "topic": topic,
                "learned_at": datetime.now().isoformat(),
                "repositories": [repo["full_name"] for repo in repos],
                "repository_count": len(repos),
                "analysis_results": analysis_results
            }
            
            summary_file = os.path.join(topic_dir, "topic_summary.json")
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
                
            return {
                "status": "success",
                "message": f"Successfully learned from topic: {topic}",
                "topic": topic,
                "repositories_analyzed": len(analysis_results),
                "summary_file": summary_file
            }
            
        except Exception as e:
            logger.error(f"Error learning from topic {topic}: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error learning from topic: {str(e)}",
                "topic": topic
            }
    
    def learn_from_user_repositories(self, username: str, max_repos: int = 5) -> Dict[str, Any]:
        """Learn from repositories owned by a specific GitHub user.
        
        Args:
            username: GitHub username
            max_repos: Maximum number of repositories to analyze
            
        Returns:
            Learning results
        """
        try:
            # Get repositories for this user
            endpoint = f"/users/{username}/repos"
            params = {
                "sort": "updated",
                "per_page": max_repos
            }
            
            repos_result = self._make_github_api_request(endpoint, params)
            
            if "error" in repos_result:
                return {
                    "status": "error",
                    "message": f"Error getting repositories for user {username}: {repos_result['error']}",
                    "username": username
                }
                
            if not repos_result:
                return {
                    "status": "error",
                    "message": f"No repositories found for user: {username}",
                    "username": username
                }
                
            # Analyze each repository
            analysis_results = []
            for repo in repos_result[:max_repos]:
                result = self.analyze_repository(repo["html_url"])
                analysis_results.append(result)
                
            # Create a user directory in the knowledge base
            user_dir = os.path.join(
                self.knowledge_base_dir,
                "github",
                "users",
                username
            )
            
            os.makedirs(user_dir, exist_ok=True)
            
            # Create a summary file
            summary = {
                "username": username,
                "learned_at": datetime.now().isoformat(),
                "repositories": [repo["full_name"] for repo in repos_result[:max_repos]],
                "repository_count": len(repos_result[:max_repos]),
                "analysis_results": analysis_results
            }
            
            summary_file = os.path.join(user_dir, "user_summary.json")
            with open(summary_file, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2)
                
            return {
                "status": "success",
                "message": f"Successfully learned from user: {username}",
                "username": username,
                "repositories_analyzed": len(analysis_results),
                "summary_file": summary_file
            }
            
        except Exception as e:
            logger.error(f"Error learning from user {username}: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error learning from user: {str(e)}",
                "username": username
            }
    
    def generate_code_from_learned_patterns(self, task_description: str, 
                                          language: str = "python") -> Dict[str, Any]:
        """Generate code for a given task based on learned patterns.
        
        Args:
            task_description: Description of the task to generate code for
            language: Target programming language
            
        Returns:
            Generated code and related information
        """
        try:
            # Search for relevant code snippets
            keywords = self._extract_keywords(task_description)
            
            # Find relevant code snippets
            snippets = self._find_relevant_snippets(keywords, language)
            
            if not snippets:
                return {
                    "status": "warning",
                    "message": f"No relevant code snippets found for task: {task_description}",
                    "generated_code": self._generate_skeleton_code(task_description, language)
                }
                
            # Generate code based on found snippets
            generated_code = self._generate_code_from_snippets(task_description, snippets, language)
            
            return {
                "status": "success",
                "message": f"Generated code for task: {task_description}",
                "language": language,
                "task": task_description,
                "generated_code": generated_code,
                "snippets_used": len(snippets)
            }
            
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error generating code: {str(e)}",
                "task": task_description
            }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract relevant keywords from text.
        
        Args:
            text: Text to extract keywords from
            
        Returns:
            List of keywords
        """
        # Remove punctuation and convert to lowercase
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        
        # Split into words
        words = text.split()
        
        # Remove common words
        stop_words = set([
            "a", "an", "the", "and", "or", "but", "if", "then", "else", "when",
            "at", "from", "by", "with", "about", "against", "between", "into",
            "through", "during", "before", "after", "above", "below", "to", "of",
            "in", "that", "this", "for", "on", "is", "was", "be", "are"
        ])
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Add specific programming terms
        if "sort" in keywords or "sorting" in keywords:
            keywords.extend(["algorithm", "quicksort", "mergesort", "bubblesort"])
            
        if "search" in keywords:
            keywords.extend(["find", "binary", "linear"])
            
        if "list" in keywords or "array" in keywords:
            keywords.extend(["collection", "iterable", "sequence"])
            
        return list(set(keywords))  # Remove duplicates
    
    def _find_relevant_snippets(self, keywords: List[str], language: str) -> List[Dict[str, Any]]:
        """Find code snippets relevant to the keywords.
        
        Args:
            keywords: List of keywords to search for
            language: Programming language to filter by
            
        Returns:
            List of relevant code snippets
        """
        snippets = []
        
        # Define the snippets directory
        snippets_dir = os.path.join(
            self.knowledge_base_dir,
            "github",
            "code_snippets",
            language
        )
        
        if not os.path.exists(snippets_dir):
            return snippets
            
        # Score function to rank snippets by relevance
        def score_snippet(content, metadata, keywords):
            score = 0
            content_lower = content.lower()
            
            # Score based on keyword matches
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
                    
            # Bonus for function and class names
            if metadata.get("pattern_type") == "function":
                score += 2
            elif metadata.get("pattern_type") == "class":
                score += 3
                
            return score
            
        # Search all snippet files
        for filename in os.listdir(snippets_dir):
            if filename.endswith(f".{language}") and not filename.endswith(".json"):
                try:
                    # Read snippet content
                    snippet_path = os.path.join(snippets_dir, filename)
                    with open(snippet_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                        
                    # Read metadata if available
                    metadata_path = f"{snippet_path}.json"
                    metadata = {}
                    
                    if os.path.exists(metadata_path):
                        with open(metadata_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                            
                    # Calculate relevance score
                    score = score_snippet(content, metadata, keywords)
                    
                    if score > 0:  # Only include if there's at least one match
                        snippets.append({
                            "content": content,
                            "metadata": metadata,
                            "file": snippet_path,
                            "score": score
                        })
                        
                except Exception as e:
                    logger.error(f"Error reading snippet {filename}: {e}")
                    
        # Sort by relevance score (highest first)
        snippets.sort(key=lambda x: x["score"], reverse=True)
        
        # Return the top 5 snippets
        return snippets[:5]
    
    def _generate_code_from_snippets(self, task: str, snippets: List[Dict[str, Any]], 
                                   language: str) -> str:
        """Generate code for a task based on relevant snippets.
        
        Args:
            task: Task description
            snippets: List of relevant code snippets
            language: Target programming language
            
        Returns:
            Generated code
        """
        # Generate a basic skeleton based on the task
        skeleton = self._generate_skeleton_code(task, language)
        
        # Combine with the most relevant snippets
        task_words = self._extract_keywords(task)
        task_parts = task.lower().split()
        
        if language == "python":
            # For Python, generate a comprehensive module
            if any(word in task_parts for word in ["class", "object", "oop"]):
                # Generate a class-based solution
                return self._generate_python_class(task, snippets)
            else:
                # Generate a function-based solution
                return self._generate_python_functions(task, snippets)
                
        elif language in ["js", "javascript"]:
            # For JavaScript, generate appropriate module
            if any(word in task_parts for word in ["class", "object", "oop"]):
                return self._generate_javascript_class(task, snippets)
            else:
                return self._generate_javascript_functions(task, snippets)
                
        # For other languages, return the skeleton with snippets as comments
        code = skeleton + "\n\n/* Reference code snippets:\n\n"
        
        for i, snippet in enumerate(snippets):
            code += f"Snippet {i+1}:\n{snippet['content']}\n\n"
            
        code += "*/\n"
        
        return code
    
    def _generate_skeleton_code(self, task: str, language: str) -> str:
        """Generate a basic code skeleton for a task.
        
        Args:
            task: Task description
            language: Target programming language
            
        Returns:
            Skeleton code
        """
        task_words = task.lower().split()
        
        if language == "python":
            # Generate Python skeleton
            code = f'"""\n{task}\n"""\n\n'
            
            # Add common imports
            imports = ["import os", "import sys"]
            
            if "file" in task_words or "directory" in task_words:
                imports.append("import os.path")
                
            if "json" in task_words:
                imports.append("import json")
                
            if "time" in task_words or "date" in task_words:
                imports.append("import datetime")
                
            if "random" in task_words:
                imports.append("import random")
                
            if "web" in task_words or "http" in task_words:
                imports.append("import requests")
                
            code += "\n".join(imports) + "\n\n"
            
            # Add main function
            code += f"""def main():\n    """{task}\n    pass\n\nif __name__ == "__main__":\n    main()"""
            
            return code
            
        elif language in ["js", "javascript"]:
            # Generate JavaScript skeleton
            code = f'/**\n * {task}\n */\n\n'
            
            # Add a main function
            code += f"""function main() {{
    // {task}
}}

// Call the main function
main();"""

            return code
            
        else:
            # Generic skeleton for other languages
            return f"// Code for: {task}\n\n// TODO: Implement the solution\n"
    
    def _generate_python_class(self, task: str, snippets: List[Dict[str, Any]]) -> str:
        """Generate a Python class based on the task and snippets.
        
        Args:
            task: Task description
            snippets: Relevant code snippets
            
        Returns:
            Generated Python class code
        """
        # Extract a class name from the task
        words = re.findall(r'\b[A-Za-z][a-z]+\b', task.title())
        class_name = "".join(words)
        
        if not class_name:
            class_name = "TaskSolver"
            
        # Start with the docstring and imports
        code = f'"""\n{task}\n"""\n\n'
        
        # Add common imports
        imports = ["import os", "import sys", "import logging"]
        code += "\n".join(imports) + "\n\n"
        
        # Add logging configuration
        code += "# Configure logging\n"
        code += "logging.basicConfig(level=logging.INFO)\n"
        code += "logger = logging.getLogger(__name__)\n\n"
        
        # Start the class
        code += f"class {class_name}:\n"
        code += f'    """Class for {task}."""\n\n'
        
        # Add initialization
        code += "    def __init__(self):\n"
        code += '        """Initialize the class."""\n'
        code += f"        logger.info(\"{class_name} initialized\")\n\n"
        
        # Add methods based on task and snippets
        has_methods = False
        
        for snippet in snippets:
            if "pattern_type" in snippet["metadata"] and snippet["metadata"]["pattern_type"] == "function":
                # Extract function name and adapt it
                function_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', snippet["content"])
                
                if function_match:
                    func_name = function_match.group(1)
                    # Skip common function names like main, init, etc.
                    if func_name in ["main", "__init__", "__main__", "init"]:
                        continue
                        
                    # Extract function content
                    code_lines = snippet["content"].split('\n')
                    indented_lines = []
                    for line in code_lines:
                        # Skip function definition line
                        if line.strip().startswith("def "):
                            continue
                        # Indent the lines appropriately for a method
                        indented_lines.append("    " + line)
                        
                    # Add the method with adapted indentation
                    code += f"    def {func_name}(self, *args, **kwargs):\n"
                    code += f'        """Perform {func_name} operation."""\n'
                    code += "\n".join(indented_lines) + "\n\n"
                    has_methods = True
                    
        # If no methods were extracted from snippets, add a process method
        if not has_methods:
            code += "    def process(self, data):\n"
            code += '        """Process the input data."""\n'
            code += "        logger.info(f\"Processing data: {data}\")\n"
            code += "        # TODO: Implement processing logic\n"
            code += "        return data\n\n"
            
        # Add a main function to demonstrate usage
        code += "# Example usage\n"
        code += "if __name__ == \"__main__\":\n"
        code += f"    solver = {class_name}()\n"
        
        if has_methods:
            # Use the first method found
            first_method = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\(self', code)
            if first_method:
                method_name = first_method.group(1)
                code += f"    result = solver.{method_name}()\n"
                code += "    print(result)\n"
        else:
            code += "    result = solver.process(\"sample data\")\n"
            code += "    print(result)\n"
            
        return code
    
    def _generate_python_functions(self, task: str, snippets: List[Dict[str, Any]]) -> str:
        """Generate Python functions based on the task and snippets.
        
        Args:
            task: Task description
            snippets: Relevant code snippets
            
        Returns:
            Generated Python code with functions
        """
        # Start with the docstring and imports
        code = f'"""\n{task}\n"""\n\n'
        
        # Add common imports
        imports = ["import os", "import sys", "import logging"]
        code += "\n".join(imports) + "\n\n"
        
        # Add logging configuration
        code += "# Configure logging\n"
        code += "logging.basicConfig(level=logging.INFO)\n"
        code += "logger = logging.getLogger(__name__)\n\n"
        
        # Add functions from snippets
        added_functions = set()
        for snippet in snippets:
            content = snippet["content"]
            
            # Try to extract function definition
            function_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)', content)
            
            if function_match:
                func_name = function_match.group(1)
                
                # Skip if we already added this function or it's a special function
                if func_name in added_functions or func_name in ["__init__"]:
                    continue
                    
                # Add the function (original code)
                code += content + "\n\n"
                added_functions.add(func_name)
                
        # If no functions were extracted, add a basic function
        if not added_functions:
            code += "def process_task(data):\n"
            code += f'    """{task}"""\n'
            code += "    logger.info(f\"Processing data: {data}\")\n"
            code += "    # TODO: Implement processing logic\n"
            code += "    return data\n\n"
            
        # Add a main function
        code += "def main():\n"
        code += f'    """{task}"""\n'
        
        if added_functions:
            for func in added_functions:
                # Skip test, main, and helper functions
                if func in ["main", "test", "setup", "helper"]:
                    continue
                    
                code += f"    result = {func}()\n"
                code += "    print(result)\n"
        else:
            code += "    result = process_task(\"sample data\")\n"
            code += "    print(result)\n"
            
        code += "\nif __name__ == \"__main__\":\n"
        code += "    main()\n"
        
        return code
    
    def _generate_javascript_class(self, task: str, snippets: List[Dict[str, Any]]) -> str:
        """Generate a JavaScript class based on the task and snippets.
        
        Args:
            task: Task description
            snippets: Relevant code snippets
            
        Returns:
            Generated JavaScript class code
        """
        # Extract a class name from the task
        words = re.findall(r'\b[A-Za-z][a-z]+\b', task.title())
        class_name = "".join(words)
        
        if not class_name:
            class_name = "TaskSolver"
            
        # Start with the documentation
        code = f'/**\n * {task}\n */\n\n'
        
        # Start the class
        code += f"class {class_name} {{\n"
        
        # Add constructor
        code += "    /**\n"
        code += "     * Initialize the class\n"
        code += "     */\n"
        code += "    constructor() {\n"
        code += f"        console.log('{class_name} initialized');\n"
        code += "    }\n\n"
        
        # Add methods based on task and snippets
        has_methods = False
        
        for snippet in snippets:
            content = snippet["content"]
            
            # Try to extract method or function
            method_match = re.search(r'(?:function\s+([a-zA-Z_][a-zA-Z0-9_]*)|(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?\()', content)
            
            if method_match:
                method_name = method_match.group(1) or method_match.group(2)
                
                # Skip common names
                if method_name in ["main", "init", "constructor"]:
                    continue
                    
                # Extract the method body
                if "function " in content:
                    # For regular functions
                    body_match = re.search(r'function\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*{((?:(?:[^\n])+\n?)+)}', content)
                    if body_match:
                        body = body_match.group(1)
                    else:
                        continue
                else:
                    # For arrow functions
                    body_match = re.search(r'=\s*(?:async\s*)?\([^)]*\)\s*=>\s*{((?:(?:[^\n])+\n?)+)}', content)
                    if body_match:
                        body = body_match.group(1)
                    else:
                        continue
                        
                # Add the method with proper indentation
                code += f"    /**\n"
                code += f"     * {method_name} method\n"
                code += f"     */\n"
                code += f"    {method_name}(data) {{\n"
                
                # Indent the body
                body_lines = body.split('\n')
                for line in body_lines:
                    code += f"        {line.strip()}\n"
                    
                code += "    }\n\n"
                has_methods = True
                
        # If no methods were extracted, add a process method
        if not has_methods:
            code += "    /**\n"
            code += "     * Process the input data\n"
            code += "     * @param {any} data - The data to process\n"
            code += "     * @returns {any} - The processed data\n"
            code += "     */\n"
            code += "    process(data) {\n"
            code += "        console.log(`Processing data: ${data}`);\n"
            code += "        // TODO: Implement processing logic\n"
            code += "        return data;\n"
            code += "    }\n"
            
        # Close the class
        code += "}\n\n"
        
        # Add example usage
        code += "// Example usage\n"
        code += f"const solver = new {class_name}();\n"
        
        if has_methods:
            # Use the first method found
            first_method = re.search(r'\s+([a-zA-Z_][a-zA-Z0-9_]*)\(data\)', code)
            if first_method:
                method_name = first_method.group(1)
                code += f"const result = solver.{method_name}('sample data');\n"
                code += "console.log(result);\n"
        else:
            code += "const result = solver.process('sample data');\n"
            code += "console.log(result);\n"
            
        # Add module export
        code += f"\nmodule.exports = {class_name};\n"
        
        return code
    
    def _generate_javascript_functions(self, task: str, snippets: List[Dict[str, Any]]) -> str:
        """Generate JavaScript functions based on the task and snippets.
        
        Args:
            task: Task description
            snippets: Relevant code snippets
            
        Returns:
            Generated JavaScript code with functions
        """
        # Start with the documentation
        code = f'/**\n * {task}\n */\n\n'
        
        # Add functions from snippets
        added_functions = set()
        for snippet in snippets:
            content = snippet["content"]
            
            # Try to extract function definition
            function_match = re.search(r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)', content)
            arrow_match = re.search(r'(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(?:async\s*)?\(', content)
            
            if function_match:
                func_name = function_match.group(1)
                
                # Skip if we already added this function or it's a special function
                if func_name in added_functions or func_name in ["constructor"]:
                    continue
                    
                # Add the function (original code)
                code += content + "\n\n"
                added_functions.add(func_name)
                
            elif arrow_match:
                func_name = arrow_match.group(1)
                
                # Skip if we already added this function
                if func_name in added_functions:
                    continue
                    
                # Add the function (original code)
                code += content + "\n\n"
                added_functions.add(func_name)
                
        # If no functions were extracted, add a basic function
        if not added_functions:
            code += "/**\n"
            code += f" * {task}\n"
            code += " * @param {any} data - The data to process\n"
            code += " * @returns {any} - The processed data\n"
            code += " */\n"
            code += "function processTask(data) {\n"
            code += "    console.log(`Processing data: ${data}`);\n"
            code += "    // TODO: Implement processing logic\n"
            code += "    return data;\n"
            code += "}\n\n"
            added_functions.add("processTask")
            
        # Add a main function
        code += "/**\n"
        code += " * Main function\n"
        code += " */\n"
        code += "function main() {\n"
        
        for func in added_functions:
            # Skip test, main, and helper functions
            if func in ["main", "test", "setup", "helper"]:
                continue
                
            code += f"    const result = {func}('sample data');\n"
            code += "    console.log(result);\n"
            
        code += "}\n\n"
        
        # Call the main function
        code += "// Execute the main function\n"
        code += "main();\n"
        
        return code
    
    def generate_new_module_from_github(self, topic: str, module_type: str = "feature") -> Dict[str, Any]:
        """Generate a new module for RILEY based on GitHub learning.
        
        Args:
            topic: The topic for the new module
            module_type: Type of module ('feature', 'core', or 'util')
            
        Returns:
            Dictionary with generation results
        """
        try:
            # First learn from GitHub about this topic
            learn_result = self.learn_from_github_topic(topic, max_repos=3)
            
            # Generate code skeleton based on learned patterns
            code_result = self.generate_code_from_learned_patterns(
                f"Create a {module_type} module for {topic}",
                "python"
            )
            
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
                
            # Get the generated code
            module_code = code_result["generated_code"]
            
            # Write the module file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(module_code)
                
            return {
                "status": "success",
                "message": f"Successfully generated {module_type} module for {topic} from GitHub learning",
                "topic": topic,
                "path": filepath,
                "module_type": module_type,
                "learn_result": learn_result,
                "code_result": code_result
            }
            
        except Exception as e:
            logger.error(f"Error generating new module from GitHub: {e}")
            logger.error(traceback.format_exc())
            
            return {
                "status": "error",
                "message": f"Error generating module from GitHub: {str(e)}",
                "topic": topic
            }
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get statistics about GitHub learning activities.
        
        Returns:
            Dictionary with learning statistics
        """
        return self.learning_stats