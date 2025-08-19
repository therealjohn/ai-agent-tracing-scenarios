# Setup Instructions

> Complete environment setup for the AI tracing scenarios

## Overview 📋

This guide will help you set up everything needed to run the AI tracing scenarios. The setup process takes about 10-15 minutes and ensures you have a clean, isolated environment for learning.

## System Requirements ✅

### Minimum Requirements
- **Python 3.8+** (Python 3.9+ recommended)
- **Git 2.0+**
- **10 GB free disk space**
- **Internet connection** (for downloading dependencies and API access)

### Supported Platforms
- ✅ **Windows 10+** (PowerShell or Command Prompt)
- ✅ **macOS 10.15+** (Terminal)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+, or equivalent)

## Step 1: Verify Prerequisites 🔍

First, let's verify your system has the required software installed:

<!-- tabs:start -->

#### **Windows (PowerShell)**

```powershell
# Open PowerShell as regular user (no admin needed)

# Check Python version (should show 3.8.0 or higher)
python --version

# Check Git installation
git --version

# Check pip is available
pip --version
```

#### **macOS (Terminal)**

```bash
# Open Terminal application

# Check Python version (should show 3.8.0 or higher)
python3 --version

# Check Git installation  
git --version

# Check pip is available
pip3 --version
```

#### **Linux (Terminal)**

```bash
# Open terminal

# Check Python version (should show 3.8.0 or higher)
python3 --version

# Check Git installation
git --version

# Check pip is available
pip3 --version
```

<!-- tabs:end -->

### Installing Missing Prerequisites

If any commands fail, install the missing software:

| Software | Windows | macOS | Linux |
|----------|---------|--------|--------|
| **Python** | [python.org](https://python.org) | `brew install python` | `sudo apt install python3 python3-pip` |
| **Git** | [git-scm.com](https://git-scm.com) | `brew install git` | `sudo apt install git` |

## Step 2: Clone the Repository 📥

Clone the repository and navigate to it:

```bash
# Clone the repository
git clone https://github.com/therealjohn/ai-agent-tracing-scenarios.git

# Navigate to the project directory
cd ai-agent-tracing-scenarios

# Verify you're in the right place
ls -la  # Should show README.md, requirements.txt, etc.
```

## Step 3: Create Python Virtual Environment 🐍

Create an isolated Python environment to avoid conflicts with your system Python:

<!-- tabs:start -->

#### **Windows (PowerShell)**

```powershell
# Create virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Verify activation (prompt should show (.venv))
# Your prompt should now start with (.venv)
```

**Note**: If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **macOS/Linux (Terminal)**

```bash
# Create virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Verify activation (prompt should show (.venv))
# Your prompt should now start with (.venv)
```

<!-- tabs:end -->

### Verification

After activation, verify your environment:

```bash
# Check Python location (should point to .venv)
which python  # macOS/Linux
where python  # Windows

# Check Python version
python --version
```

## Step 4: Install Dependencies 📦

Install the required Python packages:

```bash
# Ensure you're in the project directory with activated virtual environment
# Your prompt should show (.venv)

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages include:
- `openai` - For AI model interactions
- `python-dotenv` - For environment variable management
- `requests` - For HTTP requests
- Plus their dependencies

## Step 5: Configure API Access 🔑

Set up access to GitHub Models for AI functionality:

### 5.1 Get GitHub Personal Access Token

1. **Navigate** to [GitHub Models](https://github.com/marketplace/models)
2. **Select** a model (e.g., GPT-4o)
3. **Click** "Use this model" (upper-right)
4. **Click** "Create Personal Access Token"
5. **Click** "Generate new token" → "Generate new token (classic)"
6. **Configure** the token:
   - **Note**: "AI Tracing Scenarios"
   - **Expiration**: Choose appropriate duration (30-90 days recommended)
   - **Scopes**: The required scopes will be pre-selected
7. **Click** "Generate token"
8. **Copy** the generated token immediately (you won't see it again!)

### 5.2 Create Environment File

Create your environment configuration:

```bash
# Copy the sample environment file
cp .env.sample .env  # macOS/Linux
copy .env.sample .env  # Windows

# Open the .env file in your preferred editor
# VS Code: code .env
# Notepad: notepad .env
# Nano: nano .env
```

### 5.3 Configure the Environment File

Edit your `.env` file to include your token:

```bash
# .env file content
MODEL_ENDPOINT=https://models.github.ai/inference
API_CREDENTIAL_TOKEN=your_github_token_here
MODEL_NAME=openai/gpt-4.1-nano
```

**Replace** `your_github_token_here` with the token you copied from GitHub.

### 5.4 Verify API Configuration

Test your API setup:

```bash
# Quick test (we'll create a simple test)
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_CREDENTIAL_TOKEN')
print('✅ Token configured!' if token else '❌ Token missing!')
print(f'Token starts with: {token[:10]}...' if token else '')
"
```

## Step 6: Verify Complete Setup ✅

Let's verify everything is working correctly:

### 6.1 Environment Check

```bash
# Verify virtual environment is active
python -c "import sys; print('✅ Virtual env active!' if '.venv' in sys.prefix else '❌ Virtual env not active!')"

# Verify dependencies installed
python -c "import openai, dotenv; print('✅ Dependencies installed!')"

# Verify environment file
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_CREDENTIAL_TOKEN')
endpoint = os.getenv('MODEL_ENDPOINT')
model = os.getenv('MODEL_NAME')
print(f'✅ Environment configured!' if all([token, endpoint, model]) else '❌ Environment incomplete!')
"
```

### 6.2 Git Branch Check

```bash
# Verify current branch
git branch

# Should show: * main (or * docs if you're viewing documentation)

# Verify all scenario branches exist
git branch -a
```

You should see branches for `scenario_00` through `scenario_05`.

## Step 7: Test First Scenario 🚀

Let's test that everything works by running the first scenario:

```bash
# Switch to scenario 00
git checkout scenario_00

# Verify you're on the right branch
git branch

# List files (should see main.py and README_scenario_00.md)
ls

# Run the scenario (should execute without errors)
python main.py
```

If everything is working, you should see output from the AI tracing scenario!

## Troubleshooting 🔧

### Common Issues and Solutions

#### Virtual Environment Issues

**Problem**: "Command not found" or activation fails
```bash
# Solution: Recreate virtual environment
rm -rf .venv  # Remove existing environment
python -m venv .venv  # Create new environment
# Then activate and install dependencies again
```

#### Dependency Issues

**Problem**: Import errors or missing packages
```bash
# Solution: Reinstall dependencies
pip install --upgrade pip  # Upgrade pip first
pip install -r requirements.txt --force-reinstall
```

#### API Configuration Issues

**Problem**: "Invalid token" or API errors
- **Check token**: Ensure you copied the complete token
- **Check expiration**: Tokens can expire
- **Check scopes**: Regenerate with correct permissions
- **Check .env file**: Ensure no extra spaces or quotes

#### Git Branch Issues

**Problem**: "Branch not found" or wrong files
```bash
# Solution: Fetch all branches
git fetch origin
git checkout scenario_00
```

#### Platform-Specific Issues

**Windows PowerShell Execution Policy**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS Permission Issues**:
```bash
sudo xcode-select --install  # Install command line tools
```

**Linux Missing Packages**:
```bash
sudo apt update
sudo apt install python3-venv python3-pip git
```

## Post-Setup Workflow 🔄

Once setup is complete, your typical workflow will be:

1. **Activate environment** (if not already active):
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux  
   source .venv/bin/activate
   ```

2. **Switch to scenario**:
   ```bash
   git checkout scenario_XX
   ```

3. **Run the scenario**:
   ```bash
   python main.py
   ```

## Next Steps 🎯

Great! You're now ready to start learning AI tracing:

👉 **[Start with Scenario 00](scenarios/scenario-00.md)** - Basic tracing concepts

👉 **[View All Scenarios](scenarios/overview.md)** - See the complete learning path

👉 **[Troubleshooting Guide](troubleshooting.md)** - If you run into issues

---

## Need Help? 🆘

If you're still having issues after following this guide:

1. **Check the [Troubleshooting Guide](troubleshooting.md)**
2. **Verify each step was completed**
3. **Try the setup on a fresh terminal/command prompt**
4. **Check your internet connection for downloads**