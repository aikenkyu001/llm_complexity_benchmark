import os
import torch
from peft import PeftModel, LoraConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

def merge_adapters():
    model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
    adapter_4_path = "07_Finetune/qwen_absolute_discipline_results/final_lora_adapter"
    adapter_4_1_path = "07_Finetune/qwen_targeted_eradication_results/final_lora_adapter"
    output_path = "07_Finetune/qwen_merged_hyper_faithful_adapter"

    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="cpu" # Use CPU for merging to save VRAM
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    print("Loading Phase 4 (Absolute Discipline) adapter...")
    model = PeftModel.from_pretrained(base_model, adapter_4_path, adapter_name="phase4")
    
    print("Loading Phase 4.1 (Targeted Eradication) adapter...")
    model.load_adapter(adapter_4_1_path, adapter_name="phase4_1")

    print("Merging adapters with weighted average (Discipline 0.7 : Knowledge 0.3)...")
    # Discipline (Phase 4) is the foundation to prevent forgetting.
    model.add_weighted_adapter(
        adapters=["phase4", "phase4_1"],
        weights=[0.7, 0.3],
        adapter_name="merged",
        combination_type="linear"
    )

    print(f"Saving merged adapter to {output_path}...")
    model.set_adapter("merged")
    model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print("Merge complete!")

if __name__ == "__main__":
    merge_adapters()
