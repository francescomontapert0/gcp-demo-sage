from sage.config import get_app_config
from sage.integrations.llm.client import get_genai_client


def embed_text(text: str) -> list[float]:
    config = get_app_config()
    result = get_genai_client().models.embed_content(
        model=config.embedding_model, contents=text
    )
    return list(result.embeddings[0].values)