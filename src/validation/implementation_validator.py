# src/validation/implementation_validator.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import ast
import re

@dataclass
class ValidationResult:
    """Result of code validation"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metadata: Dict[str, Any]

class ImplementationValidator:
    """Validates code implementation against requirements"""
    
    def __init__(self):
        self.requirements: Dict[str, Any] = {}
        self.validation_rules: Dict[str, callable] = {}
        self._initialize_validators()

    def _initialize_validators(self) -> None:
        """Initialize validation rules"""
        self.validation_rules.update({
            'python': self._validate_python_code,
            'javascript': self._validate_javascript_code,
            'html': self._validate_html_code,
            'css': self._validate_css_code
        })

    async def validate_implementation(self,
                                   code: str,
                                   language: str,
                                   requirements: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate code implementation"""
        if requirements:
            self.requirements.update(requirements)
            
        validator = self.validation_rules.get(language.lower())
        if not validator:
            return ValidationResult(
                valid=False,
                errors=[f"Unsupported language: {language}"],
                warnings=[],
                suggestions=[],
                metadata={}
            )
            
        return await validator(code)

    async def _validate_python_code(self, code: str) -> ValidationResult:
        """Validate Python code"""
        errors = []
        warnings = []
        suggestions = []
        
        try:
            # Parse code
            tree = ast.parse(code)
            
            # Check syntax
            compile(code, '<string>', 'exec')
            
            # Analyze structure
            for node in ast.walk(tree):
                # Check function definitions
                if isinstance(node, ast.FunctionDef):
                    if not node.returns:
                        warnings.append(f"Missing return type hint in function {node.name}")
                    if not ast.get_docstring(node):
                        warnings.append(f"Missing docstring in function {node.name}")
                
                # Check class definitions
                elif isinstance(node, ast.ClassDef):
                    if not ast.get_docstring(node):
                        warnings.append(f"Missing docstring in class {node.name}")
                
                # Check error handling
                elif isinstance(node, ast.Try):
                    if not any(isinstance(handler.type, ast.Name) for handler in node.handlers):
                        warnings.append("Generic exception handler found")
                
                # Check variable names
                elif isinstance(node, ast.Name):
                    if not re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                        warnings.append(f"Variable name {node.id} does not follow PEP 8")
            
            # Check requirements
            if 'required_functions' in self.requirements:
                found_functions = {n.name for n in ast.walk(tree) 
                                 if isinstance(n, ast.FunctionDef)}
                missing = set(self.requirements['required_functions']) - found_functions
                if missing:
                    errors.append(f"Missing required functions: {missing}")
            
        except SyntaxError as e:
            errors.append(f"Syntax error: {str(e)}")
        except Exception as e:
            errors.append(f"Validation error: {str(e)}")
            
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={
                "language": "python",
                "ast_nodes": len(list(ast.walk(tree))) if 'tree' in locals() else 0
            }
        )

    async def _validate_javascript_code(self, code: str) -> ValidationResult:
        """Validate JavaScript code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check basic syntax
        if code.count('{') != code.count('}'):
            errors.append("Mismatched curly braces")
            
        # Check for common issues
        if 'eval(' in code:
            warnings.append("Use of eval() detected")
        if 'with(' in code:
            warnings.append("Use of with statement detected")
            
        # Check semicolons
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if line and not line.endswith('{') and not line.endswith('}') and \
               not line.endswith(';') and not line.startswith('//'):
                warnings.append(f"Missing semicolon on line {i}")
                
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "javascript"}
        )

    async def _validate_html_code(self, code: str) -> ValidationResult:
        """Validate HTML code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for unclosed tags
        tag_stack = []
        for match in re.finditer(r'</?(\w+)[^>]*>', code):
            tag = match.group(1)
            if match.group(0).startswith('</'):
                if not tag_stack or tag_stack[-1] != tag:
                    errors.append(f"Mismatched closing tag: {tag}")
                else:
                    tag_stack.pop()
            elif not match.group(0).endswith('/>'):
                tag_stack.append(tag)
                
        if tag_stack:
            errors.append(f"Unclosed tags: {', '.join(tag_stack)}")
            
        # Check for accessibility
        for match in re.finditer(r'<img[^>]*>', code):
            if 'alt=' not in match.group(0):
                warnings.append("Image missing alt attribute")
                
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "html"}
        )

    async def _validate_css_code(self, code: str) -> ValidationResult:
        """Validate CSS code"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for unclosed blocks
        if code.count('{') != code.count('}'):
            errors.append("Mismatched curly braces")
            
        # Check for vendor prefixes
        vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
        for prefix in vendor_prefixes:
            if prefix in code:
                suggestions.append(f"Consider using autoprefixer for {prefix} properties")
                
        # Check for !important
        if '!important' in code:
            warnings.append("Use of !important found - consider refactoring")
            
        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metadata={"language": "css"}
        )
