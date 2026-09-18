from abc import ABC, abstractmethod

from core.types import AIRequest, AIResponse, ModelInfo


class ModelAdapter(ABC):

    @property
    @abstractmethod
    def info(self) -> ModelInfo:
        pass

    @abstractmethod
    async def generate(self, request: AIRequest) -> AIResponse:
        pass
