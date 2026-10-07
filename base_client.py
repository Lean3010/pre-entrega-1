from abc import ABC, abstractmethod
from typing import List, AsyncGenerator
from schemas import ChatMessage, ModelConfig

class BaseLLMClient(ABC):
    @abstractmethod
    async def generate (self, messages: List[ChatMessage], config: ModelConfig) -> str:
        """
        Recibe una lista de mensajes y la comfiguracion
        debe devolver la respuesta completa como un string.
        """
    pass

    @abstractmethod
    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        """
        Recibe una lista de mensajes y la comfiguracion
        debe devolver un generador asincrono que emita fragmento de texto (tokens).
        """
        pass