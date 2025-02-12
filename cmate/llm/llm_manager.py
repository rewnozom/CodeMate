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
