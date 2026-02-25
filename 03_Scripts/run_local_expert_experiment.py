import os
import json
import subprocess
import torch
from pathlib import Path
from datetime import datetime
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
from complexity_analyzer import analyze_complexity

# --- Configuration ---
BASE_DIR = Path(__file__).parent.parent
TEST_DEFINITIONS_DIR = BASE_DIR / "01_TestDefinitions"
PROMPTS_DIR = BASE_DIR / "02_Prompts"
RAW_DATA_DIR = BASE_DIR / "04_RawData"

class LocalExpertLLM:
    def __init__(self, model_path: str, adapter_path: str = None):
        print(f"Loading Model from {model_path}...")
        
        # 4-bit quantization for memory efficiency
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
        )

        # Force local files to avoid DNS issues
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True, local_files_only=True)
            base_model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
                local_files_only=True
            )
        except Exception as e:
            print(f"Offline load failed, attempting online: {e}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            base_model = AutoModelForCausalLM.from_pretrained(
                model_path,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
        
        if adapter_path:
            print(f"Applying Adapter from {adapter_path}...")
            self.model = PeftModel.from_pretrained(base_model, adapter_path)
        else:
            self.model = base_model
            
        print("Model loaded successfully.")

    def generate(self, prompt: str, temperature: float = 0.0) -> str:
        # ChatML format for Qwen
        full_prompt = f"""<|im_start|>system
You are an expert Python programmer. 
CRITICAL RULE: Convert the LISP specification into a Python class 'Solution'. 
You MUST use the EXACT method name specified in the LISP (name ...) section. 
Do NOT convert it to snake_case if it is camelCase. 
Strictly follow the interface.<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
"""
        
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=2048,
                temperature=max(temperature, 0.01),
                do_sample=True if temperature > 0 else False,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
        return response.strip()

def get_natural_language_problem(task_name: str) -> str:
    problem_file = TEST_DEFINITIONS_DIR / task_name / "problem.nl"
    return problem_file.read_text().strip() if problem_file.exists() else ""

def extract_code_block(text: str, language: str = "python") -> str:
    if f"```{language}" in text:
        return text.split(f"```{language}")[1].split("```")[0].strip()
    elif "```" in text:
        parts = text.split("```")
        if len(parts) > 1:
            return parts[1].strip()
    return text.strip()

def run_single_experiment(task_name: str, expert: LocalExpertLLM, model_name: str, output_root: Path):
    print(f"\n=== [Local Expert] Running task: {task_name} ===")

    nl_problem = get_natural_language_problem(task_name)
    if not nl_problem:
        print(f"Error: No problem.nl found for {task_name}")
        return

    # Step 1: NL -> LISP
    print("Step 1: NL -> LISP (temp=0.2)...")
    nl_to_lisp_prompt = (PROMPTS_DIR / "nl_to_lisp.prompt").read_text().format(natural_language_problem=nl_problem)
    lisp_response = expert.generate(nl_to_lisp_prompt, temperature=0.2)
    lisp_spec = extract_code_block(lisp_response, "lisp")
    if not lisp_spec: lisp_spec = lisp_response

    # Step 2: LISP -> Code
    print("Step 2: LISP -> Code (temp=0.0)...")
    lisp_to_code_prompt = (PROMPTS_DIR / "lisp_to_code.prompt").read_text().format(lisp_specification=lisp_spec)
    code_response = expert.generate(lisp_to_code_prompt, temperature=0.0)
    generated_code = extract_code_block(code_response, "python")

    # Step 3: Save and Test
    solution_path = TEST_DEFINITIONS_DIR / task_name / "solution.py"
    solution_path.write_text(generated_code)
    
    test_path = TEST_DEFINITIONS_DIR / task_name / "test_solution.py"
    test_result = subprocess.run(["pytest", str(test_path)], capture_output=True, text=True)
    test_passed = test_result.returncode == 0
    print(f"Tests passed: {test_passed}")

    # Step 4: Complexity Analysis
    try:
        complexity_data = analyze_complexity(str(solution_path), lisp_spec)
    except Exception as e:
        print(f"Complexity analysis failed: {e}")
        complexity_data = {}

    # Step 5: Save Results
    result_data = {
        "task_name": task_name,
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "nl_problem": nl_problem,
        "lisp_spec": lisp_spec,
        "generated_code": generated_code,
        "test_passed": test_passed,
        "test_output": test_result.stdout,
        "complexity_metrics": complexity_data,
    }

    output_dir = output_root / task_name
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / f"result_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    result_path.write_text(json.dumps(result_data, indent=2))
    (output_dir / "solution.py").write_text(generated_code)
    
    print(f"Results saved to {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="Qwen/Qwen2.5-Coder-3B-Instruct")
    parser.add_argument("--adapter_path", type=str, default=None)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--tasks", type=str, nargs="+", default=["lru_cache"])
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    expert = LocalExpertLLM(args.model_path, args.adapter_path)
    model_name = Path(args.model_path).name + ("_" + Path(args.adapter_path).name if args.adapter_path else "")
    
    output_root = Path(args.output_dir) if args.output_dir else RAW_DATA_DIR / model_name.replace(":", "_")
    output_root.mkdir(parents=True, exist_ok=True)

    tasks_to_run = [d.name for d in TEST_DEFINITIONS_DIR.iterdir() if d.is_dir() and (d / "problem.nl").exists()] if args.all else args.tasks
    tasks_to_run.sort()

    for task in tasks_to_run:
        run_single_experiment(task, expert, model_name, output_root)
