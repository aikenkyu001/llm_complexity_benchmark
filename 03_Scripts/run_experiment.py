import os
import json
import subprocess
import requests
from pathlib import Path
from datetime import datetime

# Assuming the other scripts are in the same directory
from complexity_analyzer import analyze_complexity

import argparse

# --- Configuration ---
# Directories
BASE_DIR = Path(__file__).parent.parent
TEST_DEFINITIONS_DIR = BASE_DIR / "01_TestDefinitions"
PROMPTS_DIR = BASE_DIR / "02_Prompts"
RAW_DATA_DIR = BASE_DIR / "04_RawData"
REPORTS_DIR = BASE_DIR / "05_Reports"

def get_natural_language_problem(task_name: str) -> str:
    """
    Returns the natural language description for a task by reading problem.nl.
    """
    problem_file = TEST_DEFINITIONS_DIR / task_name / "problem.nl"
    if problem_file.exists():
        return problem_file.read_text().strip()
    return ""

def call_llm(prompt: str, model: str, url: str, temperature: float = 0.0) -> str:
    """
    Calls the Ollama API to generate a response for a given prompt and model.
    """
    print(f"[{model}] Calling Ollama API at {url} (temp={temperature})...")
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""

def extract_code_block(text: str, language: str = "python") -> str:
    """
    Extracts code from a markdown-style code block.
    """
    if f"```{language}" in text:
        return text.split(f"```{language}")[1].split("```")[0].strip()
    elif "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()

def run_single_experiment(task_name: str, model: str, url: str):
    """
    Runs the full NL -> LISP -> Code -> Test pipeline for a single task and model.
    """
    print(f"\n=== Running experiment for task: {task_name}, model: {model} ===")

    # 1. Get NL problem
    nl_problem = get_natural_language_problem(task_name)
    if not nl_problem:
        print(f"Error: No natural language problem found for task '{task_name}'")
        return

    # 2. Generate LISP from NL (Refined Insight: Use higher temp for structural mapping)
    print(f"Step 2: NL -> LISP...")
    nl_to_lisp_prompt_template = (PROMPTS_DIR / "nl_to_lisp.prompt").read_text()
    final_nl_prompt = nl_to_lisp_prompt_template.format(natural_language_problem=nl_problem)
    lisp_response = call_llm(final_nl_prompt, model, url, temperature=0.2)
    lisp_spec = extract_code_block(lisp_response, "lisp")
    if not lisp_spec:
        lisp_spec = lisp_response # Fallback if no code blocks

    # 3. Generate Code from LISP (Refined Insight: Use low temp for deterministic implementation)
    print(f"Step 3: LISP -> Code...")
    lisp_to_code_prompt_template = (PROMPTS_DIR / "lisp_to_code.prompt").read_text()
    final_lisp_prompt = lisp_to_code_prompt_template.format(lisp_specification=lisp_spec)
    code_response = call_llm(final_lisp_prompt, model, url, temperature=0.0)
    generated_code = extract_code_block(code_response, "python")

    # 4. Save the generated code
    solution_file_path = TEST_DEFINITIONS_DIR / task_name / "solution.py"
    solution_file_path.write_text(generated_code)
    print(f"Generated code saved to: {solution_file_path}")

    # 5. Run tests
    test_file_path = TEST_DEFINITIONS_DIR / task_name / "test_solution.py"
    print(f"Step 5: Running tests: pytest {test_file_path}")
    test_result = subprocess.run(["pytest", str(test_file_path)], capture_output=True, text=True)

    test_passed = test_result.returncode == 0
    print(f"Tests passed: {test_passed}")


    # 6. Analyze complexity
    print(f"Step 6: Analyzing complexity...")
    complexity_data = analyze_complexity(str(solution_file_path), lisp_spec)

    # 7. Record results
    result_data = {
        "task_name": task_name,
        "model": model,
        "timestamp": datetime.now().isoformat(),
        "nl_problem": nl_problem,
        "lisp_spec": lisp_spec,
        "generated_code": generated_code,
        "test_passed": test_passed,
        "test_output": test_result.stdout,
        "test_errors": test_result.stderr,
        "complexity_metrics": complexity_data,
    }

    # Use a safe filename for the model
    safe_model_name = model.replace(":", "_").replace(".", "_")
    model_output_dir = RAW_DATA_DIR / safe_model_name
    model_output_dir.mkdir(parents=True, exist_ok=True)
    
    result_filename = f"{task_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    result_path = model_output_dir / result_filename
    result_path.write_text(json.dumps(result_data, indent=2))
    print(f"Results saved to: {result_path}")
    print("-" * 50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run LLM Complexity Benchmark Experiments")
    parser.add_argument("--url", type=str, default="http://10.5.42.169:11434/api/generate", help="Ollama API URL")
    parser.add_argument("--models", type=str, nargs="+", default=["llama3.1:latest", "qwen2.5-coder:7b"], help="List of models to test")
    parser.add_argument("--tasks", type=str, nargs="+", default=["sudoku_solver", "word_ladder"], help="List of tasks to run (defaults to verification set)")
    parser.add_argument("--all", action="store_true", help="Run all available tasks")
    
    args = parser.parse_args()

    # Ensure raw data directory exists
    RAW_DATA_DIR.mkdir(exist_ok=True)

    if args.all:
        tasks_to_run = [d.name for d in TEST_DEFINITIONS_DIR.iterdir() if d.is_dir() and (d / "problem.nl").exists()]
        tasks_to_run.sort()
    else:
        tasks_to_run = args.tasks
    
    print(f"Starting experiment run for {len(tasks_to_run)} tasks using models: {args.models}")
    print(f"Using Ollama URL: {args.url}")
    
    for task in tasks_to_run:
        for model in args.models:
            run_single_experiment(task, model, args.url)
            
    print(f"\nExperiment run completed.")
