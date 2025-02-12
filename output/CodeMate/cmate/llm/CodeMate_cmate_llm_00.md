# Project Details

# Table of Contents
- [..\CodeMate\cmate\llm\__init__.py](#-CodeMate-cmate-llm-__init__py)
- [..\CodeMate\cmate\llm\conversation.py](#-CodeMate-cmate-llm-conversationpy)
- [..\CodeMate\cmate\llm\llm_agent.py](#-CodeMate-cmate-llm-llm_agentpy)
- [..\CodeMate\cmate\llm\llm_manager.py](#-CodeMate-cmate-llm-llm_managerpy)
- [..\CodeMate\cmate\llm\model_selector.py](#-CodeMate-cmate-llm-model_selectorpy)
- [..\CodeMate\cmate\llm\prompt_optimizer.py](#-CodeMate-cmate-llm-prompt_optimizerpy)
- [..\CodeMate\cmate\llm\response_parser.py](#-CodeMate-cmate-llm-response_parserpy)


# ..\..\CodeMate\cmate\llm\__init__.py
## File: ..\..\CodeMate\cmate\llm\__init__.py

```py
# ..\..\CodeMate\cmate\llm\__init__.py
# Auto-generated __init__.py file

```

---

# ..\..\CodeMate\cmate\llm\conversation.py
## File: ..\..\CodeMate\cmate\llm\conversation.py

```py
# ..\..\CodeMate\cmate\llm\conversation.py
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

```

---

# ..\..\CodeMate\cmate\llm\llm_agent.py
## File: ..\..\CodeMate\cmate\llm\llm_agent.py

```py
# ..\..\CodeMate\cmate\llm\llm_agent.py
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

```

---

# ..\..\CodeMate\cmate\llm\llm_manager.py
## File: ..\..\CodeMate\cmate\llm\llm_manager.py

```py
# ..\..\CodeMate\cmate\llm\llm_manager.py
# cmate/llm/llm_manager.py
"""
llm_manager.py

This module manages integration with various LLM providers.
It defines ModelProvider, ModelConfig, and ModelResponse,
and an LLMManager class that initializes clients based on environment variables.
"""

from typing import Optional, Dict, Any, Union
from enum import Enum
import os
from datetime import datetime
from dotenv import load_dotenv
import asyncio

# (The following imports are examples – adjust to your actual client libraries)
from anthropic import Anthropic
from openai import OpenAI, AzureOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

load_dotenv()

class ModelProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    AZURE = "azure"
    GROQ = "groq"
    LM_STUDIO = "lm_studio"

class ModelConfig(BaseModel):
    provider: ModelProvider
    model_name: str
    temperature: float = Field(default=float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = Field(default=int(os.getenv("MAX_TOKENS", "60000")))
    top_p: float = Field(default=float(os.getenv("TOP_P", "0.9")))
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    additional_params: Dict[str, Any] = Field(default_factory=dict)

class ModelResponse(BaseModel):
    content: str
    model_name: str
    total_tokens: int
    prompt_tokens: int
    completion_tokens: int
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)

class LLMManager:
    def __init__(self):
        self.models = self._load_default_models()
        self.current_model = os.getenv("DEFAULT_MODEL", "claude-3-sonnet")
        self._load_api_keys()
        self._initialize_clients()

    def _load_default_models(self) -> Dict[str, ModelConfig]:
        return {
            "claude-3-haiku": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=os.getenv("CLAUDE_HAIKU_MODEL", "claude-3-haiku-20240307")
            ),
            "claude-3-sonnet": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=os.getenv("CLAUDE_SONNET_MODEL", "claude-3-sonnet-20240229")
            ),
            "claude-3-opus": ModelConfig(
                provider=ModelProvider.ANTHROPIC,
                model_name=os.getenv("CLAUDE_OPUS_MODEL", "claude-3-opus-20240229")
            ),
            "gpt-4": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name=os.getenv("GPT4_MODEL", "gpt-4")
            ),
            "gpt-3.5-turbo": ModelConfig(
                provider=ModelProvider.OPENAI,
                model_name=os.getenv("GPT35_MODEL", "gpt-3.5-turbo")
            ),
            "mixtral-8x7b": ModelConfig(
                provider=ModelProvider.GROQ,
                model_name=os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")
            ),
            "lm-studio-local": ModelConfig(
                provider=ModelProvider.LM_STUDIO,
                model_name=os.getenv("LM_STUDIO_MODEL", "model-identifier"),
                api_base=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
            )
        }

    def _load_api_keys(self):
        self.api_keys = {
            ModelProvider.ANTHROPIC: os.getenv("ANTHROPIC_API_KEY"),
            ModelProvider.OPENAI: os.getenv("OPENAI_API_KEY"),
            ModelProvider.GROQ: os.getenv("GROQ_API_KEY"),
            ModelProvider.AZURE: os.getenv("AZURE_OPENAI_API_KEY"),
            ModelProvider.LM_STUDIO: os.getenv("LM_STUDIO_API_KEY", "lm-studio")
        }

    def _initialize_clients(self):
        self.clients = {}
        if self.api_keys.get(ModelProvider.ANTHROPIC):
            self.clients[ModelProvider.ANTHROPIC] = Anthropic(
                api_key=self.api_keys[ModelProvider.ANTHROPIC]
            )
        if self.api_keys.get(ModelProvider.OPENAI):
            self.clients[ModelProvider.OPENAI] = OpenAI(
                api_key=self.api_keys[ModelProvider.OPENAI]
            )
        if self.api_keys.get(ModelProvider.GROQ):
            self.clients[ModelProvider.GROQ] = ChatGroq(
                api_key=self.api_keys[ModelProvider.GROQ]
            )
        # For LM Studio, we assume the client is similar to OpenAI's client.
        self.clients[ModelProvider.LM_STUDIO] = OpenAI(
            base_url=self.models["lm-studio-local"].api_base,
            api_key=self.api_keys[ModelProvider.LM_STUDIO]
        )

    def add_model(self, name: str, config: ModelConfig):
        self.models[name] = config

    def set_current_model(self, model_name: str):
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found in available models")
        self.current_model = model_name

    def get_available_models(self) -> Dict[str, ModelConfig]:
        return self.models

    async def generate_response(
        self,
        messages: list,
        model_name: Optional[str] = None,
        **kwargs
    ) -> ModelResponse:
        start_time = datetime.now()
        model_name = model_name or self.current_model
        model_config = self.models[model_name]
        try:
            if model_config.provider == ModelProvider.ANTHROPIC:
                response = await self._generate_anthropic_response(messages, model_config, **kwargs)
            elif model_config.provider == ModelProvider.OPENAI:
                response = await self._generate_openai_response(messages, model_config, **kwargs)
            elif model_config.provider == ModelProvider.GROQ:
                response = await self._generate_groq_response(messages, model_config, **kwargs)
            elif model_config.provider == ModelProvider.LM_STUDIO:
                response = await self._generate_lm_studio_response(messages, model_config, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {model_config.provider}")

            processing_time = (datetime.now() - start_time).total_seconds()
            return ModelResponse(
                content=response.content,
                model_name=model_name,
                total_tokens=response.usage.total_tokens,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                processing_time=processing_time
            )
        except Exception as e:
            raise Exception(f"Error generating response with {model_name}: {str(e)}")

    async def _generate_anthropic_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.ANTHROPIC]
        return await client.messages.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

    async def _generate_openai_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.OPENAI]
        return await client.chat.completions.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

    async def _generate_groq_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.GROQ]
        return await client.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

    async def _generate_lm_studio_response(self, messages, model_config: ModelConfig, **kwargs):
        client = self.clients[ModelProvider.LM_STUDIO]
        # Wrap the synchronous call in asyncio.to_thread
        return await asyncio.to_thread(
            client.chat.completions.create,
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

# Create a singleton instance for ease of use
llm_manager = LLMManager()

```

---

# ..\..\CodeMate\cmate\llm\model_selector.py
## File: ..\..\CodeMate\cmate\llm\model_selector.py

```py
# ..\..\CodeMate\cmate\llm\model_selector.py
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

```

---

# ..\..\CodeMate\cmate\llm\prompt_optimizer.py
## File: ..\..\CodeMate\cmate\llm\prompt_optimizer.py

```py
# ..\..\CodeMate\cmate\llm\prompt_optimizer.py
"""
prompt_optimizer.py

En enkel promptoptimizer som exempelvis kan trimma prompts om de blir för långa.
Här kan du lägga till mer avancerad logik vid behov.
"""

from typing import Dict, Any

class PromptOptimizer:
    def __init__(self, max_tokens: int = 60000):
        self.max_tokens = max_tokens

    def optimize(self, prompt: str) -> str:
        # Enkel uppskattning: 4 tecken per token
        token_estimate = len(prompt) // 4
        if token_estimate > self.max_tokens:
            # Trunkera prompten så att den ryms inom max_tokens
            prompt = prompt[: self.max_tokens * 4]
        return prompt

# Skapa en singleton-instans
prompt_optimizer = PromptOptimizer()

```

---

# ..\..\CodeMate\cmate\llm\response_parser.py
## File: ..\..\CodeMate\cmate\llm\response_parser.py

```py
# ..\..\CodeMate\cmate\llm\response_parser.py
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

```

---

