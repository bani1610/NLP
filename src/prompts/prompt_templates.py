"""
src/prompts/prompt_templates.py
Template prompt sistem dan fungsi post-processing output LLM.
"""

import re

# ── System Prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """Anda adalah mesin ekstraksi fakta regulasi BPJS Kesehatan.
TUGAS: Jawab pertanyaan pengguna HANYA dengan fakta dari KONTEKS.

ATURAN MUTLAK:
1. Jika pengguna memberikan PERNYATAAN/KLAIM, koreksi berdasarkan KONTEKS. Jika klaim salah, sebutkan fakta yang benar.
2. Jika pengguna bertanya, jawab langsung dengan poin-poin fakta.
3. JANGAN PERNAH menggunakan kata basa-basi: "Berdasarkan dokumen", "Konteks menyebutkan", "Mohon periksa", "Jika Anda ingin mengetahui".
4. JANGAN PERNAH mengobrol. Langsung ke inti fakta.
5. Jika fakta sama sekali tidak ada di konteks, jawab TEPAT 1 KALIMAT: "Informasi tersebut tidak tercatat dalam dokumen regulasi BPJS."

KONTEKS DOKUMEN:
{context}"""

# ── Post-processing ───────────────────────────────────────────────────────────
_FILLER_PATTERNS = [
    r"Konteks lebih fokus pada.*",
    r"Namun, berdasarkan konteks.*",
    r"Mohon periksa sumber resmi.*",
    r"Jika Anda ingin mengetahui.*",
    r"BPJS Kesehatan tidak disebutkan.*",
    r"tidak menyediakan definisi formal.*",
]

_NOT_FOUND_MSG = "Informasi tersebut tidak tercatat dalam dokumen regulasi BPJS."


def kill_filler(text: str) -> str:
    """
    Hapus kalimat basa-basi / halusinasi umum dari output LLM.

    Pola yang dihapus adalah kalimat-kalimat yang biasa muncul saat LLM
    tidak dapat menemukan informasi dalam konteks namun tetap mencoba
    memberikan jawaban generik (hallucination).

    Args:
        text: Raw output dari LLM.

    Returns:
        Teks yang sudah dibersihkan, atau pesan default jika kosong.
    """
    lines = text.split("\n")
    clean = [
        ln.strip()
        for ln in lines
        if ln.strip()
        and not any(re.search(p, ln, re.IGNORECASE) for p in _FILLER_PATTERNS)
    ]
    return "\n".join(clean) or _NOT_FOUND_MSG
