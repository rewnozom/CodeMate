# cmate/validation/validation_rules.py
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime
import re
from enum import Enum

# Updated enum values: use numeric values for ordering.
class ValidationLevel(Enum):
    STRICT = 1
    NORMAL = 2
    LENIENT = 3

@dataclass
class ValidationRule:
    """Individual validation rule"""
    name: str
    description: str
    validator: Callable
    level: ValidationLevel
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Result of validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    metadata: Dict[str, Any]

class ValidationRules:
    """Manages and applies validation rules"""
    
    def __init__(self, level: ValidationLevel = ValidationLevel.NORMAL):
        self.level = level
        self.rules: Dict[str, ValidationRule] = {}
        self._initialize_rules()

    def _initialize_rules(self) -> None:
        """Initialize default validation rules"""
        # Setup basic rules
        self.add_rule(
            "valid_path",
            "Validate file path format",
            self._validate_path,
            ValidationLevel.STRICT
        )
        
        self.add_rule(
            "code_syntax",
            "Validate Python code syntax",
            self._validate_code_syntax,
            ValidationLevel.STRICT
        )
        
        self.add_rule(
            "function_name",
            "Validate function naming convention",
            self._validate_function_name,
            ValidationLevel.NORMAL
        )
        
        self.add_rule(
            "variable_name",
            "Validate variable naming convention",
            self._validate_variable_name,
            ValidationLevel.NORMAL
        )

    def add_rule(self,
                name: str,
                description: str,
                validator: Callable,
                level: ValidationLevel) -> None:
        """Add new validation rule"""
        self.rules[name] = ValidationRule(
            name=name,
            description=description,
            validator=validator,
            level=level
        )

    def validate(self, content: Any, rule_names: Optional[List[str]] = None) -> ValidationResult:
        """Validate content against rules"""
        errors = []
        warnings = []
        metadata = {}
        
        rules_to_apply = []
        if rule_names:
            rules_to_apply = [r for n, r in self.rules.items() if n in rule_names and r.enabled]
        else:
            rules_to_apply = [r for r in self.rules.values() if r.enabled]
        
        for rule in rules_to_apply:
            try:
                if rule.level.value <= self.level.value:
                    result = rule.validator(content)
                    if isinstance(result, dict):
                        if not result.get("valid", False):
                            if rule.level == ValidationLevel.STRICT:
                                errors.extend(result.get("errors", []))
                            else:
                                warnings.extend(result.get("errors", []))
                        metadata[rule.name] = result.get("metadata", {})
            except Exception as e:
                errors.append(f"Rule '{rule.name}' failed: {str(e)}")
        
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            metadata=metadata
        )

    def _validate_path(self, path: str) -> Dict[str, Any]:
        """Validate file path"""
        if not isinstance(path, str):
            return {"valid": False, "errors": ["Path must be a string"]}
            
        if ".." in path:
            return {"valid": False, "errors": ["Path cannot contain parent directory references"]}
            
        if not path.startswith("./Workspace"):
            return {"valid": False, "errors": ["Path must be within Workspace directory"]}
            
        return {"valid": True, "metadata": {"path": path}}

    def _validate_code_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Python code syntax"""
        try:
            compile(code, "<string>", "exec")
            return {"valid": True}
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"Syntax error: {str(e)}"],
                "metadata": {"line": e.lineno, "offset": e.offset}
            }

    def _validate_function_name(self, name: str) -> Dict[str, Any]:
        """Validate function naming convention"""
        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
            return {
                "valid": False,
                "errors": ["Function name must be lowercase with underscores"]
            }
        return {"valid": True}

    def _validate_variable_name(self, name: str) -> Dict[str, Any]:
        """Validate variable naming convention"""
        if not re.match(r'^[a-z_][a-z0-9_]*$', name):
            return {
                "valid": False,
                "errors": ["Variable name must be lowercase with underscores"]
            }
        return {"valid": True}
