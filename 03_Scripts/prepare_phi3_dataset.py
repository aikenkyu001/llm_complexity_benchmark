import os
import json
from pathlib import Path

# Constants
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "04_RawData"
OUTPUT_FILE = BASE_DIR / "phi3_finetune_data.jsonl"

def prepare_dataset():
    """
    Extracts successful task results (NL, LISP, Code) from all models 
    to create a high-quality fine-tuning dataset for phi3:3.8b.
    """
    dataset = []
    seen_tasks = set() # To track unique successful tasks

    if not RAW_DATA_DIR.exists():
        print(f"Error: {RAW_DATA_DIR} does not exist.")
        return

    print(f"Scanning {RAW_DATA_DIR} for successful tasks...")

    # Iterate through all model results
    for model_dir in RAW_DATA_DIR.iterdir():
        if not model_dir.is_dir():
            continue
        
        for json_file in model_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Only take successful results with code
                    if data.get("test_passed") == True and data.get("generated_code"):
                        task_name = data.get("task_name")
                        lisp_spec = data.get("lisp_spec", "")
                        nl_problem = data.get("nl_problem", "")
                        generated_code = data.get("generated_code", "")

                        # Format for Phi-3 Instruct/SFT
                        entry = {
                            "instruction": "Convert the following LISP specification into a complete, efficient Python class 'Solution'. Ensure all constraints and rules are strictly followed.",
                            "input": f"### LISP Specification:\n{lisp_spec}\n\n### Task Context:\n{nl_problem}",
                            "output": f"```python\n{generated_code}\n```"
                        }
                        dataset.append(entry)
                        seen_tasks.add(task_name)
            except Exception as e:
                print(f"Error reading {json_file}: {e}")

    # Write to JSONL
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for entry in dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n--- Dataset Preparation Complete ---")
    print(f"Total Successful Examples: {len(dataset)}")
    print(f"Unique Tasks Covered: {len(seen_tasks)}")
    print(f"Dataset saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    prepare_dataset()
