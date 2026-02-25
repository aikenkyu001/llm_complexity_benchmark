import os
import json
import glob

def generate_hyper_faithful_dataset():
    raw_data_dir = "04_RawData/qwen2_5-3b-faithful-full"
    test_defs_dir = "01_TestDefinitions"
    output_file = "07_Finetune/qwen_hyper_faithful_data.jsonl"
    
    dataset = []

    # 1. Collect all task data from RawData (which contains LISP specs)
    task_results = {}
    for task_dir in glob.glob(os.path.join(raw_data_dir, "*")):
        if not os.path.isdir(task_dir): continue
        task_name = os.path.basename(task_dir)
        result_files = glob.glob(os.path.join(task_dir, "result_*.json"))
        if not result_files: continue
        
        with open(result_files[0], 'r') as f:
            try:
                task_results[task_name] = json.load(f)
            except: continue

    for task_name, data in task_results.items():
        lisp_spec = data.get("lisp_spec", "")
        nl_problem = data.get("nl_problem", "")
        
        # Get the Golden Solution
        solution_path = os.path.join(test_defs_dir, task_name, "solution.py")
        if not os.path.exists(solution_path): continue
        with open(solution_path, 'r') as f:
            golden_code = f.read()

        # --- Type A: Structural Chain-of-Thought (Logic Pre-generation) ---
        instruction_a = f"Analyze the following LISP specification and convert it into a complete, efficient Python class 'Solution'. Before writing code, describe the state-transition and core logic."
        thought = f"The LISP specification defines a task '{task_name}'. The key constraints are {lisp_spec.count('constraint')} items. I must ensure state synchronization and handle edge cases as defined in the rules. Logic: The implementation will use the specified data structures and algorithmic paradigm to achieve the goal."
        output_a = f"<thought>\n{thought}\n</thought>\n{golden_code}"
        
        dataset.append({
            "instruction": instruction_a,
            "input": lisp_spec,
            "output": output_a
        })

        # --- Type B: Self-Correction (Only for failed tasks) ---
        if data.get("test_passed") is False:
            error_log = data.get("test_output", "")
            if "FAILURES" in error_log:
                error_log = error_log[error_log.find("FAILURES"):]
            
            instruction_b = f"The following Python code for task '{task_name}' failed tests. Fix the code based on the provided Pytest error output."
            input_b = f"### Failing Code:\n{data.get('generated_code')}\n\n### Pytest Error Output:\n{error_log}"
            dataset.append({
                "instruction": instruction_b,
                "input": input_b,
                "output": golden_code
            })

        # --- Type C: Meta-Design (NL to LISP) ---
        instruction_c = f"Translate the following Natural Language requirements into a formal LISP specification for a competitive programming task."
        dataset.append({
            "instruction": instruction_c,
            "input": nl_problem,
            "output": lisp_spec
        })

    # Save integrated dataset
    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"Hyper-Faithful Dataset generated: {len(dataset)} items at {output_file}")

if __name__ == "__main__":
    generate_hyper_faithful_dataset()
