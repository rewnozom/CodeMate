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

## File: ..\..\cmate\core\event_bus.py
Line = 1378, Starts = 1380, Ends = 1498

## File: ..\..\cmate\core\memory_manager.py
Line = 1498, Starts = 1500, Ends = 1707

## File: ..\..\cmate\core\prompt_manager.py
Line = 1707, Starts = 1709, Ends = 1894

## File: ..\..\cmate\core\state_manager.py
Line = 1894, Starts = 1896, Ends = 2108

## File: ..\..\cmate\core\workflow_manager.py
Line = 2108, Starts = 2110, Ends = 2451

## File: ..\..\cmate\core\__init__.py
Line = 2451, Starts = 2453, Ends = 2462

## File: ..\..\cmate\file_services\file_analyzer.py
Line = 2462, Starts = 2464, Ends = 2738

## File: ..\..\cmate\file_services\file_watcher.py
Line = 2738, Starts = 2740, Ends = 2928

## File: ..\..\cmate\file_services\workspace_scanner.py
Line = 2928, Starts = 2930, Ends = 3072

## File: ..\..\cmate\file_services\__init__.py
Line = 3072, Starts = 3074, Ends = 3083

## File: ..\..\cmate\interfaces\cli_interface copy.py
Line = 3083, Starts = 3085, Ends = 3449

## File: ..\..\cmate\interfaces\cli_interface.py
Line = 3449, Starts = 3451, Ends = 3802

## File: ..\..\cmate\interfaces\request_handler.py
Line = 3802, Starts = 3804, Ends = 3951

## File: ..\..\cmate\interfaces\response_formatter.py
Line = 3951, Starts = 3953, Ends = 4118

## File: ..\..\cmate\interfaces\terminal_manager.py
Line = 4118, Starts = 4120, Ends = 4386

## File: ..\..\cmate\interfaces\__init__.py
Line = 4386, Starts = 4388, Ends = 4397

## File: ..\..\cmate\llm\conversation.py
Line = 4397, Starts = 4399, Ends = 4460

## File: ..\..\cmate\llm\llm_agent.py
Line = 4460, Starts = 4462, Ends = 4520

## File: ..\..\cmate\llm\llm_manager.py
Line = 4520, Starts = 4522, Ends = 4735

## File: ..\..\cmate\llm\model_selector.py
Line = 4735, Starts = 4737, Ends = 4772

## File: ..\..\cmate\llm\prompt_optimizer.py
Line = 4772, Starts = 4774, Ends = 4805

## File: ..\..\cmate\llm\response_parser.py
Line = 4805, Starts = 4807, Ends = 4840

## File: ..\..\cmate\llm\__init__.py
Line = 4840, Starts = 4842, Ends = 4851

## File: ..\..\cmate\storage\cache_manager.py
Line = 4851, Starts = 4853, Ends = 5051

## File: ..\..\cmate\storage\persistence_manager.py
Line = 5051, Starts = 5053, Ends = 5255

## File: ..\..\cmate\storage\__init__.py
Line = 5255, Starts = 5257, Ends = 5266

## File: ..\..\cmate\task_management\checklist_manager.py
Line = 5266, Starts = 5268, Ends = 5545

## File: ..\..\cmate\task_management\process_manager.py
Line = 5545, Starts = 5547, Ends = 5724

## File: ..\..\cmate\task_management\progress_tracker.py
Line = 5729, Starts = 5731, Ends = 5944

## File: ..\..\cmate\task_management\task_prioritizer.py
Line = 5944, Starts = 5946, Ends = 6038

## File: ..\..\cmate\task_management\__init__.py
Line = 6038, Starts = 6040, Ends = 6049

## File: ..\..\cmate\utils\config copy.py
Line = 6049, Starts = 6051, Ends = 6089

## File: ..\..\cmate\utils\config.py
Line = 6089, Starts = 6091, Ends = 6149

## File: ..\..\cmate\utils\error_handler.py
Line = 6149, Starts = 6151, Ends = 6368

## File: ..\..\cmate\utils\logger.py
Line = 6368, Starts = 6370, Ends = 6424

## File: ..\..\cmate\utils\log_analyzer.py
Line = 6424, Starts = 6426, Ends = 6616

## File: ..\..\cmate\utils\prompt_templates.py
Line = 6616, Starts = 6618, Ends = 6799

## File: ..\..\cmate\utils\system_metrics.py
Line = 6799, Starts = 6801, Ends = 6997

## File: ..\..\cmate\utils\token_counter.py
Line = 6997, Starts = 6999, Ends = 7089

## File: ..\..\cmate\utils\__init__.py
Line = 7089, Starts = 7091, Ends = 7100

## File: ..\..\cmate\validation\backend_validator.py
Line = 7100, Starts = 7102, Ends = 7450

## File: ..\..\cmate\validation\frontend_validator.py
Line = 7450, Starts = 7452, Ends = 7720

## File: ..\..\cmate\validation\implementation_validator.py
Line = 7720, Starts = 7722, Ends = 7938

## File: ..\..\cmate\validation\test_manager.py
Line = 7938, Starts = 7940, Ends = 8157

## File: ..\..\cmate\validation\validation_rules.py
Line = 8157, Starts = 8159, Ends = 8328

## File: ..\..\cmate\validation\__init__.py
Line = 8328, Starts = 8330, Ends = 8339

## File: ..\..\config\default.yaml
Line = 8339, Starts = 8341, Ends = 8397

## File: ..\..\config\development.yaml
Line = 8397, Starts = 8399, Ends = 8423

## File: ..\..\config\gunicorn.py
Line = 8423, Starts = 8425, Ends = 8473

## File: ..\..\config\local.yaml
Line = 8473, Starts = 8475, Ends = 8491

## File: ..\..\config\production.yaml
Line = 8491, Starts = 8493, Ends = 8523

## File: ..\..\config\__init__.py
Line = 8523, Starts = 8525, Ends = 8534

## File: ..\..\config\prompts\base_prompts.yaml
Line = 8534, Starts = 8536, Ends = 8606

## File: ..\..\config\prompts\error_prompts.yaml
Line = 8606, Starts = 8608, Ends = 8646

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 8646, Starts = 8648, Ends = 8688

## File: ..\..\config\prompts\__init__.py
Line = 8688, Starts = 8690, Ends = 8699

