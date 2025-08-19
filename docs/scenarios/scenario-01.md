# Scenario 01: Intermediate Tracing

> Build on tracing fundamentals with multi-function workflows and shared utilities

## Overview 🎯

Building on Scenario 00, this intermediate scenario introduces more sophisticated tracing patterns. You'll learn how to trace multiple functions working together, use shared tracing utilities, and manage trace context across function calls.

**Difficulty**: Beginner+ | **Time**: 20-25 minutes | **Prerequisites**: [Scenario 00](scenario-00.md)

## Learning Objectives 📚

By the end of this scenario, you'll understand:

- ✅ Multi-function tracing patterns and span hierarchies
- ✅ Shared tracing utilities and reusable components
- ✅ Trace context propagation between functions
- ✅ Error handling and exception tracing
- ✅ More complex attribute management

## Scenario Description 📋

This scenario implements an AI-powered document analysis pipeline with multiple steps:

1. **Document Processing** - Text extraction and cleaning
2. **Content Analysis** - Sentiment and topic analysis  
3. **Summary Generation** - AI-powered summarization
4. **Result Compilation** - Combining all analysis results

Each step is traced individually, creating a hierarchical trace structure that shows the complete workflow.

## Getting Started 🚀

### Step 1: Switch to Scenario Branch

```bash
# Switch to the scenario_01 branch
git checkout scenario_01
```

Copy this command: `git checkout scenario_01`

### Step 2: Verify Setup

```bash
# Verify you're on the correct branch
git branch
# Should show: * scenario_01

# Check files (should include _shared folder)
ls -la
# Should show: main.py, README_scenario_01.md, _shared/, etc.

# Examine shared utilities
ls _shared/
# Should show: tracing.py
```

### Step 3: Review the Code Structure

This scenario introduces shared utilities:

```bash
# Review the main implementation
cat main.py

# Examine shared tracing utilities
cat _shared/tracing.py

# View scenario-specific instructions
cat README_scenario_01.md
```

### Step 4: Run the Scenario

```bash
# Execute the scenario
python main.py
```

## What You'll See 👀

### Enhanced Console Output
You'll observe:
1. **Multi-step processing** - Each pipeline stage executing
2. **Hierarchical traces** - Parent and child spans
3. **Shared utility usage** - Common tracing patterns
4. **Error handling** - How failures are traced
5. **Performance insights** - Timing for each step

### Trace Hierarchy
```
📊 document_analysis_pipeline (parent span)
├── 📄 process_document (child span)
├── 🔍 analyze_content (child span)  
├── 📝 generate_summary (child span)
└── 📋 compile_results (child span)
```

## Key Concepts Explained 🔑

### Span Hierarchies
Child spans automatically inherit context from parent spans:
```python
with tracer.start_as_current_span("parent_operation") as parent_span:
    # This creates a child span under the parent
    with tracer.start_as_current_span("child_operation") as child_span:
        # Child operations here
```

### Shared Tracing Utilities
The `_shared/tracing.py` module provides reusable components:
```python
from _shared.tracing import trace_function, add_performance_metrics

@trace_function("custom_operation")
def my_function():
    # Function automatically traced
```

### Context Propagation
Trace context automatically flows between functions:
```python
def step_one():
    with tracer.start_as_current_span("step_one"):
        step_two()  # Context automatically propagated

def step_two():
    with tracer.start_as_current_span("step_two"):
        # This span is a child of step_one
```

## Experiment and Learn 🧪

### Experiment 1: Add Custom Steps
Add a new step to the pipeline:

```python
def custom_analysis(text):
    """Add your own analysis step."""
    with tracer.start_as_current_span("custom_analysis") as span:
        span.set_attribute("analysis.type", "custom")
        # Your analysis logic here
        result = f"Custom analysis of {len(text)} characters"
        span.set_attribute("analysis.result", result)
        return result
```

### Experiment 2: Parallel Processing
Modify the pipeline to process multiple documents:

```python
documents = [
    "Document 1 content...",
    "Document 2 content...", 
    "Document 3 content..."
]

for i, doc in enumerate(documents):
    with tracer.start_as_current_span(f"document_{i}") as span:
        span.set_attribute("document.index", i)
        result = analyze_document(doc)
        print(f"Document {i} result: {result}")
```

### Experiment 3: Error Injection
Test error handling by introducing failures:

```python
def unreliable_step(text):
    """Simulate an unreliable operation."""
    import random
    if random.random() < 0.3:  # 30% failure rate
        raise Exception("Simulated processing error")
    return "Success!"
```

## Understanding Shared Utilities 🔧

### Tracing Decorators
Simplify tracing with decorators:
```python
@trace_function("operation_name")
def my_function(param1, param2):
    # Function automatically traced
    # Parameters automatically recorded
    return "result"
```

### Performance Monitoring
Automatic performance attribute collection:
```python
# Memory usage, CPU time, etc. automatically recorded
with enhanced_span("cpu_intensive_task") as span:
    # Heavy computation here
    # Performance metrics automatically added
```

### Error Handling
Standardized error tracing:
```python
try:
    risky_operation()
except Exception as e:
    # Error automatically recorded in span
    span.record_exception(e)
    span.set_status(Status(StatusCode.ERROR, str(e)))
```

## Advanced Trace Analysis 📊

### Span Relationships
Understanding the trace hierarchy:
```
Root Span: document_analysis_pipeline
├─ Child: process_document (step 1)
├─ Child: analyze_content (step 2)
│  ├─ Grandchild: sentiment_analysis
│  └─ Grandchild: topic_extraction
├─ Child: generate_summary (step 3)
└─ Child: compile_results (step 4)
```

### Performance Insights
Key metrics to analyze:
- **Total pipeline time** - End-to-end processing duration
- **Step-by-step timing** - Which steps are slowest
- **Resource usage** - Memory, CPU utilization
- **Error rates** - Which steps fail most often

## Common Patterns 🔄

### The Pipeline Pattern
```python
def pipeline(input_data):
    with tracer.start_as_current_span("pipeline") as span:
        step1_result = step1(input_data)
        step2_result = step2(step1_result)  
        step3_result = step3(step2_result)
        return step3_result
```

### The Service Call Pattern
```python
def call_external_service(data):
    with tracer.start_as_current_span("external_api_call") as span:
        span.set_attribute("service.name", "external_api")
        span.set_attribute("request.size", len(data))
        
        try:
            response = api_client.call(data)
            span.set_attribute("response.status", "success")
            return response
        except Exception as e:
            span.set_attribute("response.status", "error")
            span.record_exception(e)
            raise
```

## Real-World Applications 🌍

This intermediate tracing pattern applies to:

- **Data Pipelines**: ETL processes with multiple stages
- **Microservices**: Service-to-service communication
- **ML Workflows**: Feature engineering, training, inference
- **API Orchestration**: Coordinating multiple API calls
- **Document Processing**: Multi-step document analysis

## Troubleshooting Tips 🔧

### Issue: Spans Not Nested Properly
```python
# Problem: Spans created outside of parent context
def wrong_way():
    parent_span = tracer.start_as_current_span("parent")
    child_span = tracer.start_as_current_span("child")  # Not nested!

# Solution: Use proper context management
def right_way():
    with tracer.start_as_current_span("parent"):
        with tracer.start_as_current_span("child"):  # Properly nested
            pass
```

### Issue: Shared Utilities Not Found
```bash
# Error: ModuleNotFoundError: No module named '_shared'
# Solution: Ensure you're on scenario_01 branch
git branch
git checkout scenario_01
```

## Key Takeaways 💡

From this scenario, you should understand:

1. **Hierarchical Tracing**: How spans relate to each other
2. **Shared Utilities**: Reusable tracing components
3. **Context Flow**: How trace context propagates
4. **Error Handling**: Tracing failures and exceptions
5. **Pipeline Patterns**: Common multi-step workflows

## Next Steps 🎯

You're now ready for more advanced tracing patterns:

👉 **[Continue to Scenario 02: Advanced Tracing Patterns](scenario-02.md)**

👉 **[Return to Scenario Overview](overview.md)**

## Questions for Reflection 🤔

- How would you structure traces for your multi-step processes?
- What shared utilities would be most valuable in your projects?
- How could hierarchical tracing help with debugging complex workflows?
- What performance insights would be most valuable to capture?

---

## Need Help? 🆘

- **[Troubleshooting Guide](../troubleshooting.md)** - Common issues and solutions
- **[Previous Scenario](scenario-00.md)** - Review basic concepts
- **[Setup Instructions](../setup.md)** - If you need to reconfigure

**Ready for advanced patterns?** [Scenario 02](scenario-02.md) covers sophisticated tracing techniques!