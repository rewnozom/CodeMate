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
