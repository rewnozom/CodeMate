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

## File: ..\..\CodeMate\cmate\core\__init__.py
Line = 17, Starts = 19, Ends = 28

## File: ..\..\CodeMate\cmate\core\agent_coordinator.py
Line = 28, Starts = 30, Ends = 650

## File: ..\..\CodeMate\cmate\core\context_manager.py
Line = 650, Starts = 652, Ends = 814

## File: ..\..\CodeMate\cmate\core\dependency_analyzer.py
Line = 814, Starts = 816, Ends = 1127

## File: ..\..\CodeMate\cmate\core\event_bus.py
Line = 1127, Starts = 1129, Ends = 1501

## File: ..\..\CodeMate\cmate\core\memory_manager.py
Line = 1501, Starts = 1503, Ends = 1728

## File: ..\..\CodeMate\cmate\core\navigation_executor.py
Line = 1728, Starts = 1730, Ends = 2063

## File: ..\..\CodeMate\cmate\core\navigation_system.py
Line = 2063, Starts = 2065, Ends = 2410

## File: ..\..\CodeMate\cmate\core\prompt_manager.py
Line = 2410, Starts = 2412, Ends = 2614

## File: ..\..\CodeMate\cmate\core\state_manager.py
Line = 2614, Starts = 2616, Ends = 2959

## File: ..\..\CodeMate\cmate\core\workflow_manager.py
Line = 2959, Starts = 2961, Ends = 3418

