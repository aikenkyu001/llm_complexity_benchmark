import os

# Ensure stability
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
model_id = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
dataset_path = "07_Finetune/qwen_finetune_data_curriculum.jsonl"
output_dir = "./07_Finetune/qwen_0_5b_finetune_results"

# 1. Load Dataset
dataset = load_dataset("json", data_files=dataset_path, split="train")

# 2. BitsAndBytes Config (4-bit quantization)
# Even for 0.5B, we keep the same recipe for consistency
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
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 4. PEFT (LoRA) Config
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
You are an expert Python programmer. Convert the LISP specification into a complete, efficient Python class 'Solution'.<|im_end|>
<|im_start|>user
{example['instruction'][i]}

{example['input'][i]}<|im_end|>
<|im_start|>assistant
{example['output'][i]}<|im_end|>"""
        output_texts.append(text)
    return {"text": output_texts}

dataset = dataset.map(formatting_prompts_func, batched=True, remove_columns=dataset.column_names)

# 6. SFTConfig
sft_config = SFTConfig(
    output_dir=output_dir,
    num_train_epochs=10, # 0.5B needs more epochs to stabilize the "Design Intelligence"
    per_device_train_batch_size=2, # Batch size can be larger for 0.5B
    gradient_accumulation_steps=8,
    optim="adamw_torch",
    save_steps=50,
    logging_steps=5,
    learning_rate=1e-4, # Higher LR for smaller models
    weight_decay=0.01,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    max_steps=-1,
    warmup_steps=50,
    lr_scheduler_type="cosine",
    report_to="none",
    max_length=2048,
    dataset_text_field="text",
)

# 7. SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    args=sft_config,
)

# 8. Train
print(f"Starting Qwen 2.5-Coder-0.5B Fine-tuning...")
trainer.train()

# 9. Save final model
final_save_path = os.path.join(output_dir, "final_lora_adapter")
trainer.model.save_pretrained(final_save_path)
tokenizer.save_pretrained(final_save_path)
print(f"Training complete. Qwen 0.5B Adapter saved to {final_save_path}")
