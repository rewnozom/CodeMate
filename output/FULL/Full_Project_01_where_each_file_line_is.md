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

## File: ..\..\.github\__init__.py
Line = 112, Starts = 114, Ends = 123

## File: ..\..\.github\workflows\main.yml
Line = 123, Starts = 125, Ends = 228

## File: ..\..\.github\workflows\__init__.py
Line = 228, Starts = 230, Ends = 239

## File: ..\..\config\default.yaml
Line = 239, Starts = 241, Ends = 297

## File: ..\..\config\development.yaml
Line = 297, Starts = 299, Ends = 323

## File: ..\..\config\gunicorn.py
Line = 323, Starts = 325, Ends = 373

## File: ..\..\config\local.yaml
Line = 373, Starts = 375, Ends = 391

## File: ..\..\config\production.yaml
Line = 391, Starts = 393, Ends = 423

## File: ..\..\config\__init__.py
Line = 423, Starts = 425, Ends = 434

## File: ..\..\config\prompts\base_prompts.yaml
Line = 434, Starts = 436, Ends = 506

## File: ..\..\config\prompts\error_prompts.yaml
Line = 506, Starts = 508, Ends = 546

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 546, Starts = 548, Ends = 588

## File: ..\..\config\prompts\__init__.py
Line = 588, Starts = 590, Ends = 599

## File: ..\..\docker\Dockerfile
Line = 599, Starts = 601, Ends = 636

## File: ..\..\docker\Dockerfile.dev
Line = 636, Starts = 638, Ends = 672

## File: ..\..\docker\Dockerfile.prod
Line = 672, Starts = 674, Ends = 719

## File: ..\..\docker\__init__.py
Line = 719, Starts = 721, Ends = 730

## File: ..\..\requirements\base.txt
Line = 730, Starts = 732, Ends = 770

## File: ..\..\requirements\dev.txt
Line = 770, Starts = 772, Ends = 790

## File: ..\..\requirements\prod.txt
Line = 790, Starts = 792, Ends = 803

## File: ..\..\requirements\__init__.py
Line = 803, Starts = 805, Ends = 814

## File: ..\..\src\__init__.py
Line = 824, Starts = 826, Ends = 834

## File: ..\..\.dockerignore
Line = 1134, Starts = 1136, Ends = 1173

## File: ..\..\.editorconfig
Line = 1173, Starts = 1175, Ends = 1204

## File: ..\..\.env.example
Line = 1204, Starts = 1206, Ends = 1240

## File: ..\..\.gitignore
Line = 1240, Starts = 1242, Ends = 1327

## File: ..\..\.gitlab-ci.yml
Line = 1327, Starts = 1329, Ends = 1393

## File: ..\..\.pre-commit-config.yaml
Line = 1393, Starts = 1395, Ends = 1436

## File: ..\..\__init__.py
Line = 1436, Starts = 1438, Ends = 1447

## File: ..\..\cli_CodeMate.bat
Line = 1447, Starts = 1449, Ends = 1461

## File: ..\..\deploy.sh
Line = 1461, Starts = 1463, Ends = 1497

## File: ..\..\docker-compose.dev.yml
Line = 1497, Starts = 1499, Ends = 1590

## File: ..\..\docker-compose.yml
Line = 1590, Starts = 1592, Ends = 1636

## File: ..\..\install_CodeMate.bat
Line = 1636, Starts = 1638, Ends = 1650

## File: ..\..\Makefile
Line = 1650, Starts = 1652, Ends = 1700

## File: ..\..\open_CodeMate.bat
Line = 1700, Starts = 1702, Ends = 1713

## File: ..\..\pyproject.toml
Line = 1713, Starts = 1715, Ends = 1744

## File: ..\..\pytest.ini
Line = 1744, Starts = 1746, Ends = 1773

## File: ..\..\README.md
Line = 1773, Starts = 1775, Ends = 2196

## File: ..\..\run_tests.sh
Line = 2196, Starts = 2198, Ends = 2211

## File: ..\..\settings.toml
Line = 2211, Starts = 2213, Ends = 2245

## File: ..\..\setup.cfg
Line = 2245, Starts = 2247, Ends = 2318

## File: ..\..\setup.py
Line = 2318, Starts = 2320, Ends = 2461

## File: ..\..\tox.ini
Line = 2461, Starts = 2463, Ends = 2495

