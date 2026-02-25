#!/bin/bash

# --- Configuration ---
MODEL_PATH="Qwen/Qwen2.5-Coder-0.5B-Instruct"
ADAPTER_PATH="./07_Finetune/qwen_0_5b_finetune_results/final_lora_adapter"
OUTPUT_DIR="04_RawData/qwen2_5-0.5b-expert"
REPORT_FILE="05_Reports/0.5B_BENCHMARK_RESULTS.md"

echo "=========================================================="
echo " Starting Full Benchmark for Qwen 2.5-Coder-0.5B-Expert"
echo "=========================================================="

# 1. Run Inference & Testing
echo "[1/2] Generating code and running tests for all tasks..."
# We use a limited number of tasks first to verify it works, then we can run --all
# For this "self-verification" run, I'll pick 3 diverse tasks.
python3 03_Scripts/run_local_expert_experiment.py \
    --model_path "$MODEL_PATH" \
    --adapter_path "$ADAPTER_PATH" \
    --output_dir "$OUTPUT_DIR" \
    --tasks lru_cache dijkstra_shortest_path valid_parentheses_complex

# 2. Collect Results and Generate Summary
echo "[2/2] Generating summary report..."
echo "# Benchmark Results: Qwen 2.5-Coder-0.5B-Expert (Partial Test)" > $REPORT_FILE
echo "Date: $(date)" >> $REPORT_FILE
echo "| Task | Status |" >> $REPORT_FILE
echo "| :--- | :--- |" >> $REPORT_FILE

SUCCESS_COUNT=0
TOTAL_COUNT=0

for task_name in lru_cache dijkstra_shortest_path valid_parentheses_complex; do
    task_result_dir="$OUTPUT_DIR/$task_name"
    if [ -d "$task_result_dir" ]; then
        TOTAL_COUNT=$((TOTAL_COUNT + 1))
        latest_json=$(ls -t "$task_result_dir"/result_*.json 2>/dev/null | head -n 1)
        
        if [ -f "$latest_json" ]; then
            test_passed=$(grep "\"test_passed\":" "$latest_json" | cut -d: -f2 | tr -d ' ,')
            if [ "$test_passed" == "true" ]; then
                echo "| $task_name | ✅ PASSED |" >> $REPORT_FILE
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
            else
                echo "| $task_name | ❌ FAILED |" >> $REPORT_FILE
            fi
        else
            echo "| $task_name | ⚠️ NO RESULT |" >> $REPORT_FILE
        fi
    fi
done

# 3. Final Summary
echo "[3/3] Generating summary..."
if [ $TOTAL_COUNT -gt 0 ]; then
    SUCCESS_RATE=$(echo "scale=2; $SUCCESS_COUNT * 100 / $TOTAL_COUNT" | bc)
else
    SUCCESS_RATE=0
fi

echo "" >> $REPORT_FILE
echo "## Summary" >> $REPORT_FILE
echo "- **Total Tasks:** $TOTAL_COUNT" >> $REPORT_FILE
echo "- **Successes:** $SUCCESS_COUNT" >> $REPORT_FILE
echo "- **Success Rate:** $SUCCESS_RATE%" >> $REPORT_FILE

echo "=========================================================="
echo " Verification Run Complete!"
echo " Results saved to: $REPORT_FILE"
echo "=========================================================="
