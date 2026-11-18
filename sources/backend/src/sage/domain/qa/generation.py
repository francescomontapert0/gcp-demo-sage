"""Generation step of the RAG pipeline: build the grounded prompt, call the LLM."""

from pathlib import Path
import asyncio
from sage.integrations.storage.instructions import read_instructions
from sage.domain.qa.models import Chunk
from sage.integrations.llm.generate import generate_text

_PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "answer_prompt.txt").read_text(
    encoding="utf-8"
)
_NO_DOCUMENTS_CONTEXT = (
    "Nessun documento disponibile (base di conoscenza non ancora popolata o non configurata)."
)


def build_prompt(question: str, chunks: list[Chunk], instructions: str = "") -> str:
    if chunks:
        context = "\n\n".join(
            f"[{c.source} — {c.section}]\n{c.text}" for c in chunks
        )
    else:
        context = _NO_DOCUMENTS_CONTEXT

    prompt = _PROMPT_TEMPLATE.format(context=context, question=question)
    if instructions.strip():
        prompt = (
            "Segui anche le istruzioni aggiuntive qui sotto per forma e stile della risposta.\n\n"
            f"{instructions}\n\n---\n\n{prompt}"
        )
    return prompt


async def generate_answer(question: str, chunks: list[Chunk]) -> str:
    instructions = await asyncio.to_thread(read_instructions)
    return await generate_text(build_prompt(question, chunks, instructions))