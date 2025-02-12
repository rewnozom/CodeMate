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

file_path = '{generated_file_name}'
extract_code_blocks(file_path, instructions)
```

## File: ..\..\CodeMate\tests\test_agent_end_to_end.py
Line = 40, Starts = 42, Ends = 87

## File: ..\..\CodeMate\tests\test_backend_validator.py
Line = 87, Starts = 89, Ends = 115

## File: ..\..\CodeMate\tests\test_cache_manager.py
Line = 115, Starts = 117, Ends = 149

## File: ..\..\CodeMate\tests\test_checklist_manager.py
Line = 149, Starts = 151, Ends = 181

## File: ..\..\CodeMate\tests\test_config.py
Line = 181, Starts = 183, Ends = 202

## File: ..\..\CodeMate\tests\test_decision_system.py
Line = 202, Starts = 204, Ends = 225

## File: ..\..\CodeMate\tests\test_error_handler.py
Line = 225, Starts = 227, Ends = 253

## File: ..\..\CodeMate\tests\test_event_bus.py
Line = 253, Starts = 255, Ends = 316

## File: ..\..\CodeMate\tests\test_file_watcher.py
Line = 316, Starts = 318, Ends = 346

## File: ..\..\CodeMate\tests\test_frontend_validator.py
Line = 346, Starts = 348, Ends = 380

## File: ..\..\CodeMate\tests\test_implementation.py
Line = 380, Starts = 382, Ends = 398

## File: ..\..\CodeMate\tests\test_implementation_validator.py
Line = 398, Starts = 400, Ends = 425

## File: ..\..\CodeMate\tests\test_llm_integration.py
Line = 425, Starts = 427, Ends = 449

## File: ..\..\CodeMate\tests\test_log_analyzer.py
Line = 449, Starts = 451, Ends = 486

## File: ..\..\CodeMate\tests\test_logger.py
Line = 486, Starts = 488, Ends = 510

## File: ..\..\CodeMate\tests\test_memory_manager.py
Line = 510, Starts = 512, Ends = 545

## File: ..\..\CodeMate\tests\test_navigation.py
Line = 545, Starts = 547, Ends = 578

## File: ..\..\CodeMate\tests\test_persistence_manager.py
Line = 578, Starts = 580, Ends = 610

## File: ..\..\CodeMate\tests\test_process_manager.py
Line = 610, Starts = 612, Ends = 640

## File: ..\..\CodeMate\tests\test_progress_tracker.py
Line = 640, Starts = 642, Ends = 679

## File: ..\..\CodeMate\tests\test_prompt_templates.py
Line = 679, Starts = 681, Ends = 704

## File: ..\..\CodeMate\tests\test_request_handler.py
Line = 704, Starts = 706, Ends = 745

## File: ..\..\CodeMate\tests\test_response_formatter.py
Line = 745, Starts = 747, Ends = 775

## File: ..\..\CodeMate\tests\test_state_manager.py
Line = 775, Starts = 777, Ends = 802

## File: ..\..\CodeMate\tests\test_state_prompts.py
Line = 802, Starts = 804, Ends = 826

## File: ..\..\CodeMate\tests\test_system_metrics.py
Line = 826, Starts = 828, Ends = 856

## File: ..\..\CodeMate\tests\test_task_prioritizer.py
Line = 856, Starts = 858, Ends = 889

## File: ..\..\CodeMate\tests\test_terminal_manager.py
Line = 889, Starts = 891, Ends = 916

## File: ..\..\CodeMate\tests\test_test_manager.py
Line = 916, Starts = 918, Ends = 948

## File: ..\..\CodeMate\tests\test_test_validation.py
Line = 948, Starts = 950, Ends = 966

## File: ..\..\CodeMate\tests\test_token_counter.py
Line = 966, Starts = 968, Ends = 996

## File: ..\..\CodeMate\tests\test_validation_rules.py
Line = 996, Starts = 998, Ends = 1021

## File: ..\..\CodeMate\tests\test_workflow_manager.py
Line = 1021, Starts = 1023, Ends = 1056

## File: ..\..\CodeMate\tests\test_workspace_scanner.py
Line = 1056, Starts = 1058, Ends = 1083

