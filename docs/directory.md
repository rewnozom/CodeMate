
### Huvudmappar och deras syfte:

1. `cmate/`: Källkoden för alla komponenter
   - Organiserad i logiska moduler
   - Varje modul har sitt eget `__init__.py`

2. `tests/`: All testkod
   - Separata mappar för unit och integration tester
   - Fixtures för testdata

3. `workspace/`: Den begränsade arbetsmiljön för agenten
   - Innehåller modul filer som agenten ska arbeta med

4. `logs/`: Loggfiler
   - Automatiskt HTML Loggning

5. `temp/`: Temporär datalagring
   - Workflow states
   - Testresultat
   - m.m..

6. `config/`: Konfigurationsfiler
   - Miljöspecifika konfigurationer
   - YAML-format prompt templates inuti: `config/prompts/` för läsbarhet

7. `docs/`: Projektdokumentation
   - Arkitekturbeskrivningar
   - Workflow-dokumentation

8. `scripts`: Användbara skript "underlättar processen när man utvecklar"
   - Installation
   - Testning
   - Deployment

9. `requirements/`: Beroenden
   - Uppdelade för olika miljöer
   - Separata filer för utveckling och produktion

