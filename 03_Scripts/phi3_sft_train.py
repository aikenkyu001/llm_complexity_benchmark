import os

# Disable mixed precision scaler to avoid "unscale FP16" error on this environment
os.environ["ACCELERATE_MIXED_PRECISION"] = "no"

import torch
import numpy as np
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    AutoConfig,
)
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig

# --- Configuration ---
model_id = "microsoft/Phi-3-mini-4k-instruct"
dataset_path = "phi3_finetune_data.jsonl"
output_dir = "./phi3_finetune_results"

# 1. Load Dataset
dataset = load_dataset("json", data_files=dataset_path, split="train")

# 2. BitsAndBytes Config (4-bit quantization)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# 3. Load Model & Tokenizer
config = AutoConfig.from_pretrained(model_id, trust_remote_code=True)
if hasattr(config, "rope_scaling") and config.rope_scaling is not None:
    scaling_type = config.rope_scaling.get("type") or config.rope_scaling.get("rope_type")
    if scaling_type in ["default", None]:
        config.rope_scaling = None
    else:
        config.rope_scaling["type"] = scaling_type

config.torch_dtype = torch.float16

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    config=config,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
    dtype=torch.float16,
)
model.config.use_cache = False
model = prepare_model_for_kbit_training(model)

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 4. PEFT (LoRA) Config
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# 5. Formatting Function & Dataset Preparation
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['instruction'])):
        text = f"""<|user|>
{example['instruction'][i]}

{example['input'][i]}<|end|>
<|assistant|>
{example['output'][i]}<|end|>"""
        output_texts.append(text)
    return {"text": output_texts}

dataset = dataset.map(formatting_prompts_func, batched=True, remove_columns=dataset.column_names)

# 6. SFTConfig (Stability-First Edition)
sft_config = SFTConfig(
    output_dir=output_dir,
    num_train_epochs=5,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    optim="adamw_torch",
    save_steps=25,
    logging_steps=1, # More frequent logging to monitor collapse
    learning_rate=2e-5, # Reduced from 2e-4 for stability
    weight_decay=0.01,
    fp16=False,
    bf16=False,
    max_grad_norm=0.1, # Tightened from 0.3 to prevent explosion
    max_steps=-1,
    warmup_steps=20, # Extended from 10
    lr_scheduler_type="cosine", # Smoother than constant
    report_to="none",
    max_length=1024,
    dataset_text_field="text",
)

# 7. SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    args=sft_config,
)

# --- THE FP16 STABILIZATION ---
print("Stabilizing dtypes and cleaning NaNs...")
for param in trainer.model.parameters():
    # Force conversion of any stray bfloat16
    if param.dtype == torch.bfloat16:
        param.data = param.data.to(torch.float16)
    
    # Zero out any NaNs or Infs that might have survived from previous attempts
    if torch.isnan(param.data).any() or torch.isinf(param.data).any():
        print(f"Detected invalid values in parameters. Zeroing out...")
        param.data = torch.nan_to_num(param.data, nan=0.0, posinf=1e4, neginf=-1e4)

print("Final check of dtypes:")
dtypes = set()
for p in trainer.model.parameters():
    dtypes.add(p.dtype)
print(f"Model parameter dtypes: {dtypes}")

# 8. Train
print("Starting Stable Fine-tuning...")
trainer.train()

# 9. Save final model
trainer.model.save_pretrained(os.path.join(output_dir, "final_lora_adapter"))
tokenizer.save_pretrained(os.path.join(output_dir, "final_lora_adapter"))
print(f"Training complete. Stable Adapter saved to {output_dir}/final_lora_adapter")
