# Scenario 1: Basic AI Tracing

Use GitHub Copilot Chat in VS Code to set up tracing.

## Running This Scenario

1. **Switch to the scenario branch:**
   ```bash
   git checkout scenario_00
   ```

2. **Inspect the code in main.py**
    - Open the `main.py` file to understand the code.
    - There is currently no tracing logs added to this code.

2. **Verify the AI Toolkit MCP server is running**
   - Open GitHub Copilot Chat in VS Code
   - Select the `Configure Tools` (wrench) icon in the chat area
   - Ensure the `Extension: AI Toolkit for Visual Studio Code` option is selected
   - Press the Escape key to close the menu

4. **Verify the Tracing collector is running**
   - Select the AI Toolkit icon on the left sidebar to open AI Toolkit
   - Select Tracing to open the Tracing Viewer
   - Start the collector

## Your Task

Use GitHub Copilot Chat to add tracing logs to the `main.py` file. When done, run the `main.py` and use the tracing viewer to verify that the traces were collected. When you see a trace in the viewer, you are done with this scenario.

## Next Steps

When you're done, continue to the next scenario.