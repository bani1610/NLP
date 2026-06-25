"""
src/vectordb/vector_store.py
Mengelola FAISS vector store — build, save, dan load index.
"""

import os

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_or_load_vectorstore(
    pdf_dir: str,
    faiss_path: str,
    embeddings: HuggingFaceEmbeddings,
    chunk_size: int,
    chunk_overlap: int,
) -> FAISS:
    """
    Muat FAISS index dari disk jika sudah ada, atau bangun ulang dari PDF.

    Alur saat index belum ada:
        1. Load PDF via ingestion.loader
        2. Split via chunking.chunker
        3. Embed tiap chunk dengan HuggingFaceEmbeddings
        4. Simpan FAISS index ke disk

    Args:
        pdf_dir:       Folder berisi file-file PDF.
        faiss_path:    Path folder untuk menyimpan/memuat FAISS index.
        embeddings:    Model embedding yang sudah diinisialisasi.
        chunk_size:    Ukuran chunk (karakter).
        chunk_overlap: Overlap antar chunk.

    Returns:
        FAISS vectorstore object yang siap digunakan sebagai retriever.
    """
    # ── Load dari disk jika index sudah ada ──────────────────────────────────
    if os.path.exists(faiss_path):
        print(f"[VectorDB] Memuat FAISS index dari: '{faiss_path}'")
        return FAISS.load_local(
            faiss_path, embeddings, allow_dangerous_deserialization=True
        )

    # ── Build ulang dari PDF ──────────────────────────────────────────────────
    print("[VectorDB] FAISS index tidak ditemukan. Membangun dari PDF...")

    from src.ingestion.loader import load_documents
    from src.chunking.chunker import split_documents

    documents = load_documents(pdf_dir)
    chunks = split_documents(documents, chunk_size, chunk_overlap)

    print("[VectorDB] Membuat FAISS index dari chunks...")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(faiss_path)
    print(f"[VectorDB] FAISS index disimpan ke: '{faiss_path}'")

    return vectorstore
