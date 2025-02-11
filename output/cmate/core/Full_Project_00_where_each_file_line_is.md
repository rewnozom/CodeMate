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

## File: ..\..\cmate\core\agent_coordinator.py
Line = 14, Starts = 16, Ends = 581

## File: ..\..\cmate\core\context_manager.py
Line = 581, Starts = 583, Ends = 751

## File: ..\..\cmate\core\event_bus.py
Line = 751, Starts = 753, Ends = 871

## File: ..\..\cmate\core\memory_manager.py
Line = 871, Starts = 873, Ends = 1080

## File: ..\..\cmate\core\prompt_manager.py
Line = 1080, Starts = 1082, Ends = 1267

## File: ..\..\cmate\core\state_manager.py
Line = 1267, Starts = 1269, Ends = 1481

## File: ..\..\cmate\core\workflow_manager.py
Line = 1481, Starts = 1483, Ends = 1824

## File: ..\..\cmate\core\__init__.py
Line = 1824, Starts = 1826, Ends = 1835

