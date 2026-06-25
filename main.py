"""
main.py — Entry point BPJS Care Assistant
Mengorkestrasikan semua modul src/ untuk membangun dan menjalankan aplikasi RAG.
"""

import os
import sys
import yaml
from dotenv import load_dotenv

# ── Load .env untuk development lokal ─────────────────────────────────────────
load_dotenv()

# ── Load konfigurasi dari config.yaml ─────────────────────────────────────────
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

PDF_DIR     = cfg["pdf_dir"]
FAISS_PATH  = cfg["faiss_index"]
EMB_MODEL   = cfg["embedding"]["model"]
LLM_MODEL   = cfg["llm"]["model"]
LLM_TEMP    = cfg["llm"]["temperature"]
LLM_MAXTOK  = cfg["llm"]["max_tokens"]
CHUNK_SIZE  = cfg["chunking"]["chunk_size"]
CHUNK_OVR   = cfg["chunking"]["chunk_overlap"]
TOP_K       = cfg["retrieval"]["top_k"]
GROQ_KEY    = os.environ.get("GROQ_API_KEY", "")

# ── Import modul src/ ──────────────────────────────────────────────────────────
from src.embeddings.embedder   import get_embeddings
from src.vectordb.vector_store import build_or_load_vectorstore
from src.llm.llm_client        import get_llm
from src.retrieval.retriever   import build_rag_chain
from src.ui.gradio_app         import build_ui


def main():
    print("=" * 55)
    print("  BPJS Care Assistant — RAG Chatbot")
    print("=" * 55)

    # Step 1 — Embedding model (Teknologi 2: Transformer/HuggingFace)
    embeddings = get_embeddings(EMB_MODEL)

    # Step 2 — Vector store (Teknologi 1: RAG + FAISS)
    vectorstore = build_or_load_vectorstore(
        pdf_dir=PDF_DIR,
        faiss_path=FAISS_PATH,
        embeddings=embeddings,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVR,
    )

    # Step 3 — LLM via Groq API
    llm = get_llm(
        model=LLM_MODEL,
        api_key=GROQ_KEY,
        temperature=LLM_TEMP,
        max_tokens=LLM_MAXTOK,
    )

    # Step 4 — RAG chain
    rag_chain = build_rag_chain(vectorstore, llm, top_k=TOP_K)

    # Step 5 — Gradio UI
    demo = build_ui(rag_chain)

    print("=" * 55)
    print("  Sistem siap digunakan!")
    print("=" * 55)

    demo.launch()


if __name__ == "__main__":
    main()
