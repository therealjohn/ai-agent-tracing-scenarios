#!/usr/bin/env python3
"""
Quick test script to run all AI agent tracing scenarios.

Usage:
    python quick_test.py                    # Run all scenarios
    python quick_test.py 01 03 05          # Run specific scenarios
    python quick_test.py --list            # List all available scenarios
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def get_available_scenarios(project_root: Path):
    """Get list of available scenario directories."""
    scenarios = []
    for item in sorted(project_root.iterdir()):
        if item.is_dir() and item.name.startswith('scenario_'):
            main_py = item / "main.py"
            if main_py.exists():
                scenarios.append(item.name)
    return scenarios

def run_scenario(project_root: Path, scenario_name: str):
    """Run a single scenario."""
    scenario_dir = project_root / scenario_name
    main_py = scenario_dir / "main.py"
    
    if not main_py.exists():
        print(f"❌ {scenario_name}: main.py not found")
        return False
    
    print(f"🚀 Running {scenario_name}...")
    
    # Use the virtual environment Python if available, otherwise fall back to sys.executable
    venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    python_executable = str(venv_python) if venv_python.exists() else sys.executable
    
    try:
        result = subprocess.run(
            [python_executable, "main.py"],
            cwd=scenario_dir,
            capture_output=True,
            text=True,
            timeout=15
        )
        
        if result.returncode == 0:
            print(f"✅ {scenario_name}: SUCCESS")
            if result.stdout.strip():
                # Show first 200 chars of output
                output = result.stdout.strip()
                if len(output) > 200:
                    output = output[:200] + "..."
                print(f"   Output: {output}")
            return True
        else:
            print(f"❌ {scenario_name}: FAILED")
            if result.stderr:
                # Show more detailed error information for debugging
                print(f"   Error: {result.stderr.strip()[:500]}")  # Show more characters
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {scenario_name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {scenario_name}: EXCEPTION - {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Quick test runner for AI agent scenarios")
    parser.add_argument("scenarios", nargs="*", help="Specific scenarios to run (e.g., 01 03 05)")
    parser.add_argument("--list", action="store_true", help="List all available scenarios")
    
    args = parser.parse_args()
    
    project_root = Path(__file__).resolve().parents[1]
    available_scenarios = get_available_scenarios(project_root)
    
    if args.list:
        print("Available scenarios:")
        for scenario in available_scenarios:
            print(f"  {scenario}")
        return
    
    # Determine which scenarios to run
    if args.scenarios:
        # Convert short names to full names (01 -> 01_hallucination_skips_retrieval)
        scenarios_to_run = []
        for arg in args.scenarios:
            matching = [s for s in available_scenarios if s.startswith(arg)]
            if matching:
                scenarios_to_run.extend(matching)
            else:
                print(f"⚠️  Scenario '{arg}' not found")
    else:
        scenarios_to_run = available_scenarios
    
    if not scenarios_to_run:
        print("No scenarios to run")
        return
    
    print(f"Running {len(scenarios_to_run)} scenarios...\n")
    
    # Run scenarios
    success_count = 0
    for scenario in scenarios_to_run:
        if run_scenario(project_root, scenario):
            success_count += 1
        print()  # Empty line between scenarios
    
    # Summary
    total = len(scenarios_to_run)
    failed = total - success_count
    
    print(f"{'='*50}")
    print(f"SUMMARY: {success_count}/{total} scenarios passed")
    if failed > 0:
        print(f"❌ {failed} scenarios failed")
        sys.exit(1)
    else:
        print("✅ All scenarios passed!")

if __name__ == "__main__":
    main()
