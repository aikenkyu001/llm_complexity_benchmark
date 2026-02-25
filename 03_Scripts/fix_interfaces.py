import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEST_DEFS_DIR = BASE_DIR / "01_TestDefinitions"

def extract_interface(test_file):
    content = test_file.read_text()
    # Search for pattern like: solution.method_name(arg1, arg2)
    # or Solution().method_name(arg1)
    match = re.search(r"solution\.([a-zA-Z0-9_]+)\(", content)
    if not match:
        match = re.search(r"Solution\(\)\.([a-zA-Z0-9_]+)\(", content)
    
    if match:
        method_name = match.group(1)
        # Try to find the number of arguments in that specific call
        start_idx = match.start()
        end_idx = content.find(")", start_idx)
        call_line = content[start_idx:end_idx + 1]
        args_match = re.search(r"\((.*)\)", call_line)
        args_str = args_match.group(1) if args_match else ""
        
        # Heuristic for arguments
        if not args_str.strip():
            args = "self"
        else:
            arg_count = len(args_str.split(","))
            args = "self, " + ", ".join([f"arg{i+1}" for i in range(arg_count)])
        
        return method_name, args
    return None, None

def fix_all_interfaces():
    print("Starting automatic interface recovery...")
    for task_dir in sorted(TEST_DEFS_DIR.iterdir()):
        if not task_dir.is_dir():
            continue
        
        problem_file = task_dir / "problem.nl"
        test_file = task_dir / "test_solution.py"
        
        if not problem_file.exists() or not test_file.exists():
            continue
            
        if "# Interface:" in problem_file.read_text():
            print(f"[Skip] {task_dir.name} already has interface.")
            continue
            
        method_name, args = extract_interface(test_file)
        if method_name:
            print(f"[Fix] {task_dir.name} -> {method_name}({args})")
            interface_block = f"# Task: {task_dir.name}\n# Interface:\nClass: Solution\nMethod: {method_name}({args})\n\n"
            old_content = problem_file.read_text()
            problem_file.write_text(interface_block + old_content)
        else:
            print(f"[Warn] Could not extract interface for {task_dir.name}")

if __name__ == "__main__":
    fix_all_interfaces()
