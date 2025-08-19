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

This repository is organized with each scenario in its own Git branch. Here's how to navigate between scenarios:

### Switching Between Scenarios

To work with a specific scenario:

```bash
# Switch to a scenario branch
git checkout scenario_00  # or scenario_01, scenario_02, etc.

# Verify you're on the correct branch
git branch

# List files in the current scenario
ls
```

### Scenario File Structure

**Main Branch** (`main`):
- Contains only setup files: `README.md`, `requirements.txt`, `.env.sample`, `.gitignore`

**Scenario 00** (`scenario_00`):
```
├── main.py                 # Scenario implementation
├── README_scenario_00.md   # Scenario-specific instructions
├── requirements.txt        # Dependencies
├── .env.sample            # Environment template
└── .gitignore             # Git ignore rules
```

**Scenarios 01-05** (`scenario_01` through `scenario_05`):
```
├── main.py                 # Scenario implementation
├── README_scenario_XX.md   # Scenario-specific instructions
├── _shared/               # Shared utilities and tracing code
│   └── tracing.py         # Common tracing functions
├── requirements.txt        # Dependencies
├── .env.sample            # Environment template
└── .gitignore             # Git ignore rules
```

## Running a Scenario

1. **Switch to the desired scenario branch**:
   ```bash
   git checkout scenario_01  # Replace with your chosen scenario
   ```

2. **Read the scenario-specific instructions**:
   ```bash
   # View scenario details
   cat README_scenario_01.md  # Replace with your scenario number
   ```

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

## Development Workflow

When working on scenarios:

1. Always start from the appropriate scenario branch
2. Make changes only to files in that branch
3. Test your changes before switching scenarios
4. Use `git status` to verify you're on the correct branch

## Troubleshooting

### Common Issues

- **Import errors**: Ensure you're on the correct scenario branch and virtual environment is activated
- **API errors**: Verify your `.env` file is properly configured with a valid token
- **Missing files**: Confirm you're on the correct branch with `git branch`

### Getting Help

- Check the scenario-specific README file (`README_scenario_XX.md`)
- Verify your Python environment setup
- Ensure all dependencies are installed with `pip install -r requirements.txt`

## Contributing

This repository is designed for user studies and educational purposes. Each scenario should remain isolated in its respective branch to maintain clean testing environments.
