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

## File: ..\..\src\main.py
Line = 86, Starts = 88, Ends = 201

## File: ..\..\src\__init__.py
Line = 201, Starts = 203, Ends = 212

## File: ..\..\src\config\prompts.py
Line = 212, Starts = 214, Ends = 386

## File: ..\..\src\config\__init__.py
Line = 386, Starts = 388, Ends = 397

## File: ..\..\src\core\agent_coordinator.py
Line = 397, Starts = 399, Ends = 964

## File: ..\..\src\core\context_manager.py
Line = 964, Starts = 966, Ends = 1134

## File: ..\..\src\core\core-base.py
Line = 1134, Starts = 1136, Ends = 1408

## File: ..\..\src\core\event_bus.py
Line = 1408, Starts = 1410, Ends = 1528

## File: ..\..\src\core\memory_manager.py
Line = 1528, Starts = 1530, Ends = 1737

## File: ..\..\src\core\prompt_manager.py
Line = 1737, Starts = 1739, Ends = 1924

## File: ..\..\src\core\state_manager.py
Line = 1924, Starts = 1926, Ends = 2138

## File: ..\..\src\core\workflow_manager.py
Line = 2138, Starts = 2140, Ends = 2481

## File: ..\..\src\core\__init__.py
Line = 2481, Starts = 2483, Ends = 2492

## File: ..\..\src\file_services\file_analyzer.py
Line = 2492, Starts = 2494, Ends = 2768

## File: ..\..\src\file_services\file_watcher.py
Line = 2768, Starts = 2770, Ends = 2958

## File: ..\..\src\file_services\workspace_scanner.py
Line = 2958, Starts = 2960, Ends = 3102

## File: ..\..\src\file_services\__init__.py
Line = 3102, Starts = 3104, Ends = 3113

## File: ..\..\src\interfaces\cli_interface.py
Line = 3113, Starts = 3115, Ends = 3479

## File: ..\..\src\interfaces\request_handler.py
Line = 3479, Starts = 3481, Ends = 3629

## File: ..\..\src\interfaces\response_formatter.py
Line = 3629, Starts = 3631, Ends = 3796

## File: ..\..\src\interfaces\terminal_manager.py
Line = 3796, Starts = 3798, Ends = 4064

## File: ..\..\src\interfaces\__init__.py
Line = 4064, Starts = 4066, Ends = 4075

## File: ..\..\src\llm\conversation.py
Line = 4075, Starts = 4077, Ends = 4138

## File: ..\..\src\llm\llm_agent.py
Line = 4138, Starts = 4140, Ends = 4198

## File: ..\..\src\llm\llm_manager.py
Line = 4198, Starts = 4200, Ends = 4413

## File: ..\..\src\llm\model_selector.py
Line = 4413, Starts = 4415, Ends = 4450

## File: ..\..\src\llm\prompt_optimizer.py
Line = 4450, Starts = 4452, Ends = 4483

## File: ..\..\src\llm\response_parser.py
Line = 4483, Starts = 4485, Ends = 4518

## File: ..\..\src\storage\cache_manager.py
Line = 4518, Starts = 4520, Ends = 4718

## File: ..\..\src\storage\persistence_manager.py
Line = 4718, Starts = 4720, Ends = 4922

## File: ..\..\src\storage\__init__.py
Line = 4922, Starts = 4924, Ends = 4933

## File: ..\..\src\task_management\checklist_manager.py
Line = 4933, Starts = 4935, Ends = 5212

## File: ..\..\src\task_management\process_manager.py
Line = 5212, Starts = 5214, Ends = 5391

## File: ..\..\src\task_management\progress_tracker copy.py
Line = 5391, Starts = 5393, Ends = 5630

## File: ..\..\src\task_management\progress_tracker.py
Line = 5630, Starts = 5632, Ends = 5845

## File: ..\..\src\task_management\task_prioritizer.py
Line = 5845, Starts = 5847, Ends = 5939

## File: ..\..\src\task_management\__init__.py
Line = 5939, Starts = 5941, Ends = 5950

## File: ..\..\src\utils\config.py
Line = 5950, Starts = 5952, Ends = 5990

## File: ..\..\src\utils\error_handler.py
Line = 5990, Starts = 5992, Ends = 6209

## File: ..\..\src\utils\logger.py
Line = 6209, Starts = 6211, Ends = 6265

## File: ..\..\src\utils\log_analyzer.py
Line = 6265, Starts = 6267, Ends = 6457

## File: ..\..\src\utils\prompt_templates.py
Line = 6457, Starts = 6459, Ends = 6640

## File: ..\..\src\utils\system_metrics.py
Line = 6640, Starts = 6642, Ends = 6838

## File: ..\..\src\utils\token_counter.py
Line = 6838, Starts = 6840, Ends = 6930

## File: ..\..\src\utils\__init__.py
Line = 6930, Starts = 6932, Ends = 6941

## File: ..\..\src\validation\backend_validator.py
Line = 6941, Starts = 6943, Ends = 7291

## File: ..\..\src\validation\frontend_validator.py
Line = 7291, Starts = 7293, Ends = 7561

## File: ..\..\src\validation\implementation_validator.py
Line = 7561, Starts = 7563, Ends = 7779

## File: ..\..\src\validation\test_manager.py
Line = 7779, Starts = 7781, Ends = 7998

## File: ..\..\src\validation\validation_rules.py
Line = 7998, Starts = 8000, Ends = 8169

## File: ..\..\src\validation\__init__.py
Line = 8169, Starts = 8171, Ends = 8180

## File: ..\..\.env.example
Line = 8180, Starts = 8182, Ends = 8216

## File: ..\..\config\default.yaml
Line = 8216, Starts = 8218, Ends = 8274

## File: ..\..\config\development.yaml
Line = 8274, Starts = 8276, Ends = 8300

## File: ..\..\config\gunicorn.py
Line = 8300, Starts = 8302, Ends = 8350

## File: ..\..\config\local.yaml
Line = 8350, Starts = 8352, Ends = 8368

## File: ..\..\config\production.yaml
Line = 8368, Starts = 8370, Ends = 8400

## File: ..\..\config\prompts\base_prompts.yaml
Line = 8400, Starts = 8402, Ends = 8472

## File: ..\..\config\prompts\error_prompts.yaml
Line = 8472, Starts = 8474, Ends = 8512

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 8512, Starts = 8514, Ends = 8554

## File: ..\..\.dockerignore
Line = 8554, Starts = 8556, Ends = 8593

## File: ..\..\.editorconfig
Line = 8593, Starts = 8595, Ends = 8624

## File: ..\..\.gitignore
Line = 8624, Starts = 8626, Ends = 8711

## File: ..\..\.gitlab-ci.yml
Line = 8711, Starts = 8713, Ends = 8775

## File: ..\..\.pre-commit-config.yaml
Line = 8775, Starts = 8777, Ends = 8818

## File: ..\..\__init__.py
Line = 8818, Starts = 8820, Ends = 8829

## File: ..\..\cli_CodeMate.bat
Line = 8829, Starts = 8831, Ends = 8843

## File: ..\..\deploy.sh
Line = 8843, Starts = 8845, Ends = 8877

## File: ..\..\docker-compose.dev.yml
Line = 8877, Starts = 8879, Ends = 8970

## File: ..\..\docker-compose.yml
Line = 8970, Starts = 8972, Ends = 9016

## File: ..\..\install_CodeMate.bat
Line = 9016, Starts = 9018, Ends = 9030

## File: ..\..\Makefile
Line = 9030, Starts = 9032, Ends = 9076

## File: ..\..\pyproject.toml
Line = 9076, Starts = 9078, Ends = 9111

## File: ..\..\pytest.ini
Line = 9111, Starts = 9113, Ends = 9139

## File: ..\..\README.md
Line = 9139, Starts = 9141, Ends = 9562

## File: ..\..\run_tests.sh
Line = 9562, Starts = 9564, Ends = 9577

## File: ..\..\settings.toml
Line = 9577, Starts = 9579, Ends = 9611

## File: ..\..\setup.cfg
Line = 9611, Starts = 9613, Ends = 9678

## File: ..\..\setup.py
Line = 9678, Starts = 9680, Ends = 9816

## File: ..\..\tox.ini
Line = 9816, Starts = 9818, Ends = 9847

