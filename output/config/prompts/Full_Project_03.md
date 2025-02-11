# Project Details

# Table of Contents
- [..\config\default.yaml](#-config-defaultyaml)
- [..\config\development.yaml](#-config-developmentyaml)
- [..\config\gunicorn.py](#-config-gunicornpy)
- [..\config\local.yaml](#-config-localyaml)
- [..\config\production.yaml](#-config-productionyaml)
- [..\config\__init__.py](#-config-__init__py)
- [..\config\prompts\base_prompts.yaml](#-config-prompts-base_promptsyaml)
- [..\config\prompts\error_prompts.yaml](#-config-prompts-error_promptsyaml)
- [..\config\prompts\workflow_prompts.yaml](#-config-prompts-workflow_promptsyaml)
- [..\config\prompts\__init__.py](#-config-prompts-__init__py)


# ..\..\config\default.yaml
## File: ..\..\config\default.yaml

```yaml
# ..\..\config\default.yaml
# config/default.yaml
# Default configuration for semi-autonomous agent

general:
  workspace_path: "./Workspace"
  max_files_per_scan: 10
  debug_mode: false
  log_level: "INFO"

llm:
  default_provider: "lm_studio"
  # The following LLM variables will be loaded from .env (e.g., CONTEXT_WINDOW, TEMPERATURE)
  # context_window, temperature, and max_tokens are controlled via .env.
  providers:
    lm_studio:
      base_url: "http://localhost:1234/v1"
      timeout: 300
    anthropic:
      model: "claude-3-sonnet-20240229"
      timeout: 300
    openai:
      model: "gpt-4"
      timeout: 300

agent:
  auto_test: true
  max_retries: 3
  timeout: 300
  memory:
    short_term_limit: 100
    working_memory_limit: 50
    long_term_limit: 1000

storage:
  format: "json"
  compression: false
  backup_enabled: true
  max_backups: 5

validation:
  strict_mode: false
  auto_fix: true
  test_timeout: 30

monitoring:
  enabled: true
  metrics_interval: 60
  log_metrics: true

```

---

# ..\..\config\development.yaml
## File: ..\..\config\development.yaml

```yaml
# ..\..\config\development.yaml
# config/development.yaml
inherit: default.yaml

general:
  debug_mode: true
  log_level: "DEBUG"

llm:
  # Optionally override non-sensitive LLM settings here
  # Note: Temperature and similar variables are loaded from .env
  prompt_optimizer:
    optimization_factor: 0.9

validation:
  strict_mode: true
  auto_fix: false

```

---

# ..\..\config\gunicorn.py
## File: ..\..\config\gunicorn.py

```py
# ..\..\config\gunicorn.py
# config/gunicorn.py
import multiprocessing

# Gunicorn config
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
keepalive = 120
timeout = 120
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 50
reload = False
accesslog = "-"
errorlog = "-"
loglevel = "info"

# nginx/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream agent_server {
        server agent:8000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://agent_server;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}

```

---

# ..\..\config\local.yaml
## File: ..\..\config\local.yaml

```yaml
# ..\..\config\local.yaml
# Local configuration
config/local.yaml
*.local.yaml

# Temporary files
*.log
*.tmp
*.temp

```

---

# ..\..\config\production.yaml
## File: ..\..\config\production.yaml

```yaml
# ..\..\config\production.yaml
# config/production.yaml
inherit: default.yaml

general:
  debug_mode: false
  log_level: "WARNING"

llm:
  # Temperature and similar sensitive variables remain under .env control.
  # Production-specific overrides can be added here if necessary.
  
validation:
  strict_mode: true
  auto_fix: false

storage:
  compression: true
  backup_enabled: true
  max_backups: 10

monitoring:
  metrics_interval: 30

```

---

# ..\..\config\__init__.py
## File: ..\..\config\__init__.py

```py
# ..\..\config\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\config\prompts\base_prompts.yaml
## File: ..\..\config\prompts\base_prompts.yaml

```yaml
# ..\..\config\prompts\base_prompts.yaml
# config/prompts/base_prompts.yaml
# Base prompts for the system with comprehensive guidance

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
      6. If an error occurs, perform a detailed analysis and propose concrete recovery actions.
    Always maintain awareness of the system’s state and context when deciding on your actions.
  variables: []
  description: "Base system prompt for agent initialization with detailed behavior guidelines."
  category: "system"
  version: "2.0"

analysis_prompt:
  content: |
    Analyze the following files thoroughly and provide a detailed report that includes:
      1. A high-level overview of the structure and architecture.
      2. Identification of key components and module dependencies.
      3. Potential issues, risks, or areas for improvement.
      4. Specific recommendations for immediate actions and long-term enhancements.
      5. Suggestions for further testing or analysis.
    Files to analyze: {files}
  variables: ["files"]
  description: "Detailed prompt for file analysis requiring a comprehensive report."
  category: "analysis"
  version: "2.0"

implementation_prompt:
  content: |
    Implement the requested changes by adhering to these guidelines:
      1. Analyze the existing codebase and preserve the current coding style.
      2. Add detailed documentation and inline comments to explain your changes.
      3. Develop comprehensive unit tests and, if necessary, integration tests to validate the modifications.
      4. Incorporate robust error handling to manage unexpected situations.
      5. Provide a detailed report outlining the changes, the rationale behind your decisions, and any assumptions made.
    Requested changes: {changes}
    Affected files: {files}
  variables: ["changes", "files"]
  description: "Prompt for implementation with detailed instructions and documentation requirements."
  category: "implementation"
  version: "2.0"

test_prompt:
  content: |
    Develop a comprehensive test suite to validate the implemented changes. Your test plan should include:
      1. Unit tests covering all new functionality and logical branches.
      2. Integration tests to ensure proper interaction between modules.
      3. Test cases for edge scenarios and error handling.
      4. A summary of test results and any observed anomalies.
    Implementation details: {implementation}
    Files to test: {files}
  variables: ["implementation", "files"]
  description: "Prompt for creating a full test suite with detailed validation criteria."
  category: "testing"
  version: "2.0"

```

---

# ..\..\config\prompts\error_prompts.yaml
## File: ..\..\config\prompts\error_prompts.yaml

```yaml
# ..\..\config\prompts\error_prompts.yaml
# config/prompts/error_prompts.yaml
# Error prompts for in-depth error analysis and recovery with detailed guidance

error_analysis:
  content: |
    Analyze the following error message and provide a comprehensive report that includes:
      1. A detailed root cause analysis identifying all relevant factors and contextual issues.
      2. Concrete recommendations for immediate corrective actions.
      3. Long-term prevention strategies to avoid similar errors in the future.
      4. Suggestions for additional tests or monitoring to ensure system stability.
    Error details: {error_message}
    Context: {context}
  variables: ["error_message", "context"]
  description: "Prompt for detailed error analysis, including both immediate fixes and long-term prevention."
  category: "error"
  version: "2.0"

error_recovery:
  content: |
    Propose a detailed recovery plan to restore the system to a functional state. Your plan should include:
      1. Immediate actions to stabilize the system.
      2. Steps to recover data or state if necessary.
      3. Validation measures to confirm the success of the recovery.
      4. Recommendations for follow-up tests and monitoring to prevent future issues.
    Error: {error}
    Current state: {state}
  variables: ["error", "state"]
  description: "Prompt for detailed error recovery steps, covering both immediate stabilization and long-term solutions."
  category: "error"
  version: "2.0"

```

---

# ..\..\config\prompts\workflow_prompts.yaml
## File: ..\..\config\prompts\workflow_prompts.yaml

```yaml
# ..\..\config\prompts\workflow_prompts.yaml
# config/prompts/workflow_prompts.yaml
# Workflow prompts providing step-by-step guidance for planning and validating workflows

workflow_planning:
  content: |
    Develop a comprehensive workflow plan that includes the following:
      1. A clear, step-by-step description of all actions to be taken.
      2. Identification of all dependencies between steps.
      3. Specific validation checkpoints to ensure each step is executed correctly.
      4. Clear objectives and measurable success criteria for the entire process.
      5. A detailed risk analysis along with recommended mitigation measures.
    Task description: {task}
    Context: {context}
  variables: ["task", "context"]
  description: "Prompt for creating a detailed workflow plan with clear steps, dependencies, and validation points."
  category: "workflow"
  version: "2.0"

workflow_validation:
  content: |
    Review the completed workflow and provide a detailed validation report that covers:
      1. Verification that all steps have been successfully completed.
      2. Confirmation that the results meet the specified requirements and objectives.
      3. Identification of any discrepancies or issues within the workflow.
      4. Recommendations for improvements and risk minimization.
      5. Suggestions for additional tests or inspections if needed.
    Workflow: {workflow}
    Results: {results}
  variables: ["workflow", "results"]
  description: "Prompt for validating a workflow with a focus on completeness, accuracy, and improvement recommendations."
  category: "workflow"
  version: "2.0"

```

---

# ..\..\config\prompts\__init__.py
## File: ..\..\config\prompts\__init__.py

```py
# ..\..\config\prompts\__init__.py
# Auto-generated __init__.py file

```

---

