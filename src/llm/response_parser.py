"""
response_parser.py

Modul för att parsa och standardisera svar från LLM.
"""

from typing import Dict, Any
from .llm_manager import ModelResponse

class ResponseParser:
    def parse(self, response: ModelResponse) -> Dict[str, Any]:
        # Konvertera ModelResponse till en dictionary och försök
        # parsa innehållet (t.ex. om det är JSON)
        parsed = response.dict()
        content = parsed.get("content", "")
        try:
            import json
            parsed_json = json.loads(content)
            parsed["parsed_content"] = parsed_json
        except Exception:
            parsed["parsed_content"] = content
        return parsed

# Skapa en singleton-instans
response_parser = ResponseParser()
