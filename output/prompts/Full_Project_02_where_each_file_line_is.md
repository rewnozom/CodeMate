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

## File: ..\..\config\default.yaml
Line = 16, Starts = 18, Ends = 74

## File: ..\..\config\development.yaml
Line = 74, Starts = 76, Ends = 100

## File: ..\..\config\gunicorn.py
Line = 100, Starts = 102, Ends = 150

## File: ..\..\config\local.yaml
Line = 150, Starts = 152, Ends = 168

## File: ..\..\config\production.yaml
Line = 168, Starts = 170, Ends = 200

## File: ..\..\config\__init__.py
Line = 200, Starts = 202, Ends = 211

## File: ..\..\config\prompts\base_prompts.yaml
Line = 211, Starts = 213, Ends = 283

## File: ..\..\config\prompts\error_prompts.yaml
Line = 283, Starts = 285, Ends = 323

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 323, Starts = 325, Ends = 365

## File: ..\..\config\prompts\__init__.py
Line = 365, Starts = 367, Ends = 376

