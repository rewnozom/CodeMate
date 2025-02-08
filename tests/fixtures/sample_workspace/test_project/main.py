# tests/fixtures/sample_workspace/test_project/main.py
def example_function():
    """Example function for testing"""
    return True

class ExampleClass:
    """Example class for testing"""
    def method(self):
        return None

# tests/fixtures/mock_data/test_requests.json
{
    "analyze": {
        "type": "analyze",
        "data": {
            "path": "test.py"
        }
    },
    "modify": {
        "type": "modify",
        "data": {
            "path": "test.py",
            "changes": "Rename function"
        }
    },
    "test": {
        "type": "test",
        "data": {
            "path": "test.py"
        }
    }
}