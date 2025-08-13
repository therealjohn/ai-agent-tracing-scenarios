#!/usr/bin/env python3
"""
Test script to run all AI agent tracing scenarios in sequence.

This script runs each scenario's main.py file and captures their output,
execution time, and any errors. Results are displayed in a summary at the end.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))

class ScenarioRunner:
    def __init__(self):
        self.project_root = project_root
        self.results = []
        
    def get_scenarios(self) -> List[Tuple[str, Path]]:
        """Get all scenario directories with main.py files."""
        scenarios = []
        
        for item in sorted(self.project_root.iterdir()):
            if item.is_dir() and item.name.startswith(('0', '1')):  # Match 00_, 01_, etc.
                main_py = item / "main.py"
                if main_py.exists():
                    scenarios.append((item.name, main_py))
        
        return scenarios
    
    def run_scenario(self, scenario_name: str, main_py_path: Path) -> Dict:
        """Run a single scenario and capture its results."""
        print(f"\n{'='*60}")
        print(f"Running: {scenario_name}")
        print(f"Path: {main_py_path}")
        print(f"{'='*60}")
        
        start_time = time.time()
        result = {
            "scenario": scenario_name,
            "path": str(main_py_path),
            "start_time": start_time,
            "success": False,
            "output": "",
            "error": "",
            "duration": 0.0
        }
        
        try:
            # Run the scenario in its own directory
            process = subprocess.run(
                [sys.executable, "main.py"],
                cwd=main_py_path.parent,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            result["duration"] = time.time() - start_time
            result["output"] = process.stdout
            result["error"] = process.stderr
            result["exit_code"] = process.returncode
            result["success"] = process.returncode == 0
            
            if result["success"]:
                print(f"✅ SUCCESS ({result['duration']:.2f}s)")
                if result["output"]:
                    print("Output:")
                    print(result["output"])
            else:
                print(f"❌ FAILED ({result['duration']:.2f}s)")
                if result["error"]:
                    print("Error:")
                    print(result["error"])
                    
        except subprocess.TimeoutExpired:
            result["duration"] = time.time() - start_time
            result["error"] = f"Timeout after 30 seconds"
            print(f"⏰ TIMEOUT ({result['duration']:.2f}s)")
            
        except Exception as e:
            result["duration"] = time.time() - start_time
            result["error"] = f"Exception: {str(e)}"
            print(f"💥 EXCEPTION ({result['duration']:.2f}s): {e}")
        
        return result
    
    def print_summary(self):
        """Print a summary of all test results."""
        print(f"\n\n{'='*80}")
        print("SUMMARY REPORT")
        print(f"{'='*80}")
        
        total_scenarios = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        failed = total_scenarios - successful
        total_time = sum(r["duration"] for r in self.results)
        
        print(f"Total Scenarios: {total_scenarios}")
        print(f"Successful: {successful} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Total Execution Time: {total_time:.2f}s")
        print(f"Average Time per Scenario: {total_time/total_scenarios:.2f}s")
        
        print(f"\n{'Scenario':<35} {'Status':<10} {'Time':<8} {'Notes'}")
        print(f"{'-'*70}")
        
        for result in self.results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            time_str = f"{result['duration']:.2f}s"
            notes = ""
            
            if not result["success"]:
                if "timeout" in result["error"].lower():
                    notes = "Timeout"
                elif "modulenotfounderror" in result["error"].lower():
                    notes = "Missing deps"
                elif result["error"]:
                    notes = "Error"
            
            print(f"{result['scenario']:<35} {status:<10} {time_str:<8} {notes}")
        
        # Show failed scenarios in detail
        failed_scenarios = [r for r in self.results if not r["success"]]
        if failed_scenarios:
            print(f"\n{'FAILED SCENARIOS DETAILS'}")
            print(f"{'-'*40}")
            for result in failed_scenarios:
                print(f"\n{result['scenario']}:")
                if result["error"]:
                    # Show first few lines of error
                    error_lines = result["error"].strip().split('\n')[:5]
                    for line in error_lines:
                        print(f"  {line}")
                    if len(result["error"].strip().split('\n')) > 5:
                        print("  ...")
    
    def save_results_json(self):
        """Save detailed results to a JSON file."""
        results_file = self.project_root / "tests" / "test_results.json"
        
        # Prepare results for JSON serialization
        json_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "summary": {
                "total_scenarios": len(self.results),
                "successful": sum(1 for r in self.results if r["success"]),
                "failed": sum(1 for r in self.results if not r["success"]),
                "total_time": sum(r["duration"] for r in self.results)
            },
            "scenarios": self.results
        }
        
        with open(results_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"\nDetailed results saved to: {results_file}")
    
    def run_all(self):
        """Run all scenarios and generate reports."""
        print("AI Agent Tracing Scenarios Test Runner")
        print(f"Project Root: {self.project_root}")
        
        scenarios = self.get_scenarios()
        
        if not scenarios:
            print("❌ No scenarios found!")
            return
        
        print(f"\nFound {len(scenarios)} scenarios to run:")
        for name, path in scenarios:
            print(f"  - {name}")
        
        # Run all scenarios
        for scenario_name, main_py_path in scenarios:
            result = self.run_scenario(scenario_name, main_py_path)
            self.results.append(result)
        
        # Generate reports
        self.print_summary()
        self.save_results_json()

def main():
    """Main entry point."""
    runner = ScenarioRunner()
    runner.run_all()
    
    # Exit with error code if any scenarios failed
    failed_count = sum(1 for r in runner.results if not r["success"])
    if failed_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
