

```

src/
├── core/
│   ├── __init__.py
│   ├── agent_coordinator.py
│   ├── state_manager.py
│   ├── workflow_manager.py
│   ├── event_bus.py
│   + ├── context_manager.py      # Hantering av context window och minne
│   + ├── memory_manager.py       # Specifik minneshantering för olika typer av minne
│   + └── prompt_manager.py       # Hantering av systemets prompts
│
├── file_services/
│   ├── __init__.py
│   ├── file_system_navigator.py
│   ├── file_analyzer.py
│   ├── workspace_scanner.py
│   + └── file_watcher.py         # Övervakar ändringar i workspace
│
├── task_management/
│   ├── __init__.py
│   ├── task_planner.py
│   ├── checklist_manager.py
│   ├── progress_tracker.py
│   + └── task_priority.py        # Hanterar prioritering av uppgifter
│
├── validation/
│   ├── __init__.py
│   ├── test_manager.py
│   ├── implementation_validator.py
│   ├── frontend_validator.py
│   ├── backend_validator.py
│   + └── validation_rules.py     # Definierar validerings-regler
│
├── storage/
│   ├── __init__.py
│   ├── temporary_storage.py
│   ├── persistence_manager.py
│   + └── cache_manager.py        # Hanterar caching av resultat/data
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── error_handler.py
│   ├── config.py
│   + ├── token_counter.py        # Räknar tokens för context window
│   + ├── prompt_templates.py     # Mallar för olika prompts
│   + └── system_metrics.py       # Övervakar systemresurser
│
├── interfaces/
│   ├── __init__.py
│   ├── request_handler.py
│   ├── response_formatter.py
│   + ├── cli_interface.py        # Kommandorads-gränssnitt
│   + └── terminal_manager.py     # Hanterar terminal-interaktioner
│
+ ├── llm/                        # Ny mapp för LLM-relaterade moduler
│   ├── __init__.py
│   ├── llm_models.py            # Din existerande LLM-hantering
│   ├── model_router.py          # Routing mellan olika LLM-modeller
│   └── response_parser.py       # Parsning av LLM-svar
│
+ └── prompts/                    # Ny mapp för prompt-hantering
    ├── __init__.py
    ├── base_prompts.py          # Grundläggande prompts
    ├── task_prompts.py          # Uppgiftsspecifika prompts
    └── system_prompts.py        # Systemprompts

```



```

config/
├── default.yaml
├── development.yaml
├── production.yaml
+ ├── prompts/                    # Konfiguration för olika prompts
│   ├── base_prompts.yaml
│   ├── task_prompts.yaml
│   └── system_prompts.yaml
+ └── llm/                        # LLM-specifik konfiguration
    ├── model_config.yaml
    └── routing_rules.yaml

```

Ah, du har rätt! Låt oss analysera och eventuellt uppdatera directory-strukturen först. Vi behöver se över vilka ytterligare filer som kan behövas baserat på systemets krav.

Här är några förslag på uppdateringar till strukturen (nya filer markerade med +):

```
src/
├── core/
│   ├── __init__.py
│   ├── agent_coordinator.py
│   ├── state_manager.py
│   ├── workflow_manager.py
│   ├── event_bus.py
│   + ├── context_manager.py      # Hantering av context window och minne
│   + ├── memory_manager.py       # Specifik minneshantering för olika typer av minne
│   + └── prompt_manager.py       # Hantering av systemets prompts
│
├── file_services/
│   ├── __init__.py
│   ├── file_system_navigator.py
│   ├── file_analyzer.py
│   ├── workspace_scanner.py
│   + └── file_watcher.py         # Övervakar ändringar i workspace
│
├── task_management/
│   ├── __init__.py
│   ├── task_planner.py
│   ├── checklist_manager.py
│   ├── progress_tracker.py
│   + └── task_priority.py        # Hanterar prioritering av uppgifter
│
├── validation/
│   ├── __init__.py
│   ├── test_manager.py
│   ├── implementation_validator.py
│   ├── frontend_validator.py
│   ├── backend_validator.py
│   + └── validation_rules.py     # Definierar validerings-regler
│
├── storage/
│   ├── __init__.py
│   ├── temporary_storage.py
│   ├── persistence_manager.py
│   + └── cache_manager.py        # Hanterar caching av resultat/data
│
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   ├── error_handler.py
│   ├── config.py
│   + ├── token_counter.py        # Räknar tokens för context window
│   + ├── prompt_templates.py     # Mallar för olika prompts
│   + └── system_metrics.py       # Övervakar systemresurser
│
├── interfaces/
│   ├── __init__.py
│   ├── request_handler.py
│   ├── response_formatter.py
│   + ├── cli_interface.py        # Kommandorads-gränssnitt
│   + └── terminal_manager.py     # Hanterar terminal-interaktioner
│
+ ├── llm/                        # Ny mapp för LLM-relaterade moduler
│   ├── __init__.py
│   ├── llm_models.py            # Din existerande LLM-hantering
│   ├── model_router.py          # Routing mellan olika LLM-modeller
│   └── response_parser.py       # Parsning av LLM-svar
│
+ └── prompts/                    # Ny mapp för prompt-hantering
    ├── __init__.py
    ├── base_prompts.py          # Grundläggande prompts
    ├── task_prompts.py          # Uppgiftsspecifika prompts
    └── system_prompts.py        # Systemprompts
```

Vi behöver också uppdatera config-strukturen:

```
config/
├── default.yaml
├── development.yaml
├── production.yaml
+ ├── prompts/                    # Konfiguration för olika prompts
│   ├── base_prompts.yaml
│   ├── task_prompts.yaml
│   └── system_prompts.yaml
+ └── llm/                        # LLM-specifik konfiguration
    ├── model_config.yaml
    └── routing_rules.yaml
```

Viktiga tillägg och motiveringar:

1. **context_manager.py** och **memory_manager.py**
   - Kritiska för hantering av context window
   - Separerar olika typer av minne (korttids/långtids)

2. **prompt_manager.py** och prompts/-mappen
   - Centraliserar prompt-hantering
   - Gör det lättare att underhålla och uppdatera prompts

3. **llm/-mappen**
   - Samlar all LLM-relaterad funktionalitet
   - Förenklar integration av olika modeller

4. **token_counter.py**
   - Viktigt för att hålla koll på context window size
   - Hjälper till med optimering av token-användning

5. **terminal_manager.py**
   - Hanterar terminal-interaktioner för agenten
   - Standardiserar hur agenten interagerar med systemet
