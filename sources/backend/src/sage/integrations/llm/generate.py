from sage.config import get_app_config
from sage.integrations.llm.client import get_genai_client

async def generate_text(prompt: str) -> str:
    response = await get_genai_client().aio.models.generate_content(
        model=get_app_config().chat_model, contents=prompt
    )
    return response.text or ""