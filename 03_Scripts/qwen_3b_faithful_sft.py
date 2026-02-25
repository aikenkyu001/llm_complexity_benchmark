import os
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
dataset_path = "07_Finetune/qwen_finetune_data_golden.jsonl" 
output_dir = "./07_Finetune/qwen_3b_faithful_results"

# 1. Load Dataset
dataset = load_dataset("json", data_files=dataset_path, split="train")

# 2. BitsAndBytes Config (4-bit for 8GB VRAM compatibility)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
)

# 3. Load Model & Tokenizer
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
model.config.use_cache = False
model = prepare_model_for_kbit_training(model)

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 4. PEFT (LoRA) - High rank to overwrite "arrogant" pre-trained priors
peft_config = LoraConfig(
    r=32,
    lora_alpha=64,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# 5. Formatting Function (The "Machine" Prompt)
def formatting_prompts_func(example):
    output_texts = []
    for i in range(len(example['instruction'])):
        text = f"""<|im_start|>system
You are a mechanical symbolic converter. Do not think. Do not optimize. 
Convert each LISP S-expression directly into the corresponding Python line. 
Follow the structure with 100% faithfulness.<|im_end|>
<|im_start|>user
### LISP Specification:
{example['input'][i]}<|im_end|>
<|im_start|>assistant
{example['output'][i]}<|im_end|>"""
        output_texts.append(text)
    return {"text": output_texts}

dataset = dataset.map(formatting_prompts_func, batched=True, remove_columns=dataset.column_names)

# 6. SFTConfig (Intense Discipline)
sft_config = SFTConfig(
    output_dir=output_dir,
    num_train_epochs=12, # 12 epochs for 3B is heavy enough to enforce discipline
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    optim="paged_adamw_32bit",
    save_steps=50,
    logging_steps=5,
    learning_rate=5e-5,
    fp16=False,
    bf16=False,
    max_grad_norm=0.3,
    warmup_steps=30,
    lr_scheduler_type="cosine",
    report_to="none",
    max_length=1536,
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
print(f"Starting Qwen 2.5-Coder-3B FAITHFUL (Machine) Fine-tuning...")
trainer.train()

# 9. Save
final_save_path = os.path.join(output_dir, "final_lora_adapter")
trainer.model.save_pretrained(final_save_path)
tokenizer.save_pretrained(final_save_path)
print(f"Training complete. Faithful 3B (Machine) Adapter saved to {final_save_path}")
