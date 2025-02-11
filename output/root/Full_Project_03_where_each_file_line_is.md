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

## File: ..\..\.dockerignore
Line = 30, Starts = 32, Ends = 69

## File: ..\..\.editorconfig
Line = 69, Starts = 71, Ends = 100

## File: ..\..\.env.example
Line = 105, Starts = 107, Ends = 141

## File: ..\..\.gitignore
Line = 146, Starts = 148, Ends = 233

## File: ..\..\.gitlab-ci.yml
Line = 233, Starts = 235, Ends = 299

## File: ..\..\.pre-commit-config.yaml
Line = 299, Starts = 301, Ends = 342

## File: ..\..\__init__.py
Line = 342, Starts = 344, Ends = 353

## File: ..\..\cli_CodeMate.bat
Line = 353, Starts = 355, Ends = 367

## File: ..\..\docker-compose.dev.yml
Line = 372, Starts = 374, Ends = 465

## File: ..\..\docker-compose.yml
Line = 465, Starts = 467, Ends = 511

## File: ..\..\install_CodeMate.bat
Line = 511, Starts = 513, Ends = 525

## File: ..\..\Makefile
Line = 525, Starts = 527, Ends = 575

## File: ..\..\open_CodeMate.bat
Line = 575, Starts = 577, Ends = 588

## File: ..\..\pyproject.toml
Line = 588, Starts = 590, Ends = 619

## File: ..\..\pytest.ini
Line = 619, Starts = 621, Ends = 648

## File: ..\..\README.md
Line = 653, Starts = 655, Ends = 1076

## File: ..\..\setup.cfg
Line = 1086, Starts = 1088, Ends = 1159

## File: ..\..\tox.ini
Line = 1159, Starts = 1161, Ends = 1193

