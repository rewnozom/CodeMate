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

## File: ..\..\CodeMate\requirements\__init__.py
Line = 10, Starts = 12, Ends = 21

## File: ..\..\CodeMate\requirements\base.txt
Line = 21, Starts = 23, Ends = 61

## File: ..\..\CodeMate\requirements\dev.txt
Line = 61, Starts = 63, Ends = 81

## File: ..\..\CodeMate\requirements\prod.txt
Line = 81, Starts = 83, Ends = 94

