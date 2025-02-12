# Project Details

# Table of Contents
- [..\CodeMate\config\prompts_backup_3.0\__init__.py](#-CodeMate-config-prompts_backup_30-__init__py)
- [..\CodeMate\config\prompts_backup_3.0\base_prompts.yaml](#-CodeMate-config-prompts_backup_30-base_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\decision_prompts.yaml](#-CodeMate-config-prompts_backup_30-decision_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\error_prompts.yaml](#-CodeMate-config-prompts_backup_30-error_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\implementation_prompts.yaml](#-CodeMate-config-prompts_backup_30-implementation_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\navigation_prompts.yaml](#-CodeMate-config-prompts_backup_30-navigation_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\state_prompts.yaml](#-CodeMate-config-prompts_backup_30-state_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\test_prompts.yaml](#-CodeMate-config-prompts_backup_30-test_promptsyaml)
- [..\CodeMate\config\prompts_backup_3.0\workflow_prompts.yaml](#-CodeMate-config-prompts_backup_30-workflow_promptsyaml)


# ..\..\CodeMate\config\prompts_backup_3.0\__init__.py
## File: ..\..\CodeMate\config\prompts_backup_3.0\__init__.py

```py
# ..\..\CodeMate\config\prompts_backup_3.0\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\base_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\base_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\base_prompts.yaml
# config/prompts/base_prompts.yaml
# Base prompts for the system – version 3.0
# These prompts form the core guidance for the agent's behavior.
# Note that there are now separate modules for navigation, implementation, testing, decision, and state.
# This file still contains some important generic templates used in the system.

system_prompt:
  content: |
    You are a semi-autonomous agent assistant specialized in code analysis, modification, and testing.
    Your workspace is strictly limited to the "./Workspace" directory.
    Follow these principles meticulously:
      1. Thoroughly analyze the current code and context before making any modifications.
      2. Develop clear, step-by-step plans prior to implementation.
      3. Implement changes while preserving the existing code style and structure.
      4. Rigorously test all modifications using unit and integration tests.
      5. Document your decisions, changes, and underlying reasoning in detail.
      6. In case of errors, perform a detailed analysis and propose concrete recovery actions.
    Always maintain awareness of the system’s state and context when deciding on your actions.
  variables: []
  description: "Base system prompt for agent initialization with detailed behavior guidelines."
  category: "system"
  version: "3.0"

analysis_prompt:
  content: |
    Analyze the following files thoroughly and provide a detailed report that includes:
      1. An overview of the system architecture and module dependencies.
      2. Identification of key components and potential issues.
      3. Recommendations for immediate actions and long-term improvements.
      4. Suggestions for further testing or analysis.
    Files to analyze: {files}
  variables:
    - files
  description: "Detailed prompt for file analysis requiring a comprehensive report."
  category: "analysis"
  version: "3.0"

implementation_prompt:
  content: |
    Implement the requested changes by adhering to these guidelines:
      1. Analyze the existing codebase and preserve the current coding style.
      2. Add detailed documentation and inline comments to explain your changes.
      3. Develop comprehensive unit tests and integration tests to validate the modifications.
      4. Incorporate robust error handling to manage unexpected situations.
      5. Provide a detailed report outlining the changes, rationale, and any assumptions.
    Requested changes: {changes}
    Affected files: {files}
  variables:
    - changes
    - files
  description: "Prompt for implementation with detailed instructions and documentation requirements."
  category: "implementation"
  version: "3.0"

test_prompt:
  content: |
    Develop a comprehensive test suite to validate the implemented changes. Your test plan should include:
      1. Unit tests for all new functionality and edge cases.
      2. Integration tests to ensure proper interaction between modules.
      3. Test cases covering error handling and unexpected scenarios.
      4. A summary of test results and any identified issues.
    Implementation details: {implementation}
    Files to test: {files}
  variables:
    - implementation
    - files
  description: "Prompt for creating a full test suite with detailed validation criteria."
  category: "testing"
  version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\decision_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\decision_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\decision_prompts.yaml
# config/prompts/decision_prompts.yaml

base_decision:
  content: |
    Current Context:
    STATE: {current_state}
    REQUEST: {user_request}
    SYSTEM_CONTEXT: {system_context}
    
    Available Actions:
    {available_actions}
    
    Previous Decisions:
    {previous_decisions}
    
    Make a decision considering:
    1. Current state requirements
    2. User request goals
    3. System constraints
    4. Previous actions
    
    Respond with:
    1. Analysis: [Your analysis]
    2. Decision: <{Decide} action_name>
    3. Reasoning: [Explain your choice]
  variables:
    - current_state
    - user_request
    - system_context
    - available_actions
    - previous_decisions
  description: "Prompt for making a decision based on the current context, available actions, and previous decisions."
  category: "decision"
  version: "3.0"

recovery_decision_prompt:
  content: |
    Error Context:
    ERROR: {error_details}
    PREVIOUS_DECISION: {previous_decision}
    SYSTEM_STATE: {system_state}
    
    Available Recovery Actions:
    {recovery_actions}
    
    Determine recovery path:
    1. Analyze error cause
    2. Consider alternative actions
    3. Evaluate impact
    
    Respond with:
    4. Analysis: [Error analysis]
    5. Recovery: <{Recover} action_name>
    6. Justification: [Explain recovery choice]
  variables:
    - error_details
    - previous_decision
    - system_state
    - recovery_actions
  description: "Prompt for determining a recovery decision when an error occurs."
  category: "decision"
  version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\error_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\error_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\error_prompts.yaml
# config/prompts/error_prompts.yaml
# Error prompts for in-depth error analysis and recovery – version 3.0
# These prompt templates guide the agent to perform both detailed root cause analysis and propose concrete recovery steps.

error_analysis:
  content: |
    Analyze the following error message and provide a comprehensive report that includes:
      1. A detailed root cause analysis identifying all relevant factors and contextual issues.
      2. Concrete recommendations for immediate corrective actions.
      3. Long-term prevention strategies to avoid similar errors.
      4. Suggestions for additional tests or monitoring to ensure system stability.
    Error details: {error_message}
    Context: {context}
  variables:
    - error_message
    - context
  description: "Prompt for detailed error analysis, including immediate fixes and long-term prevention."
  category: "error"
  version: "3.0"

error_recovery:
  content: |
    Propose a detailed recovery plan to restore the system to a functional state. Your plan should include:
      1. Immediate actions to stabilize the system.
      2. Steps to recover data or state if necessary.
      3. Validation measures to confirm the success of the recovery.
      4. Recommendations for follow-up tests and monitoring to prevent future issues.
    Error: {error}
    Current state: {state}
  variables:
    - error
    - state
  description: "Prompt for detailed error recovery steps covering both immediate stabilization and long-term solutions."
  category: "error"
  version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\implementation_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\implementation_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\implementation_prompts.yaml
# config/prompts/implementation_prompts.yaml

implementation_planning_prompt:
  content: |
    Based on:
    REQUEST: {user_request}
    CURRENT CODE: {current_code}
    DEPENDENCIES: {dependencies}

    Create an implementation plan that includes:
    1. Required changes
    2. Dependency impacts
    3. Test requirements
    4. Potential risks

    Respond with:
    1. Analysis: [Detailed analysis]
    2. Plan: [Step-by-step plan]
    3. Decision: <{Implement} strategy_name>
  variables:
    - user_request
    - current_code
    - dependencies
  description: "Prompt for creating a detailed implementation plan including required changes, dependencies, tests, and risks."
  category: "implementation"
  version: "3.0"

code_generation_prompt:
  content: |
    Task: {implementation_task}
    Current Code: {current_code}
    Dependencies: {dependencies}
    Requirements: {requirements}
    Style Guide: {style_guide}

    Generate the implementation following these guidelines:
    1. Match existing code style
    2. Include documentation
    3. Handle errors appropriately
    4. Consider edge cases

    Respond with:
    1. Implementation:
    ```python
    [Your code here]
    ```
    2. Explanation: [Implementation details]
    3. Testing Notes: [What should be tested]
  variables:
    - implementation_task
    - current_code
    - dependencies
    - requirements
    - style_guide
  description: "Prompt for generating code for a given task, ensuring adherence to style, documentation, and error handling."
  category: "implementation"
  version: "3.0"

implementation_recovery_prompt:
  content: |
    ERROR LOG: {error_log}
    PREVIOUS IMPLEMENTATION: {previous_code}
    TEST RESULTS: {test_results}
    ORIGINAL REQUEST: {user_request}
    IMPLEMENTATION PLAN: {implementation_plan}

    Analyze the failure and determine:
    1. Root cause
    2. Required fixes
    3. Additional dependencies needed

    Available Actions:
    {recovery_actions}

    Respond with:
    4. Analysis: [Error analysis]
    5. Action: <{Recover} action_name>
    6. Changes: [Required changes]
  variables:
    - error_log
    - previous_code
    - test_results
    - user_request
    - implementation_plan
    - recovery_actions
  description: "Prompt for recovering from implementation failures by analyzing errors and proposing corrective actions."
  category: "implementation"
  version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\navigation_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\navigation_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\navigation_prompts.yaml
# config/prompts/navigation_prompts.yaml

navigation_analysis_prompt:
  content: |
    Based on the following:
    USER REQUEST: {user_request}
    WORKSPACE STRUCTURE: {workspace_data}
    CURRENT STATE: {current_state}

    Your task is to:
    1. Analyze if this requires:
       - Modifying existing files
       - Creating new files
       - Multiple file changes
    2. Identify target components
    3. Choose appropriate action

    Available Actions:
    {available_actions}

    Respond in the following format:
    4. Analysis: [Your detailed analysis]
    5. Decision: <{Navigate} action_name>
    6. Reasoning: [Explain your choice]
  variables:
    - user_request
    - workspace_data
    - current_state
    - available_actions
  description: "Prompt for analyzing navigation requirements and choosing appropriate file actions based on the workspace structure and current state."
  category: "navigation"
  version: "3.0"

multi_component_prompt:
  content: |
    Based on your previous analysis, you need to handle multiple components.
    
    Components identified:
    {identified_components}

    For each component, specify:
    1. Priority order
    2. Dependencies
    3. Required changes

    Format your response as:
    4. Component Plan: [Ordered list with dependencies]
    5. Navigation Order: <{NavigateMulti} [ordered_components]>
    6. Reasoning: [Explain your planning]
  variables:
    - identified_components
  description: "Prompt for handling multiple components by specifying priority order, dependencies, and required changes."
  category: "navigation"
  version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\state_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\state_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\state_prompts.yaml
analysis_state_prompts:
  initial_analysis:
    content: |
      Analyze the current situation:
      REQUEST: {user_request}
      WORKSPACE: {workspace_data}
      CONTEXT: {current_context}
      
      Provide:
      1. Situation Analysis
      2. Required Actions
      3. Potential Challenges
      
      Response Format:
      4. Analysis: [Your analysis]
      5. Action: <{Action} chosen_action>
      6. Details: [Implementation details]
    variables:
      - user_request
      - workspace_data
      - current_context
    description: "Prompt to analyze the current state based on the user request and workspace context."
    category: "state"
    version: "3.0"

  dependency_analysis:
    content: |
      Analyze dependencies for:
      TARGET: {target_component}
      RELATED: {related_components}
      
      Identify:
      1. Direct Dependencies
      2. Indirect Dependencies
      3. Impact Assessment
    variables:
      - target_component
      - related_components
    description: "Prompt to analyze dependencies for a target component and assess their impact."
    category: "state"
    version: "3.0"

implementation_state_prompts:
  code_generation:
    content: |
      Generate implementation for:
      TASK: {implementation_task}
      CONTEXT: {implementation_context}
      STYLE_GUIDE: {style_guide}
      
      Requirements:
      1. Match existing code style
      2. Include documentation
      3. Handle errors
      4. Consider edge cases
    variables:
      - implementation_task
      - implementation_context
      - style_guide
    description: "Prompt to generate code for a specified task while considering style and documentation."
    category: "state"
    version: "3.0"

  code_review:
    content: |
      Review generated code:
      CODE: {generated_code}
      REQUIREMENTS: {requirements}
      
      Check for:
      1. Style Compliance
      2. Error Handling
      3. Edge Cases
      4. Documentation
    variables:
      - generated_code
      - requirements
    description: "Prompt for reviewing generated code for style, error handling, and compliance."
    category: "state"
    version: "3.0"

testing_state_prompts:
  test_generation:
    content: |
      Generate tests for:
      IMPLEMENTATION: {implementation}
      REQUIREMENTS: {requirements}
      
      Include tests for:
      1. Core Functionality
      2. Edge Cases
      3. Error Cases
      4. Integration Points
    variables:
      - implementation
      - requirements
    description: "Prompt to generate a comprehensive test suite for the given implementation."
    category: "state"
    version: "3.0"

  test_analysis:
    content: |
      Analyze test results:
      RESULTS: {test_results}
      ERRORS: {error_log}
      
      Provide:
      1. Failure Analysis
      2. Required Fixes
      3. Recovery Strategy
    variables:
      - test_results
      - error_log
    description: "Prompt to analyze test failures and propose fixes and recovery strategies."
    category: "state"
    version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\test_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\test_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\test_prompts.yaml
# config/prompts/test_prompts.yaml

base_test_generation:
  content: |
    Generate tests for:
    IMPLEMENTATION: {implementation_code}
    REQUIREMENTS: {test_requirements}
    
    Create tests covering:
    1. Core functionality
    2. Edge cases
    3. Error handling
    4. Integration points
    
    Include for each test:
    1. Test case description
    2. Input data
    3. Expected output
    4. Setup requirements
  variables:
    - implementation_code
    - test_requirements
  description: "Prompt for generating comprehensive tests covering functionality, edge cases, errors, and integration."
  category: "testing"
  version: "3.0"

coverage_gap_tests:
  content: |
    Generate additional tests for coverage gaps:
    GAPS: {coverage_gaps}
    EXISTING_TESTS: {existing_tests}
    
    Focus on:
    1. Uncovered code paths
    2. Missing edge cases
    3. Integration scenarios
  variables:
    - coverage_gaps
    - existing_tests
  description: "Prompt for generating additional tests to cover gaps in test coverage."
  category: "testing"
  version: "3.0"

test_failure_analysis:
  content: |
    Analyze test failures:
    FAILED_TESTS: {failed_tests}
    ERROR_LOGS: {error_logs}
    IMPLEMENTATION: {implementation}
    
    Provide:
    1. Root cause analysis
    2. Required fixes
    3. Implementation impact
    4. Test updates needed
  variables:
    - failed_tests
    - error_logs
    - implementation
  description: "Prompt for analyzing test failures and proposing fixes and improvements."
  category: "testing"
  version: "3.0"

```

---

# ..\..\CodeMate\config\prompts_backup_3.0\workflow_prompts.yaml
## File: ..\..\CodeMate\config\prompts_backup_3.0\workflow_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts_backup_3.0\workflow_prompts.yaml
# config/prompts/workflow_prompts.yaml
# Workflow prompts providing step-by-step guidance for planning and validating workflows – version 3.0
# These prompt templates guide the agent through creating detailed workflow plans and performing thorough validations.

workflow_planning:
  content: |
    Develop a comprehensive workflow plan that includes the following:
      1. A clear, step-by-step description of all actions to be taken.
      2. Identification of all dependencies between steps.
      3. Specific validation checkpoints for each step.
      4. Clear objectives and measurable success criteria.
      5. A detailed risk analysis with recommended mitigation measures.
    Task description: {task}
    Context: {context}
  variables:
    - task
    - context
  description: "Prompt for creating a detailed workflow plan with clear steps, dependencies, and validation checkpoints."
  category: "workflow"
  version: "3.0"

workflow_validation:
  content: |
    Review the completed workflow and provide a detailed validation report that covers:
      1. Verification that all workflow steps have been successfully completed.
      2. Confirmation that the results meet the specified objectives.
      3. Identification of any discrepancies or issues.
      4. Recommendations for improvements and risk minimization.
      5. Suggestions for additional tests or inspections if necessary.
    Workflow: {workflow}
    Results: {results}
  variables:
    - workflow
    - results
  description: "Prompt for validating a workflow with focus on completeness, accuracy, and improvement recommendations."
  category: "workflow"
  version: "3.0"

```

---

