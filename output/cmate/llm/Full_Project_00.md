# Project Details

# Table of Contents
- [..\cmate\llm\conversation.py](#-cmate-llm-conversationpy)
- [..\cmate\llm\llm_agent.py](#-cmate-llm-llm_agentpy)
- [..\cmate\llm\llm_manager.py](#-cmate-llm-llm_managerpy)
- [..\cmate\llm\model_selector.py](#-cmate-llm-model_selectorpy)
- [..\cmate\llm\prompt_optimizer.py](#-cmate-llm-prompt_optimizerpy)
- [..\cmate\llm\response_parser.py](#-cmate-llm-response_parserpy)
- [..\cmate\llm\__init__.py](#-cmate-llm-__init__py)


# ..\..\cmate\llm\conversation.py
## File: ..\..\cmate\llm\conversation.py

```py
# ..\..\cmate\llm\conversation.py
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

# ..\..\cmate\llm\llm_agent.py
## File: ..\..\cmate\llm\llm_agent.py

```py
# ..\..\cmate\llm\llm_agent.py
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

```

---

# ..\..\cmate\llm\llm_manager.py
## File: ..\..\cmate\llm\llm_manager.py

```py
# ..\..\cmate\llm\llm_manager.py
"""
llm_manager.py

Detta modul hanterar integrationen med olika LLM‐providers.
Den definierar en ModelProvider‐enum, ModelConfig och ModelResponse,
samt en LLMManager-klass som initialiserar klienter baserat på miljövariabler.
"""

from typing import Optional, Dict, Any, Union
from enum import Enum
import os
from datetime import datetime
from dotenv import load_dotenv

from anthropic import Anthropic
from openai import OpenAI, AzureOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

# Ladda miljövariabler
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
        # För LM Studio antas klienten likna OpenAI-klienten
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
        return await client.chat.completions.create(
            model=model_config.model_name,
            messages=messages,
            temperature=model_config.temperature,
            max_tokens=model_config.max_tokens,
            **kwargs
        )

# Skapa en singleton-instans för enkel åtkomst
llm_manager = LLMManager()

```

---

# ..\..\cmate\llm\model_selector.py
## File: ..\..\cmate\llm\model_selector.py

```py
# ..\..\cmate\llm\model_selector.py
"""
model_selector.py

Detta modul väljer rätt LM Studio-modell baserat på agentens state.
Alla modeller kommer från LM Studio.
"""

from typing import Optional, Dict, Any
from ..core.state_manager import AgentState

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

```

---

# ..\..\cmate\llm\prompt_optimizer.py
## File: ..\..\cmate\llm\prompt_optimizer.py

```py
# ..\..\cmate\llm\prompt_optimizer.py
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

# ..\..\cmate\llm\response_parser.py
## File: ..\..\cmate\llm\response_parser.py

```py
# ..\..\cmate\llm\response_parser.py
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

```

---

# ..\..\cmate\llm\__init__.py
## File: ..\..\cmate\llm\__init__.py

```py
# ..\..\cmate\llm\__init__.py
# Auto-generated __init__.py file

```

---

