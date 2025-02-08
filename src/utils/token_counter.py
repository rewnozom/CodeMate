from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field
import re
from transformers import AutoTokenizer

@dataclass
class TokenCount:
    """Token count information"""
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

class TokenCounter:
    """Counts tokens for different model types."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.tokenizer = None
        self._initialize_tokenizer()
        
    def _initialize_tokenizer(self) -> None:
        """Initialize appropriate tokenizer based on the model name."""
        try:
            if "gpt" in self.model_name.lower():
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            elif "claude" in self.model_name.lower():
                # Use GPT2 tokenizer as an approximation for Claude models
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
            else:
                # Default to GPT2 tokenizer
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        except Exception as e:
            print(f"Error initializing tokenizer: {str(e)}")
            self.tokenizer = None

    def count_tokens(self, text: Union[str, Dict, List]) -> TokenCount:
        """
        Count tokens in the given text. If text is a dict or list, it is converted to a string.
        Returns a TokenCount dataclass instance.
        """
        if isinstance(text, (dict, list)):
            text = str(text)
        try:
            if self.tokenizer:
                tokens = self.tokenizer.encode(text)
                return TokenCount(
                    total_tokens=len(tokens),
                    prompt_tokens=len(tokens),
                    metadata={"tokenizer": self.tokenizer.__class__.__name__}
                )
            else:
                # Fallback approximation: word count plus punctuation count
                words = text.split()
                tokens_estimate = len(words) + len(re.findall(r'[.!?]', text))
                return TokenCount(
                    total_tokens=tokens_estimate,
                    prompt_tokens=tokens_estimate,
                    metadata={"method": "approximation"}
                )
        except Exception as e:
            print(f"Error counting tokens: {str(e)}")
            return TokenCount(total_tokens=0, prompt_tokens=0)

    def check_token_limit(self, text: Union[str, Dict, List], limit: int) -> bool:
        """Check if the token count for the text does not exceed the given limit."""
        count = self.count_tokens(text)
        return count.total_tokens <= limit

    def truncate_to_token_limit(self, text: str, limit: int) -> str:
        """Truncate the text so that its token count does not exceed the specified limit."""
        if not self.check_token_limit(text, limit):
            if self.tokenizer:
                tokens = self.tokenizer.encode(text)
                truncated_tokens = tokens[:limit]
                return self.tokenizer.decode(truncated_tokens)
            else:
                # Fallback approximation: reduce by estimated number of words
                words = text.split()
                estimated_limit = int(limit / 1.3)
                return ' '.join(words[:estimated_limit])
        return text
