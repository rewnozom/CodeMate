# src/utils/error_handler.py
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import traceback
import sys
import logging
from enum import Enum

class ErrorSeverity(Enum):
    """Error severity levels"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ErrorContext:
    """Context information for error"""
    timestamp: datetime
    severity: ErrorSeverity
    location: str
    traceback: str
    metadata: Dict[str, Any]

@dataclass
class ErrorReport:
    """Detailed error report"""
    error_type: str
    message: str
    context: ErrorContext
    recovery_steps: List[str]
    recommendations: List[str]

class ErrorHandler:
    """Handles error tracking and recovery"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_history: List[ErrorReport] = []
        self.recovery_strategies: Dict[str, callable] = {}
        self._initialize_strategies()

    def _initialize_strategies(self) -> None:
        """Initialize error recovery strategies"""
        self.recovery_strategies.update({
            'FileNotFoundError': self._handle_missing_file,
            'PermissionError': self._handle_permission_error,
            'TimeoutError': self._handle_timeout,
            'ValueError': self._handle_value_error,
            'KeyError': self._handle_key_error
        })

    def handle_error(self,
                    error: Exception,
                    severity: ErrorSeverity,
                    metadata: Optional[Dict[str, Any]] = None) -> ErrorReport:
        """Handle and report error"""
        # Create error context
        context = ErrorContext(
            timestamp=datetime.now(),
            severity=severity,
            location=f"{error.__class__.__module__}.{error.__class__.__name__}",
            traceback=''.join(traceback.format_tb(error.__traceback__)),
            metadata=metadata or {}
        )
        
        # Create error report
        report = ErrorReport(
            error_type=error.__class__.__name__,
            message=str(error),
            context=context,
            recovery_steps=self._get_recovery_steps(error),
            recommendations=self._get_recommendations(error)
        )
        
        # Log error
        self._log_error(report)
        
        # Store in history
        self.error_history.append(report)
        
        # Attempt recovery
        self._attempt_recovery(error, context)
        
        return report

    def _log_error(self, report: ErrorReport) -> None:
        """Log error report"""
        self.logger.error(
            f"{report.error_type}: {report.message}\n"
            f"Location: {report.context.location}\n"
            f"Severity: {report.context.severity.value}\n"
            f"Traceback:\n{report.context.traceback}"
        )

    def _get_recovery_steps(self, error: Exception) -> List[str]:
        """Get recovery steps for error"""
        error_type = error.__class__.__name__
        
        if error_type in self.recovery_strategies:
            return self.recovery_strategies[error_type](error)
            
        return ["Document the error context",
                "Review recent changes",
                "Check system logs",
                "Contact support if persists"]

    def _get_recommendations(self, error: Exception) -> List[str]:
        """Get recommendations for preventing error"""
        recommendations = []
        
        if isinstance(error, FileNotFoundError):
            recommendations.extend([
                "Verify file paths before operations",
                "Implement file existence checks",
                "Add error handling for file operations"
            ])
        elif isinstance(error, PermissionError):
            recommendations.extend([
                "Check file/directory permissions",
                "Verify user access rights",
                "Implement proper permission handling"
            ])
        elif isinstance(error, TimeoutError):
            recommendations.extend([
                "Review timeout settings",
                "Implement retry mechanisms",
                "Add timeout handling"
            ])
            
        return recommendations

    def _attempt_recovery(self, error: Exception, context: ErrorContext) -> None:
        """Attempt to recover from error"""
        error_type = error.__class__.__name__
        
        if error_type in self.recovery_strategies:
            try:
                self.recovery_strategies[error_type](error)
            except Exception as e:
                self.logger.error(f"Recovery failed: {str(e)}")

    def _handle_missing_file(self, error: FileNotFoundError) -> List[str]:
        """Handle missing file error"""
        return [
            "Check if file exists at specified path",
            "Verify file name and extension",
            "Create file if missing and required",
            "Update file path if incorrect"
        ]

    def _handle_permission_error(self, error: PermissionError) -> List[str]:
        """Handle permission error"""
        return [
            "Check file/directory permissions",
            "Verify user access rights",
            "Request elevated permissions if needed",
            "Update file/directory ownership"
        ]

    def _handle_timeout(self, error: TimeoutError) -> List[str]:
        """Handle timeout error"""
        return [
            "Increase timeout duration",
            "Check system resources",
            "Implement retry mechanism",
            "Optimize operation if possible"
        ]

    def _handle_value_error(self, error: ValueError) -> List[str]:
        """Handle value error"""
        return [
            "Validate input values",
            "Check data types and formats",
            "Add input validation",
            "Provide valid value examples"
        ]

    def _handle_key_error(self, error: KeyError) -> List[str]:
        """Handle key error"""
        return [
            "Verify dictionary keys exist",
            "Check key case sensitivity",
            "Add key existence check",
            "Provide fallback values"
        ]

    def get_error_history(self, 
                         severity: Optional[ErrorSeverity] = None,
                         limit: Optional[int] = None) -> List[ErrorReport]:
        """Get error history"""
        history = self.error_history
        
        if severity:
            history = [
                report for report in history
                if report.context.severity == severity
            ]
            
        if limit:
            history = history[-limit:]
            
        return history

    def clear_history(self) -> None:
        """Clear error history"""
        self.error_history.clear()

