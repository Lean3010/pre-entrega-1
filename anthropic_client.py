import anthropic
from anthropic import AsyncAnthropic
from typing import List, AsyncGenerator
from base_client import BaseLLMClient
from schemas import ChatMessage, ModelConfig

class AnthropicClient(BaseLLMClient):
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
        
        self.model = "claude-3-haiku-20240307"

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> str:
        
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages if msg.role != "system"]
        
        
        system_message = next((msg.content for msg in messages if msg.role == "system"), anthropic.NOT_GIVEN)

        try:
            
            response = await self.client.messages.create(
                model=self.model,
                messages=formatted_messages,
                system=system_message,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
            
            return response.content[0].text
            
        except Exception as e:
            return f"[Error controlado Anthropic]: Fallo en la comunicación - {str(e)}"

    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        formatted_messages = [{"role": msg.role, "content": msg.content} for msg in messages if msg.role != "system"]
        system_message = next((msg.content for msg in messages if msg.role == "system"), anthropic.NOT_GIVEN)

        try:
            
            async with self.client.messages.stream(
                model=self.model,
                messages=formatted_messages,
                system=system_message,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            ) as stream:
                
                async for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            yield f"\n[Error controlado Anthropic en streaming]: {str(e)}"