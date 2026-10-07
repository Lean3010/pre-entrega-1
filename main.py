import os
import asyncio
from dotenv import load_dotenv
from manager import AsyncLLMManager
from schemas import ChatMessage, ModelConfig

async def main():
    
    load_dotenv()
    
    # Obtener la API key 
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: No se encontró la API Key en el archivo .env")
        return

    
    manager = AsyncLLMManager(provider="gemini", api_key=api_key)
    
    
    messages = [
        ChatMessage(role="system", content="Eres un profesor de física experto en explicar conceptos complejos de forma sencilla."),
        ChatMessage(role="user", content="¿Qué es la entropía?")
    ]
    
    config = ModelConfig(temperature=0.5, max_tokens=300)

    
    print("\n" + "="*40)
    print("🚀 PROBANDO MODO NORMAL (Esperando...)")
    print("="*40)
    respuesta_normal = await manager.generate(messages, config)
    print(respuesta_normal)

    
    print("\n" + "="*40)
    print("🌊 PROBANDO MODO STREAMING (Tiempo real)")
    print("="*40)
    
    
    async for token in manager.stream(messages, config):
        
        print(token, end="", flush=True)
        
    print("\n\n✅ ¡Prueba finalizada con éxito!")


if __name__ == "__main__":
    
    asyncio.run(main())