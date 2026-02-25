import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TEST_DIR = BASE_DIR / "01_TestDefinitions"

def generate_nesting_task(depth: int):
    task_name = f"synthetic_nesting_d{depth}"
    task_path = TEST_DIR / task_name
    task_path.mkdir(exist_ok=True)
    
    # 1. Generate problem.nl
    nl_content = f"# Task: Nested Logic Test (Depth {depth})\n"
    nl_content += "# Interface:\n"
    nl_content += "Class: Solution\n"
    args_str = ", ".join([f"x{i}: int" for i in range(depth)])
    nl_content += f"Method: checkNested(self, {args_str}) -> bool\n\n"
    nl_content += "# Objective:\n"
    nl_content += "This is a test of structural nesting. Return True ONLY if all the following conditions are met:\n"
    for i in range(depth):
        nl_content += f"{i+1}. x{i} is greater than 0\n"
    nl_content += "\nEach condition must be checked inside the previous one (nested if statements)."
    
    (task_path / "problem.nl").write_text(nl_content)
    
    # 2. Generate test_solution.py
    args_true = ", ".join(["1"] * depth)
    args_false = ", ".join(["1"] * (depth-1) + ["0"])
    
    test_content = f"""import pytest
from solution import Solution

def test_nesting_true():
    sol = Solution()
    assert sol.checkNested({args_true}) == True

def test_nesting_false():
    sol = Solution()
    assert sol.checkNested({args_false}) == False
"""
    (task_path / "test_solution.py").write_text(test_content)
    print(f"Generated task: {task_name}")

def generate_constraint_task(num_constraints: int):
    task_name = f"synthetic_constraints_n{num_constraints}"
    task_path = TEST_DIR / task_name
    task_path.mkdir(exist_ok=True)
    
    # 1. Generate problem.nl
    nl_content = f"# Task: Multi-Constraint Check (Density {num_constraints})\n"
    nl_content += "# Interface:\n"
    nl_content += "Class: Solution\n"
    nl_content += "Method: isValid(self, n: int) -> bool\n\n"
    nl_content += "# Objective:\n"
    nl_content += f"Return True if the integer `n` satisfies ALL of the following {num_constraints} independent constraints:\n"
    
    # Generating diverse but simple constraints
    for i in range(num_constraints):
        val = (i + 1) * 2
        if i % 3 == 0:
            nl_content += f"{i+1}. n is greater than {val}\n"
        elif i % 3 == 1:
            nl_content += f"{i+1}. n is not equal to {val + 100}\n"
        else:
            nl_content += f"{i+1}. n is a multiple of {max(1, i // 2)}\n"
    
    (task_path / "problem.nl").write_text(nl_content)
    
    # 2. Generate test_solution.py
    # For simplicity, we just need a value that passes and one that fails.
    # High value like 1000 usually passes 'greater than' and 'not equal to'.
    test_content = f"""import pytest
from solution import Solution

def test_constraints_pass():
    sol = Solution()
    # A large value like 100000 should satisfy simple 'greater than' and 'not equal' rules
    # We use a value that is likely to be a multiple of small primes too
    assert sol.isValid(720720) == True 

def test_constraints_fail():
    sol = Solution()
    assert sol.isValid(-1) == False
"""
    (task_path / "test_solution.py").write_text(test_content)
    print(f"Generated task: {task_name}")

def generate_context_task(num_words: int):
    task_name = f"synthetic_context_v{num_words}"
    task_path = TEST_DIR / task_name
    task_path.mkdir(exist_ok=True)
    
    secret_word = "SIGMA"
    noise = "This is background information that is irrelevant to the core task. " * (num_words // 10)
    
    # 1. Generate problem.nl
    nl_content = f"# Task: Contextual Memory Test (Volume {num_words})\n"
    nl_content += "# Interface:\n"
    nl_content += "Class: Solution\n"
    nl_content += "Method: findSecret(self, text: str) -> str\n\n"
    nl_content += "# Objective:\n"
    nl_content += "Read the provided text and find the secret word mentioned at the very end. Return only that word.\n\n"
    nl_content += "--- START OF TEXT ---\n"
    nl_content += noise
    nl_content += f"\nThe secret word you are looking for is: {secret_word}\n"
    nl_content += "--- END OF TEXT ---\n"
    
    (task_path / "problem.nl").write_text(nl_content)
    
    # 2. Generate test_solution.py
    # We pass a placeholder text in test, but the generated code should be 
    # able to extract it logic-wise or just return the known constant if it understood the spec.
    test_content = f"""import pytest
from solution import Solution

def test_context_secret():
    sol = Solution()
    # The actual text doesn't matter as much as the LLM's understanding of the NL spec
    assert sol.findSecret("Some long text... secret word is: {secret_word}") == "{secret_word}"
"""
    (task_path / "test_solution.py").write_text(test_content)
    print(f"Generated task: {task_name}")

if __name__ == "__main__":
    # Generate linear complexity from depth 1 to 15
    print("Generating Nesting tasks...")
    for d in [1, 2, 3, 4, 5, 7, 10, 15]:
        generate_nesting_task(d)
    
    print("\nGenerating Constraint tasks...")
    for n in [1, 2, 3, 5, 8, 13, 20]:
        generate_constraint_task(n)
        
    print("\nGenerating Context tasks...")
    for v in [100, 500, 1000, 2000, 4000, 8000]:
        generate_context_task(v)
