from adapters.base import ModelAdapter
from core.types import AIRequest, AIResponse, ModelInfo, ModelCapability


class CoreAIAdapter(ModelAdapter):

    def __init__(self, model_id="coreai-qwen3-0.6b"):
        self._info = ModelInfo(
            id=model_id,
            name="Qwen3 0.6B",
            provider="apple-coreai",
            capabilities=[
                ModelCapability.CHAT,
                ModelCapability.TEXT_GENERATION,
                ModelCapability.LOCAL,
            ],
            local=True,
            enabled=True,
        )

        self.bridge = None

    @property
    def info(self):
        return self._info

    def attach_bridge(self, bridge):
        """
        Attach the native Swift Core AI bridge.

        The bridge is supplied by the iOS application.
        """
        self.bridge = bridge

    async def generate(self, request: AIRequest) -> AIResponse:

        if self.bridge is None:
            raise RuntimeError(
                "Core AI native bridge is not attached. "
                "This adapter requires the iOS Core AI runtime."
            )

        prompt = request.prompt

        if request.system_prompt:
            prompt = (
                f"System instructions:\n"
                f"{request.system_prompt}\n\n"
                f"User:\n"
                f"{request.prompt}"
            )

        text = await self.bridge.respond(prompt)

        return AIResponse(
            text=text,
            model=self.info.id,
            metadata={
                "provider": "apple-coreai",
                "local": True,
                "runtime": "CoreAILanguageModel",
            },
        )
