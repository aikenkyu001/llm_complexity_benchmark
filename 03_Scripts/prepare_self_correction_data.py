import os
import json
import glob

def prepare_data():
    raw_data_dir = "04_RawData/qwen2_5-3b-faithful-full"
    test_defs_dir = "01_TestDefinitions"
    output_file = "07_Finetune/qwen_self_correction_data.jsonl"
    
    dataset = []
    
    # Iterate through all task directories in raw data
    for task_dir in glob.glob(os.path.join(raw_data_dir, "*")):
        if not os.path.isdir(task_dir):
            continue
            
        task_name = os.path.basename(task_dir)
        result_files = glob.glob(os.path.join(task_dir, "result_*.json"))
        
        if not result_files:
            continue
            
        with open(result_files[0], 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
            
        if data.get("test_passed") is False:
            # Get the correct solution from TestDefinitions
            solution_path = os.path.join(test_defs_dir, task_name, "solution.py")
            if not os.path.exists(solution_path):
                continue
                
            with open(solution_path, 'r') as f:
                correct_code = f.read()
            
            # Extract relevant parts of the error log (limit size)
            error_log = data.get("test_output", "")
            if "FAILURES" in error_log:
                error_log = error_log[error_log.find("FAILURES"):]
            
            # Format for SFT
            instruction = f"The following Python code for task '{task_name}' failed tests. Fix the code based on the provided Pytest error output."
            input_text = f"### Failing Code:\n{data.get('generated_code')}\n\n### Pytest Error Output:\n{error_log}"
            
            dataset.append({
                "instruction": instruction,
                "input": input_text,
                "output": correct_code
            })

    # Save to JSONL
    with open(output_file, 'w') as f:
        for entry in dataset:
            f.write(json.dumps(entry) + '\n')
            
    print(f"Generated {len(dataset)} self-correction pairs at {output_file}")

if __name__ == "__main__":
    prepare_data()
