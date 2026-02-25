import json
import re
import ast
from pathlib import Path
from radon.visitors import ComplexityVisitor
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze
from radon.complexity import cc_rank

def calculate_lisp_complexity(lisp_code: str) -> dict:
    """
    Analyzes LISP specification to estimate structural and semantic complexity.
    """
    if not lisp_code:
        return {}
    
    # Simple proxies for LISP complexity
    # 1. Depth of S-expressions
    depth = 0
    max_depth = 0
    for char in lisp_code:
        if char == '(':
            depth += 1
            max_depth = max(max_depth, depth)
        elif char == ')':
            depth -= 1
    
    # 2. Number of constraints and rules
    constraints_count = len(re.findall(r'\(constraint', lisp_code))
    rules_count = len(re.findall(r'\(rule', lisp_code))
    
    # 3. Token length (Contextual Complexity proxy)
    tokens = len(lisp_code.split())
    
    return {
        "lisp_max_depth": max_depth,
        "lisp_constraints": constraints_count,
        "lisp_rules": rules_count,
        "lisp_token_count": tokens
    }

def get_max_nesting_depth(code: str) -> int:
    """
    Uses AST to find the maximum nesting depth of control structures.
    This is a key component of Cognitive Complexity.
    """
    try:
        tree = ast.parse(code)
        max_depth = 0

        def walk(node, current_depth):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)
            
            # Nodes that increase cognitive nesting
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.FunctionDef, ast.ClassDef)):
                new_depth = current_depth + 1
            else:
                new_depth = current_depth
            
            for child in ast.iter_child_nodes(node):
                walk(child, new_depth)

        walk(tree, 0)
        return max_depth
    except:
        return 0

def analyze_complexity(python_file_path: str, lisp_spec: str = "") -> dict:
    """
    Analyzes complexity from both generated Python code and its LISP specification.
    Includes:
    - Cyclomatic Complexity
    - Halstead Volume
    - Maintainability Index (MI)
    - Max Nesting Depth (Cognitive proxy)
    - WMC (Weighted Methods per Class)
    """
    try:
        p = Path(python_file_path)
        code = p.read_text() if p.is_file() else ""
        
        # --- Python Metrics ---
        python_metrics = {}
        if code:
            visitor = ComplexityVisitor.from_code(code)
            all_blocks = []
            all_blocks.extend(visitor.functions)
            for cls in visitor.classes:
                all_blocks.extend(cls.methods)
            
            total_cc = sum(f.complexity for f in all_blocks)
            avg_cc = total_cc / len(all_blocks) if all_blocks else 0
            max_cc = max((f.complexity for f in all_blocks), default=0)

            # Maintainability Index
            try:
                mi_score = mi_visit(code, multi=True)
            except:
                mi_score = 0

            # Halstead Volume
            halstead = h_visit(code)
            h_volume = 0
            if halstead:
                if hasattr(halstead, "volume"):
                    h_volume = halstead.volume
                elif isinstance(halstead, (list, tuple)) and len(halstead) > 7:
                    h_volume = halstead[7]

            raw = analyze(code)
            
            python_metrics = {
                "cyclomatic_avg": avg_cc,
                "cyclomatic_max": max_cc,
                "wmc": total_cc,
                "maintainability_index": mi_score,
                "max_nesting_depth": get_max_nesting_depth(code),
                "halstead_volume": h_volume,
                "lloc": raw.lloc if raw else 0,
                "loc": raw.loc if raw else 0
            }
        
        # --- LISP Metrics ---
        lisp_metrics = calculate_lisp_complexity(lisp_spec)
        
        # --- Total Normalized Score (0.0 to 1.0) ---
        # Refined calculation weighting structural, contextual, and nesting complexity
        s_cc = min(python_metrics.get("cyclomatic_max", 0) / 20.0, 1.0) * 0.25
        s_nesting = min(python_metrics.get("max_nesting_depth", 0) / 10.0, 1.0) * 0.25
        s_ctx = min(lisp_metrics.get("lisp_token_count", 0) / 1000.0, 1.0) * 0.20
        s_rules = min((lisp_metrics.get("lisp_constraints", 0) + lisp_metrics.get("lisp_rules", 0)) / 15.0, 1.0) * 0.30
        
        total_score = s_cc + s_nesting + s_ctx + s_rules

        return {
            "total_complexity_score": total_score,
            "python": python_metrics,
            "lisp": lisp_metrics
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    dummy_code = """
def factorial(n):
    if n == 0:
        return 1
    else:
        for i in range(n):
            if i % 2 == 0:
                print(i)
        return n * factorial(n-1)
"""
    complexity_data = analyze_complexity("", "") # Test empty
    # For actual test, create temp file
    temp = Path("temp_test.py")
    temp.write_text(dummy_code)
    print(json.dumps(analyze_complexity(str(temp), "(task (name 'test'))"), indent=2))
    temp.unlink()
