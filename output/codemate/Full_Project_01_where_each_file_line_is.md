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
Line = 66, Starts = 68, Ends = 181

## File: ..\..\src\__init__.py
Line = 181, Starts = 183, Ends = 192

## File: ..\..\src\config\prompts.py
Line = 192, Starts = 194, Ends = 366

## File: ..\..\src\config\__init__.py
Line = 366, Starts = 368, Ends = 377

## File: ..\..\src\core\agent_coordinator.py
Line = 377, Starts = 379, Ends = 944

## File: ..\..\src\core\context_manager.py
Line = 944, Starts = 946, Ends = 1114

## File: ..\..\src\core\core-base.py
Line = 1114, Starts = 1116, Ends = 1388

## File: ..\..\src\core\event_bus.py
Line = 1388, Starts = 1390, Ends = 1508

## File: ..\..\src\core\memory_manager.py
Line = 1508, Starts = 1510, Ends = 1717

## File: ..\..\src\core\prompt_manager.py
Line = 1717, Starts = 1719, Ends = 1904

## File: ..\..\src\core\state_manager.py
Line = 1904, Starts = 1906, Ends = 2118

## File: ..\..\src\core\workflow_manager.py
Line = 2118, Starts = 2120, Ends = 2461

## File: ..\..\src\core\__init__.py
Line = 2461, Starts = 2463, Ends = 2472

## File: ..\..\src\file_services\file_analyzer.py
Line = 2472, Starts = 2474, Ends = 2748

## File: ..\..\src\file_services\file_watcher.py
Line = 2748, Starts = 2750, Ends = 2938

## File: ..\..\src\file_services\workspace_scanner.py
Line = 2938, Starts = 2940, Ends = 3082

## File: ..\..\src\file_services\__init__.py
Line = 3082, Starts = 3084, Ends = 3093

## File: ..\..\src\interfaces\cli_interface.py
Line = 3093, Starts = 3095, Ends = 3459

## File: ..\..\src\interfaces\request_handler.py
Line = 3459, Starts = 3461, Ends = 3609

## File: ..\..\src\interfaces\response_formatter.py
Line = 3609, Starts = 3611, Ends = 3776

## File: ..\..\src\interfaces\terminal_manager.py
Line = 3776, Starts = 3778, Ends = 4044

## File: ..\..\src\interfaces\__init__.py
Line = 4044, Starts = 4046, Ends = 4055

## File: ..\..\src\llm\conversation.py
Line = 4055, Starts = 4057, Ends = 4118

## File: ..\..\src\llm\llm_agent.py
Line = 4118, Starts = 4120, Ends = 4178

## File: ..\..\src\llm\llm_manager.py
Line = 4178, Starts = 4180, Ends = 4393

## File: ..\..\src\llm\model_selector.py
Line = 4393, Starts = 4395, Ends = 4430

## File: ..\..\src\llm\prompt_optimizer.py
Line = 4430, Starts = 4432, Ends = 4463

## File: ..\..\src\llm\response_parser.py
Line = 4463, Starts = 4465, Ends = 4498

## File: ..\..\src\storage\cache_manager.py
Line = 4498, Starts = 4500, Ends = 4698

## File: ..\..\src\storage\persistence_manager.py
Line = 4698, Starts = 4700, Ends = 4902

## File: ..\..\src\storage\__init__.py
Line = 4902, Starts = 4904, Ends = 4913

## File: ..\..\src\task_management\checklist_manager.py
Line = 4913, Starts = 4915, Ends = 5192

## File: ..\..\src\task_management\process_manager.py
Line = 5192, Starts = 5194, Ends = 5371

## File: ..\..\src\task_management\progress_tracker copy.py
Line = 5371, Starts = 5373, Ends = 5610

## File: ..\..\src\task_management\progress_tracker.py
Line = 5610, Starts = 5612, Ends = 5825

## File: ..\..\src\task_management\task_prioritizer.py
Line = 5825, Starts = 5827, Ends = 5919

## File: ..\..\src\task_management\__init__.py
Line = 5919, Starts = 5921, Ends = 5930

## File: ..\..\src\utils\config.py
Line = 5930, Starts = 5932, Ends = 5970

## File: ..\..\src\utils\error_handler.py
Line = 5970, Starts = 5972, Ends = 6189

## File: ..\..\src\utils\logger.py
Line = 6189, Starts = 6191, Ends = 6245

## File: ..\..\src\utils\log_analyzer.py
Line = 6245, Starts = 6247, Ends = 6437

## File: ..\..\src\utils\prompt_templates.py
Line = 6437, Starts = 6439, Ends = 6620

## File: ..\..\src\utils\system_metrics.py
Line = 6620, Starts = 6622, Ends = 6818

## File: ..\..\src\utils\token_counter.py
Line = 6818, Starts = 6820, Ends = 6910

## File: ..\..\src\utils\__init__.py
Line = 6910, Starts = 6912, Ends = 6921

## File: ..\..\src\validation\backend_validator.py
Line = 6921, Starts = 6923, Ends = 7271

## File: ..\..\src\validation\frontend_validator.py
Line = 7271, Starts = 7273, Ends = 7541

## File: ..\..\src\validation\implementation_validator.py
Line = 7541, Starts = 7543, Ends = 7759

## File: ..\..\src\validation\test_manager.py
Line = 7759, Starts = 7761, Ends = 7978

## File: ..\..\src\validation\validation_rules.py
Line = 7978, Starts = 7980, Ends = 8149

## File: ..\..\src\validation\__init__.py
Line = 8149, Starts = 8151, Ends = 8160

## File: ..\..\.env.example
Line = 8160, Starts = 8162, Ends = 8196

## File: ..\..\config\default.yaml
Line = 8196, Starts = 8198, Ends = 8254

## File: ..\..\config\development.yaml
Line = 8254, Starts = 8256, Ends = 8280

## File: ..\..\config\gunicorn.py
Line = 8280, Starts = 8282, Ends = 8330

## File: ..\..\config\local.yaml
Line = 8330, Starts = 8332, Ends = 8348

## File: ..\..\config\production.yaml
Line = 8348, Starts = 8350, Ends = 8380

## File: ..\..\config\prompts\base_prompts.yaml
Line = 8380, Starts = 8382, Ends = 8452

## File: ..\..\config\prompts\error_prompts.yaml
Line = 8452, Starts = 8454, Ends = 8492

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 8492, Starts = 8494, Ends = 8534

