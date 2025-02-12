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

file_path = '{generated_file_name}'
extract_code_blocks(file_path, instructions)
```

## File: ..\..\CodeMate\cmate\task_management\__init__.py
Line = 11, Starts = 13, Ends = 22

## File: ..\..\CodeMate\cmate\task_management\checklist_manager.py
Line = 22, Starts = 24, Ends = 301

## File: ..\..\CodeMate\cmate\task_management\process_manager.py
Line = 301, Starts = 303, Ends = 470

## File: ..\..\CodeMate\cmate\task_management\progress_tracker.py
Line = 470, Starts = 472, Ends = 685

## File: ..\..\CodeMate\cmate\task_management\task_prioritizer.py
Line = 685, Starts = 687, Ends = 779

