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

## File: ..\..\src\utils\config.py
Line = 14, Starts = 16, Ends = 54

## File: ..\..\src\utils\error_handler.py
Line = 54, Starts = 56, Ends = 273

## File: ..\..\src\utils\logger.py
Line = 273, Starts = 275, Ends = 329

## File: ..\..\src\utils\log_analyzer.py
Line = 329, Starts = 331, Ends = 521

## File: ..\..\src\utils\prompt_templates.py
Line = 521, Starts = 523, Ends = 704

## File: ..\..\src\utils\system_metrics.py
Line = 704, Starts = 706, Ends = 902

## File: ..\..\src\utils\token_counter.py
Line = 902, Starts = 904, Ends = 994

## File: ..\..\src\utils\__init__.py
Line = 994, Starts = 996, Ends = 1005

