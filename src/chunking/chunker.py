"""
src/chunking/chunker.py
Memecah dokumen menjadi chunk-chunk kecil untuk diindeks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents: list, chunk_size: int, chunk_overlap: int) -> list:
    """
    Memecah list of Documents menjadi chunk-chunk teks.

    Args:
        documents:     List of LangChain Document objects.
        chunk_size:    Ukuran maksimal tiap chunk (karakter).
        chunk_overlap: Jumlah karakter overlap antar chunk.

    Returns:
        List of chunk Documents.

    Raises:
        RuntimeError: Jika tidak ada chunk yang dihasilkan.
    """
    print(f"[Chunking] Memecah {len(documents)} halaman "
          f"(chunk_size={chunk_size}, overlap={chunk_overlap})")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_documents(documents)

    if not chunks:
        raise RuntimeError(
            "PDF tidak menghasilkan chunk teks. "
            "Periksa apakah file PDF valid dan berisi teks yang dapat diekstrak."
        )

    print(f"[Chunking] Total chunks: {len(chunks)}")
    return chunks
