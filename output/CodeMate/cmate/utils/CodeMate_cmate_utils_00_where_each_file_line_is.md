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

## File: ..\..\CodeMate\cmate\utils\__init__.py
Line = 15, Starts = 17, Ends = 26

## File: ..\..\CodeMate\cmate\utils\config.py
Line = 26, Starts = 28, Ends = 86

## File: ..\..\CodeMate\cmate\utils\error_handler.py
Line = 86, Starts = 88, Ends = 305

## File: ..\..\CodeMate\cmate\utils\html_logger.py
Line = 305, Starts = 307, Ends = 585

## File: ..\..\CodeMate\cmate\utils\log_analyzer.py
Line = 585, Starts = 587, Ends = 778

## File: ..\..\CodeMate\cmate\utils\logger.py
Line = 778, Starts = 780, Ends = 846

## File: ..\..\CodeMate\cmate\utils\prompt_templates.py
Line = 846, Starts = 848, Ends = 1029

## File: ..\..\CodeMate\cmate\utils\system_metrics.py
Line = 1029, Starts = 1031, Ends = 1227

## File: ..\..\CodeMate\cmate\utils\token_counter.py
Line = 1227, Starts = 1229, Ends = 1319

