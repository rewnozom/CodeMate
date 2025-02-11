"""
conversation.py

Detta modul hanterar konversationer med agenten. Här lagras
historik och meddelanden skickas till LLM via llm_manager.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import asyncio
from uuid import uuid4

from .llm_manager import llm_manager, ModelResponse

class ConversationMessage:
    def __init__(self, role: str, content: str, timestamp: Optional[datetime] = None):
        self.id = str(uuid4())
        self.role = role  # ex. "user" eller "assistant"
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp.isoformat()
        }

class ConversationManager:
    def __init__(self):
        self.history: List[ConversationMessage] = []
        self.max_history = 50  # max antal meddelanden att spara

    def add_message(self, role: str, content: str) -> None:
        message = ConversationMessage(role, content)
        self.history.append(message)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_history(self) -> List[Dict[str, Any]]:
        return [msg.to_dict() for msg in self.history]

    async def send_message(self, user_message: str, model_name: Optional[str] = None) -> ModelResponse:
        self.add_message("user", user_message)
        # Skicka med hela konversationshistoriken som kontext
        messages = [{"role": msg.role, "content": msg.content} for msg in self.history]
        response: ModelResponse = await llm_manager.generate_response(messages, model_name=model_name)
        self.add_message("assistant", response.content)
        return response

# Skapa en singleton-instans om så önskas
conversation_manager = ConversationManager()
