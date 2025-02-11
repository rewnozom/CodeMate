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

## File: ..\..\src\llm\conversation.py
Line = 12, Starts = 14, Ends = 75

## File: ..\..\src\llm\llm_agent.py
Line = 75, Starts = 77, Ends = 135

## File: ..\..\src\llm\llm_manager.py
Line = 135, Starts = 137, Ends = 350

## File: ..\..\src\llm\model_selector.py
Line = 350, Starts = 352, Ends = 387

## File: ..\..\src\llm\prompt_optimizer.py
Line = 387, Starts = 389, Ends = 420

## File: ..\..\src\llm\response_parser.py
Line = 420, Starts = 422, Ends = 455

