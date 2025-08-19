# Setup Instructions

Complete environment setup for the AI tracing scenarios.

## Prerequisites

Before starting, install the following:

- **Python 3.8+** - [Download from python.org](https://python.org)
- **Git** - [Download from git-scm.com](https://git-scm.com)
- **VS Code** - [Download from code.visualstudio.com](https://code.visualstudio.com)
- **AI Toolkit (Prerelease)** - Install from VS Code Extensions

### Install AI Toolkit Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "AI Toolkit"
4. Install the **Prerelease** version
5. Restart VS Code

## Quick Setup

### 1. Clone Repository and Setup Environment

```bash
# Clone the repository
git clone https://github.com/therealjohn/ai-agent-tracing-scenarios.git
cd ai-agent-tracing-scenarios

# Get all the branches
git fetch --all

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Access

1. Go to [GitHub Models](https://github.com/marketplace/models)
2. Select a model (e.g., GPT-4o)
3. Click "Use this model" → "Create Personal Access Token"
4. Generate a new classic token
5. Copy the token
6. Create `.env` file from template:
   ```bash
   cp .env.sample .env
   ```
7. Edit `.env` and add your token:
   ```
   API_CREDENTIAL_TOKEN=your_github_token_here
   ```

### 3. Verify Setup

```bash
# Test environment
python -c "import openai; print('Setup complete!')"
```

## VS Code Configuration

1. Open the repository folder in VS Code
2. Ensure the AI Toolkit extension is installed
3. The Tracing Viewer will be available in the AI Toolkit panel

You're now ready to start the scenarios!

[Begin with Scenario 1](scenario-01.md)