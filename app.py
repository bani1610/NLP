"""
BPJS Care Assistant - RAG Chatbot
Deploy: HuggingFace Spaces (Gradio) — CPU Free Tier
LLM   : Groq API (llama-3.3-70b-versatile) — gratis, cepat
Embed : sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
Vector: FAISS
"""

import os
import re
import gradio as gr

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# ============================================================
# KONFIGURASI
# ============================================================
PDF_DIR         = "dataset"
FAISS_INDEX     = "faiss_index_bpjs"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Model Groq — gratis, tidak perlu GPU
# Opsi lain: "mixtral-8x7b-32768" / "gemma2-9b-it"
GROQ_MODEL    = "llama-3.3-70b-versatile"
GROQ_API_KEY  = os.environ.get("GROQ_API_KEY", "")  # Diset via HF Secrets

CHUNK_SIZE    = 800
CHUNK_OVERLAP = 150
TOP_K_RESULTS = 5

# ============================================================
# STEP 1 — LOAD & INDEX DOKUMEN PDF
# ============================================================
def build_vectorstore():
    """Build FAISS index dari PDF, atau load jika sudah ada."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    if os.path.exists(FAISS_INDEX):
        print("✅ Memuat FAISS index yang sudah ada...")
        return FAISS.load_local(
            FAISS_INDEX, embeddings, allow_dangerous_deserialization=True
        )

    print("🔄 Membangun FAISS index dari PDF...")
    loader = PyPDFDirectoryLoader(PDF_DIR)
    documents = loader.load()
    print(f"   📄 Total halaman terbaca : {len(documents)}")

    if not documents:
        raise RuntimeError(
            f"Tidak ada PDF yang terbaca dari folder '{PDF_DIR}'. "
            "Pastikan file PDF tersedia di dataset/ dan nama folder benar."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    texts = splitter.split_documents(documents)
    print(f"   🔪 Total chunks          : {len(texts)}")

    if not texts:
        raise RuntimeError(
            f"PDF di folder '{PDF_DIR}' tidak menghasilkan chunk teks. "
            "Periksa apakah file PDF valid dan berisi teks yang dapat diekstrak."
        )

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(FAISS_INDEX)
    print("✅ FAISS index berhasil disimpan.")
    return vectorstore


# ============================================================
# STEP 2 — INISIALISASI LLM via Groq API
# ============================================================
def build_llm():
    """Inisialisasi Groq LLM — tidak perlu GPU, gratis."""
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY belum diset! "
            "Tambahkan di HuggingFace Space → Settings → Secrets."
        )
    print(f"✅ Groq LLM siap: {GROQ_MODEL}")
    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0.1,
        max_tokens=512,
    )


# ============================================================
# STEP 3 — BANGUN RAG CHAIN
# ============================================================
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


def kill_filler(text: str) -> str:
    """Hapus paksa kalimat basa-basi / halusinasi LLM."""
    patterns_to_remove = [
        r"Konteks lebih fokus pada.*",
        r"Namun, berdasarkan konteks.*",
        r"Mohon periksa sumber resmi.*",
        r"Jika Anda ingin mengetahui.*",
        r"BPJS Kesehatan tidak disebutkan.*",
        r"tidak menyediakan definisi formal.*",
    ]
    lines = text.split("\n")
    clean = [
        ln.strip()
        for ln in lines
        if ln.strip()
        and not any(re.search(p, ln, re.IGNORECASE) for p in patterns_to_remove)
    ]
    return "\n".join(clean) or "Informasi tersebut tidak tercatat dalam dokumen regulasi BPJS."


def build_rag_chain(vectorstore, llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K_RESULTS})
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
        | RunnableLambda(kill_filler)
    )
    return chain


# ============================================================
# INISIALISASI SAAT STARTUP
# ============================================================
print("=" * 50)
print("🚀 Memulai BPJS Care Assistant (Groq)...")
print("=" * 50)

vectorstore = build_vectorstore()
llm         = build_llm()
rag_chain   = build_rag_chain(vectorstore, llm)

print("=" * 50)
print("✅ Sistem siap digunakan!")
print("=" * 50)

GROQ_API_KEY  = "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"

# ============================================================
# GRADIO UI
# ============================================================
def chatbot_bpjs(message: str, history: list) -> str:
    if not message.strip():
        return "Silakan ketik pertanyaan Anda."
    try:
        return rag_chain.invoke(message)
    except Exception as e:
        return f"⚠️ Terjadi kesalahan: {str(e)}"


demo = gr.ChatInterface(
    fn=chatbot_bpjs,
    title="🏥 BPJS Care Assistant",
    description=(
        "Asisten virtual berbasis **RAG (Retrieval-Augmented Generation)** "
        "untuk menjawab pertanyaan seputar regulasi BPJS Kesehatan.\n\n"
        "📄 **Sumber:** Perpres 82/2018 · Perban No.2/2024 · Perban No.3/2024 · Buku Saku JKN-KIS"
    ),
    examples=[
        "Apa itu BPJS Kesehatan?",
        "Berapa besar denda keterlambatan pembayaran iuran?",
        "Apa saja penyakit yang ditanggung dalam program Prolanis?",
        "Bagaimana prosedur mendaftarkan bayi baru lahir?",
        "Apakah operasi plastik ditanggung BPJS?",
        "Bagaimana prosedur jika kondisi gawat darurat?",
    ],
    theme=gr.themes.Soft(),
    type="messages",
)

if __name__ == "__main__":
    demo.launch()