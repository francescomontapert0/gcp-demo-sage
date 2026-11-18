"""Reads and writes on the `chunks` collection: vector search at request time, and the
writes used by utils/ingest_documents.py to populate the knowledge base.

MOCK: in-memory placeholder, nothing is persisted across process restarts and
`find_nearest_chunks` never actually ranks by similarity. Replace with a real Firestore
`find_nearest` vector query (see esercizio 12_firestore_dati) and real document writes.
"""

from sage.domain.qa.models import Chunk
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector

from sage.config import get_app_config
from sage.domain.qa.models import Chunk
from sage.integrations.firestore.client import get_firestore_client

def _col():
    return get_firestore_client().collection(get_app_config().firestore_collection)

def find_nearest_chunks(embedding: list[float]) -> list[Chunk]:
    query = _col().find_nearest(
        vector_field="embedding",
        query_vector=Vector(embedding),
        distance_measure=DistanceMeasure.COSINE,
        limit=get_app_config().top_k,
    )
    return [
        Chunk(id=d.id, text=d.get("text"), source=d.get("source"),
              section=d.get("section"), chunk_index=d.get("chunk_index"))
        for d in query.stream()
    ]

def delete_chunks_for_source(source: str) -> None:
    for d in _col().where("source", "==", source).stream():
        d.reference.delete()

def add_chunk(chunk_id, text, embedding, source, section, chunk_index) -> None:
    _col().document(chunk_id).set({
        "text": text, "embedding": Vector(embedding), "source": source,
        "section": section, "chunk_index": chunk_index,
    })