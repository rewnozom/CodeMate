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

## File: ..\..\CodeMate\config\__init__.py
Line = 12, Starts = 14, Ends = 23

## File: ..\..\CodeMate\config\default.yaml
Line = 23, Starts = 25, Ends = 81

## File: ..\..\CodeMate\config\development.yaml
Line = 81, Starts = 83, Ends = 107

## File: ..\..\CodeMate\config\gunicorn.py
Line = 107, Starts = 109, Ends = 157

## File: ..\..\CodeMate\config\local.yaml
Line = 157, Starts = 159, Ends = 175

## File: ..\..\CodeMate\config\production.yaml
Line = 175, Starts = 177, Ends = 207

