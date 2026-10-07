import openai
from openai import AsyncOpenAI
from typing import List, AsyncGenerator
from base_client import BaseLLMClient
from schemas import ChatMessage, ModelConfig

class OpenAIClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-3.5-turbo"

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> str:
        formated_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=formated_messages,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            return response.choices[0].message["content"]
        
        except Exception as e:
            ##prevencion de crash
            return f"[Error controlado OpenAI]:Fallo de la comunicacion - {str(e)}"
        async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
            formated_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
            try:
                stream_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=formated_messages,
                    temperature=config.temperature,
                    max_tokens=config.max_tokens,
                    stream=True
                )
                async for chunk in stream_response:
                    token = chunk.choices[0].delta.content
                    if token is not None:
                        yield token
            except Exception as e:
                yield f"\n[Error controlado OpenAI en streaming]:Fallo de la comunicacion - {str(e)}"