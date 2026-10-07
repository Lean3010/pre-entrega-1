from pydantic import BaseModel, Field
class ChatMessage(BaseModel):
    role: str
    content: str

class ModelConfig(BaseModel):
    temperature: float = Field (default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1024 )
