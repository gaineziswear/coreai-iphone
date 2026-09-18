from .types import AIRequest, AIResponse


class AIEngine:

    def __init__(self, model_manager, router):
        self.model_manager = model_manager
        self.router = router

    async def generate(
        self,
        request: AIRequest,
    ) -> AIResponse:

        model_id = self.router.select_model(request)

        model = self.model_manager.get_runtime_model(
            model_id
        )

        if model is None:
            raise RuntimeError(
                f"No runtime adapter available for: {model_id}"
            )

        return await model.generate(request)
