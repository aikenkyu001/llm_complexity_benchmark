import os

# Ensure FP16 stability on GTX 1070
os.environ["ACCELERATE_MIXED_PRECISION"] = "no"

import torch
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
model_id = "Qwen/Qwen2.5-Coder-3B-Instruct"
dataset_path = "07_Finetune/qwen_targeted_eradication_data.jsonl"
output_dir = "./07_Finetune/qwen_targeted_eradication_results"

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
config.torch_dtype = torch.float16

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    config=config,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
model.config.use_cache = False
model = prepare_model_for_kbit_training(model)

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
# Qwen uses <|endoftext|> as pad/eos usually, but we ensure it matches the model
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 4. PEFT (LoRA) Config - Targeting all linear layers for maximum intelligence transfer
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# 5. Formatting Function (ChatML Format for Qwen)
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['instruction'])):
        text = f"""<|im_start|>system
You are an expert software engineer specialized in algorithm design, Python implementation, and rigorous debugging.<|im_end|>
<|im_start|>user
{example['instruction'][i]}

{example['input'][i]}<|im_end|>
<|im_start|>assistant
{example['output'][i]}<|im_end|>"""
        output_texts.append(text)
    return {"text": output_texts}

dataset = dataset.map(formatting_prompts_func, batched=True, remove_columns=dataset.column_names)

# 6. SFTConfig (Optimized for 8GB VRAM and stability)
sft_config = SFTConfig(
    output_dir=output_dir,
    num_train_epochs=5,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    optim="adamw_torch",
    save_steps=25,
    logging_steps=1,
    learning_rate=5e-5, # Slightly more aggressive but still safe for Qwen
    weight_decay=0.01,
    fp16=False, # We use bnb_4bit_compute_dtype=float16
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_steps=20,
    lr_scheduler_type="cosine",
    report_to="none",
    max_length=1536, # Qwen handles context better, but keep within VRAM limits
    dataset_text_field="text",
)

# 7. SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    args=sft_config,
)

# Final check of dtypes
print("Final check of dtypes:")
dtypes = set()
for p in trainer.model.parameters():
    dtypes.add(p.dtype)
print(f"Model parameter dtypes: {dtypes}")

# 8. Train
print(f"Starting Qwen 2.5-Coder-3B Fine-tuning...")
trainer.train()

# 9. Save final model
trainer.model.save_pretrained(os.path.join(output_dir, "final_lora_adapter"))
tokenizer.save_pretrained(os.path.join(output_dir, "final_lora_adapter"))
print(f"Training complete. Qwen Adapter saved to {output_dir}/final_lora_adapter")
