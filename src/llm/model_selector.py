"""
model_selector.py

Detta modul väljer rätt LM Studio-modell baserat på agentens state.
Alla modeller kommer från LM Studio.
"""

from typing import Optional, Dict, Any
from core.state_manager import AgentState

class ModelSelector:
    def __init__(self):
        # Mappning från specifika AgentState till modellnamn
        self.state_model_mapping = {
            AgentState.CODING: "rewnozom/nodex_l-8b/nodex_l-8b-q4_k_m.gguf",
            AgentState.WRITING_TESTS: "llama-3.2-3b-codereactor",
            AgentState.NAVIGATION: "nodex_l-8b@q8_0",
            AgentState.EMBEDDING: "text-embedding-nomic-embed-text-v1.5@q4_k_m"
        }
        # Om inget state matchar, använd denna standardmodell
        self.default_model = "lm-studio-local"

    def select_model(self, agent_state: AgentState) -> str:
        return self.state_model_mapping.get(agent_state, self.default_model)

# Skapa en singleton-instans
model_selector = ModelSelector()
