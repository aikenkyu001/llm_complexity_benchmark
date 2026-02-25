import json
import os
from pathlib import Path

def aggregate_results(raw_data_dir, output_file):
    raw_data_path = Path(raw_data_dir)
    models = [d for d in raw_data_path.iterdir() if d.is_dir()]
    
    summary = {}
    
    for model_dir in models:
        model_name = model_dir.name
        results = []
        # Support both flat and nested directory structures
        for json_file in model_dir.rglob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    # Handle potential multiple trials or results in the same task
                    results.append({
                        "task": data.get("task_name"),
                        "passed": data.get("test_passed"),
                        "complexity": data.get("complexity_metrics", {}).get("total_complexity_score", 0)
                    })
            except Exception as e:
                print(f"Error reading {json_file}: {e}")
        
        if results:
            pass_count = sum(1 for r in results if r["passed"])
            total_count = len(results)
            avg_complexity = sum(r["complexity"] for r in results) / total_count if total_count > 0 else 0
            
            summary[model_name] = {
                "pass_rate": (pass_count / total_count) * 100 if total_count > 0 else 0,
                "passed": pass_count,
                "total": total_count,
                "avg_complexity": avg_complexity
            }
            
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary saved to {output_file}")

if __name__ == "__main__":
    aggregate_results("/private/test/llm_complexity_benchmark/04_RawData", "/private/test/llm_complexity_benchmark/05_Reports/latest_aggregate_results.json")
