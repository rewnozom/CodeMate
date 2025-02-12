# Project Details

# Table of Contents
- [..\CodeMate\config\prompts\__init__.py](#-CodeMate-config-prompts-__init__py)
- [..\CodeMate\config\prompts\base_prompts.yaml](#-CodeMate-config-prompts-base_promptsyaml)
- [..\CodeMate\config\prompts\decision_prompts.yaml](#-CodeMate-config-prompts-decision_promptsyaml)
- [..\CodeMate\config\prompts\error_prompts.yaml](#-CodeMate-config-prompts-error_promptsyaml)
- [..\CodeMate\config\prompts\implementation_prompts.yaml](#-CodeMate-config-prompts-implementation_promptsyaml)
- [..\CodeMate\config\prompts\navigation_prompts.yaml](#-CodeMate-config-prompts-navigation_promptsyaml)
- [..\CodeMate\config\prompts\state_prompts.yaml](#-CodeMate-config-prompts-state_promptsyaml)
- [..\CodeMate\config\prompts\test_prompts.yaml](#-CodeMate-config-prompts-test_promptsyaml)
- [..\CodeMate\config\prompts\workflow_prompts.yaml](#-CodeMate-config-prompts-workflow_promptsyaml)


# ..\..\CodeMate\config\prompts\__init__.py
## File: ..\..\CodeMate\config\prompts\__init__.py

```py
# ..\..\CodeMate\config\prompts\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\config\prompts\base_prompts.yaml
## File: ..\..\CodeMate\config\prompts\base_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\base_prompts.yaml
# config/prompts/base_prompts.yaml
# Core System Prompts - Version 3.1
# Foundation prompts defining agent behavior, analysis patterns, and operational guidelines.
# Enhanced with comprehensive instructions for code quality, security, and maintainability.

system_prompt:
  content: |
    You are a sophisticated semi-autonomous agent specializing in code development, analysis, and quality assurance.
    Operating Environment: "./Workspace" directory (strictly enforced)

    Core Operational Principles:
    1. Analysis & Planning
       - Perform thorough code and context analysis
       - Evaluate security implications and risks
       - Identify dependencies and potential impacts
       - Create detailed implementation roadmaps

    2. Development Standards
       - Maintain consistent code style and patterns
       - Follow clean code principles
       - Implement comprehensive error handling
       - Add detailed logging for operations
       - Use type hints and proper documentation

    3. Quality Assurance
       - Write comprehensive test suites
       - Validate edge cases and error conditions
       - Ensure backward compatibility
       - Verify security considerations

    4. Documentation & Communication
       - Document all decisions and rationales
       - Maintain clear change logs
       - Provide implementation details
       - Include usage examples

    5. Error Management
       - Implement graceful error handling
       - Provide detailed error analysis
       - Develop recovery strategies
       - Document error patterns

    6. Performance & Security
       - Optimize critical paths
       - Implement security best practices
       - Consider resource usage
       - Monitor system impacts

    Always maintain system state awareness and context sensitivity in decision-making.
  variables: []
  description: "Enhanced system prompt with comprehensive guidelines for high-quality code development and maintenance."
  category: "system"
  version: "3.1"

analysis_prompt:
  content: |
    Perform comprehensive codebase analysis:

    TARGET: {files}

    Analysis Requirements:
    1. Architecture Assessment
       - System structure and design patterns
       - Component relationships
       - Dependency graph
       - Integration points

    2. Code Quality Evaluation
       - Style consistency
       - Documentation coverage
       - Error handling patterns
       - Testing coverage

    3. Technical Debt Analysis
       - Code complexity
       - Duplicate patterns
       - Outdated practices
       - Performance bottlenecks

    4. Security Assessment
       - Vulnerability scanning
       - Security best practices
       - Input validation
       - Data protection

    5. Recommendations
       - Immediate improvements
       - Long-term refactoring
       - Security enhancements
       - Performance optimization

    Provide detailed report with:
    ANALYSIS:
      Architecture: [Detailed architecture breakdown]
      Quality: [Code quality assessment]
      Security: [Security findings]
      Performance: [Performance analysis]
    
    RECOMMENDATIONS:
      Priority: [Prioritized action items]
      Timeline: [Implementation timeline]
      Risks: [Risk assessment]
      Resources: [Required resources]
  variables:
    - files
  description: "Comprehensive analysis prompt covering architecture, quality, security, and improvement recommendations."
  category: "analysis"
  version: "3.1"

implementation_prompt:
  content: |
    Execute codebase modifications:

    CHANGES: {changes}
    FILES: {files}

    Implementation Guidelines:
    1. Code Quality Standards
       - Maintain consistent style
       - Follow SOLID principles
       - Implement clean code practices
       - Add comprehensive logging
       - Include type hints
       - Write detailed documentation

    2. Error Management
       - Implement try-catch blocks
       - Add error recovery
       - Log error details
       - Provide user feedback

    3. Testing Requirements
       - Unit test coverage
       - Integration tests
       - Edge case validation
       - Performance testing

    4. Security Considerations
       - Input validation
       - Data sanitization
       - Access control
       - Secure coding practices

    5. Documentation
       - Update API documentation
       - Add usage examples
       - Document edge cases
       - Include error scenarios

    Deliverables:
    IMPLEMENTATION:
      Changes: [Detailed change list]
      Tests: [Test coverage details]
      Docs: [Documentation updates]
      Review: [Review checklist]
  variables:
    - changes
    - files
  description: "Detailed implementation prompt ensuring high-quality, secure, and well-tested code modifications."
  category: "implementation"
  version: "3.1"

test_prompt:
  content: |
    Develop comprehensive test suite:

    IMPLEMENTATION: {implementation}
    FILES: {files}

    Testing Requirements:
    1. Unit Testing
       - Core functionality
       - Edge cases
       - Error conditions
       - Parameter validation
       - State management

    2. Integration Testing
       - Component interaction
       - API contracts
       - Data flow
       - Error propagation

    3. Performance Testing
       - Load handling
       - Resource usage
       - Response times
       - Scalability

    4. Security Testing
       - Input validation
       - Authentication
       - Authorization
       - Data protection

    5. Documentation
       - Test scenarios
       - Setup requirements
       - Test data
       - Expected results

    Deliverables:
    TEST_SUITE:
      Coverage: [Test coverage metrics]
      Results: [Test execution results]
      Issues: [Identified issues]
      Fixes: [Required fixes]
  variables:
    - implementation
    - files
  description: "Comprehensive test suite development prompt ensuring thorough validation of all aspects."
  category: "testing"
  version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\decision_prompts.yaml
## File: ..\..\CodeMate\config\prompts\decision_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\decision_prompts.yaml
# config/prompts/decision_prompts.yaml
# Decision-Making Framework - Version 3.1
# Enhanced prompts for intelligent action selection and error recovery

base_decision:
  content: |
    Evaluate current context and determine optimal action:

    CONTEXT:
      State: {current_state}
      Request: {user_request}
      System: {system_context}

    AVAILABLE_ACTIONS:
    {available_actions}

    HISTORY:
      Previous Decisions: {previous_decisions}

    Decision Framework:
    1. Context Analysis
       - State requirements and constraints
       - Request objectives and priorities
       - System capabilities and limitations
       - Resource availability

    2. Impact Assessment
       - Short-term effects
       - Long-term implications
       - Resource requirements
       - Risk factors

    3. Action Evaluation
       - Success probability
       - Required resources
       - Implementation complexity
       - Recovery options

    4. Constraint Validation
       - System boundaries
       - Security implications
       - Performance impact
       - Maintainability

    Provide structured response:
    DECISION:
      Analysis: [Detailed context analysis]
      Choice: <{Decide} action_name>
      Priority: [High/Medium/Low]
      Impact: [Expected outcomes]
      Risks: [Identified risks]
      Mitigation: [Risk mitigation steps]
      Validation: [Success criteria]
  variables:
    - current_state
    - user_request
    - system_context
    - available_actions
    - previous_decisions
  description: "Enhanced decision-making prompt with comprehensive context analysis and structured evaluation framework."
  category: "decision"
  version: "3.1"

recovery_decision_prompt:
  content: |
    Analyze error situation and determine recovery strategy:

    ERROR_CONTEXT:
      Details: {error_details}
      Previous Action: {previous_decision}
      System State: {system_state}

    RECOVERY_OPTIONS:
    {recovery_actions}

    Recovery Analysis Framework:
    1. Error Assessment
       - Root cause analysis
       - Error propagation
       - Impact scope
       - System stability

    2. Context Evaluation
       - System state integrity
       - Data consistency
       - Resource availability
       - Service stability

    3. Recovery Strategy
       - Immediate actions
       - Rollback requirements
       - Data recovery needs
       - Service restoration

    4. Prevention Planning
       - Similar error prevention
       - Monitoring improvements
       - Process enhancements
       - Documentation updates

    Provide structured recovery plan:
    RECOVERY:
      Analysis: [Detailed error analysis]
      Action: <{Recover} action_name>
      Priority: [Critical/High/Medium/Low]
      Steps: [Ordered recovery steps]
      Validation: [Recovery validation points]
      Prevention: [Future prevention measures]
      Documentation: [Required documentation updates]
      
    MONITORING:
      Metrics: [Key metrics to watch]
      Thresholds: [Alert thresholds]
      Checks: [Validation checks]
  variables:
    - error_details
    - previous_decision
    - system_state
    - recovery_actions
  description: "Comprehensive error recovery prompt with detailed analysis, structured recovery planning, and prevention strategies."
  category: "decision"
  version: "3.1"

validation_decision_prompt:
  content: |
    Validate action outcomes and determine next steps:

    ACTION_CONTEXT:
      Action: {completed_action}
      Results: {action_results}
      Expectations: {expected_outcomes}

    Validation Framework:
    1. Result Analysis
       - Success criteria evaluation
       - Performance metrics
       - Error conditions
       - Side effects

    2. Compliance Check
       - Security requirements
       - Performance standards
       - Quality criteria
       - Documentation completeness

    3. Impact Assessment
       - System stability
       - Resource usage
       - User impact
       - Integration effects

    Provide validation report:
    VALIDATION:
      Status: [Success/Partial/Failed]
      Analysis: [Detailed analysis]
      Issues: [Identified issues]
      Actions: [Required actions]
      Recommendations: [Improvement suggestions]
  variables:
    - completed_action
    - action_results
    - expected_outcomes
  description: "New validation decision prompt for evaluating action outcomes and determining follow-up steps."
  category: "decision"
  version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\error_prompts.yaml
## File: ..\..\CodeMate\config\prompts\error_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\error_prompts.yaml
# config/prompts/error_prompts.yaml
# Advanced Error Analysis and Recovery Framework - Version 3.1
# Sophisticated templates for systematic error analysis, recovery planning, and prevention

error_analysis:
  content: |
    Perform comprehensive error analysis:

    ERROR_CONTEXT:
      Message: {error_message}
      System Context: {context}

    Analysis Framework:
    1. Error Classification
       - Error type and severity
       - Component affected
       - Scope of impact
       - Data integrity status

    2. Root Cause Analysis
       - Direct trigger
       - Contributing factors
       - Environmental conditions
       - System state analysis
       - Resource constraints
       - Timing factors

    3. Impact Assessment
       - System stability
       - Data consistency
       - Service availability
       - User impact
       - Resource utilization
       - Performance metrics

    4. Pattern Recognition
       - Similar past incidents
       - Common factors
       - System vulnerabilities
       - Error patterns

    Provide detailed analysis report:
    ANALYSIS:
      Classification: [Error classification]
      Root Cause: [Detailed cause analysis]
      Impact: [Impact assessment]
      Patterns: [Identified patterns]

    RECOMMENDATIONS:
      Immediate: [Urgent actions needed]
      Short-term: [Quick improvements]
      Long-term: [Strategic changes]
      Prevention: [Prevention measures]

    MONITORING:
      Metrics: [Key metrics to track]
      Thresholds: [Alert thresholds]
      Validation: [Success criteria]
  variables:
    - error_message
    - context
  description: "Enhanced error analysis prompt with systematic investigation framework and comprehensive recommendations."
  category: "error"
  version: "3.1"

error_recovery:
  content: |
    Develop structured recovery strategy:

    ERROR_DETAILS:
      Error: {error}
      State: {state}

    Recovery Framework:
    1. Immediate Response
       - System stabilization
       - Service restoration
       - Data protection
       - User communication

    2. Recovery Process
       - State restoration
       - Data recovery
       - Service validation
       - Integration checks
       - Performance verification

    3. Validation Steps
       - System integrity
       - Data consistency
       - Service functionality
       - Performance metrics
       - Security checks

    4. Post-Recovery Actions
       - System hardening
       - Monitoring enhancement
       - Documentation updates
       - Process improvements

    Provide detailed recovery plan:
    RECOVERY:
      Priority: [Critical/High/Medium/Low]
      Timeline: [Expected recovery time]
      Resources: [Required resources]
      
      Steps:
        Immediate: [Immediate actions]
        Recovery: [Recovery process]
        Validation: [Validation steps]
        Closure: [Completion criteria]

    VERIFICATION:
      Checks: [Required validations]
      Tests: [Test scenarios]
      Metrics: [Success metrics]
      
    DOCUMENTATION:
      Incident: [Incident details]
      Actions: [Actions taken]
      Results: [Recovery results]
      Lessons: [Lessons learned]
  variables:
    - error
    - state
  description: "Comprehensive error recovery prompt with structured recovery planning and thorough validation framework."
  category: "error"
  version: "3.1"

incident_closure:
  content: |
    Document error incident resolution:

    INCIDENT_DETAILS:
      Error: {error_details}
      Recovery: {recovery_actions}
      Duration: {incident_duration}

    Closure Requirements:
    1. Incident Summary
       - Initial trigger
       - Impact scope
       - Resolution steps
       - Recovery time

    2. Success Validation
       - System stability
       - Service availability
       - Data integrity
       - Performance metrics

    3. Learning Points
       - Root causes
       - Prevention measures
       - Process improvements
       - Documentation updates

    4. Follow-up Actions
       - Monitoring improvements
       - System hardening
       - Training needs
       - Documentation updates

    Provide closure report:
    CLOSURE:
      Summary: [Incident summary]
      Resolution: [Resolution details]
      Validation: [Success validation]
      Learning: [Key learnings]
      Actions: [Follow-up items]
  variables:
    - error_details
    - recovery_actions
    - incident_duration
  description: "New incident closure prompt ensuring thorough documentation and learning from error incidents."
  category: "error"
  version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\implementation_prompts.yaml
## File: ..\..\CodeMate\config\prompts\implementation_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\implementation_prompts.yaml
# config/prompts/implementation_prompts.yaml
# Advanced Implementation Framework - Version 3.1
# Comprehensive templates for code planning, generation, and recovery

implementation_planning_prompt:
  content: |
    Develop implementation strategy based on:

    CONTEXT:
      Request: {user_request}
      Current Code: {current_code}
      Dependencies: {dependencies}

    Planning Framework:
    1. Architecture Analysis
       - System design impact
       - Component interactions
       - Integration points
       - Performance considerations
       - Security implications

    2. Implementation Strategy
       - Code modifications
       - New components
       - Refactoring needs
       - Migration steps
       - Rollback plan

    3. Resource Requirements
       - Development time
       - Testing resources
       - Documentation needs
       - Training requirements
       - Maintenance impact

    4. Risk Assessment
       - Technical risks
       - Integration risks
       - Performance risks
       - Security risks
       - Mitigation strategies

    Provide detailed implementation plan:
    ANALYSIS:
      Architecture: [Design analysis]
      Impact: [System impact]
      Resources: [Required resources]
      Timeline: [Implementation timeline]
    
    STRATEGY:
      Plan: [Detailed implementation steps]
      Decision: <{Implement} strategy_name>
      Priority: [High/Medium/Low]
      Phases: [Implementation phases]
      
    VALIDATION:
      Tests: [Required tests]
      Metrics: [Success metrics]
      Checkpoints: [Validation points]
  variables:
    - user_request
    - current_code
    - dependencies
  description: "Enhanced implementation planning prompt with comprehensive analysis and structured planning framework."
  category: "implementation"
  version: "3.1"

code_generation_prompt:
  content: |
    Generate implementation for:

    REQUIREMENTS:
      Task: {implementation_task}
      Code: {current_code}
      Dependencies: {dependencies}
      Requirements: {requirements}
      Style: {style_guide}

    Development Guidelines:
    1. Code Quality
       - Follow clean code principles
       - Maintain consistent style
       - Use meaningful names
       - Keep functions focused
       - Optimize for readability

    2. Documentation
       - Class/function docstrings
       - Implementation details
       - Usage examples
       - Edge cases
       - Assumptions

    3. Error Handling
       - Input validation
       - Exception handling
       - Error recovery
       - Logging strategy
       - User feedback

    4. Security & Performance
       - Security best practices
       - Resource management
       - Performance optimization
       - Memory efficiency
       - Thread safety

    Provide implementation:
    CODE:
    ```python
    [Implementation here]
    ```

    DOCUMENTATION:
      Overview: [Implementation overview]
      Details: [Technical details]
      Usage: [Usage examples]
      Notes: [Important considerations]

    TESTING:
      Units: [Unit test requirements]
      Integration: [Integration test needs]
      Edge Cases: [Edge case scenarios]
      Performance: [Performance test cases]
  variables:
    - implementation_task
    - current_code
    - dependencies
    - requirements
    - style_guide
  description: "Comprehensive code generation prompt ensuring high-quality, secure, and well-documented implementations."
  category: "implementation"
  version: "3.1"

implementation_recovery_prompt:
  content: |
    Analyze implementation failure and determine recovery strategy:

    CONTEXT:
      Error: {error_log}
      Code: {previous_code}
      Tests: {test_results}
      Request: {user_request}
      Plan: {implementation_plan}

    ACTIONS:
    {recovery_actions}

    Recovery Framework:
    1. Error Analysis
       - Root cause identification
       - Error patterns
       - Impact assessment
       - Dependency issues
       - Performance factors

    2. Recovery Strategy
       - Code fixes
       - Dependency updates
       - Configuration changes
       - Data recovery
       - Service restoration

    3. Validation Requirements
       - Code review
       - Test coverage
       - Performance validation
       - Security checks
       - Integration testing

    Provide recovery plan:
    ANALYSIS:
      Cause: [Root cause analysis]
      Impact: [Error impact]
      Patterns: [Error patterns]
      
    RECOVERY:
      Action: <{Recover} action_name>
      Changes: [Required changes]
      Steps: [Recovery steps]
      
    VALIDATION:
      Tests: [Required tests]
      Checks: [Validation points]
      Metrics: [Success criteria]
  variables:
    - error_log
    - previous_code
    - test_results
    - user_request
    - implementation_plan
    - recovery_actions
  description: "Enhanced implementation recovery prompt with systematic error analysis and structured recovery planning."
  category: "implementation"
  version: "3.1"

code_review_prompt:
  content: |
    Review implementation quality:

    CODE:
      Implementation: {implementation}
      Changes: {changes}
      Tests: {tests}

    Review Framework:
    1. Code Quality
       - Clean code principles
       - Style consistency
       - Documentation quality
       - Error handling
       - Performance aspects

    2. Security Review
       - Input validation
       - Data protection
       - Access control
       - Security patterns
       - Vulnerability checks

    3. Testing Assessment
       - Test coverage
       - Edge cases
       - Error scenarios
       - Performance tests
       - Integration tests

    Provide review report:
    REVIEW:
      Quality: [Code quality assessment]
      Security: [Security review]
      Testing: [Test coverage analysis]
      Issues: [Identified issues]
      Fixes: [Required changes]
  variables:
    - implementation
    - changes
    - tests
  description: "New code review prompt ensuring comprehensive quality assessment of implementations."
  category: "implementation"
  version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\navigation_prompts.yaml
## File: ..\..\CodeMate\config\prompts\navigation_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\navigation_prompts.yaml
# config/prompts/navigation_prompts.yaml
# Advanced Navigation and Component Management Framework - Version 3.1
# Enhanced templates for intelligent workspace navigation and multi-component operations

navigation_analysis_prompt:
  content: |
    Analyze workspace navigation requirements:

    CONTEXT:
      Request: {user_request}
      Workspace: {workspace_data}
      State: {current_state}

    Analysis Framework:
    1. Operation Type Assessment
       - File Modifications
         * Content changes
         * Structure updates
         * Permission changes
         * Dependency updates

       - New File Requirements
         * Component types
         * File locations
         * Naming conventions
         * Required templates

       - Multi-file Operations
         * Change patterns
         * Consistency requirements
         * Order dependencies
         * Rollback considerations

    2. Component Analysis
       - Target Identification
         * Primary components
         * Related files
         * Configuration needs
         * Resource dependencies

       - Impact Assessment
         * Direct changes
         * Indirect effects
         * Integration points
         * Performance implications

    3. Navigation Strategy
       - Access Patterns
         * Read operations
         * Write operations
         * Atomic requirements
         * Backup needs

       - Safety Measures
         * Validation checks
         * Backup procedures
         * Rollback points
         * State preservation

    Available Actions:
    {available_actions}

    Provide navigation decision:
    ANALYSIS:
      Operations: [Required operations]
      Components: [Affected components]
      Impact: [Change impact]
      
    STRATEGY:
      Decision: <{Navigate} action_name>
      Priority: [High/Medium/Low]
      Order: [Operation sequence]
      
    SAFETY:
      Validation: [Required checks]
      Backups: [Backup needs]
      Rollback: [Rollback strategy]
  variables:
    - user_request
    - workspace_data
    - current_state
    - available_actions
  description: "Enhanced navigation analysis prompt with comprehensive file operation planning and safety considerations."
  category: "navigation"
  version: "3.1"

multi_component_prompt:
  content: |
    Develop multi-component operation strategy:

    COMPONENTS:
    {identified_components}

    Component Analysis Framework:
    1. Dependency Mapping
       - Direct Dependencies
         * Required components
         * Shared resources
         * API contracts
         * Configuration needs

       - Indirect Dependencies
         * Transitive requirements
         * Resource chains
         * Service dependencies
         * Integration points

    2. Priority Assessment
       - Critical Path
         * Core functionality
         * User impact
         * System stability
         * Performance effects

       - Resource Optimization
         * Parallel operations
         * Sequential requirements
         * Resource constraints
         * Time dependencies

    3. Change Management
       - Operation Sequencing
         * Preparation steps
         * Core changes
         * Validation points
         * Cleanup tasks

       - Risk Mitigation
         * Atomic operations
         * Rollback procedures
         * State management
         * Error handling

    Provide component strategy:
    PLANNING:
      Dependencies: [Dependency map]
      Priority: [Component priority]
      Timeline: [Operation timeline]
      
    EXECUTION:
      Order: <{NavigateMulti} [ordered_components]>
      Steps: [Detailed steps]
      Validation: [Check points]
      
    SAFETY:
      Atomicity: [Atomic operations]
      Recovery: [Recovery strategy]
      Monitoring: [Key metrics]
  variables:
    - identified_components
  description: "Comprehensive multi-component operation prompt with dependency management and execution planning."
  category: "navigation"
  version: "3.1"

workspace_validation_prompt:
  content: |
    Validate workspace operation results:

    OPERATION:
      Changes: {completed_changes}
      Components: {affected_components}
      State: {workspace_state}

    Validation Framework:
    1. Structure Verification
       - File integrity
       - Directory structure
       - Permission status
       - Resource availability

    2. Component Validation
       - Functionality checks
       - Integration tests
       - Performance impact
       - Security status

    3. State Assessment
       - System stability
       - Resource usage
       - Service availability
       - Error conditions

    Provide validation report:
    VALIDATION:
      Structure: [Structure check]
      Components: [Component status]
      Integration: [Integration status]
      Issues: [Found issues]
      Actions: [Required actions]
  variables:
    - completed_changes
    - affected_components
    - workspace_state
  description: "New workspace validation prompt ensuring integrity of navigation operations."
  category: "navigation"
  version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\state_prompts.yaml
## File: ..\..\CodeMate\config\prompts\state_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\state_prompts.yaml
analysis_state_prompts:
  initial_analysis:
    content: |
      Analyze the current development request and context:
      
      REQUEST: {user_request}
      WORKSPACE: {workspace_data}
      CONTEXT: {current_context}
      
      Provide a structured analysis covering:
      1. Situation Assessment
         - Key requirements and constraints
         - Available resources and limitations
         - Critical dependencies
      
      2. Action Planning
         - Required implementation steps
         - Priority order of execution
         - Risk mitigation strategies
      
      3. Technical Considerations
         - Architecture impacts
         - Performance implications
         - Security considerations
      
      Response Format:
      ANALYSIS:
        Situation: [Detailed situation analysis]
        Technical: [Technical impact assessment]
        Risks: [Identified risks and mitigations]
      
      ACTION:
        <{Action} primary_action>
        Priority: [High/Medium/Low]
        Dependencies: [List of dependencies]
      
      IMPLEMENTATION:
        Steps: [Ordered implementation steps]
        Validation: [Required validation points]
        Rollback: [Rollback strategy if needed]
    variables:
      - user_request
      - workspace_data
      - current_context
    description: "Comprehensive prompt for analyzing development requests with technical, risk, and implementation considerations."
    category: "state"
    version: "3.1"

  dependency_analysis:
    content: |
      Perform dependency analysis for component:
      
      TARGET: {target_component}
      RELATED: {related_components}
      
      Analyze and document:
      1. Direct Dependencies
         - Required libraries and versions
         - External service dependencies
         - Internal component dependencies
      
      2. Indirect Dependencies
         - Transitive dependencies
         - Shared resource requirements
         - Configuration dependencies
      
      3. Impact Assessment
         - Change propagation analysis
         - Performance implications
         - Security considerations
         - Breaking changes
      
      4. Migration Strategy
         - Required updates
         - Version compatibility
         - Update sequence
      
      Provide recommendations for:
      - Dependency optimization
      - Risk mitigation
      - Update strategy
    variables:
      - target_component
      - related_components
    description: "Detailed dependency analysis prompt covering direct, indirect, and impact assessment with migration planning."
    category: "state"
    version: "3.1"

implementation_state_prompts:
  code_generation:
    content: |
      Generate production-ready implementation for:
      
      TASK: {implementation_task}
      CONTEXT: {implementation_context}
      STYLE_GUIDE: {style_guide}
      
      Implementation Requirements:
      1. Code Quality
         - Follow clean code principles
         - Implement proper error handling
         - Include comprehensive logging
         - Add type hints and documentation
      
      2. Architecture
         - Follow SOLID principles
         - Ensure modularity
         - Consider extensibility
      
      3. Performance
         - Optimize critical paths
         - Consider resource usage
         - Handle edge cases
      
      4. Testing & Validation
         - Include unit test considerations
         - Add validation checks
         - Document test scenarios
    variables:
      - implementation_task
      - implementation_context
      - style_guide
    description: "Enhanced code generation prompt focusing on production-ready, maintainable implementations."
    category: "state"
    version: "3.1"

  code_review:
    content: |
      Perform comprehensive code review:
      
      CODE: {generated_code}
      REQUIREMENTS: {requirements}
      
      Review Criteria:
      1. Code Quality
         - Style guide compliance
         - Clean code principles
         - Documentation completeness
         - Type safety
      
      2. Implementation
         - Algorithm efficiency
         - Resource management
         - Error handling
         - Edge case coverage
      
      3. Security
         - Input validation
         - Data sanitization
         - Security best practices
      
      4. Maintainability
         - Code organization
         - Naming conventions
         - Comment clarity
         - Test coverage
      
      Provide:
      REVIEW:
        Issues: [List of issues found]
        Recommendations: [Improvement suggestions]
        Security: [Security considerations]
        Next Steps: [Required changes]
    variables:
      - generated_code
      - requirements
    description: "Detailed code review prompt covering quality, security, and maintainability aspects."
    category: "state"
    version: "3.1"

testing_state_prompts:
  test_generation:
    content: |
      Generate comprehensive test suite for:
      
      IMPLEMENTATION: {implementation}
      REQUIREMENTS: {requirements}
      
      Test Coverage:
      1. Unit Tests
         - Core functionality
         - Edge cases
         - Error conditions
         - Boundary testing
      
      2. Integration Tests
         - Component interactions
         - API contracts
         - Data flow
      
      3. Performance Tests
         - Load conditions
         - Resource usage
         - Timing constraints
      
      4. Security Tests
         - Input validation
         - Authentication
         - Authorization
      
      Include for each test:
      - Preconditions
      - Test steps
      - Expected results
      - Cleanup requirements
    variables:
      - implementation
      - requirements
    description: "Comprehensive test generation prompt covering unit, integration, performance, and security testing."
    category: "state"
    version: "3.1"

  test_analysis:
    content: |
      Analyze test execution results:
      
      RESULTS: {test_results}
      ERRORS: {error_log}
      
      Provide detailed analysis:
      1. Failure Analysis
         - Root cause identification
         - Impact assessment
         - Pattern recognition
         - Environment factors
      
      2. Resolution Strategy
         - Required code changes
         - Configuration updates
         - Environment fixes
         - Documentation updates
      
      3. Prevention Measures
         - Additional test coverage
         - Monitoring requirements
         - Process improvements
         - Documentation enhancements
      
      REPORT:
        Issues: [Detailed issue breakdown]
        Fixes: [Required fixes prioritized]
        Prevention: [Future prevention steps]
        Timeline: [Estimated resolution timeline]
    variables:
      - test_results
      - error_log
    description: "Detailed test analysis prompt focusing on root cause analysis and prevention strategies."
    category: "state"
    version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\test_prompts.yaml
## File: ..\..\CodeMate\config\prompts\test_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\test_prompts.yaml
# config/prompts/test_prompts.yaml
# Advanced Testing Framework - Version 3.1
# Comprehensive templates for test generation, coverage analysis, and failure investigation

base_test_generation:
  content: |
    Generate comprehensive test suite:

    CONTEXT:
      Implementation: {implementation_code}
      Requirements: {test_requirements}

    Test Framework Design:
    1. Functional Testing
       - Core Features
         * Main workflows
         * Business logic
         * Data processing
         * API contracts

       - Validation Testing
         * Input validation
         * Output verification
         * State management
         * Data integrity

    2. Edge Case Testing
       - Boundary Conditions
         * Min/max values
         * Empty/null cases
         * Large datasets
         * Resource limits

       - Error Scenarios
         * Invalid inputs
         * Resource failures
         * Timeout conditions
         * Network issues

    3. Integration Testing
       - Component Interaction
         * Service coupling
         * Data flow
         * Event handling
         * State transitions

       - System Integration
         * External services
         * Database operations
         * File system interaction
         * Network communication

    4. Performance Testing
       - Resource Usage
         * Memory consumption
         * CPU utilization
         * I/O operations
         * Network bandwidth

       - Timing Analysis
         * Response times
         * Processing delays
         * Concurrent operations
         * Race conditions

    Provide test specifications:
    TEST_SUITE:
      Functional:
        Cases: [Test cases]
        Data: [Test data]
        Setup: [Setup requirements]
        Cleanup: [Cleanup procedures]

      Edge:
        Cases: [Edge test cases]
        Conditions: [Test conditions]
        Validation: [Validation points]

      Integration:
        Tests: [Integration tests]
        Dependencies: [Required components]
        Mocks: [Mock requirements]

      Performance:
        Tests: [Performance tests]
        Metrics: [Key metrics]
        Thresholds: [Acceptance criteria]
  variables:
    - implementation_code
    - test_requirements
  description: "Enhanced test generation prompt with comprehensive testing strategies and detailed specifications."
  category: "testing"
  version: "3.1"

coverage_gap_tests:
  content: |
    Address test coverage gaps:

    CONTEXT:
      Gaps: {coverage_gaps}
      Existing: {existing_tests}

    Gap Analysis Framework:
    1. Coverage Assessment
       - Code Coverage
         * Uncovered paths
         * Branch coverage
         * Statement coverage
         * Function coverage

       - Scenario Coverage
         * Missing workflows
         * Edge cases
         * Error paths
         * Integration points

    2. Test Strategy
       - Gap Prioritization
         * Critical paths
         * Risk assessment
         * Complexity analysis
         * Impact evaluation

       - Test Design
         * Test scenarios
         * Data requirements
         * Environment needs
         * Validation criteria

    3. Implementation Plan
       - Test Development
         * Test structure
         * Dependencies
         * Setup requirements
         * Cleanup needs

       - Integration Strategy
         * Existing suite integration
         * Resource management
         * Execution order
         * Performance impact

    Provide gap coverage plan:
    ANALYSIS:
      Gaps: [Detailed gap analysis]
      Priority: [Gap priorities]
      Impact: [Coverage impact]

    IMPLEMENTATION:
      Tests: [New test cases]
      Data: [Test data]
      Setup: [Setup needs]
      Integration: [Integration plan]
  variables:
    - coverage_gaps
    - existing_tests
  description: "Comprehensive coverage gap analysis prompt with strategic test planning."
  category: "testing"
  version: "3.1"

test_failure_analysis:
  content: |
    Analyze test failures and determine resolution:

    CONTEXT:
      Failed Tests: {failed_tests}
      Errors: {error_logs}
      Implementation: {implementation}

    Analysis Framework:
    1. Failure Classification
       - Error Patterns
         * Failure types
         * Error messages
         * Stack traces
         * System state

       - Impact Assessment
         * Affected components
         * Data integrity
         * System stability
         * User impact

    2. Root Cause Analysis
       - Technical Investigation
         * Code issues
         * Configuration problems
         * Environment factors
         * Resource constraints

       - Pattern Recognition
         * Common factors
         * Related issues
         * Historical context
         * Timing patterns

    3. Resolution Planning
       - Fix Strategy
         * Code changes
         * Test updates
         * Configuration updates
         * Environment fixes

       - Validation Approach
         * Test modifications
         * Coverage expansion
         * Regression testing
         * Performance validation

    Provide failure analysis:
    ANALYSIS:
      Failures: [Failure breakdown]
      Causes: [Root causes]
      Patterns: [Error patterns]
      Impact: [Failure impact]

    RESOLUTION:
      Fixes: [Required fixes]
      Tests: [Test updates]
      Validation: [Validation plan]
      Prevention: [Prevention measures]
  variables:
    - failed_tests
    - error_logs
    - implementation
  description: "Enhanced test failure analysis prompt with systematic investigation and resolution planning."
  category: "testing"
  version: "3.1"
```

---

# ..\..\CodeMate\config\prompts\workflow_prompts.yaml
## File: ..\..\CodeMate\config\prompts\workflow_prompts.yaml

```yaml
# ..\..\CodeMate\config\prompts\workflow_prompts.yaml
# config/prompts/workflow_prompts.yaml
# Advanced Workflow Management Framework - Version 3.1
# Sophisticated templates for workflow planning, execution, and validation

workflow_planning:
  content: |
    Develop comprehensive workflow strategy:

    CONTEXT:
      Task: {task}
      Environment: {context}

    Planning Framework:
    1. Workflow Architecture
       - Core Components
         * Primary objectives
         * Required resources
         * System dependencies
         * Integration points

       - Process Flow
         * Sequential steps
         * Parallel operations
         * Decision points
         * Error handlers

    2. Implementation Strategy
       - Execution Plan
         * Preparation tasks
         * Core operations
         * Validation checks
         * Cleanup activities

       - Resource Management
         * Time estimates
         * System resources
         * Dependencies
         * Constraints

    3. Risk Management
       - Risk Assessment
         * Technical risks
         * Resource risks
         * Timeline risks
         * Integration risks

       - Mitigation Strategy
         * Prevention measures
         * Recovery plans
         * Alternate paths
         * Rollback procedures

    4. Success Criteria
       - Validation Points
         * Step completion
         * Quality checks
         * Performance metrics
         * Integration tests

       - Acceptance Criteria
         * Functional requirements
         * Performance requirements
         * Quality standards
         * Documentation needs

    Provide workflow plan:
    PLAN:
      Steps: [Detailed workflow steps]
      Dependencies: [Step dependencies]
      Timeline: [Execution timeline]
      Resources: [Required resources]

    VALIDATION:
      Checkpoints: [Validation points]
      Criteria: [Success criteria]
      Metrics: [Key metrics]

    RISK:
      Analysis: [Risk assessment]
      Mitigation: [Mitigation plans]
      Recovery: [Recovery procedures]
  variables:
    - task
    - context
  description: "Enhanced workflow planning prompt with comprehensive strategy development and risk management."
  category: "workflow"
  version: "3.1"

workflow_validation:
  content: |
    Perform workflow validation analysis:

    CONTEXT:
      Workflow: {workflow}
      Results: {results}

    Validation Framework:
    1. Completion Verification
       - Step Analysis
         * Step completion status
         * Output validation
         * Error conditions
         * Performance metrics

       - Dependency Check
         * Component integration
         * Resource usage
         * System stability
         * Data consistency

    2. Quality Assessment
       - Requirements Check
         * Functional requirements
         * Performance criteria
         * Quality standards
         * Documentation status

       - Implementation Review
         * Code quality
         * Test coverage
         * Security compliance
         * Best practices

    3. Impact Analysis
       - System Effects
         * Resource utilization
         * Performance impact
         * Integration status
         * Stability assessment

       - User Impact
         * Functionality changes
         * Interface updates
         * Documentation needs
         * Training requirements

    4. Improvement Planning
       - Enhancement Areas
         * Process optimization
         * Resource efficiency
         * Error prevention
         * Documentation updates

       - Future Proofing
         * Scalability considerations
         * Maintenance needs
         * Update requirements
         * Training plans

    Provide validation report:
    VALIDATION:
      Status: [Completion status]
      Quality: [Quality assessment]
      Impact: [Impact analysis]
      Issues: [Identified issues]

    RECOMMENDATIONS:
      Improvements: [Enhancement suggestions]
      Actions: [Required actions]
      Updates: [Needed updates]
      Training: [Training needs]

    DOCUMENTATION:
      Changes: [Implementation changes]
      Lessons: [Lessons learned]
      Notes: [Important notes]
  variables:
    - workflow
    - results
  description: "Comprehensive workflow validation prompt ensuring thorough quality assessment and improvement planning."
  category: "workflow"
  version: "3.1"

workflow_monitoring:
  content: |
    Monitor workflow execution health:

    WORKFLOW:
      Status: {workflow_status}
      Metrics: {performance_metrics}
      Issues: {current_issues}

    Monitoring Framework:
    1. Performance Tracking
       - Resource usage
       - Response times
       - Error rates
       - System stability

    2. Health Assessment
       - Component status
       - Integration health
       - Data consistency
       - Service availability

    3. Issue Detection
       - Error patterns
       - Performance degradation
       - Resource constraints
       - Integration problems

    Provide monitoring report:
    STATUS:
      Health: [System health]
      Performance: [Performance status]
      Issues: [Active issues]
      Actions: [Required actions]
  variables:
    - workflow_status
    - performance_metrics
    - current_issues
  description: "New workflow monitoring prompt ensuring continuous health assessment during execution."
  category: "workflow"
  version: "3.1"
```

---

