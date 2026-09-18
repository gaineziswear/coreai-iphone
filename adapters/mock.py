from adapters.base import ModelAdapter
from core.types import AIRequest, AIResponse, ModelInfo, ModelCapability


class MockAdapter(ModelAdapter):

    @property
    def info(self):
        return ModelInfo(
            id="coreai-qwen-06b",
            name="Qwen 0.6B Core AI",
            provider="apple-coreai",
            capabilities=[
                ModelCapability.CHAT,
                ModelCapability.TEXT_GENERATION,
                ModelCapability.LOCAL,
            ],
            local=True,
            enabled=True,
        )

    async def generate(self, request: AIRequest) -> AIResponse:
        return AIResponse(
            text=f"[MODEL TEST] Received: {request.prompt}",
            model=self.info.id,
            metadata={
                "provider": self.info.provider,
                "local": True,
            },
        )
