from .types import AIRequest


class ModelRouter:

    def __init__(self, model_manager):
        self.model_manager = model_manager

    def select_model(self, request: AIRequest):

        if request.model:
            model = self.model_manager.get_model(request.model)

            if model and model.enabled:
                return model.id

            raise RuntimeError(
                f"Requested model is unavailable: {request.model}"
            )

        models = self.model_manager.list_models()

        # Prefer local models.
        for model in models:
            if model.enabled and model.local:
                return model.id

        # Fall back to remote models.
        for model in models:
            if model.enabled:
                return model.id

        raise RuntimeError(
            "No enabled AI model is available."
        )
