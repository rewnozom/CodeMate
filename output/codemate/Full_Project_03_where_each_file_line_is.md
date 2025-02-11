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

## File: ..\..\src\__init__.py
Line = 91, Starts = 93, Ends = 101

## File: ..\..\.env.example
Line = 346, Starts = 348, Ends = 382

## File: ..\..\config\default.yaml
Line = 382, Starts = 384, Ends = 440

## File: ..\..\config\development.yaml
Line = 440, Starts = 442, Ends = 466

## File: ..\..\config\gunicorn.py
Line = 466, Starts = 468, Ends = 516

## File: ..\..\config\local.yaml
Line = 516, Starts = 518, Ends = 534

## File: ..\..\config\production.yaml
Line = 534, Starts = 536, Ends = 566

## File: ..\..\config\prompts\base_prompts.yaml
Line = 566, Starts = 568, Ends = 638

## File: ..\..\config\prompts\error_prompts.yaml
Line = 638, Starts = 640, Ends = 678

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 678, Starts = 680, Ends = 720

## File: ..\..\.dockerignore
Line = 720, Starts = 722, Ends = 759

## File: ..\..\.editorconfig
Line = 759, Starts = 761, Ends = 790

## File: ..\..\.gitignore
Line = 790, Starts = 792, Ends = 877

## File: ..\..\.gitlab-ci.yml
Line = 877, Starts = 879, Ends = 943

## File: ..\..\.pre-commit-config.yaml
Line = 943, Starts = 945, Ends = 986

## File: ..\..\__init__.py
Line = 986, Starts = 988, Ends = 997

## File: ..\..\cli_CodeMate.bat
Line = 997, Starts = 999, Ends = 1011

## File: ..\..\deploy.sh
Line = 1011, Starts = 1013, Ends = 1047

## File: ..\..\docker-compose.dev.yml
Line = 1047, Starts = 1049, Ends = 1140

## File: ..\..\docker-compose.yml
Line = 1140, Starts = 1142, Ends = 1186

## File: ..\..\install_CodeMate.bat
Line = 1186, Starts = 1188, Ends = 1200

## File: ..\..\Makefile
Line = 1200, Starts = 1202, Ends = 1250

## File: ..\..\pyproject.toml
Line = 1250, Starts = 1252, Ends = 1281

## File: ..\..\pytest.ini
Line = 1281, Starts = 1283, Ends = 1310

## File: ..\..\README.md
Line = 1310, Starts = 1312, Ends = 1733

## File: ..\..\run_tests.sh
Line = 1733, Starts = 1735, Ends = 1748

## File: ..\..\settings.toml
Line = 1748, Starts = 1750, Ends = 1782

## File: ..\..\setup.cfg
Line = 1782, Starts = 1784, Ends = 1855

## File: ..\..\setup.py
Line = 1855, Starts = 1857, Ends = 1998

## File: ..\..\tox.ini
Line = 1998, Starts = 2000, Ends = 2032

