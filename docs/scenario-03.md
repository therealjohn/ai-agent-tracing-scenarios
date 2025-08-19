# Scenario 3: Error Handling

## Running This Scenario

1. **Switch to the scenario branch:**
   ```bash
   git checkout scenario_02
   ```

2. **Verify the tracing viewer is running:**
   - Open the AI Toolkit panel (View → Open View → AI Toolkit)
   - Click on "Traces" to open the Tracing Viewer
   - Ensure the viewer is ready to capture traces

3. **Run the scenario:**

   First run the script with the parameter "Miami":

   ```bash
   python main.py "Miami"
   ```

   Next, run the script with the parameter "New York":

   ```bash
   python main.py "New York"
   ```

4. **Analyze the traces:**
   - Return to the Tracing Viewer in the AI Toolkit panel
   - Examine the trace
   - Complete the task below

## Your Task

The trace for Miami correctly shows weather information. The trace for New York does not. Use the traces to try and identify why the "New York" trace is not reporting weather data.

## Next Steps

Continue with the next scenario.