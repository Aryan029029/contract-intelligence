import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
import time

from config.settings import CONTRACTS_JSON, OUTPUT_DIR
from llm_client import generate_response
from prompts import SUMMARY_PROMPT


def load_contracts():
    with open(CONTRACTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def load_existing_summaries():
    output_file = OUTPUT_DIR / "summaries.json"

    if output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            return json.load(f)

    return []


def summarize_contract(contract_text):
    prompt = SUMMARY_PROMPT.format(contract=contract_text)

    wait_time = 5

    for attempt in range(5):
        try:
            return generate_response(prompt)

        except Exception as e:

            print(f"Attempt {attempt + 1} failed: {e}")
            print(f"Waiting {wait_time} seconds...")

            time.sleep(wait_time)

            wait_time *= 2

    return "Summary generation failed."


def main():

    contracts = load_contracts()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summaries = load_existing_summaries()

    completed_ids = {
        item["contract_id"]
        for item in summaries
    }

    print(f"Already completed: {len(completed_ids)}")

    for i, contract in enumerate(contracts, start=1):

        if contract["contract_id"] in completed_ids:

            print(f"Skipping {contract['filename']}")

            continue

        print(f"\n[{i}/{len(contracts)}] Processing {contract['filename']}")

        summary = summarize_contract(contract["text"])

        summaries.append(
            {
                "contract_id": contract["contract_id"],
                "filename": contract["filename"],
                "summary": summary,
            }
        )

        with open(
            OUTPUT_DIR / "summaries.json",
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                summaries,
                f,
                indent=2,
                ensure_ascii=False,
            )

    print("\nSummaries completed.")
    print(f"Saved to {OUTPUT_DIR / 'summaries.json'}")


if __name__ == "__main__":
    main()