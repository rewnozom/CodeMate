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
Line = 21, Starts = 23, Ends = 78

## File: ..\..\tests\__init__.py
Line = 78, Starts = 80, Ends = 89

## File: ..\..\tests\fixtures\__init__.py
Line = 89, Starts = 91, Ends = 99

## File: ..\..\tests\fixtures\sample_workspace\__init__.py
Line = 99, Starts = 101, Ends = 110

## File: ..\..\tests\fixtures\sample_workspace\test_project\main.py
Line = 110, Starts = 112, Ends = 151

## File: ..\..\tests\fixtures\sample_workspace\test_project\__init__.py
Line = 151, Starts = 153, Ends = 162

## File: ..\..\tests\integration\test_end_to_end.py
Line = 162, Starts = 164, Ends = 218

## File: ..\..\tests\integration\test_workflows.py
Line = 218, Starts = 220, Ends = 280

## File: ..\..\tests\integration\__init__.py
Line = 280, Starts = 282, Ends = 291

## File: ..\..\tests\unit\test_agent_coordinator.py
Line = 291, Starts = 293, Ends = 301

## File: ..\..\tests\unit\test_file_analyzer.py
Line = 301, Starts = 303, Ends = 339

## File: ..\..\tests\unit\test_state_manager.py
Line = 339, Starts = 341, Ends = 368

## File: ..\..\tests\unit\test_test_manager.py
Line = 368, Starts = 370, Ends = 394

## File: ..\..\tests\unit\test_workflow_manager.py
Line = 394, Starts = 396, Ends = 429

## File: ..\..\tests\unit\__init__.py
Line = 429, Starts = 431, Ends = 440

