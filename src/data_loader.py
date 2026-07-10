from pathlib import Path
import fitz
import json
import re

RAW_PDF_DIR = Path("data/raw_pdfs")
OUTPUT_PATH = Path("data/contracts_subset.json")
MAX_CONTRACTS = 50


def get_pdf_files(pdf_dir: Path):
    return sorted(pdf_dir.rglob("*.pdf"))[:MAX_CONTRACTS]

def extract_text_from_pdf(pdf_path: Path):
    text = []

    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text.append(page.get_text())

    return "\n".join(text)


def normalize_text(text: str):
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\x0c", " ", text)
    return text.strip()


def load_contracts():
    contracts = []

    pdf_files = get_pdf_files(RAW_PDF_DIR)

    for pdf_file in pdf_files:
        try:
            raw_text = extract_text_from_pdf(pdf_file)
            cleaned_text = normalize_text(raw_text)

            contracts.append({
                "contract_id": pdf_file.stem,
                "filename": pdf_file.name,
                "text": cleaned_text
            })

            print(f"Processed {pdf_file.name}")

        except Exception as e:
            print(f"Skipped {pdf_file.name}: {e}")

    return contracts


def save_contracts(contracts):
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(contracts, f, indent=2, ensure_ascii=False)


def main():
    contracts = load_contracts()

    print(f"\nLoaded {len(contracts)} contracts")

    save_contracts(contracts)

    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()