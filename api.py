"""
api.py — FastAPI backend untuk BPJS Care Assistant
Mengekspose RAG pipeline sebagai REST API dan menyajikan frontend statis.
"""

import os
import sys
import yaml
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# ── Load konfigurasi ──────────────────────────────────────────────────────────
with open("config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

PDF_DIR    = cfg["pdf_dir"]
FAISS_PATH = cfg["faiss_index"]
EMB_MODEL  = cfg["embedding"]["model"]
LLM_MODEL  = cfg["llm"]["model"]
LLM_TEMP   = cfg["llm"]["temperature"]
LLM_MAXTOK = cfg["llm"]["max_tokens"]
CHUNK_SIZE = cfg["chunking"]["chunk_size"]
CHUNK_OVR  = cfg["chunking"]["chunk_overlap"]
TOP_K      = cfg["retrieval"]["top_k"]
GROQ_KEY   = os.environ.get("GROQ_API_KEY", "")

# ── Import modul src/ ─────────────────────────────────────────────────────────
from src.embeddings.embedder   import get_embeddings
from src.vectordb.vector_store import build_or_load_vectorstore
from src.llm.llm_client        import get_llm
from src.retrieval.retriever   import build_rag_chain

# ── State global untuk menyimpan RAG chain ────────────────────────────────────
rag_chain = None


# ── Data evaluasi Q&A (sama dengan gradio_app.py) ────────────────────────────
QA_EVAL_DATA = [
    {
        "no": "1",
        "pertanyaan": "Apa itu BPJS Kesehatan?",
        "jawaban": "BPJS Kesehatan adalah badan hukum publik yang dibentuk untuk menyelenggarakan program Jaminan Kesehatan Nasional (JKN) berdasarkan Undang-Undang No. 24 Tahun 2011.",
        "status": "Akurat",
    },
    {
        "no": "2",
        "pertanyaan": "Berapa besar denda keterlambatan pembayaran iuran?",
        "jawaban": "Denda keterlambatan adalah 2,5% per bulan dari total biaya pelayanan yang ditagihkan, dengan maksimal 30% dari total biaya.",
        "status": "Akurat",
    },
    {
        "no": "3",
        "pertanyaan": "Apa saja yang ditanggung BPJS dalam program Prolanis?",
        "jawaban": "Prolanis mencakup konsultasi medis, pemeriksaan laboratorium, obat Formularium Nasional, dan edukasi kesehatan untuk Diabetes Melitus Tipe 2 dan Hipertensi.",
        "status": "Akurat",
    },
    {
        "no": "4",
        "pertanyaan": "Bagaimana prosedur mendaftarkan bayi baru lahir?",
        "jawaban": "Bayi baru lahir wajib didaftarkan paling lambat 28 hari setelah lahir di kantor BPJS terdekat dengan melampirkan akta kelahiran dan kartu keluarga.",
        "status": "Akurat",
    },
    {
        "no": "5",
        "pertanyaan": "Apakah operasi plastik ditanggung BPJS?",
        "jawaban": "Operasi plastik kosmetik/estetika TIDAK ditanggung. Yang ditanggung hanya bedah plastik rekonstruktif akibat kecelakaan atau kelainan bawaan.",
        "status": "Akurat",
    },
    {
        "no": "6",
        "pertanyaan": "Bagaimana prosedur jika kondisi gawat darurat?",
        "jawaban": "Dalam kondisi gawat darurat, peserta dapat langsung ke IGD fasilitas kesehatan terdekat tanpa rujukan, termasuk fasilitas non-jaringan BPJS.",
        "status": "Akurat",
    },
    {
        "no": "7",
        "pertanyaan": "Berapa lama masa tunggu peserta baru?",
        "jawaban": "Peserta PBPU yang baru mendaftar memiliki masa tunggu 14 hari sebelum dapat menggunakan manfaat rawat inap.",
        "status": "Akurat",
    },
    {
        "no": "8",
        "pertanyaan": "Apa itu peserta PBI?",
        "jawaban": "PBI (Penerima Bantuan Iuran) adalah peserta JKN yang iurannya dibayarkan pemerintah, terdiri dari fakir miskin dan orang tidak mampu.",
        "status": "Akurat",
    },
    {
        "no": "9",
        "pertanyaan": "Apakah layanan gigi ditanggung BPJS?",
        "jawaban": "BPJS menanggung pelayanan gigi dasar (pencabutan, penambalan, karang gigi) di FKTP. Perawatan gigi estetika tidak ditanggung.",
        "status": "Akurat",
    },
    {
        "no": "10",
        "pertanyaan": "Berapa iuran BPJS untuk kelas 1, 2, dan 3?",
        "jawaban": "Informasi tersebut tidak tercatat dalam dokumen regulasi BPJS yang tersedia dalam sistem ini.",
        "status": "Out-of-scope (ditolak dengan benar)",
    },
]


# ── Lifespan: inisialisasi RAG saat startup ───────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_chain
    print("=" * 55)
    print("  BPJS Care Assistant — FastAPI Server")
    print("=" * 55)

    embeddings  = get_embeddings(EMB_MODEL)
    vectorstore = build_or_load_vectorstore(
        pdf_dir=PDF_DIR,
        faiss_path=FAISS_PATH,
        embeddings=embeddings,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVR,
    )
    llm = get_llm(
        model=LLM_MODEL,
        api_key=GROQ_KEY,
        temperature=LLM_TEMP,
        max_tokens=LLM_MAXTOK,
    )
    rag_chain = build_rag_chain(vectorstore, llm, top_k=TOP_K)
    print("  Sistem siap digunakan!")
    print("=" * 55)
    yield
    # Cleanup (jika diperlukan)


# ── Inisialisasi FastAPI ──────────────────────────────────────────────────────
app = FastAPI(
    title="BPJS Care Assistant API",
    description="REST API untuk chatbot RAG BPJS Kesehatan",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — izinkan semua origin saat development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic models ───────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


# ── API Endpoints ─────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Cek status server dan model yang digunakan."""
    return {
        "status": "ok",
        "model": LLM_MODEL,
        "embedding": EMB_MODEL,
        "rag_ready": rag_chain is not None,
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Terima pertanyaan user, proses melalui RAG pipeline,
    kembalikan jawaban dalam Bahasa Indonesia.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong.")

    if rag_chain is None:
        raise HTTPException(status_code=503, detail="RAG pipeline belum siap, coba lagi sebentar.")

    try:
        answer = rag_chain.invoke(request.message)
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")


@app.get("/api/evaluation")
async def get_evaluation():
    """Kembalikan data evaluasi Q&A dan metrik sistem."""
    return {
        "metrics": {
            "accuracy": "90%",
            "correct_count": 9,
            "total_count": 10,
            "hallucination_count": 0,
            "avg_response_time": "2–4 detik",
            "out_of_scope_handled": 1,
        },
        "qa_data": QA_EVAL_DATA,
    }


# ── Serve frontend statis ─────────────────────────────────────────────────────
# Mount SETELAH semua API route agar tidak konflik
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
