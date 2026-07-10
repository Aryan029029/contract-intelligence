CLAUSE_EXTRACTION_PROMPT = """
You are an AI legal assistant.

Analyze the following legal contract and extract:

1. Termination Clause
2. Confidentiality Clause
3. Liability Clause

Rules:
- Return ONLY valid JSON.
- If a clause is not present, return "Not Found".
- Do not include markdown.
- Do not explain anything.

Output format:

{
    "termination_clause": "...",
    "confidentiality_clause": "...",
    "liability_clause": "..."
}

Contract:

{contract}
"""


SUMMARY_PROMPT = """
You are an AI legal assistant.

Summarize the following contract in 100-150 words.

Include:
- Purpose of the agreement
- Key obligations of each party
- Risks or penalties

Return only the summary.

Contract:

{contract}
"""