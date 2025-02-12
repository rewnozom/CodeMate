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
