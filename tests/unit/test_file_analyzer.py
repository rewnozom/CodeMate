# tests/unit/test_file_analyzer.py
import pytest
from pathlib import Path
from src.file_services.file_analyzer import FileAnalyzer

@pytest.fixture
def test_file(workspace_path):
    """Create test Python file"""
    file_path = workspace_path / "test.py"
    file_path.write_text("""
def test_function():
    '''Test docstring'''
    return True

class TestClass:
    def method(self):
        return None
    """)
    return file_path

async def test_analyze_python_file(test_file):
    """Test Python file analysis"""
    analyzer = FileAnalyzer()
    result = await analyzer.analyze_file(test_file)
    
    assert result is not None
    assert result.metadata.path == test_file
    assert len(result.code_analysis.functions) == 1
    assert len(result.code_analysis.classes) == 1