"""
model_selector.py

This module selects the appropriate LM Studio model based on the agent's current state.
All models are sourced from LM Studio.

For states that are explicitly defined in the mapping below, the corresponding model is used.
For all other states, the default model "athene-phi-3.5-mini-instruct-orpo" is returned.
This ensures that the agent always has a valid model for any state, including new or unexpected ones.
"""

from typing import Optional, Dict, Any
from ..core.state_manager import AgentState

class ModelSelector:
    """
    A class responsible for selecting the appropriate LM Studio model
    based on the agent's current state.

    Mapping:
      - AgentState.CODING: "athene-phi-3.5-mini-instruct-orpo"
      - AgentState.WRITING_TESTS: "athene-phi-3.5-mini-instruct-orpo"
      - AgentState.NAVIGATING: "athene-phi-3.5-mini-instruct-orpo"
      - AgentState.EMBEDDING: "text-embedding-nomic-embed-text-v1.5@q4_k_m"

    Default:
      For any state that is not explicitly defined in the mapping,
      the default model "athene-phi-3.5-mini-instruct-orpo" is used.
    """
    
    def __init__(self):
        # Mapping from specific AgentState to model names.
        # These are used for states that require specialized handling.
        self.state_model_mapping = {
            AgentState.CODING: "athene-phi-3.5-mini-instruct-orpo",
            AgentState.WRITING_TESTS: "athene-phi-3.5-mini-instruct-orpo",
            AgentState.NAVIGATING: "athene-phi-3.5-mini-instruct-orpo",
            AgentState.EMBEDDING: "text-embedding-nomic-embed-text-v1.5@q4_k_m"
        }
        
        # Default model for all states that are not explicitly defined.
        self.default_model = "athene-phi-3.5-mini-instruct-orpo"

    def select_model(self, agent_state: AgentState) -> str:
        """
        Select the appropriate model based on the current agent state.

        Args:
            agent_state (AgentState): The current state of the agent.

        Returns:
            str: The name of the model to be used.
                 If the state is mapped in the dictionary, its corresponding model is returned.
                 Otherwise, the default model ("athene-phi-3.5-mini-instruct-orpo") is returned.
        """
        return self.state_model_mapping.get(agent_state, self.default_model)

# Create a singleton instance for easy access throughout the system.
model_selector = ModelSelector()
