# Project Details

# Table of Contents
- [..\CodeMate\tests\test_agent_end_to_end.py](#-CodeMate-tests-test_agent_end_to_endpy)
- [..\CodeMate\tests\test_backend_validator.py](#-CodeMate-tests-test_backend_validatorpy)
- [..\CodeMate\tests\test_cache_manager.py](#-CodeMate-tests-test_cache_managerpy)
- [..\CodeMate\tests\test_checklist_manager.py](#-CodeMate-tests-test_checklist_managerpy)
- [..\CodeMate\tests\test_config.py](#-CodeMate-tests-test_configpy)
- [..\CodeMate\tests\test_decision_system.py](#-CodeMate-tests-test_decision_systempy)
- [..\CodeMate\tests\test_error_handler.py](#-CodeMate-tests-test_error_handlerpy)
- [..\CodeMate\tests\test_event_bus.py](#-CodeMate-tests-test_event_buspy)
- [..\CodeMate\tests\test_file_watcher.py](#-CodeMate-tests-test_file_watcherpy)
- [..\CodeMate\tests\test_frontend_validator.py](#-CodeMate-tests-test_frontend_validatorpy)
- [..\CodeMate\tests\test_implementation.py](#-CodeMate-tests-test_implementationpy)
- [..\CodeMate\tests\test_implementation_validator.py](#-CodeMate-tests-test_implementation_validatorpy)
- [..\CodeMate\tests\test_llm_integration.py](#-CodeMate-tests-test_llm_integrationpy)
- [..\CodeMate\tests\test_log_analyzer.py](#-CodeMate-tests-test_log_analyzerpy)
- [..\CodeMate\tests\test_logger.py](#-CodeMate-tests-test_loggerpy)
- [..\CodeMate\tests\test_memory_manager.py](#-CodeMate-tests-test_memory_managerpy)
- [..\CodeMate\tests\test_navigation.py](#-CodeMate-tests-test_navigationpy)
- [..\CodeMate\tests\test_persistence_manager.py](#-CodeMate-tests-test_persistence_managerpy)
- [..\CodeMate\tests\test_process_manager.py](#-CodeMate-tests-test_process_managerpy)
- [..\CodeMate\tests\test_progress_tracker.py](#-CodeMate-tests-test_progress_trackerpy)
- [..\CodeMate\tests\test_prompt_templates.py](#-CodeMate-tests-test_prompt_templatespy)
- [..\CodeMate\tests\test_request_handler.py](#-CodeMate-tests-test_request_handlerpy)
- [..\CodeMate\tests\test_response_formatter.py](#-CodeMate-tests-test_response_formatterpy)
- [..\CodeMate\tests\test_state_manager.py](#-CodeMate-tests-test_state_managerpy)
- [..\CodeMate\tests\test_state_prompts.py](#-CodeMate-tests-test_state_promptspy)
- [..\CodeMate\tests\test_system_metrics.py](#-CodeMate-tests-test_system_metricspy)
- [..\CodeMate\tests\test_task_prioritizer.py](#-CodeMate-tests-test_task_prioritizerpy)
- [..\CodeMate\tests\test_terminal_manager.py](#-CodeMate-tests-test_terminal_managerpy)
- [..\CodeMate\tests\test_test_manager.py](#-CodeMate-tests-test_test_managerpy)
- [..\CodeMate\tests\test_test_validation.py](#-CodeMate-tests-test_test_validationpy)
- [..\CodeMate\tests\test_token_counter.py](#-CodeMate-tests-test_token_counterpy)
- [..\CodeMate\tests\test_validation_rules.py](#-CodeMate-tests-test_validation_rulespy)
- [..\CodeMate\tests\test_workflow_manager.py](#-CodeMate-tests-test_workflow_managerpy)
- [..\CodeMate\tests\test_workspace_scanner.py](#-CodeMate-tests-test_workspace_scannerpy)


# ..\..\CodeMate\tests\test_agent_end_to_end.py
## File: ..\..\CodeMate\tests\test_agent_end_to_end.py

```py
# ..\..\CodeMate\tests\test_agent_end_to_end.py
import unittest
import asyncio
from cmate.core.agent_coordinator import AgentCoordinator, AgentConfig
from cmate.core.state_manager import StateManager
from cmate.core.workflow_manager import WorkflowManager

class TestAgentEndToEnd(unittest.TestCase):
    def setUp(self):
        config = AgentConfig(
            workspace_path="./Workspace",
            max_files_per_scan=5,
            context_window_size=60000,
            auto_test=True,
            debug_mode=True
        )
        state_manager = StateManager()
        workflow_manager = WorkflowManager()
        self.agent = AgentCoordinator(config, state_manager, workflow_manager)
    
    def test_process_request_and_status(self):
        async def run_test():
            request = {
                "type": "analyze",
                "data": {"path": "./Workspace"}
            }
            result = await self.agent.process_request(request)
            self.assertIn("success", result)
            self.assertTrue(result["success"])
            status = await self.agent.check_status()
            self.assertIn("state", status)
            await self.agent.refresh_llm_context()
            code = await self.agent.generate_code("Generate a simple hello world function in Python")
            self.assertIsInstance(code, str)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_backend_validator.py
## File: ..\..\CodeMate\tests\test_backend_validator.py

```py
# ..\..\CodeMate\tests\test_backend_validator.py
import unittest
import asyncio
from cmate.validation.backend_validator import BackendValidator

class TestBackendValidator(unittest.TestCase):
    def setUp(self):
        self.validator = BackendValidator()
    
    def test_validate_python(self):
        code = "def foo(x):\n    return x * 2\n"
        async def run_test():
            result = await self.validator._validate_python(code, "dummy.py")
            self.assertTrue(result.valid)
            self.assertGreaterEqual(len(result.functions), 1)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_cache_manager.py
## File: ..\..\CodeMate\tests\test_cache_manager.py

```py
# ..\..\CodeMate\tests\test_cache_manager.py
import unittest
from cmate.storage.cache_manager import CacheManager

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.cache = CacheManager(cache_dir="temp/test_cache", default_ttl=2)
    
    def test_set_get_delete(self):
        self.cache.set("test_key", "test_data")
        data = self.cache.get("test_key")
        self.assertEqual(data, "test_data")
        deleted = self.cache.delete("test_key")
        self.assertTrue(deleted)
        data_after = self.cache.get("test_key")
        self.assertIsNone(data_after)
    
    def test_cleanup_expired(self):
        self.cache.set("temp_key", "temp", ttl=1)
        import time; time.sleep(2)
        removed = self.cache.cleanup_expired()
        self.assertGreaterEqual(removed, 1)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_checklist_manager.py
## File: ..\..\CodeMate\tests\test_checklist_manager.py

```py
# ..\..\CodeMate\tests\test_checklist_manager.py
import unittest
from cmate.task_management.checklist_manager import ChecklistManager, ChecklistItemStatus
from uuid import UUID

class TestChecklistManager(unittest.TestCase):
    def setUp(self):
        self.cm = ChecklistManager()
    
    def test_create_and_update_checklist(self):
        checklist_id = self.cm.create_checklist("Test Checklist", "Testing checklist", items=[
            {"title": "Task 1", "description": "First task", "priority": 1},
            {"title": "Task 2", "description": "Second task", "priority": 2}
        ])
        self.assertIsInstance(checklist_id, UUID)
        checklist = self.cm.get_checklist(checklist_id)
        first_item_id = checklist.items[0].id
        self.cm.update_item_status(checklist_id, first_item_id, ChecklistItemStatus.COMPLETED)
        item = self.cm.get_item(checklist_id, first_item_id)
        self.assertEqual(item.status, ChecklistItemStatus.COMPLETED)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_config.py
## File: ..\..\CodeMate\tests\test_config.py

```py
# ..\..\CodeMate\tests\test_config.py
import unittest
from cmate.utils.config import load_config

class TestConfig(unittest.TestCase):
    def test_load_default_config(self):
        config = load_config()
        self.assertIsInstance(config, dict)
        self.assertIn("general", config)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_decision_system.py
## File: ..\..\CodeMate\tests\test_decision_system.py

```py
# ..\..\CodeMate\tests\test_decision_system.py
import unittest
from cmate.llm.model_selector import model_selector
from cmate.core.state_manager import AgentState

class TestDecisionSystem(unittest.TestCase):
    def test_model_selection(self):
        model = model_selector.select_model(AgentState.CODING)
        self.assertIsInstance(model, str)
        model_default = model_selector.select_model(AgentState.IDLE)
        self.assertEqual(model_default, model_selector.default_model)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_error_handler.py
## File: ..\..\CodeMate\tests\test_error_handler.py

```py
# ..\..\CodeMate\tests\test_error_handler.py
import unittest
from cmate.utils.error_handler import ErrorHandler, ErrorSeverity

class TestErrorHandler(unittest.TestCase):
    def setUp(self):
        self.handler = ErrorHandler()
    
    def test_handle_value_error(self):
        try:
            raise ValueError("Test value error")
        except Exception as e:
            report = self.handler.handle_error(e, ErrorSeverity.ERROR, {"info": "test"})
            self.assertEqual(report.error_type, "ValueError")
            self.assertIn("Test value error", report.message)
            self.assertGreater(len(report.recovery_steps), 0)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_event_bus.py
## File: ..\..\CodeMate\tests\test_event_bus.py

```py
# ..\..\CodeMate\tests\test_event_bus.py
import unittest
import asyncio
from uuid import UUID
from cmate.core.event_bus import EventBus, EventPriority, EventCategory

class TestEventBus(unittest.TestCase):
    def setUp(self):
        self.event_bus = EventBus()
        # Create a new event loop and store it for use in tests.
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.event_bus.start())

    def tearDown(self):
        # Stop the event bus on the same loop and then close it.
        self.loop.run_until_complete(self.event_bus.stop())
        self.loop.close()

    def test_publish_and_subscribe(self):
        events = []

        def handler(event):
            events.append(event)

        subscription_id = self.event_bus.subscribe("test_event", handler, priority=EventPriority.HIGH)
        self.assertIsInstance(subscription_id, UUID)
        self.loop.run_until_complete(
            self.event_bus.publish("test_event", {"message": "Hello"},
                                     priority=EventPriority.HIGH,
                                     category=EventCategory.USER)
        )
        self.loop.run_until_complete(asyncio.sleep(0.2))
        self.assertGreater(len(events), 0)
        for event in events:
            self.assertEqual(event.get("priority"), EventPriority.HIGH)

    def test_unsubscribe(self):
        events = []

        def handler(event):
            events.append(event)

        subscription_id = self.event_bus.subscribe("test_event", handler)
        unsubscribed = self.event_bus.unsubscribe(subscription_id)
        self.assertTrue(unsubscribed)
        self.loop.run_until_complete(
            self.event_bus.publish("test_event", {"message": "After unsubscribe"})
        )
        self.loop.run_until_complete(asyncio.sleep(0.2))
        self.assertEqual(len(events), 0)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_file_watcher.py
## File: ..\..\CodeMate\tests\test_file_watcher.py

```py
# ..\..\CodeMate\tests\test_file_watcher.py
import unittest
import asyncio
from cmate.file_services.file_watcher import FileWatcher

class TestFileWatcher(unittest.TestCase):
    def setUp(self):
        self.workspace = "./Workspace"
        self.file_watcher = FileWatcher(self.workspace)
    
    def test_start_and_stop_watching(self):
        async def run_test():
            await self.file_watcher.start_watching()
            self.assertTrue(self.file_watcher._is_running)
            await asyncio.sleep(0.1)
            await self.file_watcher.stop_watching()
            self.assertFalse(self.file_watcher._is_running)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_frontend_validator.py
## File: ..\..\CodeMate\tests\test_frontend_validator.py

```py
# ..\..\CodeMate\tests\test_frontend_validator.py
import unittest
import asyncio
from cmate.validation.frontend_validator import FrontendValidator

class TestFrontendValidator(unittest.TestCase):
    def setUp(self):
        self.validator = FrontendValidator()
    
    def test_validate_pyside6(self):
        code = """
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
"""
        async def run_test():
            result = await self.validator._validate_pyside6(code, "dummy.py")
            self.assertTrue(result.valid)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_implementation.py
## File: ..\..\CodeMate\tests\test_implementation.py

```py
# ..\..\CodeMate\tests\test_implementation.py
import unittest

class TestImplementationWorkflow(unittest.TestCase):
    def test_dummy_implementation(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_implementation_validator.py
## File: ..\..\CodeMate\tests\test_implementation_validator.py

```py
# ..\..\CodeMate\tests\test_implementation_validator.py
import unittest
import asyncio
from cmate.validation.implementation_validator import ImplementationValidator

class TestImplementationValidator(unittest.TestCase):
    def setUp(self):
        self.validator = ImplementationValidator()
    
    def test_validate_python_code(self):
        code = "def add(a, b):\n    return a + b\n"
        async def run_test():
            result = await self.validator.validate_implementation(code, "python", {"required_functions": ["add"]})
            self.assertTrue(result.valid)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_llm_integration.py
## File: ..\..\CodeMate\tests\test_llm_integration.py

```py
# ..\..\CodeMate\tests\test_llm_integration.py
import unittest
import asyncio
from cmate.llm.llm_agent import llm_agent

class TestLLMIntegration(unittest.TestCase):
    def test_ask_method(self):
        async def run_test():
            response = await llm_agent.ask("Hello, world!")
            self.assertIn("content", response)
            self.assertIsInstance(response["content"], str)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_log_analyzer.py
## File: ..\..\CodeMate\tests\test_log_analyzer.py

```py
# ..\..\CodeMate\tests\test_log_analyzer.py
import unittest
import asyncio
import os
from datetime import datetime
from cmate.utils.log_analyzer import LogAnalyzer, LogAnalysis
from pathlib import Path

class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = LogAnalyzer()
        self.log_path = "temp/test_log.log"
        os.makedirs("temp", exist_ok=True)
        with open(self.log_path, "w") as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{now} [INFO] [test] This is an info message\n")
            f.write(f"{now} [ERROR] [test] This is an error message\n")
    
    def test_analyze_log(self):
        async def run_test():
            analysis: LogAnalysis = await self.analyzer.analyze_log(self.log_path)
            self.assertGreaterEqual(analysis.total_entries, 2)
            self.assertIn("INFO", analysis.entries_by_level)
            self.assertIn("ERROR", analysis.entries_by_level)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_logger.py
## File: ..\..\CodeMate\tests\test_logger.py

```py
# ..\..\CodeMate\tests\test_logger.py
import unittest
from cmate.utils.logger import setup_logging, get_logger
import os

class TestLogger(unittest.TestCase):
    def test_get_logger(self):
        logger = get_logger("test_logger")
        self.assertIsNotNone(logger)
        setup_logging("DEBUG", log_file="temp/test_logger.log")
        logger.debug("This is a test message")
        self.assertTrue(os.path.exists("temp/test_logger.log"))

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_memory_manager.py
## File: ..\..\CodeMate\tests\test_memory_manager.py

```py
# ..\..\CodeMate\tests\test_memory_manager.py
import unittest
from cmate.core.memory_manager import MemoryManager, MemoryType
from uuid import UUID

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory_manager = MemoryManager()
    
    def test_store_and_retrieve(self):
        key = "test_item"
        content = "This is a test."
        memory_id = self.memory_manager.store(content, MemoryType.SHORT_TERM)
        self.assertIsInstance(memory_id, UUID)
        retrieved = self.memory_manager.retrieve(memory_id)
        self.assertEqual(retrieved, content)
    
    def test_cleanup_expired(self):
        key = "cleanup_test"
        memory_id = self.memory_manager.store("temporary", MemoryType.SHORT_TERM, ttl=1)
        import time; time.sleep(2)
        count = self.memory_manager.cleanup()
        self.assertGreaterEqual(count, 1)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_navigation.py
## File: ..\..\CodeMate\tests\test_navigation.py

```py
# ..\..\CodeMate\tests\test_navigation.py
import unittest
import asyncio
from cmate.core.navigation_system import NavigationDecisionSystem, NavigationContext, NavigationResult
from cmate.core.state_manager import AgentState

class TestNavigationSystem(unittest.TestCase):
    def setUp(self):
        self.workspace_path = "./Workspace"
        self.nav_system = NavigationDecisionSystem(self.workspace_path)
    
    def test_prepare_and_execute_navigation(self):
        async def run_test():
            request = "Analyze file structure"
            workspace_data = {"dummy": "data"}
            context = await self.nav_system.prepare_decision_context(request, workspace_data, AgentState.IDLE)
            self.assertIsInstance(context, NavigationContext)
            result = await self.nav_system.execute_navigation("ANALYZE_FILE", context)
            self.assertIsInstance(result, NavigationResult)
            self.assertTrue(result.success)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_persistence_manager.py
## File: ..\..\CodeMate\tests\test_persistence_manager.py

```py
# ..\..\CodeMate\tests\test_persistence_manager.py
import unittest
import asyncio
from cmate.storage.persistence_manager import PersistenceManager
from pathlib import Path

class TestPersistenceManager(unittest.TestCase):
    def setUp(self):
        self.storage_path = "temp/test_storage"
        self.pm = PersistenceManager(storage_path=self.storage_path, compression=False)
    
    def test_store_and_retrieve(self):
        async def run_test():
            key = "persistent_test"
            data = {"value": 123}
            item_id = await self.pm.store(key, data)
            self.assertIsNotNone(item_id)
            retrieved = await self.pm.retrieve(key)
            self.assertEqual(retrieved, data)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_process_manager.py
## File: ..\..\CodeMate\tests\test_process_manager.py

```py
# ..\..\CodeMate\tests\test_process_manager.py
import unittest
import asyncio
from cmate.task_management.process_manager import ProcessManager

class TestProcessManager(unittest.TestCase):
    def setUp(self):
        self.pm = ProcessManager("./Workspace")
    
    def test_start_and_stop_process(self):
        async def run_test():
            # Use a string command; on Windows "echo Hello" runs via the shell.
            process_id = await self.pm.start_process("echo_test", "echo Hello")
            self.assertIsNotNone(process_id)
            await asyncio.sleep(1)
            active = self.pm.get_active_processes()
            self.assertIsInstance(active, list)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_progress_tracker.py
## File: ..\..\CodeMate\tests\test_progress_tracker.py

```py
# ..\..\CodeMate\tests\test_progress_tracker.py
import unittest
from cmate.task_management.progress_tracker import ProgressTracker
from uuid import uuid4
from datetime import datetime

class TestProgressTracker(unittest.TestCase):
    def setUp(self):
        self.pt = ProgressTracker("temp/test_progress")
    
    def test_record_snapshot(self):
        task_id = uuid4()
        # Create a dummy task object with required attributes.
        self.pt.tasks[task_id] = type("DummyTask", (), {
            "task_id": task_id,
            "name": "Test Task",
            "description": "Dummy task",
            "status": "in_progress",
            "progress": 50,
            "created_at": datetime.now(),
            "started_at": datetime.now(),
            "completed_at": None,
            "dependencies": [],
            "metadata": {}
        })
        self.pt.record_snapshot()
        self.assertGreater(len(self.pt.snapshots), 0)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_prompt_templates.py
## File: ..\..\CodeMate\tests\test_prompt_templates.py

```py
# ..\..\CodeMate\tests\test_prompt_templates.py
import unittest
from cmate.utils.prompt_templates import PromptTemplateManager

class TestPromptTemplates(unittest.TestCase):
    def setUp(self):
        self.ptm = PromptTemplateManager("config/prompts")
    
    def test_get_and_format_template(self):
        template = self.ptm.get_template("system_prompt")
        self.assertIsNotNone(template)
        formatted = self.ptm.format_prompt("system_prompt", {})
        self.assertIn("semi-autonomous", formatted)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_request_handler.py
## File: ..\..\CodeMate\tests\test_request_handler.py

```py
# ..\..\CodeMate\tests\test_request_handler.py
import unittest
import asyncio
from cmate.interfaces.request_handler import RequestHandler
from cmate.core.state_manager import StateManager, AgentState
from cmate.core.workflow_manager import WorkflowManager

class DummyWorkflowManager(WorkflowManager):
    async def create_workflow(self, workflow_type, name, description, context=None, parent_id=None):
        from uuid import uuid4
        class DummyWorkflow:
            def __init__(self):
                self.id = uuid4()
        return DummyWorkflow()
    async def execute_workflow(self, workflow_id):
        return {"success": True, "workflow_id": str(workflow_id)}

class TestRequestHandler(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
        self.workflow_manager = DummyWorkflowManager()
        self.request_handler = RequestHandler(self.state_manager, self.workflow_manager)
    
    def test_handle_request(self):
        async def run_test():
            request = {"type": "analyze", "data": {"path": "./Workspace"}}
            result = await self.request_handler.handle_request(request)
            self.assertTrue(result.success)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_response_formatter.py
## File: ..\..\CodeMate\tests\test_response_formatter.py

```py
# ..\..\CodeMate\tests\test_response_formatter.py
import unittest
from cmate.interfaces.response_formatter import ResponseFormatter, FormattingConfig, ResponseFormat

class TestResponseFormatter(unittest.TestCase):
    def setUp(self):
        config = FormattingConfig(format_type=ResponseFormat.JSON)
        self.formatter = ResponseFormatter(config)
    
    def test_format_json(self):
        content = {"key": "value"}
        formatted = self.formatter.format_response(content, ResponseFormat.JSON)
        self.assertTrue(formatted.startswith("{"))
    
    def test_format_text(self):
        content = "Hello world!"
        formatted = self.formatter.format_response(content, ResponseFormat.TEXT)
        self.assertIn("Hello world!", formatted)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_state_manager.py
## File: ..\..\CodeMate\tests\test_state_manager.py

```py
# ..\..\CodeMate\tests\test_state_manager.py
import unittest
from cmate.core.state_manager import StateManager, AgentState

class TestStateManager(unittest.TestCase):
    def setUp(self):
        self.state_manager = StateManager()
    
    def test_valid_transition(self):
        self.state_manager.update_state(AgentState.SCANNING_WORKSPACE, {"user_request": "scan"})
        self.assertEqual(self.state_manager.current_state, AgentState.SCANNING_WORKSPACE)
    
    def test_invalid_transition(self):
        with self.assertRaises(ValueError):
            self.state_manager.update_state(AgentState.CODING, {"user_request": "invalid transition"})

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_state_prompts.py
## File: ..\..\CodeMate\tests\test_state_prompts.py

```py
# ..\..\CodeMate\tests\test_state_prompts.py
import unittest
from cmate.core.prompt_manager import PromptManager

class TestStatePrompts(unittest.TestCase):
    def setUp(self):
        self.prompt_manager = PromptManager("config/prompts")
    
    def test_get_system_prompt(self):
        prompt = self.prompt_manager.get_prompt("system_prompt")
        self.assertIsInstance(prompt, str)
        self.assertIn("semi-autonomous", prompt)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_system_metrics.py
## File: ..\..\CodeMate\tests\test_system_metrics.py

```py
# ..\..\CodeMate\tests\test_system_metrics.py
import unittest
import asyncio
from cmate.utils.system_metrics import MetricsCollector

class TestSystemMetrics(unittest.TestCase):
    def setUp(self):
        self.collector = MetricsCollector("temp/metrics")
    
    def test_collect_metrics(self):
        metrics = self.collector.collect_metrics()
        self.assertIn("cpu_percent", metrics.__dict__)
    
    def test_async_collect_metrics(self):
        async def run_test():
            metrics = await self.collector.async_collect_metrics()
            self.assertIsNotNone(metrics.network_io)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_task_prioritizer.py
## File: ..\..\CodeMate\tests\test_task_prioritizer.py

```py
# ..\..\CodeMate\tests\test_task_prioritizer.py
import unittest
from cmate.task_management.task_prioritizer import TaskPrioritizer, PriorityLevel
from uuid import uuid4

class TestTaskPrioritizer(unittest.TestCase):
    def setUp(self):
        self.tp = TaskPrioritizer()
        self.task_id = uuid4()
        self.tp.set_task_priority(self.task_id, PriorityLevel.HIGH, {"age": 2})
    
    def test_get_priority(self):
        priority = self.tp.get_priority(self.task_id)
        self.assertIsNotNone(priority)
        self.assertGreater(priority.dynamic_priority, 0)
    
    def test_prioritized_tasks(self):
        another_id = uuid4()
        self.tp.set_task_priority(another_id, PriorityLevel.LOW, {"age": 1})
        prioritized = self.tp.get_prioritized_tasks()
        self.assertEqual(prioritized[0], self.task_id)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_terminal_manager.py
## File: ..\..\CodeMate\tests\test_terminal_manager.py

```py
# ..\..\CodeMate\tests\test_terminal_manager.py
import unittest
import asyncio
from cmate.interfaces.terminal_manager import TerminalManager

class TestTerminalManager(unittest.TestCase):
    def setUp(self):
        self.tm = TerminalManager("./Workspace")
    
    def test_execute_command(self):
        async def run_test():
            result = await self.tm.execute_command("echo Hello", capture_output=True)
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Hello", result.stdout)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_test_manager.py
## File: ..\..\CodeMate\tests\test_test_manager.py

```py
# ..\..\CodeMate\tests\test_test_manager.py
import unittest
import asyncio
from cmate.validation.test_manager import TestManager
import os

class TestTestManager(unittest.TestCase):
    def setUp(self):
        self.tm = TestManager("./Workspace")
        self.test_file = "temp/dummy_test.py"
        os.makedirs("temp", exist_ok=True)
        with open(self.test_file, "w") as f:
            f.write("def test_dummy():\n    assert True\n")
    
    def test_add_and_run_test(self):
        async def run_test():
            test_id = await self.tm.add_test_case("dummy_test", "A dummy test case", self.test_file, "unit")
            result = await self.tm.run_test(test_id)
            self.assertTrue(result.success)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_test_validation.py
## File: ..\..\CodeMate\tests\test_test_validation.py

```py
# ..\..\CodeMate\tests\test_test_validation.py
import unittest

class TestValidationPipeline(unittest.TestCase):
    def test_dummy_validation(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_token_counter.py
## File: ..\..\CodeMate\tests\test_token_counter.py

```py
# ..\..\CodeMate\tests\test_token_counter.py
import unittest
from cmate.utils.token_counter import TokenCounter

class TestTokenCounter(unittest.TestCase):
    def setUp(self):
        self.counter = TokenCounter("gpt-3.5-turbo")
    
    def test_count_tokens(self):
        text = "Hello, world! This is a test."
        result = self.counter.count_tokens(text)
        self.assertGreater(result.total_tokens, 0)
    
    def test_truncate_to_token_limit(self):
        text = "word " * 1000
        truncated = self.counter.truncate_to_token_limit(text, 100)
        result = self.counter.count_tokens(truncated)
        self.assertLessEqual(result.total_tokens, 100)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_validation_rules.py
## File: ..\..\CodeMate\tests\test_validation_rules.py

```py
# ..\..\CodeMate\tests\test_validation_rules.py
import unittest
from cmate.validation.validation_rules import ValidationRules, ValidationLevel

class TestValidationRules(unittest.TestCase):
    def setUp(self):
        self.vr = ValidationRules(ValidationLevel.NORMAL)
    
    def test_validate_path_rule(self):
        result = self.vr.validate("./Workspace/test.py", ["valid_path"])
        self.assertTrue(result.valid)
        result_fail = self.vr.validate("../outside/test.py", ["valid_path"])
        self.assertFalse(result_fail.valid)

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_workflow_manager.py
## File: ..\..\CodeMate\tests\test_workflow_manager.py

```py
# ..\..\CodeMate\tests\test_workflow_manager.py
import unittest
import asyncio
from uuid import UUID
from cmate.core.workflow_manager import WorkflowManager, WorkflowType

class TestWorkflowManager(unittest.TestCase):
    def setUp(self):
        self.workflow_manager = WorkflowManager()
    
    def test_create_and_execute_workflow(self):
        async def run_test():
            workflow = await self.workflow_manager.create_workflow(
                workflow_type=WorkflowType.NAVIGATION,
                name="Test Navigation Workflow",
                description="Testing workflow creation",
                context={"target_path": "./Workspace/dummy.txt"}
            )
            self.assertIsInstance(workflow.id, UUID)
            result = await self.workflow_manager.execute_workflow(workflow.id)
            self.assertIn("success", result)
            self.assertTrue(result.get("success"))
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

# ..\..\CodeMate\tests\test_workspace_scanner.py
## File: ..\..\CodeMate\tests\test_workspace_scanner.py

```py
# ..\..\CodeMate\tests\test_workspace_scanner.py
import unittest
import asyncio
from cmate.file_services.workspace_scanner import WorkspaceScanner, ScanResult

class TestWorkspaceScanner(unittest.TestCase):
    def setUp(self):
        self.scanner = WorkspaceScanner("./Workspace")
    
    def test_scan_workspace(self):
        async def run_test():
            result = await self.scanner.scan_workspace(max_depth=2)
            self.assertIsInstance(result, ScanResult)
            self.assertIsInstance(result.files, list)
        asyncio.run(run_test())

if __name__ == '__main__':
    unittest.main()

```

---

