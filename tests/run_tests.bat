@echo off
REM Quick test runner for Windows
REM Usage: run_tests.bat [scenario_numbers...]
REM Example: run_tests.bat 01 03 05

echo Running AI Agent Tracing Scenarios...
echo.

if "%1"=="" (
    echo Running all scenarios...
    python tests\quick_test.py
) else (
    echo Running specified scenarios: %*
    python tests\quick_test.py %*
)

echo.
echo Test run complete.
pause
