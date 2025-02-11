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

## File: ..\..\cmate\task_management\progress_tracker copy.py
Line = 5724, Starts = 5726, Ends = 5963

## File: ..\..\cmate\task_management\progress_tracker.py
Line = 5963, Starts = 5965, Ends = 6178

## File: ..\..\cmate\task_management\task_prioritizer.py
Line = 6178, Starts = 6180, Ends = 6272

## File: ..\..\cmate\task_management\__init__.py
Line = 6272, Starts = 6274, Ends = 6283

## File: ..\..\cmate\utils\config copy.py
Line = 6283, Starts = 6285, Ends = 6323

## File: ..\..\cmate\utils\config.py
Line = 6323, Starts = 6325, Ends = 6383

## File: ..\..\cmate\utils\error_handler.py
Line = 6383, Starts = 6385, Ends = 6602

## File: ..\..\cmate\utils\logger.py
Line = 6602, Starts = 6604, Ends = 6658

## File: ..\..\cmate\utils\log_analyzer.py
Line = 6658, Starts = 6660, Ends = 6850

## File: ..\..\cmate\utils\prompt_templates.py
Line = 6850, Starts = 6852, Ends = 7033

## File: ..\..\cmate\utils\system_metrics.py
Line = 7033, Starts = 7035, Ends = 7231

## File: ..\..\cmate\utils\token_counter.py
Line = 7231, Starts = 7233, Ends = 7323

## File: ..\..\cmate\utils\__init__.py
Line = 7323, Starts = 7325, Ends = 7334

## File: ..\..\cmate\validation\backend_validator.py
Line = 7334, Starts = 7336, Ends = 7684

## File: ..\..\cmate\validation\frontend_validator.py
Line = 7684, Starts = 7686, Ends = 7954

## File: ..\..\cmate\validation\implementation_validator.py
Line = 7954, Starts = 7956, Ends = 8172

## File: ..\..\cmate\validation\test_manager.py
Line = 8172, Starts = 8174, Ends = 8391

## File: ..\..\cmate\validation\validation_rules.py
Line = 8391, Starts = 8393, Ends = 8562

## File: ..\..\cmate\validation\__init__.py
Line = 8562, Starts = 8564, Ends = 8573

## File: ..\..\config\default.yaml
Line = 8573, Starts = 8575, Ends = 8631

## File: ..\..\config\development.yaml
Line = 8631, Starts = 8633, Ends = 8657

## File: ..\..\config\gunicorn.py
Line = 8657, Starts = 8659, Ends = 8707

## File: ..\..\config\local.yaml
Line = 8707, Starts = 8709, Ends = 8725

## File: ..\..\config\production.yaml
Line = 8725, Starts = 8727, Ends = 8757

## File: ..\..\config\__init__.py
Line = 8757, Starts = 8759, Ends = 8768

## File: ..\..\config\prompts\base_prompts.yaml
Line = 8768, Starts = 8770, Ends = 8840

## File: ..\..\config\prompts\error_prompts.yaml
Line = 8840, Starts = 8842, Ends = 8880

## File: ..\..\config\prompts\workflow_prompts.yaml
Line = 8880, Starts = 8882, Ends = 8922

## File: ..\..\config\prompts\__init__.py
Line = 8922, Starts = 8924, Ends = 8933

