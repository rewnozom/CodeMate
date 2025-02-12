"""
llm_agent.py

This is the central interface for LLM integration. It binds together:
- Conversation (with history)
- Prompt optimization
- Model selection based on the agent's state
- Response parsing

The ask() method takes a user message and an optional agent_state.
If no state is provided, the default state (IDLE) is used, and the model_selector
chooses the default model.
"""

from typing import Dict, Any, Optional
import asyncio
import logging

from ..core.state_manager import AgentState
from .conversation import conversation_manager
from .prompt_optimizer import prompt_optimizer
from .model_selector import model_selector
from .response_parser import response_parser
from .llm_manager import llm_manager

class LLMAgent:
    def __init__(self):
        self.conversation = conversation_manager
        self.optimizer = prompt_optimizer
        self.selector = model_selector
        self.parser = response_parser
        self.llm = llm_manager
        self.logger = logging.getLogger(__name__)

    async def ask(self, user_input: str, agent_state: Optional[AgentState] = None) -> Dict[str, Any]:
        self.logger.debug("Received user input: %s", user_input)
        
        # Optimize prompt
        optimized_prompt = self.optimizer.optimize(user_input)
        self.logger.debug("Optimized prompt: %s", optimized_prompt)
        
        # Use default state if none provided
        if agent_state is None:
            self.logger.debug("No agent_state provided; defaulting to IDLE")
            agent_state = AgentState.IDLE
        
        # Select model based on agent state
        selected_model = self.selector.select_model(agent_state)
        self.logger.debug("Selected model for state '%s': %s", agent_state.value, selected_model)
        
        # Send message via conversation (with full history as context)
        self.logger.debug("Sending message to conversation with model: %s", selected_model)
        response = await self.conversation.send_message(optimized_prompt, model_name=selected_model)
        self.logger.debug("Received raw response: %s", response)
        
        # Parse response
        parsed_response = self.parser.parse(response)
        self.logger.debug("Parsed response: %s", parsed_response)
        
        return parsed_response

    def get_conversation_history(self) -> Any:
        return self.conversation.get_history()

# Create a singleton instance
llm_agent = LLMAgent()
