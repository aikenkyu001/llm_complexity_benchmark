import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import os

base_model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
adapter_path = "./qwen_finetune_results/final_lora_adapter"
output_merged_dir = "./qwen_merged_model"

print(f"Loading base model: {base_model_id}")
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=torch.float16,
    device_map="cpu", # Merge on CPU to save VRAM
    trust_remote_code=True
)

print(f"Loading adapter from: {adapter_path}")
model = PeftModel.from_pretrained(base_model, adapter_path)

print("Merging adapter with base model...")
merged_model = model.merge_and_unload()

print(f"Saving merged model to: {output_merged_dir}")
merged_model.save_pretrained(output_merged_dir)

print("Saving tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
tokenizer.save_pretrained(output_merged_dir)

print("Merging complete. Now you can use this directory with llama.cpp or other tools.")
