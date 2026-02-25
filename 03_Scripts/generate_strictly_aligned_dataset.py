import os
import json
import glob

def generate_strictly_aligned_dataset():
    test_defs_dir = "01_TestDefinitions"
    prompts_dir = "02_Prompts"
    output_file = "07_Finetune/qwen_hyper_faithful_data_v2.jsonl"
    
    raw_data_dirs = [
        "04_RawData/Qwen2.5-Coder-3B-Instruct_final_lora_adapter",
        "04_RawData/qwen2_5-3b-faithful-full",
        "04_RawData.bk/qwen2_5-3b-expert-full"
    ]
    
    with open(os.path.join(prompts_dir, "lisp_to_code.prompt"), 'r') as f:
        lisp_to_code_template = f.read()
    with open(os.path.join(prompts_dir, "nl_to_lisp.prompt"), 'r') as f:
        nl_to_lisp_template = f.read()

    prompt_base = lisp_to_code_template.split("{lisp_specification}")[0].strip()
    prompt_c_base = nl_to_lisp_template.split("{nl_problem}")[0].strip()

    dataset = []
    seen_tasks = set()

    for base_dir in raw_data_dirs:
        if not os.path.exists(base_dir): continue
        for task_dir in glob.glob(os.path.join(base_dir, "*")):
            if not os.path.isdir(task_dir): continue
            task_name = os.path.basename(task_dir)
            
            result_files = glob.glob(os.path.join(task_dir, "result_*.json"))
            if not result_files: continue
            
            with open(result_files[0], 'r') as f:
                try: data = json.load(f)
                except: continue

            solution_path = os.path.join(test_defs_dir, task_name, "solution.py")
            if not os.path.exists(solution_path): continue
            with open(solution_path, 'r') as f:
                golden_code = f.read()

            # Ensure we only add each task once
            if task_name in seen_tasks: continue
            seen_tasks.add(task_name)

            if "class Solution:" in golden_code:
                impl_part = golden_code.split("class Solution:")[1]
            else:
                impl_part = golden_code

            # Type A: LISP -> Code
            dataset.append({
                "instruction": prompt_base,
                "input": data.get("lisp_spec", ""),
                "output": impl_part
            })

            # Type C: NL -> LISP
            dataset.append({
                "instruction": prompt_c_base,
                "input": data.get("nl_problem", ""),
                "output": data.get("lisp_spec", "")
            })

    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"Dataset v2 generated with {len(dataset)} items from {len(seen_tasks)} tasks.")

if __name__ == "__main__":
    generate_strictly_aligned_dataset()
