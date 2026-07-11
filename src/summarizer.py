import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
import time

from config.settings import CONTRACTS_JSON, OUTPUT_DIR
from llm_client import generate_response
from prompts import SUMMARY_PROMPT
from retriever import retrieve_relevant_chunks


def load_contracts():
    with open(CONTRACTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize_contract(contract_text):
    prompt = SUMMARY_PROMPT.format(contract=contract_text)

    for attempt in range(3):
        try:
            return generate_response(prompt)

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)

    return "Summary generation failed."


def main():
    contracts = load_contracts()

    summaries = []

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for i, contract in enumerate(contracts, start=1):

        print(f"[{i}/{len(contracts)}] {contract['filename']}")

        relevant_chunks = retrieve_relevant_chunks(
            contract["text"],
            query="""
            Summarize this legal agreement.
            Retrieve the sections describing:
            - Purpose of the agreement
            - Responsibilities of both parties
            - Risks
            - Liabilities
            - Penalties
            """,
            top_k=3
        )

        combined_text = "\n\n".join(relevant_chunks)

        summary = summarize_contract(combined_text)

        summaries.append({
            "contract_id": contract["contract_id"],
            "filename": contract["filename"],
            "summary": summary
        })

        with open(
            OUTPUT_DIR / "summaries.json",
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                summaries,
                f,
                indent=2,
                ensure_ascii=False
            )

    print("\nSummaries saved.")
    print(f"Saved to {OUTPUT_DIR / 'summaries.json'}")


if __name__ == "__main__":
    main()