# SmartRepoSummarizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

Automatically analyze GitHub repositories and generate concise, structured summaries with technology detection and key file identification.

## 🎯 Problem Solved

When exploring new GitHub repositories, developers often face:
- Too much information to scan quickly
- Unclear project purpose and scope
- Difficulty identifying the tech stack
- Hard to find important files

**SmartRepoSummarizer** solves this by providing instant, structured analysis of any public GitHub repository.

## ✨ Features

- **Repository Analysis**: Fetches metadata from GitHub API
- **Technology Detection**: Automatically identifies languages, frameworks, and tools
- **Key File Identification**: Lists most important files with descriptions
- **Beginner-Friendly**: Simple explanations for newcomers
- **TL;DR Summaries**: One-sentence overview
- **Concise Output**: Maximum 400 words, no fluff

## 📦 Installation

### Option 1: Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/smart-repo-summarizer.git
cd smart-repo-summarizer
```

### Option 2: Download as ZIP

Download the latest release from the [Releases tab](https://github.com/YOUR_USERNAME/smart-repo-summarizer/releases).

### Requirements

- Python 3.6 or higher
- `requests` library (included in standard installation)

```bash
pip install requests
```

## 🚀 Usage

### Basic Usage

```python
from handler import analyze_repository, format_output

# Analyze a repository
result = analyze_repository(
    repository_url="https://github.com/langchain-ai/langchain",
    owner="langchain-ai",
    repo="langchain"
)

# Format as markdown
output = format_output(result)
print(output)
```

### Command Line

```bash
python handler.py
```

### As a Skill (IronClaw)

```python
# Pass repository data to the skill
skill_input = {
    "repository_url": "https://github.com/owner/repo",
    "owner": "owner",
    "repo": "repo"
}

# The skill returns a structured analysis
```

## 📋 Output Format

The skill returns a structured analysis with the following sections:

```markdown
# owner/repo - Repository Analysis

## Project Purpose
[2-3 sentences explaining what the project does]

## Technologies
- Technology 1
- Technology 2
- Technology 3

## Important Files
- `README.md`: Main documentation and project overview
- `package.json`: Node.js dependencies and scripts
- `src/`: Source code directory

## Beginner Explanation
[Simple explanation as if teaching someone new to the project]

## TL;DR
[One sentence summary]
```

## 💡 Example

### Input

```
Repository: https://github.com/langchain-ai/langchain
Owner: langchain-ai
Repo: langchain
```

### Output

```markdown
# langchain-ai/langchain - Repository Analysis

## Project Purpose
LangChain is a framework for developing applications powered by language models. It enables developers to build AI applications by connecting language models to external data sources and computational resources.

## Technologies
- Python
- TypeScript
- LLM
- NLP
- AI
- Agents
- Docker
- GraphQL

## Important Files
- `README.md`: Main documentation and project overview
- `pyproject.toml`: Python project configuration
- `package.json`: Node.js dependencies and scripts
- `libs/langchain/__init__.py`: Main library entry point
- `docs/`: Documentation files
- `tests/`: Test suite

## Beginner Explanation
This is a Python and TypeScript project that helps developers build AI applications using language models. It's designed to make it easy to connect AI models with external data sources, even if you're new to AI development. Think of it as a toolbox for creating smart applications.

## TL;DR
A framework for building AI applications that connect language models with external data sources - built with Python, TypeScript, and LLM technology.
```

## 🔧 Configuration

### GitHub API Token (Optional)

For higher rate limits, you can provide a GitHub API token:

```python
from handler import analyze_repository

result = analyze_repository(
    repository_url="https://github.com/owner/repo",
    owner="owner",
    repo="repo",
    api_token="your_github_token"
)
```

Get a token from: https://github.com/settings/tokens

## 📁 Project Structure

```
smart_repo_summarizer/
├── skill.json          # Skill configuration and metadata
├── handler.py          # Main analysis logic
├── prompt.txt          # LLM prompt template
└── README.md           # This file
```

## 🛠️ How It Works

1. **Fetch Repository Info**: Uses GitHub API to get metadata
2. **List Files**: Retrieves repository file structure
3. **Identify Important Files**: Matches against known important patterns (README, package.json, etc.)
4. **Detect Technologies**: Analyzes file extensions, names, and repository topics
5. **Generate Summary**: Formats results into a structured, readable output

## 🤝 Why This Is Useful

- **Quick Evaluation**: Assess a project in seconds instead of minutes
- **Onboarding**: Help new developers understand repositories faster
- **Research**: Compare multiple projects efficiently
- **Learning**: Discover what technologies a project uses
- **Documentation**: Generate summaries for internal knowledge bases

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or feedback, open an issue on GitHub.

---

**Built with ❤️ for the developer community**
