import asyncio

from core.ai_engine import AIEngine
from core.model_manager import ModelManager
from core.model_router import ModelRouter
from core.types import AIRequest
from adapters.mock import MockAdapter


async def main():

    manager = ModelManager()
    router = ModelRouter(manager)

    adapter = MockAdapter()
    manager.register_runtime_model(adapter)

    engine = AIEngine(manager, router)

    request = AIRequest(
        prompt="Hello from my iPhone AI engine",
        model="coreai-qwen-06b"
    )

    response = await engine.generate(request)

    print()
    print("MODEL:", response.model)
    print("TEXT:", response.text)
    print("METADATA:", response.metadata)


asyncio.run(main())
