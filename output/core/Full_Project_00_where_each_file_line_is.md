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

## File: ..\..\src\core\agent_coordinator.py
Line = 15, Starts = 17, Ends = 582

## File: ..\..\src\core\context_manager.py
Line = 582, Starts = 584, Ends = 752

## File: ..\..\src\core\core-base.py
Line = 752, Starts = 754, Ends = 1026

## File: ..\..\src\core\event_bus.py
Line = 1026, Starts = 1028, Ends = 1146

## File: ..\..\src\core\memory_manager.py
Line = 1146, Starts = 1148, Ends = 1355

## File: ..\..\src\core\prompt_manager.py
Line = 1355, Starts = 1357, Ends = 1542

## File: ..\..\src\core\state_manager.py
Line = 1542, Starts = 1544, Ends = 1756

## File: ..\..\src\core\workflow_manager.py
Line = 1756, Starts = 1758, Ends = 2099

## File: ..\..\src\core\__init__.py
Line = 2099, Starts = 2101, Ends = 2110

