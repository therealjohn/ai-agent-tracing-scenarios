# Scenario 00: Basic Tracing Setup

> Learn fundamental AI tracing concepts with a simple, single-function implementation

## Overview 🎯

Welcome to your first AI tracing scenario! This foundational scenario introduces core tracing concepts through a simple, focused example. You'll learn how to instrument a basic AI function and understand the structure of trace data.

**Difficulty**: Beginner | **Time**: 15-20 minutes

## Learning Objectives 📚

By the end of this scenario, you'll understand:

- ✅ What a trace span is and how to create one
- ✅ How to add attributes and metadata to traces
- ✅ Basic trace output structure and interpretation
- ✅ Foundation concepts used in all other scenarios

## Scenario Description 📋

This scenario implements a simple AI-powered text summarization function with basic tracing. You'll observe how tracing captures:

- Function entry and exit
- Input parameters and output results
- Execution timing
- Basic metadata

The implementation is intentionally simple to focus on tracing fundamentals without complexity.

## Getting Started 🚀

### Step 1: Switch to Scenario Branch

```bash
# Switch to the scenario_00 branch
git checkout scenario_00
```

Copy this command: `git checkout scenario_00`

### Step 2: Verify Setup

```bash
# Verify you're on the correct branch
git branch
# Should show: * scenario_00

# Verify files are present
ls
# Should show: main.py, README_scenario_00.md, requirements.txt, etc.

# Ensure virtual environment is active
# Your prompt should show (.venv)
```

### Step 3: Review the Code

Before running, examine the implementation:

```bash
# View the main implementation
cat main.py

# Or open in your editor
code main.py  # VS Code
notepad main.py  # Windows Notepad
```

### Step 4: Run the Scenario

```bash
# Execute the scenario
python main.py
```

## What You'll See 👀

When you run the scenario, you'll observe:

### Console Output
The script will display:
1. **Function execution** - The AI summarization in action
2. **Trace output** - Structured trace data showing the execution flow
3. **Results** - Both the AI-generated summary and trace metadata

### Trace Structure
The trace output includes:
- **Span ID** - Unique identifier for this operation
- **Operation Name** - What function was traced
- **Duration** - How long the operation took
- **Attributes** - Input parameters, model details, token usage
- **Status** - Success/failure indication

## Key Concepts Explained 🔑

### Spans
A **span** represents a single operation in your application:
```python
with tracer.start_as_current_span("summarize_text") as span:
    # Your function logic here
    # Everything in this block is traced
```

### Attributes
**Attributes** add context to your spans:
```python
span.set_attribute("input.text_length", len(text))
span.set_attribute("model.name", "gpt-4")
span.set_attribute("output.summary_length", len(summary))
```

### Timing
Tracing automatically captures:
- Start time
- End time  
- Duration
- Timestamp information

## Experiment and Learn 🧪

Try these modifications to deepen your understanding:

### Experiment 1: Add More Attributes
Add additional attributes to capture more context:

```python
# Add these in the span context
span.set_attribute("user.id", "demo_user")
span.set_attribute("request.priority", "normal")
span.set_attribute("environment", "development")
```

### Experiment 2: Trace Multiple Calls
Modify the script to make multiple AI calls and observe how traces stack:

```python
# Try summarizing different texts
texts = [
    "Your first text here...",
    "Your second text here...",
    "Your third text here..."
]

for i, text in enumerate(texts):
    print(f"\n=== Summary {i+1} ===")
    summary = summarize_text(text)
    print(f"Summary: {summary}")
```

### Experiment 3: Add Error Scenarios
Introduce an error to see how tracing handles failures:

```python
# Try with empty or invalid input
try:
    summary = summarize_text("")  # Empty text
    print(f"Summary: {summary}")
except Exception as e:
    print(f"Error: {e}")
```

## Understanding the Output 📊

### Successful Trace Example
```json
{
  "span_id": "abc123...",
  "operation_name": "summarize_text", 
  "duration_ms": 1250,
  "status": "OK",
  "attributes": {
    "input.text_length": 156,
    "model.name": "gpt-4",
    "output.summary_length": 45,
    "token.usage.prompt": 20,
    "token.usage.completion": 15
  }
}
```

### What Each Field Means
- **span_id**: Unique identifier for this operation
- **operation_name**: The function being traced
- **duration_ms**: Time taken in milliseconds
- **status**: Success (OK) or failure status
- **attributes**: Custom metadata about the operation

## Common Issues and Solutions 🔧

### Issue: Import Errors
```bash
# Error: ModuleNotFoundError
# Solution: Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Issue: API Errors
```bash
# Error: Authentication failed
# Solution: Check your .env file configuration
cat .env
# Ensure API_CREDENTIAL_TOKEN is set correctly
```

### Issue: No Trace Output
```bash
# Error: Script runs but no traces shown
# Solution: Check if tracing is properly initialized
# Look for tracer initialization in the code
```

## Key Takeaways 💡

From this scenario, you should understand:

1. **Tracing Basics**: How to wrap functions with tracing
2. **Span Lifecycle**: Creation, execution, and completion
3. **Attribute Usage**: Adding meaningful context to traces
4. **Output Interpretation**: Reading and understanding trace data
5. **Foundation Skills**: Core concepts for advanced scenarios

## Real-World Applications 🌍

This basic tracing pattern applies to:

- **API Endpoints**: Trace request/response cycles
- **Data Processing**: Monitor ETL pipeline steps
- **AI Functions**: Track model inference calls
- **Business Logic**: Trace critical application flows
- **External Integrations**: Monitor third-party service calls

## Next Steps 🎯

Now that you understand basic tracing:

1. **Reflect**: Consider how you'd apply this to your own projects
2. **Experiment**: Try the suggested modifications above
3. **Advance**: Move on to the next scenario

👉 **[Continue to Scenario 01: Intermediate Tracing](scenario-01.md)**

👉 **[Return to Scenario Overview](overview.md)**

## Questions for Reflection 🤔

- How could tracing help debug issues in your current projects?
- What attributes would be most valuable for your use cases?
- Where might you want to add tracing in existing code?
- How could this trace data help with performance optimization?

---

## Need Help? 🆘

- **[Troubleshooting Guide](../troubleshooting.md)** - Common issues and solutions
- **[Setup Instructions](../setup.md)** - If you need to reconfigure
- **[AI Tracing Overview](../ai-tracing-overview.md)** - Review fundamental concepts

**Ready for the next challenge?** [Scenario 01](scenario-01.md) introduces multi-function tracing with shared utilities!