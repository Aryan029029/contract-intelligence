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
ANALYSIS_PROMPT = """You are a legal contract analysis assistant.

Analyze the following contract and return your answer as a single valid JSON object
with exactly these four keys: "summary", "termination_clause", "confidentiality_clause",
and "liability_clause".

- "summary": a concise 100-150 word summary covering the purpose of the agreement,
  key obligations of each party, and notable risks or penalties.
- "termination_clause": the termination conditions found in the contract, or
  "Not found" if none exist.
- "confidentiality_clause": the confidentiality clause found in the contract, or
  "Not found" if none exist.
- "liability_clause": the liability clause found in the contract, or
  "Not found" if none exist.

Return ONLY the JSON object. Do not include markdown formatting, code fences, or
any explanation before or after it.

Contract:
{contract_text}
"""