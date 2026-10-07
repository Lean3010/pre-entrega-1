# Unified Async LLM Client

Este repositorio contiene la implementación de un cliente robusto y asíncrono para interactuar con múltiples proveedores de LLMs, cumpliendo con los requisitos de intercambiabilidad, asincronía, streaming y validación estricta de datos.

**Nota sobre la integración de proveedores:** 
Aunque la consigna original requería OpenAI y Anthropic (los cuales están completamente implementados en el código), se añadió  la integración con **Google Gemini (gemini-1.5-flash)**. Esto permite probar la arquitectura y ejecutar el código de forma 100% gratuita, demostrando además la alta escalabilidad del patrón de diseño utilizado, donde agregar un nuevo proveedor no afecta la lógica principal del programa.

## 🛠️ Arquitectura y Tecnologías
* **Python 3.12**
* **Pydantic**: Utilizado en `schemas.py` para la validación estricta de los esquemas de entrada (mensajes) y configuración (temperatura, max_tokens).
* **Patrón Factory (AsyncLLMManager)**: Interfaz central que permite instanciar el proveedor deseado (OpenAI, Anthropic o Gemini) mediante una simple variable de configuración, logrando un desacoplamiento total.
* **Async/Await y Streaming**: Implementación 100% asíncrona para evitar el bloqueo del Event Loop de Python, incluyendo soporte nativo para **Streaming** mediante generadores asíncronos (`yield`).
* **Manejo de Errores Resiliente**: Captura de excepciones de red (Rate Limits, 503, errores de conexión) mediante bloques `try/except`, devolviendo mensajes controlados para evitar el colapso (crash) de la aplicación.

## ⚙️ Configuración del Entorno

1. **Crear y activar el entorno virtual:**
   ```bash
   python -m venv venv
   
   # En Windows:
   venv\Scripts\activate
   
 . Instalar Dependencias
Con el entorno activado, instala las librerías requeridas:
pip install openai anthropic google-generativeai pydantic python-dotenv
4. Variables de Entorno
Crea un archivo llamado .env en la raíz del proyecto basándote en el archivo .env.example. Para probar la aplicación, configura al menos una clave API válida:


OPENAI_API_KEY=tu_clave_de_openai
ANTHROPIC_API_KEY=tu_clave_de_anthropic
GEMINI_API_KEY=tu_clave_de_gemini


5. Cómo correr el script de validación
Para ejecutar la prueba de generación estándar y de streaming en tiempo real, corre el siguiente comando en tu terminal:
python main.py
 Por defecto, el archivo main.py está configurado para ejecutarse con provider="gemini". Puedes cambiar este parámetro a "openai" o "anthropic" en la instanciación de AsyncLLMManager para probar los otros proveedores.  
