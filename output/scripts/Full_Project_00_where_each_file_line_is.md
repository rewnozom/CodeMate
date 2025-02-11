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

## File: ..\..\scripts\deploy.sh
Line = 10, Starts = 12, Ends = 44

## File: ..\..\scripts\run_tests.sh
Line = 44, Starts = 46, Ends = 59

## File: ..\..\scripts\setup.py
Line = 59, Starts = 61, Ends = 197

## File: ..\..\scripts\__init__.py
Line = 197, Starts = 199, Ends = 208

