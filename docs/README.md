# AI Agent Tracing Scenarios

> Interactive scenarios demonstrating AI agent tracing capabilities for user study and education

## Welcome to the AI Tracing User Study! 👋

This documentation site will guide you through a series of hands-on scenarios designed to help you understand and explore AI agent tracing. Whether you're new to AI tracing or looking to deepen your understanding, these scenarios will provide practical experience with real-world tracing patterns.

## What You'll Learn 🎯

- **Understanding AI Tracing**: Learn what tracing is and why it's essential for AI applications
- **Hands-on Experience**: Work through 6 progressive scenarios from basic to advanced
- **Best Practices**: Discover industry-standard patterns for implementing tracing
- **Real-world Applications**: See how tracing applies to different AI use cases

## Quick Navigation 🚀

<!-- tabs:start -->

#### **🏃‍♂️ I'm Ready to Start**

1. **[Setup Instructions](setup.md)** - Get your environment ready
2. **[Scenario Overview](scenarios/overview.md)** - See all available scenarios
3. **[Scenario 00](scenarios/scenario-00.md)** - Start with the basics

#### **🤔 I'm New to AI Tracing**

1. **[What is AI Tracing?](ai-tracing-overview.md)** - Learn the fundamentals
2. **[Getting Started Guide](getting-started.md)** - Step-by-step introduction
3. **[Setup Instructions](setup.md)** - Prepare your environment

#### **⚡ I Want to Jump In**

```bash
# Quick setup (requires Git and Python 3.8+)
git clone https://github.com/therealjohn/ai-agent-tracing-scenarios.git
cd ai-agent-tracing-scenarios
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
git checkout scenario_00
```

<!-- tabs:end -->

## Study Structure 📚

This user study consists of **6 progressive scenarios**, each building on the previous one:

| Scenario | Focus Area | Complexity | Time Estimate |
|----------|------------|------------|---------------|
| [00](scenarios/scenario-00.md) | Basic Tracing Setup | Beginner | 15-20 min |
| [01](scenarios/scenario-01.md) | Intermediate Patterns | Beginner+ | 20-25 min |
| [02](scenarios/scenario-02.md) | Advanced Tracing | Intermediate | 25-30 min |
| [03](scenarios/scenario-03.md) | Multi-Agent Systems | Intermediate+ | 30-35 min |
| [04](scenarios/scenario-04.md) | Performance Monitoring | Advanced | 25-30 min |
| [05](scenarios/scenario-05.md) | Production Ready | Advanced | 30-40 min |

## Repository Structure 🗂️

Each scenario is isolated in its own Git branch to provide a clean testing environment:

```
main branch          # Setup files only
├── README.md        # This documentation
├── requirements.txt # Python dependencies
└── .env.sample     # Environment template

scenario_XX branch   # Individual scenarios
├── main.py         # Scenario implementation
├── README_scenario_XX.md  # Specific instructions
├── _shared/        # Utilities (scenarios 01-05 only)
└── ...            # Other setup files
```

## Prerequisites ✅

Before starting, ensure you have:

- **Python 3.8+** installed
- **Git** installed  
- **GitHub account** with access to GitHub Models
- **Basic Python knowledge** (variables, functions, imports)
- **15-30 minutes** per scenario

## Need Help? 🆘

- 📋 **[Troubleshooting Guide](troubleshooting.md)** - Common issues and solutions
- 📚 **[Additional Resources](resources.md)** - Links and references
- 🐛 **Found a bug?** [Open an issue](https://github.com/therealjohn/ai-agent-tracing-scenarios/issues)

---

## Ready to Begin? 🎯

👉 **[Start with the Setup Instructions](setup.md)** or jump directly to **[Understanding AI Tracing](ai-tracing-overview.md)**
