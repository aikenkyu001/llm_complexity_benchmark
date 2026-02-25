import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from math import pi

# --- Configuration ---
BASE_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = BASE_DIR / "04_RawData"
REPORTS_DIR = BASE_DIR / "05_Reports"

# Task Category Mapping (Original + Synthetic)
CATEGORIES_MAP = {
    "Algorithmic": [
        "word_ladder", "sudoku_solver", "boggle_solver", "dijkstra_shortest_path",
        "minimum_spanning_tree_prim", "longest_common_subsequence", "matrix_chain_multiplication",
        "word_break", "optimal_bst_cost", "fractional_knapsack", "activity_selection",
        "serialize_deserialize_nary_tree", "procedural_quicksort", "merge_sort_in_place",
        "kth_largest_element"
    ],
    "Data Structure": [
        "lru_cache", "merge_k_sorted_lists", "word_search_ii", "autocomplete_trie",
        "interval_merger", "valid_parentheses_complex", "BitmaskGrouper",
        "binary_tree_maximum_path_sum", "lowest_common_ancestor_nary", "redundant_connection_ii"
    ],
    "Domain-Specific": [
        "regex_matcher", "text_justification", "spiral_matrix_ii", "sparse_matrix_multiplication",
        "trapping_rain_water_ii", "rotate_image_n_by_n", "bitwise_and_range", "permutations_with_duplicates"
    ],
    "Scalability": [
        "sudoku_solver_v2_nesting", "word_ladder_v2_branching", "word_break_v2_context_4k",
        "lru_cache_v2_concurrency", "dijkstra_v2_state_space"
    ]
}

def get_category(task_name):
    if task_name.startswith("synthetic_nesting"):
        return "Nesting Depth"
    if task_name.startswith("synthetic_constraints"):
        return "Constraint Density"
    if task_name.startswith("synthetic_context"):
        return "Contextual Memory"
    
    for cat, tasks in CATEGORIES_MAP.items():
        if task_name in tasks:
            return cat
    return "Other"

def load_data():
    latest_results = {}
    for json_file in RAW_DATA_DIR.rglob("*.json"):
        with open(json_file, 'r') as f:
            try:
                data = json.load(f)
                model = data['model']
                task = data['task_name']
                timestamp = data['timestamp']
                
                # Use (model, task) as key to store only the latest result
                key = (model, task)
                
                if key not in latest_results or timestamp > latest_results[key]['timestamp']:
                    category = get_category(task)
                    comp = data.get('complexity_metrics', {})
                    py_comp = comp.get('python', {})
                    
                    latest_results[key] = {
                        "task_name": task,
                        "model": model,
                        "success": data['test_passed'],
                        "category": category,
                        "total_score": comp.get('total_complexity_score', 0),
                        "cyclomatic_max": py_comp.get('cyclomatic_max', 0),
                        "lloc": py_comp.get('lloc', 0),
                        "timestamp": timestamp
                    }
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
    
    return pd.DataFrame(list(latest_results.values()))

def plot_radar_chart(df, output_path):
    # Group by model and category
    model_cat_success = df.groupby(['model', 'category'])['success'].mean().reset_index()
    models = model_cat_success['model'].unique()
    
    # Use all discovered categories for radar axes
    categories = sorted(df['category'].unique())
    if "Other" in categories: categories.remove("Other")
    
    num_vars = len(categories)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    for model in models:
        model_data = model_cat_success[model_cat_success['model'] == model]
        values = []
        for cat in categories:
            val = model_data[model_data['category'] == cat]['success'].values
            values.append(val[0] if len(val) > 0 else 0)
        values += values[:1]
        
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=model)
        ax.fill(angles, values, alpha=0.05)
        
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    plt.xticks(angles[:-1], categories, size=10)
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75, 1.0], ["25%", "50%", "75%", "100%"], color="grey", size=8)
    plt.ylim(0, 1)
    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title("LLM Capability Radar: Intelligence & Sensitivity Axes")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_complexity_vs_success(df, output_path):
    plt.figure(figsize=(12, 7))
    models = df['model'].unique()
    colors = plt.cm.tab10(np.linspace(0, 1, len(models)))
    
    for i, model in enumerate(models):
        model_df = df[df['model'] == model].sort_values('total_score')
        if model_df.empty: continue
        
        jitter = np.random.uniform(-0.03, 0.03, size=len(model_df))
        plt.scatter(model_df['total_score'], model_df['success'].astype(int) + jitter, 
                    color=colors[i], alpha=0.3, s=20)
        
        if len(model_df) >= 3:
            rolling_success = model_df['success'].rolling(window=min(7, len(model_df)), center=True, min_periods=1).mean()
            plt.plot(model_df['total_score'], rolling_success, 
                     color=colors[i], linewidth=2.5, label=f"{model} Tolerance")

    plt.axhline(y=0.5, color='black', linestyle='--', alpha=0.3, label="Collapse Threshold")
    plt.xlabel("Total Complexity Score (Normalized)")
    plt.ylabel("Success Probability")
    plt.title("LLM Complexity Collapse Map (Including Synthetic Axes)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.ylim(-0.1, 1.1)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    print("Loading data including synthetic axes...")
    df = load_data()
    if df.empty:
        print("No data found.")
        return
    
    REPORTS_DIR.mkdir(exist_ok=True)
    
    print("Generating Updated Radar Chart...")
    plot_radar_chart(df, REPORTS_DIR / "capability_radar.png")
    
    print("Generating Updated Complexity vs Success Plot...")
    plot_complexity_vs_success(df, REPORTS_DIR / "complexity_vs_success.png")
    
    summary = df.groupby(['model', 'category']).agg({
        'success': 'mean',
        'total_score': 'mean'
    }).unstack(level=1)
    summary.to_csv(REPORTS_DIR / "experiment_summary_by_category.csv")
    
    # Model-only summary
    model_summary = df.groupby('model').agg({
        'success': 'mean',
        'total_score': 'mean'
    })
    model_summary.to_csv(REPORTS_DIR / "experiment_summary_model.csv")
    
    print(f"Summaries saved to {REPORTS_DIR}")
    print("Visualization complete.")

if __name__ == "__main__":
    main()
