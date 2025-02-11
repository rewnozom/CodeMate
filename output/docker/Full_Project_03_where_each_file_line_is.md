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

## File: ..\..\docker\Dockerfile
Line = 10, Starts = 12, Ends = 47

## File: ..\..\docker\Dockerfile.dev
Line = 47, Starts = 49, Ends = 83

## File: ..\..\docker\Dockerfile.prod
Line = 83, Starts = 85, Ends = 130

## File: ..\..\docker\__init__.py
Line = 130, Starts = 132, Ends = 141

