import json

from config.settings import CONTRACTS_JSON
from retriever import retrieve_relevant_chunks

with open(CONTRACTS_JSON, "r", encoding="utf-8") as f:
    contracts = json.load(f)

text = contracts[0]["text"]

chunks = retrieve_relevant_chunks(text, top_k=3)

for i, chunk in enumerate(chunks, start=1):
    print(f"\n{'='*80}")
    print(f"CHUNK {i}")
    print(f"{'='*80}")
    print(chunk[:800])