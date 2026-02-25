import os
import subprocess
import json
import re
from pathlib import Path

# --- Configuration ---
BASE_DIR = Path(__file__).parent.parent
TEST_DEFINITIONS_DIR = BASE_DIR / "01_TestDefinitions"

def calculate_reward(task_name, generated_code):
    """
    Evaluates the generated code and returns a reward score between 0.0 and 1.0.
    """
    solution_path = TEST_DEFINITIONS_DIR / task_name / "solution.py"
    test_path = TEST_DEFINITIONS_DIR / task_name / "test_solution.py"
    
    # 1. Syntax Check
    try:
        compile(generated_code, "<string>", "exec")
    except SyntaxError:
        return 0.0  # Total failure: Syntax Error

    # 2. Write code to disk for testing
    solution_path.write_text(generated_code)
    
    # 3. Run Pytest
    result = subprocess.run(
        ["pytest", str(test_path), "--json-report", "--json-report-file=report.json"],
        capture_output=True, text=True, cwd=BASE_DIR
    )
    
    # 4. Analyze Results
    score = 0.0
    
    # Check for Interface/Name errors (common in 3B)
    if "AttributeError" in result.stdout or "ImportError" in result.stdout:
        score = 0.1 # Very low but better than syntax error
    elif "NameError" in result.stdout:
        score = 0.2 # Usually missing boilerplates
    
    # Analyze pytest summary
    # Format: "X passed, Y failed, Z errors"
    match = re.search(r"(\d+) passed", result.stdout)
    passed_count = int(match.group(1)) if match else 0
    
    match_failed = re.search(r"(\d+) failed", result.stdout)
    failed_count = int(match_failed.group(1)) if match_failed else 0
    
    total_tests = passed_count + failed_count
    
    if total_tests > 0:
        pass_ratio = passed_count / total_tests
        score = max(score, pass_ratio)
        
    # Bonus for clean completion signal
    if "# END OF IMPLEMENTATION" in generated_code:
        score += 0.05
        
    return min(score, 1.0)

if __name__ == "__main__":
    # Test script with a dummy case
    example_task = "lru_cache"
    example_code = "class Solution:
    def LRUCache(self, capacity: int):
        return None"
    print(f"Reward for {example_task}: {calculate_reward(example_task, example_code)}")
