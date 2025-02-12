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

## File: ..\..\CodeMate\docker\__init__.py
Line = 10, Starts = 12, Ends = 21

## File: ..\..\CodeMate\docker\Dockerfile
Line = 21, Starts = 23, Ends = 58

## File: ..\..\CodeMate\docker\Dockerfile.dev
Line = 58, Starts = 60, Ends = 94

## File: ..\..\CodeMate\docker\Dockerfile.prod
Line = 94, Starts = 96, Ends = 141

