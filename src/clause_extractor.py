import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json

from config.settings import CONTRACTS_JSON, OUTPUT_DIR
from gemini_client import generate_response
from prompts import CLAUSE_EXTRACTION_PROMPT


def load_contracts():
    with open(CONTRACTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_clauses(contract_text):
    prompt = CLAUSE_EXTRACTION_PROMPT.format(contract=contract_text)

    response = generate_response(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "termination_clause": "Error",
            "confidentiality_clause": "Error",
            "liability_clause": "Error"
        }


def main():
    contracts = load_contracts()

    results = []

    for i, contract in enumerate(contracts, start=1):
        print(f"[{i}/{len(contracts)}] {contract['filename']}")

        clauses = extract_clauses(contract["text"])

        results.append({
            "contract_id": contract["contract_id"],
            "filename": contract["filename"],
            **clauses
        })

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_DIR / "clauses.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\nSaved to outputs/clauses.json")


if __name__ == "__main__":
    main()