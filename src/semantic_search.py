import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
from pathlib import Path

import faiss
import numpy as np

from config.settings import OUTPUT_DIR
from .embeddings import embed_texts


CLAUSE_TYPES = [
    "termination_clause",
    "confidentiality_clause",
    "liability_clause"
]


class SemanticSearch:

    def __init__(self):

        self.documents = []

        self.index = None

    def build_index(self):

        with open(
            OUTPUT_DIR / "clauses.json",
            "r",
            encoding="utf-8"
        ) as f:

            clauses = json.load(f)

        texts = []

        for contract in clauses:

            for clause_type in CLAUSE_TYPES:

                clause = contract.get(clause_type)

                if clause and clause != "Not Found":

                    texts.append(clause)

                    self.documents.append({
                        "contract_id": contract["contract_id"],
                        "filename": contract["filename"],
                        "clause_type": clause_type,
                        "text": clause
                    })

        embeddings = embed_texts(texts).astype(np.float32)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

    def search(self, query, top_k=5):

        query_embedding = embed_texts([query]).astype(np.float32)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            results.append({
                "score": float(score),
                **self.documents[idx]
            })

        return results


if __name__ == "__main__":

    search_engine = SemanticSearch()

    search_engine.build_index()

    query = input("Search clause: ")

    results = search_engine.search(query)

    print()

    for result in results:

        print("=" * 80)

        print(result["filename"])

        print(result["clause_type"])

        print(f"Similarity: {result['score']:.3f}")

        print()

        print(result["text"][:500])

        print()