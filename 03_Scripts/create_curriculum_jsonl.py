import json
from pathlib import Path

# This script generates a valid JSONL file for the fine-tuning curriculum.
# It uses the json library to ensure all special characters are correctly escaped.

def get_golden_data():
    """Returns the core LISP spec and Python code for the solution."""
    
    lisp_spec = """(define-function fullJustify ((words (list-of string)) (maxWidth int))
  (description "Formats text to be fully justified, line by line.")
  (declare-variables
    (result (list-of string))
    (index int 0))

  (loop-while (< index (length words))
    (block get-current-line
      (declare-variables
        (current_line (list-of string))
        (line_length int 0))
      
      (loop-while (and (< index (length words)) (<= (+ line_length (length (get words index)) (length current_line)) maxWidth))
        (add-to-list current_line (get words index))
        (set! line_length (+ line_length (length (get words index))))
        (set! index (+ index 1)))
      
      (declare-variables
        (spaces_to_add (- maxWidth line_length))
        (gaps (- (length current_line) 1)))

      (if (or (== (length current_line) 1) (== index (length words)))
        ; Case: Last line or single-word line (left-justify)
        (let ((left_justified_line (join " " current_line)))
          (add-to-list result (+ left_justified_line (repeat-char " " (- maxWidth (length left_justified_line))))))
        
        ; Case: Full justification
        (block format-full-justify
          (let ((base_spaces (floor (/ spaces_to_add gaps)))
                (extra_spaces (mod spaces_to_add gaps))
                (line_builder string ""))
            
            (loop-for i (from 0 to (- (length current_line) 1))
              (set! line_builder (+ line_builder (get current_line i)))
              (if (< i extra_spaces)
                (set! line_builder (+ line_builder (repeat-char " " (+ base_spaces 1))))
                (set! line_builder (+ line_builder (repeat-char " " base_spaces)))))
            
            (set! line_builder (+ line_builder (last current_line)))
            (add-to-list result line_builder))))))
  (return result))"""

    python_code = """```python
import math

class Solution:
    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        result = []
        index = 0
        while index < len(words):
            current_line_words = []
            current_line_length = 0
            
            while (index < len(words) and 
                   (current_line_length + len(words[index]) + len(current_line_words)) <= maxWidth):
                current_line_words.append(words[index])
                current_line_length += len(words[index])
                index += 1

            spaces_to_add = maxWidth - current_line_length
            gaps = len(current_line_words) - 1

            if gaps == 0 or index == len(words):
                line_str = " ".join(current_line_words)
                padding = " " * (maxWidth - len(line_str))
                result.append(line_str + padding)
                continue

            base_spaces = spaces_to_add // gaps
            extra_spaces = spaces_to_add % gaps

            line_str = []
            for i in range(gaps):
                line_str.append(current_line_words[i])
                num_spaces = base_spaces + (1 if i < extra_spaces else 0)
                line_str.append(" " * num_spaces)
            
            line_str.append(current_line_words[-1])
            result.append("".join(line_str))
            
        return result
```"""
    return lisp_spec, python_code

def get_contexts():
    """Returns a list of different task contexts to form the curriculum."""
    
    context_basic = """# Task: text_justification (Basic Case)
# Interface:
Class: Solution
Method: fullJustify(self, arg1, arg2)

Given an array of strings words and a width maxWidth, format the text such that each line has exactly maxWidth characters and is fully (left and right) justified. You should pack your words in a greedy approach. Extra spaces between words should be distributed as evenly as possible. The last line of text should be left-justified."""

    context_last_line = """# Task: text_justification (Focus on Last Line)
# Interface:
Class: Solution
Method: fullJustify(self, arg1, arg2)

CRITICAL RULE: The final line of text is a special case. It must be left-justified. This means you join the words with a single space and pad the rest of the line with spaces to the right until it reaches `maxWidth`. Do not distribute extra spaces between words for the last line. This rule also applies to lines that naturally contain only a single word."""

    context_spaces = """# Task: text_justification (Focus on Space Distribution)
# Interface:
Class: Solution
Method: fullJustify(self, arg1, arg2)

CRITICAL RULE: For fully justified lines (not the last line), spaces must be distributed as evenly as possible. Calculate the number of gaps between words. The total spaces to add are divided by the number of gaps to get `base_spaces`. The remainder (`extra_spaces`) are distributed one by one from the left. For example, with 7 spaces and 3 gaps, the spaces between words would be [3, 2, 2]."""
    
    return [context_basic, context_last_line, context_spaces]

def main():
    """Main function to generate the JSONL file."""
    
    output_file = Path(__file__).parent.parent / "07_Finetune" / "qwen_finetune_data_curriculum.jsonl"
    lisp_spec, python_code = get_golden_data()
    contexts = get_contexts()
    
    instruction = "Convert the following LISP specification into a complete, efficient Python class 'Solution'. Ensure all constraints and rules are strictly followed."

    with open(output_file, 'w') as f:
        for context in contexts:
            # Combine LISP and context for the 'input' field
            input_text = f"""### LISP Specification:
```lisp
{lisp_spec}
```

### Task Context:
{context}"""
            
            # Create the dictionary for the JSON object
            json_object = {
                "instruction": instruction,
                "input": input_text,
                "output": python_code
            }
            
            # Serialize the dictionary to a JSON string and write it to the file, followed by a newline
            f.write(json.dumps(json_object) + '\n')

    print(f"Successfully created curriculum file at: {output_file}")


if __name__ == "__main__":
    main()
