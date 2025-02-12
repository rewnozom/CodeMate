# Project Details

# Table of Contents
- [..\CodeMate\config\__init__.py](#-CodeMate-config-__init__py)
- [..\CodeMate\config\default.yaml](#-CodeMate-config-defaultyaml)
- [..\CodeMate\config\development.yaml](#-CodeMate-config-developmentyaml)
- [..\CodeMate\config\gunicorn.py](#-CodeMate-config-gunicornpy)
- [..\CodeMate\config\local.yaml](#-CodeMate-config-localyaml)
- [..\CodeMate\config\production.yaml](#-CodeMate-config-productionyaml)


# ..\..\CodeMate\config\__init__.py
## File: ..\..\CodeMate\config\__init__.py

```py
# ..\..\CodeMate\config\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\config\default.yaml
## File: ..\..\CodeMate\config\default.yaml

```yaml
# ..\..\CodeMate\config\default.yaml
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

# ..\..\CodeMate\config\development.yaml
## File: ..\..\CodeMate\config\development.yaml

```yaml
# ..\..\CodeMate\config\development.yaml
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

# ..\..\CodeMate\config\gunicorn.py
## File: ..\..\CodeMate\config\gunicorn.py

```py
# ..\..\CodeMate\config\gunicorn.py
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

# ..\..\CodeMate\config\local.yaml
## File: ..\..\CodeMate\config\local.yaml

```yaml
# ..\..\CodeMate\config\local.yaml
# Local configuration
config/local.yaml
*.local.yaml

# Temporary files
*.log
*.tmp
*.temp

```

---

# ..\..\CodeMate\config\production.yaml
## File: ..\..\CodeMate\config\production.yaml

```yaml
# ..\..\CodeMate\config\production.yaml
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

