
### Huvudmappar och deras syfte:

1. `src/`: Källkoden för alla komponenter
   - Organiserad i logiska moduler
   - Varje modul har sitt eget `__init__.py`

2. `tests/`: All testkod
   - Separata mappar för unit och integration tester
   - Fixtures för testdata

3. `workspace/`: Den begränsade arbetsmiljön för agenten
   - Innehåller frontend och backend kod som agenten ska arbeta med

4. `logs/`: Loggfiler
   - Separata mappar för olika typer av loggar

5. `temp/`: Temporär datalagring
   - Workflow states
   - Testresultat

6. `config/`: Konfigurationsfiler
   - Miljöspecifika konfigurationer
   - YAML-format för läsbarhet

7. `docs/`: Projektdokumentation
   - API-dokumentation
   - Arkitekturbeskrivningar
   - Workflow-dokumentation

8. `scripts/`: Användbara skript
   - Installation
   - Testning
   - Deployment

9. `requirements/`: Beroenden
   - Uppdelade för olika miljöer
   - Separata filer för utveckling och produktion



```


CodeMate/
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent_coordinator.py
│   │   ├── state_manager.py
│   │   ├── workflow_manager.py
│   │   └── event_bus.py
│   │
│   ├── file_services/
│   │   ├── __init__.py
│   │   ├── file_system_navigator.py
│   │   ├── file_analyzer.py
│   │   └── workspace_scanner.py
│   │
│   ├── task_management/
│   │   ├── __init__.py
│   │   ├── task_planner.py
│   │   ├── checklist_manager.py
│   │   └── progress_tracker.py
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── test_manager.py
│   │   ├── implementation_validator.py
│   │   ├── frontend_validator.py
│   │   └── backend_validator.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── temporary_storage.py
│   │   └── persistence_manager.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   └── config.py
│   │
│   └── interfaces/
│       ├── __init__.py
│       ├── request_handler.py
│       └── response_formatter.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_file_system.py
│   │   ├── test_task_management.py
│   │   └── test_validation.py
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_workflows.py
│   │   └── test_end_to_end.py
│   │
│   └── fixtures/
│       ├── __init__.py
│       ├── sample_workspace/
│       └── mock_data/
│
├── workspace/
│   ├── frontend/
│   │   └── # PySide6 files here
│   │
│   └── backend/
│       └── # Python backend files here
│
├── logs/
│   ├── workflow_logs/
│   └── error_logs/
│
├── temp/
│   ├── workflow_states/
│   └── test_results/
│
├── config/
│   ├── default.yaml
│   ├── development.yaml
│   └── production.yaml
│
├── docs/
│   ├── api/
│   ├── architecture/
│   └── workflows/
│
├── scripts/
│   ├── setup.py
│   ├── run_tests.sh
│   └── deploy.sh
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── .gitignore
├── README.md
├── setup.py
└── requirements.txt

```

Här är en välorganiserad katalogstruktur för projektet:

```
CodeMate/
│
├── src/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent_coordinator.py
│   │   ├── state_manager.py
│   │   ├── workflow_manager.py
│   │   └── event_bus.py
│   │
│   ├── file_services/
│   │   ├── __init__.py
│   │   ├── file_system_navigator.py
│   │   ├── file_analyzer.py
│   │   └── workspace_scanner.py
│   │
│   ├── task_management/
│   │   ├── __init__.py
│   │   ├── task_planner.py
│   │   ├── checklist_manager.py
│   │   └── progress_tracker.py
│   │
│   ├── validation/
│   │   ├── __init__.py
│   │   ├── test_manager.py
│   │   ├── implementation_validator.py
│   │   ├── frontend_validator.py
│   │   └── backend_validator.py
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── temporary_storage.py
│   │   └── persistence_manager.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   └── config.py
│   │
│   └── interfaces/
│       ├── __init__.py
│       ├── request_handler.py
│       └── response_formatter.py
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_file_system.py
│   │   ├── test_task_management.py
│   │   └── test_validation.py
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_workflows.py
│   │   └── test_end_to_end.py
│   │
│   └── fixtures/
│       ├── __init__.py
│       ├── sample_workspace/
│       └── mock_data/
│
├── workspace/
│   ├── frontend/
│   │   └── # PySide6 files here
│   │
│   └── backend/
│       └── # Python backend files here
│
├── logs/
│   ├── workflow_logs/
│   └── error_logs/
│
├── temp/
│   ├── workflow_states/
│   └── test_results/
│
├── config/
│   ├── default.yaml
│   ├── development.yaml
│   └── production.yaml
│
├── docs/
│   ├── api/
│   ├── architecture/
│   └── workflows/
│
├── scripts/
│   ├── setup.py
│   ├── run_tests.sh
│   └── deploy.sh
│
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── .gitignore
├── README.md
├── setup.py
└── requirements.txt
```
