from retriever import retrieve_relevant_chunks

text = """
This agreement may be terminated by either party.
The parties shall keep all confidential information secret.
The affiliate agrees to indemnify the company for damages.
"""

chunks = retrieve_relevant_chunks(text, top_k=3)

for i, chunk in enumerate(chunks, 1):
    print(f"\nChunk {i}:\n")
    print(chunk)