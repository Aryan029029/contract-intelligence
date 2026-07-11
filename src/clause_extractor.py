import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
import time

from config.settings import CONTRACTS_JSON, OUTPUT_DIR
from llm_client import generate_response
from prompts import CLAUSE_EXTRACTION_PROMPT
from retriever import retrieve_relevant_chunks


def load_contracts():
    with open(CONTRACTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_clauses(contract_text):
    prompt = CLAUSE_EXTRACTION_PROMPT.format(contract=contract_text)

    for attempt in range(3):
        try:
            response = generate_response(prompt)
            response = response.strip()

            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()

            elif response.startswith("```"):
                response = response.replace("```", "").strip()

            return json.loads(response)

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)

    return {
        "termination_clause": "Not Found",
        "confidentiality_clause": "Not Found",
        "liability_clause": "Not Found"
    }


def main():
    contracts = load_contracts()

    results = []

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, contract in enumerate(contracts, start=1):

        print(f"[{i}/{len(contracts)}] Processing {contract['filename']}")

        relevant_chunks = retrieve_relevant_chunks(
            contract["text"],
            top_k=3
        )

        combined_text = "\n\n".join(relevant_chunks)

        clauses = extract_clauses(combined_text)

        results.append({
            "contract_id": contract["contract_id"],
            "filename": contract["filename"],
            "termination_clause": clauses.get("termination_clause", "Not Found"),
            "confidentiality_clause": clauses.get("confidentiality_clause", "Not Found"),
            "liability_clause": clauses.get("liability_clause", "Not Found")
        })

        with open(
            OUTPUT_DIR / "clauses.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    print("\nClause extraction completed.")
    print(f"Saved to {OUTPUT_DIR / 'clauses.json'}")


if __name__ == "__main__":
    main()