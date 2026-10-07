from typing import List, AsyncGenerator
from base_client import BaseLLMClient
from openai_client import OpenAIClient
from anthropic_client import AnthropicClient
from gemini_client import GeminiClient
from schemas import ChatMessage, ModelConfig

class AsyncLLMManager:
    def __init__(self, provider: str, api_key: str):
        """
        Inicializa el manager y decide qué cliente instanciar basándose en el proveedor.
        """
        self.provider = provider.lower()
        
        
        if self.provider == "openai":
            
            self.client: BaseLLMClient = OpenAIClient(api_key=api_key)
        elif self.provider == "anthropic":
            self.client: BaseLLMClient = AnthropicClient(api_key=api_key)
        elif self.provider == "gemini":
            self.client: BaseLLMClient = GeminiClient(api_key=api_key)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}. Usa 'openai', 'anthropic' o 'gemini'.")

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> str:
        """
        Delega la generación de texto normal al cliente interno.
        """
        # 
        return await self.client.generate(messages, config)

    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        """
        Delega el streaming al cliente interno, cediendo los tokens uno a uno.
        """
        
        async for chunk in self.client.stream(messages, config):
            yield chunk