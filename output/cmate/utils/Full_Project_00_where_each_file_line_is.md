## Where each File line for each ## File: ..\filename: 

## To extract code blocks from this markdown file, use the following Python script:

```python
def extract_code_blocks(file_path, instructions):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for instruction in instructions:
        file_name = instruction['file']
        start_line = instruction['start_line'] - 1
        end_line = instruction['end_line']
        code = ''.join(lines[start_line:end_line])
        print(f"## Extracted Code from {file_name}")
        print(code)
        print("#" * 80)

# Example instructions
instructions = [
    {'file': '../example.py', 'start_line': 1, 'end_line': 10},
]

file_path = 'Full_Project_00.md'
extract_code_blocks(file_path, instructions)
```

## File: ..\..\cmate\utils\config.py
Line = 14, Starts = 16, Ends = 74

## File: ..\..\cmate\utils\error_handler.py
Line = 74, Starts = 76, Ends = 293

## File: ..\..\cmate\utils\logger.py
Line = 293, Starts = 295, Ends = 349

## File: ..\..\cmate\utils\log_analyzer.py
Line = 349, Starts = 351, Ends = 541

## File: ..\..\cmate\utils\prompt_templates.py
Line = 541, Starts = 543, Ends = 724

## File: ..\..\cmate\utils\system_metrics.py
Line = 724, Starts = 726, Ends = 922

## File: ..\..\cmate\utils\token_counter.py
Line = 922, Starts = 924, Ends = 1014

## File: ..\..\cmate\utils\__init__.py
Line = 1014, Starts = 1016, Ends = 1025

