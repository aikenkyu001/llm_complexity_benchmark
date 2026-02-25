import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

def test_faithful_machine(task_name):
    base_model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
    adapter_path = "./07_Finetune/qwen_3b_faithful_results/final_lora_adapter"
    
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

    # The same LISP specification used for 0.5B and 14B tests
    lisp_spec = """(define-function generateMatrix ((n int))
  (description "Generates an n x n matrix filled with elements from 1 to n^2 in spiral order.")
  (declare-variables
    (matrix (list-of (list-of int)) (make-matrix n n 0))
    (top int 0)
    (bottom int (- n 1))
    (left int 0)
    (right int (- n 1))
    (num int 1))

  (loop-while (<= num (* n n))
    ; Move Right
    (loop-for i (from left to right)
      (set-matrix-ref! matrix top i num)
      (set! num (+ num 1)))
    (set! top (+ top 1))

    ; Move Down
    (loop-for i (from top to bottom)
      (set-matrix-ref! matrix i right num)
      (set! num (+ num 1)))
    (set! right (- right 1))

    ; Move Left
    (if (<= top bottom)
      (block move-left
        (loop-for i (from right downto left)
          (set-matrix-ref! matrix bottom i num)
          (set! num (+ num 1)))
        (set! bottom (- bottom 1))))

    ; Move Up
    (if (<= left right)
      (block move-up
        (loop-for i (from bottom downto top)
          (set-matrix-ref! matrix i left num)
          (set! num (+ num 1)))
        (set! left (+ left 1)))))
  (return matrix))"""

    prompt = f"""<|im_start|>system
You are a mechanical symbolic converter. Do not think. Do not optimize. 
Convert each LISP S-expression directly into the corresponding Python line. 
Follow the structure with 100% faithfulness.<|im_end|>
<|im_start|>user
### LISP Specification:
```lisp
{lisp_spec}
```<|im_end|>
<|im_start|>assistant
"""
    
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            temperature=0.01,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id
        )
    
    generated_code = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    print("\n--- 3B FAITHFUL MACHINE OUTPUT ---")
    print(generated_code)
    print("-----------------------------------")

if __name__ == "__main__":
    test_faithful_machine("spiral_matrix_ii")
