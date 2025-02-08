from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum
import re

class ResponseFormat(Enum):
    """Response format types"""
    TEXT = "text"
    JSON = "json"
    HTML = "html"
    MARKDOWN = "markdown"
    ERROR = "error"
    CONSOLE = "console"

@dataclass
class FormattingConfig:
    """Configuration for response formatting"""
    format_type: ResponseFormat
    indent_size: int = 2
    max_line_length: int = 80
    include_metadata: bool = True
    highlight_syntax: bool = True
    wrap_text: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

class ResponseFormatter:
    """Formats response content for output"""
    
    def __init__(self, config: Optional[FormattingConfig] = None):
        self.config = config or FormattingConfig(ResponseFormat.TEXT)
        self.formatters = {
            ResponseFormat.TEXT: self._format_text,
            ResponseFormat.JSON: self._format_json,
            ResponseFormat.HTML: self._format_html,
            ResponseFormat.MARKDOWN: self._format_markdown,
            ResponseFormat.ERROR: self._format_error,
            ResponseFormat.CONSOLE: self._format_console
        }
    
    def format_response(self, content: Any, format_type: Optional[ResponseFormat] = None) -> str:
        """Format response content"""
        format_type = format_type or self.config.format_type
        formatter = self.formatters.get(format_type)
        if not formatter:
            raise ValueError(f"Unsupported format type: {format_type}")
        try:
            formatted = formatter(content)
            if self.config.include_metadata:
                formatted = self._add_metadata(formatted, format_type)
            return formatted
        except Exception as e:
            return self._format_error(e)

    def _format_text(self, content: Any) -> str:
        """Format text content"""
        if not isinstance(content, str):
            content = str(content)
        if self.config.wrap_text and self.config.max_line_length > 0:
            lines = []
            for line in content.split('\n'):
                if len(line) > self.config.max_line_length:
                    words = line.split()
                    current_line = []
                    current_length = 0
                    for word in words:
                        word_length = len(word)
                        # Add a space only if there is already content in current_line.
                        additional = 1 if current_line else 0
                        if current_length + word_length + additional <= self.config.max_line_length:
                            current_line.append(word)
                            current_length += word_length + additional
                        else:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                            current_length = word_length
                    if current_line:
                        lines.append(' '.join(current_line))
                else:
                    lines.append(line)
            content = '\n'.join(lines)
        return content

    def _format_json(self, content: Any) -> str:
        """Format JSON content"""
        try:
            if isinstance(content, str):
                content = json.loads(content)
            return json.dumps(content, indent=self.config.indent_size, ensure_ascii=False)
        except Exception as e:
            raise ValueError(f"Invalid JSON content: {str(e)}")

    def _format_html(self, content: Any) -> str:
        """Format HTML content"""
        if not isinstance(content, str):
            content = str(content)
        indent = 0
        lines = []
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('</'):
                indent = max(0, indent - 1)
            lines.append(' ' * (indent * self.config.indent_size) + stripped)
            if (stripped.endswith('>') and not stripped.startswith('</') and
                not stripped.endswith('/>') and not stripped.startswith('<!--')):
                indent += 1
        return '\n'.join(lines)

    def _format_markdown(self, content: Any) -> str:
        """Format Markdown content"""
        if not isinstance(content, str):
            content = str(content)
        # Format headers
        content = re.sub(r'^(#+)\s*', r'\1 ', content, flags=re.MULTILINE)
        # Format lists
        content = re.sub(r'^\s*[-*+]\s*', '- ', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*(\d+\.)\s*', r'\1 ', content, flags=re.MULTILINE)
        # Format code blocks
        content = re.sub(r'^```(\w*)\s*$', r'```\1', content, flags=re.MULTILINE)
        return content

    def _format_error(self, content: Any) -> str:
        """Format error content"""
        if isinstance(content, Exception):
            error_msg = f"Error: {str(content)}"
            if hasattr(content, '__traceback__'):
                error_msg += f"\nTraceback:\n{content.__traceback__}"
            return error_msg
        return f"Error: {str(content)}"

    def _format_console(self, content: Any) -> str:
        """Format console output"""
        if isinstance(content, (list, tuple)):
            return '\n'.join(str(item) for item in content)
        return str(content)

    def _add_metadata(self, content: str, format_type: ResponseFormat) -> str:
        """Add metadata to formatted content"""
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "format": format_type.value,
            **self.config.metadata
        }
        if format_type == ResponseFormat.JSON:
            return json.dumps({"content": content, "metadata": metadata}, indent=self.config.indent_size)
        elif format_type == ResponseFormat.MARKDOWN:
            meta_section = "---\n"
            for key, value in metadata.items():
                meta_section += f"{key}: {value}\n"
            meta_section += "---\n\n"
            return meta_section + content
        else:
            meta_section = "# Metadata\n"
            for key, value in metadata.items():
                meta_section += f"# {key}: {value}\n"
            return f"{meta_section}\n{content}"
