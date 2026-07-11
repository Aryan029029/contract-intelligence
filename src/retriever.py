import faiss
import numpy as np

from text_splitter import split_text
from embeddings import embed_texts


def retrieve_relevant_chunks(text, query, top_k=3):
    chunks = split_text(text)

    if len(chunks) == 0:
        return []

    embeddings = embed_texts(chunks).astype(np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    query_embedding = embed_texts([query]).astype(np.float32)

    _, indices = index.search(
        query_embedding,
        min(top_k, len(chunks))
    )

    return [chunks[i] for i in indices[0]]