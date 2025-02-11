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

## File: ..\..\src\config.py
Line = 814, Starts = 816, Ends = 859

## File: ..\..\src\main.py
Line = 859, Starts = 861, Ends = 974

## File: ..\..\src\__init__.py
Line = 974, Starts = 976, Ends = 985

## File: ..\..\src\config\prompts.py
Line = 985, Starts = 987, Ends = 1159

## File: ..\..\src\config\__init__.py
Line = 1159, Starts = 1161, Ends = 1170

## File: ..\..\src\core\agent_coordinator copy.py
Line = 1170, Starts = 1172, Ends = 1329

## File: ..\..\src\core\agent_coordinator.py
Line = 1329, Starts = 1331, Ends = 1896

## File: ..\..\src\core\context_manager.py
Line = 1896, Starts = 1898, Ends = 2066

## File: ..\..\src\core\core-base.py
Line = 2066, Starts = 2068, Ends = 2340

## File: ..\..\src\core\event_bus.py
Line = 2340, Starts = 2342, Ends = 2460

## File: ..\..\src\core\memory_manager.py
Line = 2460, Starts = 2462, Ends = 2669

## File: ..\..\src\core\prompt_manager.py
Line = 2669, Starts = 2671, Ends = 2856

## File: ..\..\src\core\state_manager.py
Line = 2856, Starts = 2858, Ends = 3070

## File: ..\..\src\core\workflow_manager.py
Line = 3070, Starts = 3072, Ends = 3413

## File: ..\..\src\core\__init__.py
Line = 3413, Starts = 3415, Ends = 3424

## File: ..\..\src\file_services\file_analyzer.py
Line = 3444, Starts = 3446, Ends = 3720

## File: ..\..\src\file_services\file_watcher.py
Line = 3720, Starts = 3722, Ends = 3910

## File: ..\..\src\file_services\workspace_scanner.py
Line = 3910, Starts = 3912, Ends = 4054

## File: ..\..\src\file_services\__init__.py
Line = 4054, Starts = 4056, Ends = 4065

## File: ..\..\src\interfaces\cli_interface.py
Line = 4065, Starts = 4067, Ends = 4431

## File: ..\..\src\interfaces\request_handler.py
Line = 4431, Starts = 4433, Ends = 4581

## File: ..\..\src\interfaces\response_formatter.py
Line = 4581, Starts = 4583, Ends = 4748

## File: ..\..\src\interfaces\terminal_manager.py
Line = 4748, Starts = 4750, Ends = 5016

## File: ..\..\src\interfaces\__init__.py
Line = 5016, Starts = 5018, Ends = 5027

## File: ..\..\src\llm\conversation.py
Line = 5037, Starts = 5039, Ends = 5100

## File: ..\..\src\llm\llm_agent.py
Line = 5100, Starts = 5102, Ends = 5160

## File: ..\..\src\llm\llm_manager.py
Line = 5160, Starts = 5162, Ends = 5375

## File: ..\..\src\llm\model_selector.py
Line = 5375, Starts = 5377, Ends = 5412

## File: ..\..\src\llm\prompt_optimizer.py
Line = 5412, Starts = 5414, Ends = 5445

## File: ..\..\src\llm\response_parser.py
Line = 5445, Starts = 5447, Ends = 5480

## File: ..\..\src\storage\cache_manager.py
Line = 5480, Starts = 5482, Ends = 5680

## File: ..\..\src\storage\persistence_manager.py
Line = 5680, Starts = 5682, Ends = 5884

## File: ..\..\src\storage\__init__.py
Line = 5884, Starts = 5886, Ends = 5895

## File: ..\..\src\task_management\checklist_manager.py
Line = 5895, Starts = 5897, Ends = 6174

## File: ..\..\src\task_management\process_manager.py
Line = 6174, Starts = 6176, Ends = 6353

## File: ..\..\src\task_management\progress_tracker copy.py
Line = 6353, Starts = 6355, Ends = 6592

## File: ..\..\src\task_management\progress_tracker.py
Line = 6592, Starts = 6594, Ends = 6807

## File: ..\..\src\task_management\task_prioritizer.py
Line = 6807, Starts = 6809, Ends = 6901

## File: ..\..\src\task_management\__init__.py
Line = 6901, Starts = 6903, Ends = 6912

## File: ..\..\src\utils\config.py
Line = 6912, Starts = 6914, Ends = 6952

## File: ..\..\src\utils\error_handler.py
Line = 6952, Starts = 6954, Ends = 7171

## File: ..\..\src\utils\logger.py
Line = 7171, Starts = 7173, Ends = 7227

## File: ..\..\src\utils\log_analyzer.py
Line = 7227, Starts = 7229, Ends = 7419

## File: ..\..\src\utils\prompt_templates.py
Line = 7419, Starts = 7421, Ends = 7602

## File: ..\..\src\utils\system_metrics.py
Line = 7602, Starts = 7604, Ends = 7800

## File: ..\..\src\utils\token_counter.py
Line = 7800, Starts = 7802, Ends = 7892

## File: ..\..\src\utils\__init__.py
Line = 7892, Starts = 7894, Ends = 7903

## File: ..\..\src\validation\backend_validator.py
Line = 7918, Starts = 7920, Ends = 8268

## File: ..\..\src\validation\frontend_validator.py
Line = 8268, Starts = 8270, Ends = 8538

## File: ..\..\src\validation\implementation_validator.py
Line = 8538, Starts = 8540, Ends = 8756

## File: ..\..\src\validation\test_manager.py
Line = 8756, Starts = 8758, Ends = 8975

## File: ..\..\src\validation\validation_rules.py
Line = 8975, Starts = 8977, Ends = 9146

## File: ..\..\src\validation\__init__.py
Line = 9146, Starts = 9148, Ends = 9157

## File: ..\..\.dockerignore
Line = 9162, Starts = 9164, Ends = 9201

## File: ..\..\.editorconfig
Line = 9201, Starts = 9203, Ends = 9232

## File: ..\..\.env.example
Line = 9232, Starts = 9234, Ends = 9268

## File: ..\..\.gitignore
Line = 9268, Starts = 9270, Ends = 9355

## File: ..\..\.gitlab-ci.yml
Line = 9355, Starts = 9357, Ends = 9419

## File: ..\..\.pre-commit-config.yaml
Line = 9419, Starts = 9421, Ends = 9462

## File: ..\..\__init__.py
Line = 9462, Starts = 9464, Ends = 9473

## File: ..\..\cli_CodeMate.bat
Line = 9473, Starts = 9475, Ends = 9487

## File: ..\..\deploy.sh
Line = 9487, Starts = 9489, Ends = 9521

## File: ..\..\docker-compose.dev.yml
Line = 9521, Starts = 9523, Ends = 9614

## File: ..\..\docker-compose.yml
Line = 9614, Starts = 9616, Ends = 9660

## File: ..\..\install_CodeMate.bat
Line = 9660, Starts = 9662, Ends = 9674

## File: ..\..\Makefile
Line = 9674, Starts = 9676, Ends = 9720

## File: ..\..\open_CodeMate.bat
Line = 9720, Starts = 9722, Ends = 9733

## File: ..\..\pyproject.toml
Line = 9733, Starts = 9735, Ends = 9768

## File: ..\..\pytest.ini
Line = 9768, Starts = 9770, Ends = 9796

## File: ..\..\README.md
Line = 9796, Starts = 9798, Ends = 10219

## File: ..\..\run_tests.sh
Line = 10219, Starts = 10221, Ends = 10234

## File: ..\..\settings.toml
Line = 10234, Starts = 10236, Ends = 10268

## File: ..\..\setup.cfg
Line = 10268, Starts = 10270, Ends = 10335

## File: ..\..\setup.py
Line = 10335, Starts = 10337, Ends = 10473

## File: ..\..\tox.ini
Line = 10473, Starts = 10475, Ends = 10504

