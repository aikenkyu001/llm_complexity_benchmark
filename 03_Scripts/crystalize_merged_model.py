import os
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

def crystalize_model():
    model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
    adapter_4_path = "07_Finetune/qwen_absolute_discipline_results/final_lora_adapter"
    adapter_4_1_path = "07_Finetune/qwen_targeted_eradication_results/final_lora_adapter"
    output_path = "07_Finetune/qwen_merged_final_model"

    print("Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    print("Applying Phase 4 (Absolute Discipline) and Merging...")
    model = PeftModel.from_pretrained(base_model, adapter_4_path, adapter_name="phase4")
    
    print("Applying Phase 4.1 (Targeted Eradication) and Merging...")
    model.load_adapter(adapter_4_1_path, adapter_name="phase4_1")

    print("Weighted Merge (Discipline 0.7 : Knowledge 0.3)...")
    model.add_weighted_adapter(
        adapters=["phase4", "phase4_1"],
        weights=[0.7, 0.3],
        adapter_name="final_merged",
        combination_type="linear"
    )
    model.set_adapter("final_merged")

    print("Crystalizing: Merging weights into base model and unloading adapters...")
    final_model = model.merge_and_unload()

    print(f"Saving fully crystalized model to {output_path}...")
    final_model.save_pretrained(output_path)
    tokenizer.save_pretrained(output_path)
    print("Success! The weights are now unified.")

if __name__ == "__main__":
    crystalize_model()
