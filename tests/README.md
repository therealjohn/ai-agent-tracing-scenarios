# Test Scripts

This directory contains test scripts to run all the AI agent tracing scenarios.

## Scripts

### `run_all_scenarios.py`
Comprehensive test runner that executes all scenarios and provides detailed reporting.

**Features:**
- Runs all scenario main.py files in sequence
- Captures output, errors, and execution times
- Generates summary report
- Saves detailed results to JSON file
- 30-second timeout per scenario

**Usage:**
```bash
python tests/run_all_scenarios.py
```

### `quick_test.py`
Lightweight test runner for quick validation.

**Features:**
- Fast execution with 15-second timeout
- Can run specific scenarios
- Simplified output
- List available scenarios

**Usage:**
```bash
# Run all scenarios
python tests/quick_test.py

# Run specific scenarios
python tests/quick_test.py 01 03 05

# List available scenarios
python tests/quick_test.py --list
```

## Expected Scenarios

The test scripts will automatically discover and run scenarios matching these patterns:
- `00_add_tracing/`
- `01_hallucination_skips_retrieval/`
- `02_broken_tool_chain_weather/`
- `03_slow_multi-step-reasoning/`
- `04_truncated_responses/`
- `05_misrouted_requests/`
- `06_tool_timeout_swallowed/`
- `07_prompt_injection_leak/`

Each scenario directory must contain a `main.py` file to be included in the tests.

## Output

Test results include:
- ✅ Success indicators
- ❌ Failure indicators  
- ⏰ Timeout indicators
- 💥 Exception indicators
- Execution times
- Sample outputs
- Error messages

## Dependencies

The test scripts require the same dependencies as the scenarios being tested. Make sure to install requirements:

```bash
pip install -r requirements.txt
```

## Troubleshooting

**Common issues:**
- `ModuleNotFoundError`: Install missing dependencies with pip
- `Timeout`: Increase timeout values in the scripts if needed
- `Permission errors`: Ensure scripts have execute permissions
