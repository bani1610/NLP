"""
src/ingestion/loader.py
Memuat seluruh dokumen PDF dari folder dataset.
"""

from langchain_community.document_loaders import PyPDFDirectoryLoader


def load_documents(pdf_dir: str) -> list:
    """
    Load semua file PDF dari pdf_dir.

    Args:
        pdf_dir: Path ke folder berisi file-file PDF.

    Returns:
        List of LangChain Document objects (satu per halaman PDF).

    Raises:
        RuntimeError: Jika tidak ada PDF yang terbaca.
    """
    print(f"[Ingestion] Memuat PDF dari folder: '{pdf_dir}'")
    loader = PyPDFDirectoryLoader(pdf_dir)
    documents = loader.load()

    if not documents:
        raise RuntimeError(
            f"Tidak ada PDF yang terbaca dari folder '{pdf_dir}'. "
            "Pastikan file PDF tersedia dan nama folder benar."
        )

    print(f"[Ingestion] Total halaman terbaca: {len(documents)}")
    return documents
