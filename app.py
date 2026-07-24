import json
import fitz  # PyMuPDF
import streamlit as st
from src.llm_client import generate_response
from src.prompts import ANALYSIS_PROMPT
from src.semantic_search import SemanticSearch



st.set_page_config(
    page_title="Contract Intelligence",
    layout="centered",
)

def extract_text_from_pdf(uploaded_file) -> str:
    
    file_bytes = uploaded_file.read()
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages_text).strip()


def build_prompt(template: str, contract_text: str) -> str:
    
    if "{contract_text}" in template:
        return template.format(contract_text=contract_text)
    return f"{template}\n\nContract:\n{contract_text}"


@st.cache_resource
def get_semantic_search_index():
    
    searcher = SemanticSearch()
    searcher.build_index()
    return searcher


def get_result_field(result, *keys, default="N/A"):

    for key in keys:
        if isinstance(result, dict) and key in result:
            return result[key]
        if hasattr(result, key):
            return getattr(result, key)
    return default

st.title("Contract Intelligence")
st.write("Analyze legal agreements using Large Language Models.")

st.divider()


st.header("Analyze a Contract")

uploaded_file = st.file_uploader("Choose PDF", type=["pdf"])
analyze_clicked = st.button("Analyze")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if analyze_clicked:
    if uploaded_file is None:
        st.warning("Please upload a PDF contract before analyzing.")
    else:
        with st.spinner("Extracting text from PDF..."):
            try:
                contract_text = extract_text_from_pdf(uploaded_file)
            except Exception as e:
                st.error(f"Failed to extract text from PDF: {e}")
                st.stop()

        with st.spinner("Analyzing contract..."):
            try:
                contract_text = contract_text[:25000]

                analysis_prompt = build_prompt(
                    ANALYSIS_PROMPT,
                    contract_text
                )
                raw_response = generate_response(analysis_prompt)
            except Exception:
                st.error(
                    "Analysis could not be completed.\n\n"
                    "This application uses the free Google Gemini API. "
                    "The free tier occasionally reaches its request quota.\n\n"
                    "Please wait a few minutes and try again."
                )
                st.stop()

        try:
            parsed = json.loads(raw_response)
            st.session_state.analysis_result = {
                "filename": uploaded_file.name,
                "summary": parsed.get("summary", "Not found"),
                "termination_clause": parsed.get("termination_clause", "Not found"),
                "confidentiality_clause": parsed.get("confidentiality_clause", "Not found"),
                "liability_clause": parsed.get("liability_clause", "Not found"),
            }
        except (json.JSONDecodeError, TypeError):
            st.error(
                "Gemini returned an unexpected response format. Please try again."
            )
            st.stop()


if st.session_state.analysis_result:
    result = st.session_state.analysis_result

    st.divider()
    st.header("Analysis Results")

    with st.expander("Summary", expanded=True):
        st.write(result["summary"])

    with st.expander("Termination Clause"):
        st.write(result["termination_clause"])

    with st.expander("Confidentiality Clause"):
        st.write(result["confidentiality_clause"])

    with st.expander("Liability Clause"):
        st.write(result["liability_clause"])

    download_payload = {
        "summary": result["summary"],
        "termination_clause": result["termination_clause"],
        "confidentiality_clause": result["confidentiality_clause"],
        "liability_clause": result["liability_clause"],
    }

    st.download_button(
        "Download Analysis (JSON)",
        data=json.dumps(download_payload, indent=2),
        file_name=f"{result['filename']}_analysis.json",
        mime="application/json",
    )

st.divider()


st.header("Semantic Search")

search_query = st.text_input("Search")
search_clicked = st.button("Search", key="search_button")

if search_clicked:
    if not search_query.strip():
        st.warning("Please enter a search query.")
    else:
        with st.spinner("Searching..."):
            try:
                searcher = get_semantic_search_index()
                results = searcher.search(search_query)
            except Exception as e:
                st.error(f"Semantic search failed: {e}")
                results = None

        if results is not None:
            if len(results) == 0:
                st.warning("No matching clauses found.")
            else:
                for result in results:
                    filename = get_result_field(result, "filename", "file_name", "contract_id")
                    clause_type = get_result_field(result, "clause_type", "type", "label")
                    score = get_result_field(result, "score", "similarity", "similarity_score")
                    clause_text = get_result_field(result, "text", "clause_text", "content")

                    st.markdown(f"**Filename:** {filename}")
                    st.markdown(f"**Clause Type:** {clause_type}")
                    st.markdown(f"**Similarity Score:** {float(score) * 100:.1f}%")
                    st.write(clause_text)
                    st.divider()