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
Line = 233, Starts = 235, Ends = 297

## File: ..\..\.pre-commit-config.yaml
Line = 297, Starts = 299, Ends = 340

## File: ..\..\__init__.py
Line = 340, Starts = 342, Ends = 351

## File: ..\..\cli_CodeMate.bat
Line = 351, Starts = 353, Ends = 365

## File: ..\..\docker-compose.dev.yml
Line = 370, Starts = 372, Ends = 463

## File: ..\..\docker-compose.yml
Line = 463, Starts = 465, Ends = 509

## File: ..\..\install_CodeMate.bat
Line = 509, Starts = 511, Ends = 523

## File: ..\..\Makefile
Line = 523, Starts = 525, Ends = 569

## File: ..\..\open_CodeMate.bat
Line = 569, Starts = 571, Ends = 582

## File: ..\..\pyproject.toml
Line = 582, Starts = 584, Ends = 644

## File: ..\..\pytest.ini
Line = 644, Starts = 646, Ends = 672

## File: ..\..\README.md
Line = 677, Starts = 679, Ends = 1044

## File: ..\..\setup.cfg
Line = 1054, Starts = 1056, Ends = 1121

## File: ..\..\tox.ini
Line = 1121, Starts = 1123, Ends = 1152

