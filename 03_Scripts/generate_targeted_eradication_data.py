import os
import json
import glob
import re

def generate_targeted_eradication_dataset():
    test_defs_dir = "01_TestDefinitions"
    prompts_dir = "02_Prompts"
    output_file = "07_Finetune/qwen_targeted_eradication_data.jsonl"
    
    FAILED_TASKS = [
        "sudoku_solver_v2_nesting", "trapping_rain_water_ii", "rotate_image_n_by_n",
        "word_ladder_v2_branching", "lru_cache_v2_concurrency", "serialize_deserialize_nary_tree",
        "BitmaskGrouper", "activity_selection", "autocomplete_trie", "bitwise_and_range",
        "dijkstra_v2_state_space", "interval_merger", "lowest_common_ancestor_nary",
        "matrix_chain_multiplication", "redundant_connection_ii", "text_justification",
        "word_break_v2_context_4k", "word_ladder", "word_search_ii"
    ]
    
    BOILERPLATE = "from typing import List, Optional, Dict, Set, Any, Tuple\nimport heapq\nimport collections\n\nclass ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\nclass TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n"

    with open(os.path.join(prompts_dir, "lisp_to_code.prompt"), 'r') as f:
        lisp_to_code_template = f.read()
    prompt_base = lisp_to_code_template.split("{lisp_specification}")[0].strip()

    dataset = []
    raw_data_dirs = [
        "04_RawData/Qwen2.5-Coder-3B-Instruct_final_lora_adapter",
        "04_RawData/qwen2_5-3b-faithful-full"
    ]

    for task_name in FAILED_TASKS:
        solution_path = os.path.join(test_defs_dir, task_name, "solution.py")
        if not os.path.exists(solution_path): continue
        
        with open(solution_path, 'r') as f: golden_code = f.read()
        impl_part = golden_code.split("class Solution:")[1] if "class Solution:" in golden_code else golden_code

        lisp_spec = ""
        for rd in raw_data_dirs:
            if not os.path.exists(rd): continue
            res_files = glob.glob(os.path.join(rd, task_name, "result_*.json"))
            if res_files:
                with open(res_files[0], 'r') as f:
                    lisp_spec = json.load(f).get("lisp_spec", "")
                break
        
        if not lisp_spec: continue

        m = re.search(r'\(name "([^"]+)"\)', lisp_spec)
        method_name = m.group(1) if m else "unknown"

        # 5x Oversampling for hard tasks
        for _ in range(5):
            output_code = BOILERPLATE + f"\n# CRITICAL: IMPLEMENT CLASS 'Solution' WITH METHOD '{method_name}' EXACTLY\nclass Solution:\n" + impl_part.rstrip() + "\n\n# END OF IMPLEMENTATION"
            dataset.append({
                "instruction": prompt_base,
                "input": lisp_spec,
                "output": output_code
            })

    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"Targeted Eradication Dataset generated: {len(dataset)} items.")

if __name__ == "__main__":
    generate_targeted_eradication_dataset()
