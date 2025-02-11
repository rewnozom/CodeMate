"""
llm_agent.py

Detta är det centrala gränssnittet för LLM-integrationen. Här binder vi ihop:
- Konversation (med historik)
- Promptoptimering
- Modellval baserat på agentens state
- Svarsparsning

Genom metoden ask() kan du ange ett användarmeddelande samt (valfritt) ett agent_state.
Om inget state anges används default state (IDLE) och då väljer model_selector standardmodellen.
"""

from typing import Dict, Any, Optional
import asyncio

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

    async def ask(self, user_input: str, agent_state: Optional[AgentState] = None) -> Dict[str, Any]:
        # Optimera prompten
        optimized_prompt = self.optimizer.optimize(user_input)
        # Om inget state specificeras, använd IDLE som default
        if agent_state is None:
            agent_state = AgentState.IDLE
        # Välj modell baserat på det angivna agent_state
        selected_model = self.selector.select_model(agent_state)
        # Skicka meddelande via konversationen – hela historiken skickas som kontext
        response = await self.conversation.send_message(optimized_prompt, model_name=selected_model)
        # Parsar svaret och returnerar det som en dictionary
        parsed_response = self.parser.parse(response)
        return parsed_response

    def get_conversation_history(self) -> Any:
        return self.conversation.get_history()

# Skapa en singleton-instans
llm_agent = LLMAgent()
