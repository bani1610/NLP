"""
src/embeddings/embedder.py
Membuat model embedding HuggingFace untuk mengubah teks menjadi vektor.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings(model_name: str) -> HuggingFaceEmbeddings:
    """
    Inisialisasi model embedding dari HuggingFace.

    Menggunakan sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
    (default) yang mendukung Bahasa Indonesia dan 50+ bahasa lainnya.

    Arsitektur: BERT-based, 12-layer Transformer, 384 dimensi vektor.

    Args:
        model_name: Nama model HuggingFace (dari config.yaml).

    Returns:
        HuggingFaceEmbeddings object siap digunakan.
    """
    print(f"[Embeddings] Memuat model: {model_name}")
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    print("[Embeddings] Model embedding siap.")
    return embeddings
