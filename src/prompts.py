CLAUSE_EXTRACTION_PROMPT = """
You are an expert legal AI assistant.

Analyze the contract below and extract ONLY these clauses:

1. Termination Clause
2. Confidentiality Clause
3. Liability Clause

Rules:
- Return ONLY valid JSON.
- Do not use markdown.
- Do not explain anything.
- If a clause is missing, return "Not Found".

Output:

{{
    "termination_clause": "...",
    "confidentiality_clause": "...",
    "liability_clause": "..."
}}

Contract:

{contract}
"""


SUMMARY_PROMPT = """
You are an expert legal AI assistant.

Summarize the following legal contract in 100-150 words.

Your summary must include:
- Purpose of the agreement
- Key obligations of each party
- Important risks, liabilities or penalties

Return only the summary.

Contract:

{contract}
"""