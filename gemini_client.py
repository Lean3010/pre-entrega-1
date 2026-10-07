import google.generativeai as genai
from typing import List, AsyncGenerator
from base_client import BaseLLMClient
from schemas import ChatMessage, ModelConfig

class GeminiClient(BaseLLMClient):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        
        self.model_name = 'gemini-1.5-flash'

    async def generate(self, messages: List[ChatMessage], config: ModelConfig) -> str:
        formatted_messages, system_instruction = self._format_messages(messages)
        model = genai.GenerativeModel(self.model_name, system_instruction=system_instruction)
        
        try:
            response = await model.generate_content_async(
                formatted_messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens
                )
            )
            return response.text
        except Exception as e:
            return f"[Error controlado Gemini]: {str(e)}"

    async def stream(self, messages: List[ChatMessage], config: ModelConfig) -> AsyncGenerator[str, None]:
        formatted_messages, system_instruction = self._format_messages(messages)
        model = genai.GenerativeModel(self.model_name, system_instruction=system_instruction)
        
        try:
            response = await model.generate_content_async(
                formatted_messages,
                generation_config=genai.types.GenerationConfig(
                    temperature=config.temperature,
                    max_output_tokens=config.max_tokens
                ),
                stream=True
            )
            async for chunk in response:
                yield chunk.text
        except Exception as e:
            yield f"\n[Error controlado Gemini en streaming]: {str(e)}"

    
    def _format_messages(self, messages: List[ChatMessage]):
        formatted = []
        system_instruction = None
        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            else:
                
                role = "model" if msg.role == "assistant" else "user"
                formatted.append({"role": role, "parts": [msg.content]})
        return formatted, system_instruction