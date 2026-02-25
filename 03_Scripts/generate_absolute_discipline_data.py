import os
import json
import glob
import re

def generate_absolute_discipline_dataset():
    test_defs_dir = "01_TestDefinitions"
    prompts_dir = "02_Prompts"
    output_file = "07_Finetune/qwen_absolute_discipline_data.jsonl"
    
    raw_data_dirs = [
        "04_RawData/Qwen2.5-Coder-3B-Instruct_final_lora_adapter",
        "04_RawData/qwen2_5-3b-faithful-full"
    ]
    
    BOILERPLATE = "from typing import List, Optional, Dict, Set, Any, Tuple\nimport heapq\nimport collections\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n"

    with open(os.path.join(prompts_dir, "lisp_to_code.prompt"), 'r') as f:
        lisp_to_code_template = f.read()

    prompt_base = lisp_to_code_template.split("{lisp_specification}")[0].strip()

    dataset = []

    # 1. Standard Golden Data
    for task_path in glob.glob(os.path.join(test_defs_dir, "*")):
        if not os.path.isdir(task_path): continue
        task_name = os.path.basename(task_path)
        solution_path = os.path.join(task_path, "solution.py")
        if not os.path.exists(solution_path): continue
        
        with open(solution_path, 'r') as f: golden_code = f.read()
        
        impl_part = golden_code.split("class Solution:")[1] if "class Solution:" in golden_code else golden_code

        lisp_spec = ""
        for rd in raw_data_dirs:
            res_files = glob.glob(os.path.join(rd, task_name, "result_*.json"))
            if res_files:
                with open(res_files[0], 'r') as f:
                    lisp_spec = json.load(f).get("lisp_spec", "")
                break
        
        if lisp_spec:
            output_code = BOILERPLATE + "\nclass Solution:\n" + impl_part.rstrip() + "\n\n# END OF IMPLEMENTATION"
            dataset.append({
                "instruction": prompt_base,
                "input": lisp_spec,
                "output": output_code
            })

    # 2. Negative Correction Data
    for rd in raw_data_dirs:
        if not os.path.exists(rd): continue
        for task_dir in glob.glob(os.path.join(rd, "*")):
            if not os.path.isdir(task_dir): continue
            task_name = os.path.basename(task_dir)
            result_files = glob.glob(os.path.join(task_dir, "result_*.json"))
            if not result_files: continue
            
            with open(result_files[0], 'r') as f:
                try: data = json.load(f)
                except: continue

            if data.get("test_passed") is False:
                solution_path = os.path.join(test_defs_dir, task_name, "solution.py")
                if not os.path.exists(solution_path): continue
                with open(solution_path, 'r') as f: g_code = f.read()
                g_impl = g_code.split("class Solution:")[1] if "class Solution:" in g_code else g_code

                dataset.append({
                    "instruction": "CRITICAL FIX REQUIRED: Fix interface and logic based on error.",
                    "input": "Task: " + task_name + "\nError: " + data.get("test_output", "")[:200],
                    "output": BOILERPLATE + "\nclass Solution:\n" + g_impl.rstrip() + "\n\n# END OF IMPLEMENTATION"
                })

    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"Dataset v3 generated: {len(dataset)} items.")

if __name__ == "__main__":
    generate_absolute_discipline_dataset()
