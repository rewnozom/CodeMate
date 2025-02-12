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
