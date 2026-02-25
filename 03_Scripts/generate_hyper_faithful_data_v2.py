import os
import json
import glob

def generate_strictly_aligned_dataset():
    raw_data_dir = "04_RawData/qwen2_5-3b-faithful-full"
    test_defs_dir = "01_TestDefinitions"
    prompts_dir = "02_Prompts"
    output_file = "07_Finetune/qwen_hyper_faithful_data_v2.jsonl"
    
    # Load prompt templates
    with open(os.path.join(prompts_dir, "lisp_to_code.prompt"), 'r') as f:
        lisp_to_code_template = f.read()
    with open(os.path.join(prompts_dir, "nl_to_code.prompt" if os.path.exists(os.path.join(prompts_dir, "nl_to_code.prompt")) else "nl_to_lisp.prompt"), 'r') as f:
        nl_to_lisp_template = f.read()

    # Split lisp_to_code_template to identify what the model sees vs what it should generate
    # The prompt ends with: class Solution:
    # Your mandatory implementation here
    prompt_base = lisp_to_code_template.split("{lisp_specification}")[0]
    prompt_suffix = lisp_to_code_template.split("{lisp_specification}")[1]

    dataset = []

    # Collect task data
    task_results = {}
    for task_dir in glob.glob(os.path.join(raw_data_dir, "*")):
        if not os.path.isdir(task_dir): continue
        task_name = os.path.basename(task_dir)
        result_files = glob.glob(os.path.join(task_dir, "result_*.json"))
        if not result_files: continue
        with open(result_files[0], 'r') as f:
            try: task_results[task_name] = json.load(f)
            except: continue

    for task_name, data in task_results.items():
        lisp_spec = data.get("lisp_spec", "")
        nl_problem = data.get("nl_problem", "")
        
        solution_path = os.path.join(test_defs_dir, task_name, "solution.py")
        if not os.path.exists(solution_path): continue
        with open(solution_path, 'r') as f:
            golden_code = f.read()

        # Extract only the implementation part from golden_code to match the prompt suffix
        # Most golden_code starts with imports and class Solution definition.
        # We need to find where "class Solution:" ends.
        if "class Solution:" in golden_code:
            impl_part = golden_code.split("class Solution:")[1].split("
", 1)[1]
        else:
            impl_part = golden_code

        # --- Type A: Strictly Aligned LISP -> Code ---
        instruction_a = prompt_base.strip()
        input_a = lisp_spec
        # The prompt already includes the suffix after the input in the experiment runner
        # But for SFT, we provide input as the spec, and output as the code
        output_a = f"    # Mandatory implementation for {task_name}
{impl_part}"
        
        dataset.append({
            "instruction": instruction_a,
            "input": input_a,
            "output": output_a
        })

        # --- Type B: Self-Correction (Modified to fit strict role) ---
        if data.get("test_passed") is False:
            error_log = data.get("test_output", "")
            if "FAILURES" in error_log:
                error_log = error_log[error_log.find("FAILURES"):]
            
            # We use a special instruction for correction to distinguish from raw generation
            instruction_b = f"The following implementation for task '{task_name}' failed tests. Fix the implementation after the 'class Solution:' line based on the error output.

### Error Output:
{error_log}"
            input_b = f"### Failing Code Implementation:
{impl_part}" # Simplified
            dataset.append({
                "instruction": instruction_b,
                "input": input_b,
                "output": impl_part # The golden one
            })

        # --- Type C: Strictly Aligned NL -> LISP ---
        prompt_c_base = nl_to_lisp_template.split("{nl_problem}")[0]
        dataset.append({
            "instruction": prompt_c_base.strip(),
            "input": nl_problem,
            "output": lisp_spec
        })

    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '
')
            
    print(f"Strictly Aligned Dataset generated: {len(dataset)} items at {output_file}")

if __name__ == "__main__":
    generate_strictly_aligned_dataset()
