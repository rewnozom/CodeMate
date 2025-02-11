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

## File: ..\..\cmate\config.py
Line = 72, Starts = 74, Ends = 132

## File: ..\..\cmate\__init__.py
Line = 132, Starts = 134, Ends = 143

## File: ..\..\cmate\__main__.py
Line = 143, Starts = 145, Ends = 292

## File: ..\..\cmate\config\prompts.py
Line = 292, Starts = 294, Ends = 466

## File: ..\..\cmate\config\__init__.py
Line = 466, Starts = 468, Ends = 477

## File: ..\..\cmate\core\agent_coordinator copy.py
Line = 477, Starts = 479, Ends = 636

## File: ..\..\cmate\core\agent_coordinator.py
Line = 636, Starts = 638, Ends = 1203

## File: ..\..\cmate\core\context_manager.py
Line = 1203, Starts = 1205, Ends = 1373

## File: ..\..\cmate\core\core-base.py
Line = 1373, Starts = 1375, Ends = 1647

## File: ..\..\cmate\core\event_bus.py
Line = 1647, Starts = 1649, Ends = 1767

## File: ..\..\cmate\core\memory_manager.py
Line = 1767, Starts = 1769, Ends = 1976

## File: ..\..\cmate\core\prompt_manager.py
Line = 1976, Starts = 1978, Ends = 2163

## File: ..\..\cmate\core\state_manager.py
Line = 2163, Starts = 2165, Ends = 2377

## File: ..\..\cmate\core\workflow_manager.py
Line = 2377, Starts = 2379, Ends = 2720

## File: ..\..\cmate\core\__init__.py
Line = 2720, Starts = 2722, Ends = 2731

## File: ..\..\cmate\file_services\file_analyzer.py
Line = 2731, Starts = 2733, Ends = 3007

## File: ..\..\cmate\file_services\file_watcher.py
Line = 3007, Starts = 3009, Ends = 3197

## File: ..\..\cmate\file_services\workspace_scanner.py
Line = 3197, Starts = 3199, Ends = 3341

## File: ..\..\cmate\file_services\__init__.py
Line = 3341, Starts = 3343, Ends = 3352

## File: ..\..\cmate\interfaces\cli_interface copy.py
Line = 3352, Starts = 3354, Ends = 3718

## File: ..\..\cmate\interfaces\cli_interface.py
Line = 3718, Starts = 3720, Ends = 4071

## File: ..\..\cmate\interfaces\request_handler.py
Line = 4071, Starts = 4073, Ends = 4221

## File: ..\..\cmate\interfaces\response_formatter.py
Line = 4221, Starts = 4223, Ends = 4388

## File: ..\..\cmate\interfaces\terminal_manager.py
Line = 4388, Starts = 4390, Ends = 4656

## File: ..\..\cmate\interfaces\__init__.py
Line = 4656, Starts = 4658, Ends = 4667

## File: ..\..\cmate\llm\conversation.py
Line = 4667, Starts = 4669, Ends = 4730

## File: ..\..\cmate\llm\llm_agent.py
Line = 4730, Starts = 4732, Ends = 4790

## File: ..\..\cmate\llm\llm_manager.py
Line = 4790, Starts = 4792, Ends = 5005

## File: ..\..\cmate\llm\model_selector.py
Line = 5005, Starts = 5007, Ends = 5042

## File: ..\..\cmate\llm\prompt_optimizer.py
Line = 5042, Starts = 5044, Ends = 5075

## File: ..\..\cmate\llm\response_parser.py
Line = 5075, Starts = 5077, Ends = 5110

## File: ..\..\cmate\llm\__init__.py
Line = 5110, Starts = 5112, Ends = 5121

## File: ..\..\cmate\storage\cache_manager.py
Line = 5121, Starts = 5123, Ends = 5321

## File: ..\..\cmate\storage\persistence_manager.py
Line = 5321, Starts = 5323, Ends = 5525

## File: ..\..\cmate\storage\__init__.py
Line = 5525, Starts = 5527, Ends = 5536

## File: ..\..\cmate\task_management\checklist_manager.py
Line = 5536, Starts = 5538, Ends = 5815

## File: ..\..\cmate\task_management\process_manager.py
Line = 5815, Starts = 5817, Ends = 5994

## File: ..\..\cmate\task_management\progress_tracker copy.py
Line = 5994, Starts = 5996, Ends = 6233

## File: ..\..\cmate\task_management\progress_tracker.py
Line = 6233, Starts = 6235, Ends = 6448

## File: ..\..\cmate\task_management\task_prioritizer.py
Line = 6448, Starts = 6450, Ends = 6542

## File: ..\..\cmate\task_management\__init__.py
Line = 6542, Starts = 6544, Ends = 6553

## File: ..\..\cmate\utils\config copy.py
Line = 6553, Starts = 6555, Ends = 6593

## File: ..\..\cmate\utils\config.py
Line = 6593, Starts = 6595, Ends = 6653

## File: ..\..\cmate\utils\error_handler.py
Line = 6653, Starts = 6655, Ends = 6872

## File: ..\..\cmate\utils\logger.py
Line = 6872, Starts = 6874, Ends = 6928

## File: ..\..\cmate\utils\log_analyzer.py
Line = 6928, Starts = 6930, Ends = 7120

## File: ..\..\cmate\utils\prompt_templates.py
Line = 7120, Starts = 7122, Ends = 7303

## File: ..\..\cmate\utils\system_metrics.py
Line = 7303, Starts = 7305, Ends = 7501

## File: ..\..\cmate\utils\token_counter.py
Line = 7501, Starts = 7503, Ends = 7593

## File: ..\..\cmate\utils\__init__.py
Line = 7593, Starts = 7595, Ends = 7604

## File: ..\..\cmate\validation\backend_validator.py
Line = 7604, Starts = 7606, Ends = 7954

## File: ..\..\cmate\validation\frontend_validator.py
Line = 7954, Starts = 7956, Ends = 8224

## File: ..\..\cmate\validation\implementation_validator.py
Line = 8224, Starts = 8226, Ends = 8442

## File: ..\..\cmate\validation\test_manager.py
Line = 8442, Starts = 8444, Ends = 8661

## File: ..\..\cmate\validation\validation_rules.py
Line = 8661, Starts = 8663, Ends = 8832

## File: ..\..\cmate\validation\__init__.py
Line = 8832, Starts = 8834, Ends = 8843

## File: ..\..\config\default.yaml
Line = 8843, Starts = 8845, Ends = 8901

## File: ..\..\config\development.yaml
Line = 8901, Starts = 8903, Ends = 8927

## File: ..\..\config\gunicorn.py
Line = 8927, Starts = 8929, Ends = 8977

## File: ..\..\config\local.yaml
Line = 8977, Starts = 8979, Ends = 8995

## File: ..\..\config\production.yaml
Line = 8995, Starts = 8997, Ends = 9027

## File: ..\..\config\__init__.py
Line = 9027, Starts = 9029, Ends = 9038

## File: ..\..\config\prompts\base_prompts.yaml
Line = 9038, Starts = 9040, Ends = 9110

## File: ..\..\config\prompts\error_prompts.yaml
Line = 9110, Starts = 9112, Ends = 9150

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 9150, Starts = 9152, Ends = 9192

## File: ..\..\config\prompts\__init__.py
Line = 9192, Starts = 9194, Ends = 9203

