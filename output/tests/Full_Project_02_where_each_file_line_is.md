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

## File: ..\..\tests\conftest.py
Line = 22, Starts = 24, Ends = 79

## File: ..\..\tests\__init__.py
Line = 79, Starts = 81, Ends = 90

## File: ..\..\tests\fixtures\__init__.py
Line = 90, Starts = 92, Ends = 100

## File: ..\..\tests\fixtures\sample_workspace\__init__.py
Line = 100, Starts = 102, Ends = 111

## File: ..\..\tests\fixtures\sample_workspace\test_project\main.py
Line = 111, Starts = 113, Ends = 152

## File: ..\..\tests\fixtures\sample_workspace\test_project\__init__.py
Line = 152, Starts = 154, Ends = 163

## File: ..\..\tests\integration\test_end_to_end.py
Line = 163, Starts = 165, Ends = 219

## File: ..\..\tests\integration\test_workflows.py
Line = 219, Starts = 221, Ends = 281

## File: ..\..\tests\integration\__init__.py
Line = 281, Starts = 283, Ends = 292

## File: ..\..\tests\unit\test_agent_coordinator copy.py
Line = 292, Starts = 294, Ends = 329

## File: ..\..\tests\unit\test_agent_coordinator.py
Line = 329, Starts = 331, Ends = 339

## File: ..\..\tests\unit\test_file_analyzer.py
Line = 339, Starts = 341, Ends = 377

## File: ..\..\tests\unit\test_state_manager.py
Line = 377, Starts = 379, Ends = 406

## File: ..\..\tests\unit\test_test_manager.py
Line = 406, Starts = 408, Ends = 432

## File: ..\..\tests\unit\test_workflow_manager.py
Line = 432, Starts = 434, Ends = 467

## File: ..\..\tests\unit\__init__.py
Line = 467, Starts = 469, Ends = 478

