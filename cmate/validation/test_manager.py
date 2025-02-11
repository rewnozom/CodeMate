# src/validation/test_manager.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import subprocess
from pathlib import Path
import re
from uuid import UUID, uuid4

@dataclass
class TestCase:
    """Individual test case"""
    id: UUID
    name: str
    description: str
    test_file: Path
    test_type: str  # unit, integration, e2e
    dependencies: List[str]
    timeout: int = 30
    created_at: datetime = field(default_factory=datetime.now)
    last_run: Optional[datetime] = None
    last_result: Optional[bool] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestResult:
    """Result of test execution"""
    test_id: UUID
    success: bool
    output: str
    error: Optional[str]
    duration: float
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

class TestManager:
    """Manages test execution and results"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace = Path(workspace_path) if workspace_path else Path("./Workspace")
        self.test_cases: Dict[UUID, TestCase] = {}
        self.test_results: Dict[UUID, List[TestResult]] = {}
        self.active_tests: Dict[UUID, asyncio.Task] = {}
        
    async def add_test_case(self, 
                          name: str,
                          description: str,
                          test_file: Union[str, Path],
                          test_type: str,
                          dependencies: List[str] = None,
                          metadata: Optional[Dict[str, Any]] = None) -> UUID:
        """Add new test case"""
        test_id = uuid4()
        test_file = Path(test_file)
        
        if not test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        
        self.test_cases[test_id] = TestCase(
            id=test_id,
            name=name,
            description=description,
            test_file=test_file,
            test_type=test_type,
            dependencies=dependencies or [],
            metadata=metadata or {}
        )
        
        return test_id

    async def run_test(self, test_id: UUID) -> TestResult:
        """Run specific test case"""
        if test_id not in self.test_cases:
            raise ValueError(f"Test case not found: {test_id}")
            
        test_case = self.test_cases[test_id]
        start_time = datetime.now()
        
        try:
            # Check dependencies
            for dep in test_case.dependencies:
                if not await self._check_dependency(dep):
                    raise RuntimeError(f"Dependency not met: {dep}")
            
            # Run test
            process = await asyncio.create_subprocess_exec(
                "python", "-m", "pytest", str(test_case.test_file),
                "-v", "--capture=sys",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.workspace)
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=test_case.timeout
                )
                
                success = process.returncode == 0
                output = stdout.decode()
                error = stderr.decode() if stderr else None
                
            except asyncio.TimeoutError:
                success = False
                output = "Test timed out"
                error = f"Test exceeded timeout of {test_case.timeout} seconds"
                
            duration = (datetime.now() - start_time).total_seconds()
            
            # Create result
            result = TestResult(
                test_id=test_id,
                success=success,
                output=output,
                error=error,
                duration=duration,
                timestamp=datetime.now()
            )
            
            # Update test case
            test_case.last_run = datetime.now()
            test_case.last_result = success
            
            # Store result
            if test_id not in self.test_results:
                self.test_results[test_id] = []
            self.test_results[test_id].append(result)
            
            return result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            result = TestResult(
                test_id=test_id,
                success=False,
                output="",
                error=str(e),
                duration=duration,
                timestamp=datetime.now()
            )
            
            if test_id not in self.test_results:
                self.test_results[test_id] = []
            self.test_results[test_id].append(result)
            
            return result

    async def run_all_tests(self, test_type: Optional[str] = None) -> Dict[UUID, TestResult]:
        """Run all test cases of specified type"""
        results = {}
        test_cases = [
            tc for tc in self.test_cases.values()
            if not test_type or tc.test_type == test_type
        ]
        
        for test_case in test_cases:
            results[test_case.id] = await self.run_test(test_case.id)
            
        return results

    async def get_test_history(self, 
                            test_id: UUID,
                            limit: Optional[int] = None) -> List[TestResult]:
        """Get test execution history"""
        if test_id not in self.test_results:
            return []
            
        results = self.test_results[test_id]
        if limit:
            results = results[-limit:]
            
        return results

    async def analyze_results(self, results: Dict[UUID, TestResult]) -> Dict[str, Any]:
        """Analyze test results"""
        total_tests = len(results)
        passed_tests = len([r for r in results.values() if r.success])
        failed_tests = total_tests - passed_tests
        
        total_duration = sum(r.duration for r in results.values())
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_duration,
            "average_duration": avg_duration,
            "failed_test_ids": [
                test_id for test_id, result in results.items()
                if not result.success
            ]
        }

    async def _check_dependency(self, dependency: str) -> bool:
        """Check if dependency is satisfied"""
        if dependency.startswith("test:"):
            # Check test dependency
            test_name = dependency[5:]
            for test in self.test_cases.values():
                if test.name == test_name:
                    return test.last_result is True
        elif dependency.startswith("file:"):
            # Check file dependency
            file_path = self.workspace / dependency[5:]
            return file_path.exists()
        return False