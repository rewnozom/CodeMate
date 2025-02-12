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

## File: ..\..\CodeMate\cmate\tools\tools\config_tool.py
Line = 10, Starts = 12, Ends = 46

## File: ..\..\CodeMate\cmate\tools\tools\diff_tool.py
Line = 46, Starts = 48, Ends = 71

## File: ..\..\CodeMate\cmate\tools\tools\file_tool.py
Line = 71, Starts = 73, Ends = 123

## File: ..\..\CodeMate\cmate\tools\tools\logger_tool.py
Line = 123, Starts = 125, Ends = 158

