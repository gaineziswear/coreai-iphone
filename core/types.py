from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ModelCapability(str, Enum):
    CHAT = "chat"
    TEXT_GENERATION = "text_generation"
    VISION = "vision"
    AUDIO = "audio"
    EMBEDDINGS = "embeddings"
    TOOL_USE = "tool_use"
    LOCAL = "local"


@dataclass
class AIRequest:
    prompt: str
    system_prompt: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 512
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    text: str
    model: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelInfo:
    id: str
    name: str
    provider: str
    capabilities: List[ModelCapability]
    local: bool = True
    enabled: bool = True
