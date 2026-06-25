"""
src/llm/llm_client.py
Inisialisasi Large Language Model via Groq API.
"""

from langchain_groq import ChatGroq


def get_llm(
    model: str,
    api_key: str,
    temperature: float = 0.1,
    max_tokens: int = 512,
) -> ChatGroq:
    """
    Inisialisasi Groq LLM client.

    Menggunakan Groq API (LPU — Language Processing Unit) sehingga inferensi
    sangat cepat (~2-4 detik) tanpa memerlukan GPU di sisi deployment.

    Model default: llama-3.3-70b-versatile
    - 70B parameter decoder-only Transformer
    - Mendukung Bahasa Indonesia
    - Temperature 0.1 → jawaban deterministik, minim halusinasi

    Args:
        model:       Nama model Groq (dari config.yaml).
        api_key:     GROQ_API_KEY dari environment / HF Secrets.
        temperature: Tingkat keacakan output (0.0 = deterministik).
        max_tokens:  Panjang maksimal output per respons.

    Returns:
        ChatGroq object siap digunakan dalam chain.

    Raises:
        ValueError: Jika api_key kosong.
    """
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY belum diset! "
            "Lokal: isi file .env | HuggingFace: Settings → Secrets."
        )

    print(f"[LLM] Menggunakan Groq model: {model}")
    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=temperature,
        max_tokens=max_tokens,
    )
