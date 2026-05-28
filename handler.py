"""
SmartRepoSummarizer - GitHub Repository Analysis Handler

Analyzes GitHub repositories and generates concise summaries with
technology detection and key file identification.
"""

import json
import requests
from typing import Dict, List, Any, Optional


class GitHubAnalyzer:
    """GitHub repository analyzer."""
    
    def __init__(self, api_token: Optional[str] = None):
        """Initialize analyzer.
        
        Args:
            api_token: GitHub API token (optional, for rate limit bypass)
        """
        self.base_url = "https://api.github.com"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        if api_token:
            self.headers["Authorization"] = f"token {api_token}"
    
    def get_repo_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """Fetch repository metadata.
        
        Args:
            owner: Repository owner (username or organization)
            repo: Repository name
            
        Returns:
            Repository metadata dictionary
        """
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_repo_files(self, owner: str, repo: str, path: str = "") -> List[Dict[str, Any]]:
        """Get repository file listing.
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Subdirectory path (default: root)
            
        Returns:
            List of file/directory metadata
        """
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def identify_important_files(self, files: List[Dict[str, Any]], depth: int = 0) -> List[Dict[str, str]]:
        """Identify and rank important files.
        
        Args:
            files: List of file metadata from GitHub API
            depth: Current directory depth
            
        Returns:
            Ranked list of important files with descriptions
        """
        important_patterns = {
            "README.md": "Main documentation and project overview",
            "readme.md": "Main documentation and project overview",
            "package.json": "Node.js dependencies and scripts",
            "pyproject.toml": "Python project configuration",
            "setup.py": "Python package setup",
            "requirements.txt": "Python dependencies",
            "Cargo.toml": "Rust project configuration",
            "go.mod": "Go module dependencies",
            "Gemfile": "Ruby dependencies",
            "composer.json": "PHP dependencies",
            "docker-compose.yml": "Docker container orchestration",
            "Dockerfile": "Docker build instructions",
            ".github/workflows/": "GitHub Actions CI/CD",
            "src/": "Source code directory",
            "lib/": "Library code directory",
            "tests/": "Test suite",
            "docs/": "Documentation files",
            "index.js": "Main entry point",
            "main.py": "Main Python script",
            "app.py": "Application entry point",
            "server.js": "Server entry point",
        }
        
        important = []
        
        for file in files:
            file_type = file.get("type", "")
            file_name = file.get("name", "")
            file_path = file.get("path", "")
            
            # Check direct matches
            if file_name in important_patterns:
                important.append({
                    "file": file_name,
                    "purpose": important_patterns[file_name]
                })
            # Check directory patterns
            elif file_type == "dir":
                for pattern, desc in important_patterns.items():
                    if file_name == pattern.rstrip("/"):
                        important.append({
                            "file": file_name + "/",
                            "purpose": desc
                        })
                        break
        
        # Sort by relevance (README first, then config files, then directories)
        priority = ["README.md", "readme.md", "package.json", "pyproject.toml", "setup.py"]
        important.sort(key=lambda x: priority.index(x["file"]) if x["file"] in priority else len(priority))
        
        return important[:10]  # Return top 10 most important files
    
    def detect_technologies(self, repo_info: Dict[str, Any], files: List[Dict[str, Any]]) -> List[str]:
        """Detect technologies used in the repository.
        
        Args:
            repo_info: Repository metadata
            files: List of repository files
            
        Returns:
            List of detected technologies
        """
        technologies = set()
        
        # Primary language
        primary_lang = repo_info.get("language")
        if primary_lang:
            technologies.add(primary_lang)
        
        # Check file extensions and names
        file_names = [f.get("name", "").lower() for f in files]
        
        tech_indicators = {
            "package.json": ["JavaScript", "TypeScript", "Node.js", "npm"],
            "requirements.txt": ["Python", "pip"],
            "pyproject.toml": ["Python", "Poetry"],
            "Cargo.toml": ["Rust", "Cargo"],
            "go.mod": ["Go", "Golang"],
            "Gemfile": ["Ruby", "Bundler"],
            "composer.json": ["PHP", "Composer"],
            "dockerfile": ["Docker"],
            "docker-compose.yml": ["Docker", "Docker Compose"],
            "Makefile": ["Make"],
            ".gitignore": ["Git"],
        }
        
        for file_name, techs in tech_indicators.items():
            if any(file_name in name for name in file_names):
                technologies.update(techs)
        
        # Check topics/tags
        topics = repo_info.get("topics", [])
        for topic in topics:
            technologies.add(topic.title())
        
        return sorted(list(technologies))


class LLMClient:
    """Simple LLM client for generating summaries."""
    
    def __init__(self, model: str = "default"):
        """Initialize LLM client.
        
        Args:
            model: Model name to use
        """
        self.model = model
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text using LLM.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        # In a real implementation, this would call an LLM API
        # For now, we'll use a placeholder that returns structured analysis
        # This would be replaced with actual LLM integration
        pass


def load_prompt(prompt_file: str = "prompt.txt") -> str:
    """Load prompt template from file.
    
    Args:
        prompt_file: Path to prompt template file
        
    Returns:
        Prompt template string
    """
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        # Return default prompt if file not found
        return """Analyze the following GitHub repository and provide a structured summary:

Repository: {repository_url}
Owner: {owner}
Repo: {repo}

Your task:
1. Identify the project's main purpose
2. Detect technologies used (languages, frameworks, tools)
3. List important files and directories
4. Explain in beginner-friendly terms
5. Provide a TL;DR one-sentence summary

Rules:
- Be concise (max 400 words total)
- Only use information from the repository
- Do not hallucinate features not present
- Format output as markdown with clear sections
- Keep explanations simple and clear

Output format:
## Project Purpose
[2-3 sentences explaining what the project does]

## Technologies
- [Technology 1]
- [Technology 2]
- [etc.]

## Important Files
- [filename]: [brief purpose]
- [filename]: [brief purpose]
- [etc.]

## Beginner Explanation
[Simple explanation as if teaching someone new to the project]

## TL;DR
[One sentence summary]"""


def format_output(analysis: Dict[str, Any]) -> str:
    """Format analysis results as markdown.
    
    Args:
        analysis: Analysis results dictionary
        
    Returns:
        Formatted markdown string
    """
    output = []
    
    output.append(f"# {analysis['repo_name']} - Repository Analysis\n")
    
    if "error" in analysis:
        output.append(f"**Error**: {analysis['error']}")
        return "\n".join(output)
    
    # Project Purpose
    output.append("## Project Purpose\n")
    output.append(analysis["purpose"])
    output.append("")
    
    # Technologies
    output.append("## Technologies\n")
    for tech in analysis["technologies"]:
        output.append(f"- {tech}")
    output.append("")
    
    # Important Files
    output.append("## Important Files\n")
    for file_info in analysis["important_files"]:
        output.append(f"- `{file_info['file']}`: {file_info['purpose']}")
    output.append("")
    
    # Beginner Explanation
    output.append("## Beginner Explanation\n")
    output.append(analysis["beginner_explanation"])
    output.append("")
    
    # TL;DR
    output.append("## TL;DR\n")
    output.append(analysis["tldr"])
    output.append("")
    
    return "\n".join(output)


def analyze_repository(repository_url: str, owner: str, repo: str, api_token: Optional[str] = None) -> Dict[str, Any]:
    """Main function to analyze a GitHub repository.
    
    Args:
        repository_url: Full GitHub repository URL
        owner: Repository owner
        repo: Repository name
        api_token: Optional GitHub API token
        
    Returns:
        Analysis results dictionary
    """
    try:
        # Initialize analyzer
        analyzer = GitHubAnalyzer(api_token=api_token)
        
        # Fetch repository info
        repo_info = analyzer.get_repo_info(owner, repo)
        
        # Get root files
        files = analyzer.get_repo_files(owner, repo)
        
        # Identify important files
        important_files = analyzer.identify_important_files(files)
        
        # Detect technologies
        technologies = analyzer.detect_technologies(repo_info, files)
        
        # Build analysis result
        analysis = {
            "repo_name": f"{owner}/{repo}",
            "repository_url": repository_url,
            "description": repo_info.get("description", "No description available"),
            "purpose": repo_info.get("description", "No description available") or "This project's purpose is not clearly stated in the repository.",
            "technologies": technologies,
            "important_files": important_files,
            "beginner_explanation": f"This is a {', '.join(technologies[:3])} project that {repo_info.get('description', 'provides useful functionality')}. It's designed to be easy to understand and use, even for those new to the technologies involved.",
            "tldr": f"{repo_info.get('description', 'A useful software project')} - built with {', '.join(technologies[:3])}.",
            "stargazers": repo_info.get("stargazers_count", 0),
            "forks": repo_info.get("forks_count", 0),
            "language": repo_info.get("language", "Unknown")
        }
        
        return analysis
        
    except requests.exceptions.RequestException as e:
        return {
            "repo_name": f"{owner}/{repo}",
            "repository_url": repository_url,
            "error": f"Failed to fetch repository: {str(e)}"
        }
    except Exception as e:
        return {
            "repo_name": f"{owner}/{repo}",
            "repository_url": repository_url,
            "error": f"Analysis failed: {str(e)}"
        }


def main():
    """Main entry point for the skill."""
    # Example usage
    result = analyze_repository(
        repository_url="https://github.com/langchain-ai/langchain",
        owner="langchain-ai",
        repo="langchain"
    )
    
    # Format and print output
    output = format_output(result)
    print(output)
    
    return result


if __name__ == "__main__":
    main()
