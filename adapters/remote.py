import json
import urllib.request

from adapters.base import ModelAdapter
from core.types import AIRequest, AIResponse, ModelInfo, ModelCapability


class RemoteAdapter(ModelAdapter):

    def __init__(
        self,
        model_id,
        name,
        endpoint,
        api_key=None,
    ):
        self._info = ModelInfo(
            id=model_id,
            name=name,
            provider="remote",
            capabilities=[
                ModelCapability.CHAT,
                ModelCapability.TEXT_GENERATION,
            ],
            local=False,
            enabled=True,
        )

        self.endpoint = endpoint
        self.api_key = api_key

    @property
    def info(self):
        return self._info

    async def generate(self, request: AIRequest):

        messages = []

        if request.system_prompt:
            messages.append({
                "role": "system",
                "content": request.system_prompt,
            })

        messages.append({
            "role": "user",
            "content": request.prompt,
        })

        payload = {
            "model": self.info.id,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        if self.api_key:
            req.add_header(
                "Authorization",
                f"Bearer {self.api_key}",
            )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

        text = result["choices"][0]["message"]["content"]

        return AIResponse(
            text=text,
            model=self.info.id,
            metadata={
                "provider": "remote",
                "local": False,
            },
        )
