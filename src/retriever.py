from text_splitter import split_text

KEYWORDS = {
    "termination": [
        "termination",
        "terminate",
        "terminated",
        "expiry",
        "expiration"
    ],
    "confidentiality": [
        "confidential",
        "confidentiality",
        "non-disclosure",
        "secret"
    ],
    "liability": [
        "liability",
        "liable",
        "indemnify",
        "indemnification",
        "damages"
    ]
}


def retrieve_relevant_chunks(text, top_k=3):
    chunks = split_text(text)

    scored = []

    for chunk in chunks:
        score = 0
        lower = chunk.lower()

        for words in KEYWORDS.values():
            score += sum(word in lower for word in words)

        scored.append((score, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [chunk for score, chunk in scored[:top_k]]