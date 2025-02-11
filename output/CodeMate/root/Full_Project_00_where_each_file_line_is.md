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
Line = 24, Starts = 26, Ends = 63

## File: ..\..\.editorconfig
Line = 63, Starts = 65, Ends = 94

## File: ..\..\.env.example
Line = 94, Starts = 96, Ends = 130

## File: ..\..\.gitignore
Line = 130, Starts = 132, Ends = 217

## File: ..\..\.gitlab-ci.yml
Line = 217, Starts = 219, Ends = 283

## File: ..\..\.pre-commit-config.yaml
Line = 283, Starts = 285, Ends = 326

## File: ..\..\__init__.py
Line = 326, Starts = 328, Ends = 337

## File: ..\..\deploy.sh
Line = 337, Starts = 339, Ends = 373

## File: ..\..\docker-compose.dev.yml
Line = 373, Starts = 375, Ends = 418

## File: ..\..\docker-compose.yml
Line = 418, Starts = 420, Ends = 463

## File: ..\..\Makefile
Line = 463, Starts = 465, Ends = 513

## File: ..\..\pytest.ini
Line = 513, Starts = 515, Ends = 542

## File: ..\..\README.md
Line = 542, Starts = 544, Ends = 965

## File: ..\..\run_tests.sh
Line = 965, Starts = 967, Ends = 980

## File: ..\..\settings.toml
Line = 980, Starts = 982, Ends = 1014

## File: ..\..\setup.cfg
Line = 1014, Starts = 1016, Ends = 1084

## File: ..\..\setup.py
Line = 1084, Starts = 1086, Ends = 1233

## File: ..\..\tox.ini
Line = 1233, Starts = 1235, Ends = 1264

