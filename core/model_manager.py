import json
from pathlib import Path

from .types import ModelInfo


class ModelManager:

    def __init__(self, config_path="config/models.json"):
        self.config_path = Path(config_path)
        self.models = {}
        self.runtime_models = {}

        self.load_config()

    def load_config(self):

        if not self.config_path.exists():
            self.models = {}
            return

        with open(self.config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.models = {
            item["id"]: ModelInfo(
                id=item["id"],
                name=item["name"],
                provider=item["provider"],
                capabilities=item.get("capabilities", []),
                local=item.get("local", True),
                enabled=item.get("enabled", True),
            )
            for item in data.get("models", [])
        }

    def register_runtime_model(self, model):

        self.runtime_models[model.info.id] = model

    def list_models(self):

        return list(self.models.values())

    def get_model(self, model_id=None):

        if model_id:
            return self.models.get(model_id)

        for model in self.models.values():
            if model.enabled:
                return model

        return None

    def get_runtime_model(self, model_id=None):

        if model_id:
            return self.runtime_models.get(model_id)

        for model in self.runtime_models.values():
            if model.info.enabled:
                return model

        return None
