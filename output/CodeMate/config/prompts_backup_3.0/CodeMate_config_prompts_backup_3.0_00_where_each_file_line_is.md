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

## File: ..\..\CodeMate\config\prompts_backup_3.0\__init__.py
Line = 15, Starts = 17, Ends = 26

## File: ..\..\CodeMate\config\prompts_backup_3.0\base_prompts.yaml
Line = 26, Starts = 28, Ends = 105

## File: ..\..\CodeMate\config\prompts_backup_3.0\decision_prompts.yaml
Line = 105, Starts = 107, Ends = 177

## File: ..\..\CodeMate\config\prompts_backup_3.0\error_prompts.yaml
Line = 177, Starts = 179, Ends = 222

## File: ..\..\CodeMate\config\prompts_backup_3.0\implementation_prompts.yaml
Line = 222, Starts = 224, Ends = 320

## File: ..\..\CodeMate\config\prompts_backup_3.0\navigation_prompts.yaml
Line = 320, Starts = 322, Ends = 384

## File: ..\..\CodeMate\config\prompts_backup_3.0\state_prompts.yaml
Line = 384, Starts = 386, Ends = 510

## File: ..\..\CodeMate\config\prompts_backup_3.0\test_prompts.yaml
Line = 510, Starts = 512, Ends = 582

## File: ..\..\CodeMate\config\prompts_backup_3.0\workflow_prompts.yaml
Line = 582, Starts = 584, Ends = 629

