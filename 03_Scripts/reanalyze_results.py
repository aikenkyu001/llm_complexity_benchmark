import json
import os
from pathlib import Path
from complexity_analyzer import analyze_complexity

BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "04_RawData"
TEST_DEFINITIONS_DIR = BASE_DIR / "01_TestDefinitions"

def reanalyze():
    print(f"Re-analyzing results in {RAW_DATA_DIR}...")
    json_files = list(RAW_DATA_DIR.rglob("*.json"))
    
    for json_file in json_files:
        print(f"Processing {json_file.name}...")
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # We need the generated code to re-analyze
        # It's usually in the JSON itself as 'generated_code'
        code = data.get('generated_code', "")
        if not code:
            print(f"  Warning: No code found in {json_file.name}")
            continue
            
        # Create a temp file to analyze
        temp_file = BASE_DIR / "temp_analysis.py"
        temp_file.write_text(code)
        
        new_metrics = analyze_complexity(str(temp_file), data.get('lisp_spec', ""))
        temp_file.unlink()
        
        if "error" not in new_metrics:
            data['complexity_metrics'] = new_metrics
            with open(json_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"  Updated complexity: {new_metrics.get('cyclomatic_complexity')}")
        else:
            print(f"  Error analyzing {json_file.name}: {new_metrics['error']}")

if __name__ == "__main__":
    reanalyze()
