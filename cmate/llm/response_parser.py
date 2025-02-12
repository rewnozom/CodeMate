# cmate/llm/response_parser.py
"""
response_parser.py

Module for parsing and standardizing responses from the LLM.
This version is now CoT-aware: if the response contains a chain-of-thought block
delimited by <think> ... </think>, it will be separated and optionally removed.
"""

from typing import Dict, Any
from .llm_manager import ModelResponse
import re

class ResponseParser:
    def parse(self, response: ModelResponse) -> Dict[str, Any]:
        """
        Parse the ModelResponse into a standardized dictionary.
        If a chain-of-thought block is detected (i.e. text between <think> and </think>),
        it is extracted and stored in a separate field.
        """
        parsed = response.dict()
        content = parsed.get("content", "")
        
        # Check for chain-of-thought markers
        cot_pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)
        cot_match = cot_pattern.search(content)
        
        if cot_match:
            # Extract the chain-of-thought text
            chain_of_thought = cot_match.group(1).strip()
            parsed["chain_of_thought"] = chain_of_thought
            # Remove the chain-of-thought block from the final answer
            content = cot_pattern.sub("", content).strip()
        
        # Attempt to parse the remaining content as JSON; if not, keep it as text.
        try:
            import json
            parsed_json = json.loads(content)
            parsed["parsed_content"] = parsed_json
        except Exception:
            parsed["parsed_content"] = content
        
        # Also update the content field to the cleaned final answer.
        parsed["content"] = content
        
        return parsed

# Create a singleton instance
response_parser = ResponseParser()
