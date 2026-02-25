import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

def test_model(task_name):
    base_model_id = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
    adapter_path = "./07_Finetune/qwen_0_5b_finetune_results/final_lora_adapter"
    
    print(f"Loading base model: {base_model_id}")
    tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print(f"Loading adapter: {adapter_path}")
    model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()

    # Load problem definition
    problem_path = f"01_TestDefinitions/{task_name}/problem.nl"
    with open(problem_path, "r") as f:
        problem_nl = f.read()

    # We skip LISP generation for this quick test and provide the LISP directly if we want to test "Implementation Intelligence"
    # or we can test the full pipeline. Let's provide the expected prompt format.
    
    # For a fair test of implementation capability, let's use a known LISP spec for LRU Cache
    lisp_spec = """(define-class LRUCache
  (slots (capacity int) (cache (dict-of int Node)) (head Node) (tail Node))
  (method __init__ ((capacity int))
    (set! (self capacity) capacity)
    (set! (self cache) (make-dict))
    (set! (self head) (make-node 0 0))
    (set! (self tail) (make-node 0 0))
    (set-next! (self head) (self tail))
    (set-prev! (self tail) (self head)))
  (method get ((key int))
    (if (dict-has? (self cache) key)
        (let ((node (dict-ref (self cache) key)))
          (self move-to-head node)
          (return (node-value node)))
        (return -1)))
  (method put ((key int) (value int))
    (if (dict-has? (self cache) key)
        (let ((node (dict-ref (self cache) key)))
          (set-node-value! node value)
          (self move-to-head node))
        (block add-new
          (let ((new-node (make-node key value)))
            (dict-set! (self cache) key new-node)
            (self add-node new-node)
            (if (> (dict-size (self cache)) (self capacity))
                (let ((lru (self tail prev)))
                  (self remove-node lru)
                  (dict-remove! (self cache) (node-key lru)))))))))"""

    prompt = f"""<|im_start|>system
You are an expert Python programmer. Convert the LISP specification into a complete, efficient Python class 'Solution'.<|im_end|>
<|im_start|>user
### LISP Specification:
```lisp
{lisp_spec}
```<|im_end|>
<|im_start|>assistant
"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    print("Generating code...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.01,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id
        )
    
    generated_code = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    print("\n--- GENERATED CODE ---")
    print(generated_code)
    print("----------------------")

if __name__ == "__main__":
    test_model("lru_cache")
