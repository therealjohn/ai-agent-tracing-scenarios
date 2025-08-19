# AI Agent Tracing Scenarios

This repository contains interactive scenarios designed to demonstrate and explore AI agent tracing capabilities. Each scenario is isolated in its own branch to provide a clean testing environment for user studies and experimentation.

## What is AI Tracing?

AI tracing is a powerful observability technique that helps developers understand, debug, and optimize AI applications by capturing detailed execution information. Here's why tracing is essential for AI applications:

### Benefits of AI Tracing

- **Debugging Complex AI Workflows**: Track the flow of data through multi-step AI processes, making it easier to identify where issues occur
- **Performance Optimization**: Monitor response times, token usage, and resource consumption to optimize costs and performance
- **Quality Assurance**: Capture inputs, outputs, and intermediate steps to validate AI behavior and ensure consistent results
- **Compliance & Auditing**: Maintain detailed logs of AI decisions for regulatory compliance and audit trails
- **Cost Management**: Track API calls, token usage, and compute resources to manage AI operational costs
- **User Experience**: Monitor AI response quality and latency to improve user interactions

### Common Use Cases

- **Multi-agent Systems**: Track interactions between different AI agents
- **RAG Applications**: Monitor retrieval, generation, and augmentation steps
- **AI Pipelines**: Observe data flow through complex processing chains
- **Model Comparisons**: Compare performance across different AI models
- **Production Monitoring**: Real-time monitoring of AI applications in production

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.8+**: Download from [python.org](https://python.org)
- **Git**: Download from [git-scm.com](https://git-scm.com)
- **VS Code** (recommended): Download from [code.visualstudio.com](https://code.visualstudio.com)

## Initial Setup

### 1. Clone and Setup Python Environment

```bash
# Clone the repository
git clone https://github.com/therealjohn/ai-agent-tracing-scenarios.git
cd ai-agent-tracing-scenarios

# Fetch all remote branches and set up local tracking branches
git fetch --all
git checkout scenario_01
git checkout scenario_02
git checkout scenario_03
git checkout scenario_04
git checkout scenario_05
git checkout scenario_06
git checkout main

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Access

1. Navigate to [GitHub Models](https://github.com/marketplace/models) and select a model like GPT-4o
2. Select the 'Use this model' button in the upper-right
3. Select the 'Create Personal Access Token' button
4. Select the 'Generate new token' button and 'Generate new token (classic)'
5. Scroll down to the bottom and select 'Generate token'
6. Copy the generated token
7. Create a `.env` file in the repository root (copy from `.env.sample`)
8. Paste the token value for the `API_CREDENTIAL_TOKEN` variable in your `.env` file

## Scenario Navigation

This repository is organized with each scenario in its own Git branch. Each scenario provides hands-on experience with different aspects of AI agent tracing.

### Clone Repository with All Branches

```bash
# Clone the repository
git clone https://github.com/therealjohn/ai-agent-tracing-scenarios.git
cd ai-agent-tracing-scenarios

# Fetch all remote branches
git fetch --all

# Create local tracking branches for all scenarios
git checkout scenario_01
git checkout scenario_02  
git checkout scenario_03
git checkout scenario_04
git checkout scenario_05
git checkout scenario_06

# Return to main branch for setup
git checkout main
```

Now you'll have all scenario branches available locally and can switch between them easily.

### Available Scenarios

- **Scenario 01**: Basic tracing setup and foundations
- **Scenario 02**: Function calling and tool usage tracing  
- **Scenario 03**: Error handling and debugging with tracing
- **Scenario 04**: Complex workflows and multi-agent interactions
- **Scenario 05**: Performance monitoring and optimization
- **Scenario 06**: Custom metrics and advanced tracing patterns

### Switching Between Scenarios

To work with a specific scenario:

```bash
# Switch to a scenario branch
git checkout scenario_01  # or scenario_02, scenario_03, etc.

# Verify you're on the correct branch
git branch

# List files in the current scenario
ls
```

### Scenario File Structure

**Main Branch** (`main`):
- Contains only setup files: `README.md`, `requirements.txt`, `.env.sample`, `.gitignore`

**All Scenarios** (`scenario_01` through `scenario_06`):
```
├── main.py                 # Scenario implementation
├── _shared/               # Shared utilities and tracing code
│   └── tracing.py         # Common tracing functions
├── requirements.txt        # Dependencies
├── .env.sample            # Environment template
└── .gitignore             # Git ignore rules
```

## Running a Scenario

1. **Switch to the desired scenario branch**:
   ```bash
   git checkout scenario_02  # Replace with your chosen scenario
   ```

2. **Read the scenario-specific instructions**:
   
   View the scenario instructions at 

3. **Ensure your virtual environment is activated**:
   ```bash
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Run the scenario**:
   ```bash
   python main.py
   ```

## Contributing

This repository is designed for user studies and educational purposes. Each scenario should remain isolated in its respective branch to maintain clean testing environments.
