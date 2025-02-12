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

## File: ..\..\CodeMate\cmate\file_services\__init__.py
Line = 11, Starts = 13, Ends = 22

## File: ..\..\CodeMate\cmate\file_services\file_analyzer.py
Line = 22, Starts = 24, Ends = 298

## File: ..\..\CodeMate\cmate\file_services\file_watcher.py
Line = 298, Starts = 300, Ends = 489

## File: ..\..\CodeMate\cmate\file_services\workspace_analyzer.py
Line = 489, Starts = 491, Ends = 578

## File: ..\..\CodeMate\cmate\file_services\workspace_scanner.py
Line = 578, Starts = 580, Ends = 723

