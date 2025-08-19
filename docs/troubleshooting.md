# Troubleshooting Guide

> Common issues and solutions for the AI tracing scenarios

## Quick Diagnostic Checklist ✅

Before diving into specific issues, run through this quick checklist:

```bash
# 1. Check current branch
git branch
# Should show the scenario you're trying to run

# 2. Verify virtual environment  
echo $VIRTUAL_ENV  # macOS/Linux
echo $env:VIRTUAL_ENV  # Windows PowerShell
# Should show path to .venv

# 3. Check Python version
python --version
# Should be 3.8.0 or higher

# 4. Verify dependencies
pip list | grep -E "(openai|dotenv)"
# Should show installed packages

# 5. Test environment configuration
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ Config OK' if os.getenv('API_CREDENTIAL_TOKEN') else '❌ Missing token')"
```

## Common Issues by Category 🔧

### Git and Branch Issues

#### Wrong Branch Error
**Problem**: Files not found or wrong scenario content
```bash
# Check current branch
git branch

# Switch to correct branch
git checkout scenario_XX

# If branch doesn't exist, fetch from remote
git fetch origin
git checkout scenario_XX
```

#### Uncommitted Changes Blocking Switch
**Problem**: Can't switch branches due to uncommitted changes
```bash
# Stash changes temporarily
git stash

# Switch branch
git checkout scenario_XX

# Later, restore changes if needed
git stash pop
```

### Python Environment Issues

#### Virtual Environment Not Activated
**Problem**: Import errors or wrong Python version
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Verify activation (prompt should show (.venv))
which python  # Should point to .venv
```

#### Virtual Environment Corrupted
**Problem**: Activation fails or dependencies missing
```bash
# Remove and recreate virtual environment
rm -rf .venv  # macOS/Linux
rmdir /s .venv  # Windows

# Create new environment
python -m venv .venv

# Activate and reinstall
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
```

#### Python Version Issues
**Problem**: "Python 3.8+ required" errors
```bash
# Check your Python version
python --version

# If too old, install newer Python
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: sudo apt install python3.11
```

### Dependency and Import Issues

#### Package Not Found Errors
**Problem**: `ModuleNotFoundError` for required packages
```bash
# Ensure virtual environment is active
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# For specific package issues
pip install openai python-dotenv requests --upgrade
```

#### Import Path Issues
**Problem**: Can't import from `_shared` module
```bash
# Verify you're on correct branch (scenarios 01-05 need _shared)
git branch

# Check if _shared exists
ls _shared/

# If missing, ensure you're not on scenario_00
git checkout scenario_01  # or appropriate scenario
```

### API and Configuration Issues

#### Authentication Failures
**Problem**: "Invalid API key" or authentication errors

**Solution 1: Check .env file**
```bash
# Verify .env file exists and has content
cat .env

# Should contain:
# MODEL_ENDPOINT=https://models.github.ai/inference
# API_CREDENTIAL_TOKEN=your_token_here
# MODEL_NAME=openai/gpt-4.1-nano
```

**Solution 2: Regenerate token**
1. Go to [GitHub Models](https://github.com/marketplace/models)
2. Select a model and generate new token
3. Update `.env` file with new token

**Solution 3: Check token format**
```bash
# Token should start with 'ghp_' and be about 40 characters
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('API_CREDENTIAL_TOKEN')
print(f'Token length: {len(token) if token else 0}')
print(f'Token prefix: {token[:4] if token else \"None\"}')
"
```

#### Rate Limiting Issues
**Problem**: "Rate limit exceeded" errors
```bash
# Wait a few minutes before retrying
# Or modify code to add delays between requests
import time
time.sleep(2)  # Add between API calls
```

### Runtime and Execution Issues

#### Script Runs But No Output
**Problem**: Script completes but shows no traces or results

**Check 1: Verify scenario is correctly implemented**
```bash
# Look for main execution
cat main.py | grep -A 10 "if __name__"
```

**Check 2: Check for silent failures**
```bash
# Run with more verbose output
python -v main.py

# Or add debug prints to the code
```

#### Tracing Not Working
**Problem**: No trace output visible

**Solution 1: Check tracing initialization**
```python
# Look for tracer setup in code
# Should see something like:
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
```

**Solution 2: Check console output**
```bash
# Traces might be going to console exporter
# Look for trace output mixed with regular output
```

### Performance Issues

#### Slow Execution
**Problem**: Scenarios taking much longer than expected

**Solution 1: Check internet connection**
```bash
# Test API connectivity
curl -I https://models.github.ai/inference
```

**Solution 2: Check model configuration**
```bash
# Verify you're using the recommended model
grep MODEL_NAME .env
# Should be: openai/gpt-4.1-nano (faster than full gpt-4)
```

#### Memory Issues
**Problem**: Out of memory errors
```bash
# Monitor memory usage
python -c "
import psutil
print(f'Available RAM: {psutil.virtual_memory().available / 1024**3:.1f} GB')
"

# If low, close other applications or use smaller models
```

## Platform-Specific Issues 🖥️

### Windows Specific

#### PowerShell Execution Policy
**Problem**: Cannot run activation script
```powershell
# Check current policy
Get-ExecutionPolicy

# Set appropriate policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Path Issues
**Problem**: Python or Git not found
```powershell
# Check if Python in PATH
where python

# Add to PATH if needed (restart terminal after)
$env:PATH += ";C:\Python39"  # Adjust path as needed
```

### macOS Specific

#### Command Line Tools Missing
**Problem**: Git or other tools not available
```bash
# Install Xcode command line tools
xcode-select --install
```

#### Python Path Issues
**Problem**: Multiple Python versions conflict
```bash
# Use python3 explicitly
python3 -m venv .venv
python3 -m pip install -r requirements.txt
```

### Linux Specific

#### Missing System Packages
**Problem**: Build errors during pip install
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-dev python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3-devel python3-pip
```

## Advanced Debugging 🔍

### Enable Verbose Logging
```python
# Add to beginning of main.py for detailed logs
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components
```python
# Test API connectivity separately
import os
from dotenv import load_dotenv
load_dotenv()

# Test environment loading
print("Environment variables:")
print(f"TOKEN: {'Set' if os.getenv('API_CREDENTIAL_TOKEN') else 'Missing'}")
print(f"ENDPOINT: {os.getenv('MODEL_ENDPOINT')}")
print(f"MODEL: {os.getenv('MODEL_NAME')}")
```

### Clean Slate Approach
When all else fails, start fresh:
```bash
# 1. Clone fresh copy
cd ..
git clone https://github.com/therealjohn/ai-agent-tracing-scenarios.git fresh-copy
cd fresh-copy

# 2. Set up from scratch
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# 3. Configure .env
cp .env.sample .env
# Edit .env with your token

# 4. Test
git checkout scenario_00
python main.py
```

## Getting Additional Help 🆘

### Documentation Resources
- **[Setup Instructions](setup.md)** - Complete setup guide
- **[AI Tracing Overview](ai-tracing-overview.md)** - Concept review
- **[Scenario Overviews](scenarios/overview.md)** - All scenario details

### Self-Help Strategies
1. **Read Error Messages Carefully** - They often contain the solution
2. **Check Prerequisites** - Ensure all requirements are met
3. **Try Minimal Examples** - Start with simple test cases
4. **Compare Working Versions** - Look at other scenarios that work

### Community Resources
- **GitHub Issues** - Search for similar problems
- **Stack Overflow** - OpenTelemetry and Python tracing questions
- **Documentation** - Official OpenTelemetry docs

---

## Still Stuck? 🤔

If you've tried the solutions above and are still having issues:

1. **Document the Problem**:
   - What scenario are you running?
   - What command did you run?
   - What was the exact error message?
   - What's your operating system and Python version?

2. **Try the Minimal Test**:
   ```bash
   # Basic functionality test
   python -c "print('Python works')"
   git --version
   python -c "import openai; print('OpenAI imports')"
   ```

3. **Create an Issue**:
   - Include your problem documentation
   - Include the output of the minimal test
   - Describe what you've already tried

Remember: Most issues are environment-related and can be solved by carefully following the setup instructions!