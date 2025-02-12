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
