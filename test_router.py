import asyncio

from core.ai_engine import AIEngine
from core.model_manager import ModelManager
from core.model_router import ModelRouter
from core.types import AIRequest

from adapters.mock import MockAdapter
from adapters.coreai import CoreAIAdapter


async def main():

    manager = ModelManager()

    router = ModelRouter(manager)

    # Register our test runtime.
    mock = MockAdapter()
    manager.register_runtime_model(mock)

    # Register the real Core AI adapter.
    coreai = CoreAIAdapter()
    manager.register_runtime_model(coreai)

    engine = AIEngine(
        manager,
        router,
    )

    print()
    print("=== REGISTERED RUNTIME MODELS ===")

    for model_id, model in manager.runtime_models.items():
        print(
            "-",
            model_id,
            "|",
            model.info.name,
            "|",
            model.info.provider,
        )

    print()
    print("=== TEST 1: MOCK MODEL ===")

    request = AIRequest(
        prompt="Hello from the model router",
        model="coreai-qwen-06b",
    )

    response = await engine.generate(request)

    print("MODEL:", response.model)
    print("TEXT:", response.text)

    print()
    print("=== TEST 2: CORE AI ADAPTER ===")

    try:

        request = AIRequest(
            prompt="Hello Core AI",
            model="coreai-qwen3-0.6b",
        )

        response = await engine.generate(request)

        print("MODEL:", response.model)
        print("TEXT:", response.text)

    except Exception as error:

        print("EXPECTED NATIVE RUNTIME STATUS:")
        print(error)


asyncio.run(main())
