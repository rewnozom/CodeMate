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

## File: ..\..\CodeMate\config\prompts\__init__.py
Line = 15, Starts = 17, Ends = 26

## File: ..\..\CodeMate\config\prompts\base_prompts.yaml
Line = 26, Starts = 28, Ends = 248

## File: ..\..\CodeMate\config\prompts\decision_prompts.yaml
Line = 248, Starts = 250, Ends = 422

## File: ..\..\CodeMate\config\prompts\error_prompts.yaml
Line = 422, Starts = 424, Ends = 608

## File: ..\..\CodeMate\config\prompts\implementation_prompts.yaml
Line = 608, Starts = 610, Ends = 858

## File: ..\..\CodeMate\config\prompts\navigation_prompts.yaml
Line = 858, Starts = 860, Ends = 1063

## File: ..\..\CodeMate\config\prompts\state_prompts.yaml
Line = 1063, Starts = 1065, Ends = 1321

## File: ..\..\CodeMate\config\prompts\test_prompts.yaml
Line = 1321, Starts = 1323, Ends = 1558

## File: ..\..\CodeMate\config\prompts\workflow_prompts.yaml
Line = 1558, Starts = 1560, Ends = 1781

