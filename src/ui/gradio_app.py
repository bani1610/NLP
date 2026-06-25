"""
src/ui/gradio_app.py
Antarmuka Gradio dengan tiga tab: Chatbot, Evaluasi Q&A, Teknologi.
"""

import gradio as gr

# ── Data evaluasi Q&A ────────────────────────────────────────────────────────
QA_EVAL_DATA = [
    {
        "no": "1",
        "pertanyaan": "Apa itu BPJS Kesehatan?",
        "jawaban": "BPJS Kesehatan adalah badan hukum publik yang dibentuk untuk menyelenggarakan program Jaminan Kesehatan Nasional (JKN) berdasarkan Undang-Undang No. 24 Tahun 2011.",
        "status": "✅ Akurat",
    },
    {
        "no": "2",
        "pertanyaan": "Berapa besar denda keterlambatan pembayaran iuran?",
        "jawaban": "Denda keterlambatan adalah 2,5% per bulan dari total biaya pelayanan yang ditagihkan, dengan maksimal 30% dari total biaya.",
        "status": "✅ Akurat",
    },
    {
        "no": "3",
        "pertanyaan": "Apa saja yang ditanggung BPJS dalam program Prolanis?",
        "jawaban": "Prolanis mencakup konsultasi medis, pemeriksaan laboratorium, obat Formularium Nasional, dan edukasi kesehatan untuk Diabetes Melitus Tipe 2 dan Hipertensi.",
        "status": "✅ Akurat",
    },
    {
        "no": "4",
        "pertanyaan": "Bagaimana prosedur mendaftarkan bayi baru lahir?",
        "jawaban": "Bayi baru lahir wajib didaftarkan paling lambat 28 hari setelah lahir di kantor BPJS terdekat dengan melampirkan akta kelahiran dan kartu keluarga.",
        "status": "✅ Akurat",
    },
    {
        "no": "5",
        "pertanyaan": "Apakah operasi plastik ditanggung BPJS?",
        "jawaban": "Operasi plastik kosmetik/estetika TIDAK ditanggung. Yang ditanggung hanya bedah plastik rekonstruktif akibat kecelakaan atau kelainan bawaan.",
        "status": "✅ Akurat",
    },
    {
        "no": "6",
        "pertanyaan": "Bagaimana prosedur jika kondisi gawat darurat?",
        "jawaban": "Dalam kondisi gawat darurat, peserta dapat langsung ke IGD fasilitas kesehatan terdekat tanpa rujukan, termasuk fasilitas non-jaringan BPJS.",
        "status": "✅ Akurat",
    },
    {
        "no": "7",
        "pertanyaan": "Berapa lama masa tunggu peserta baru?",
        "jawaban": "Peserta PBPU yang baru mendaftar memiliki masa tunggu 14 hari sebelum dapat menggunakan manfaat rawat inap.",
        "status": "✅ Akurat",
    },
    {
        "no": "8",
        "pertanyaan": "Apa itu peserta PBI?",
        "jawaban": "PBI (Penerima Bantuan Iuran) adalah peserta JKN yang iurannya dibayarkan pemerintah, terdiri dari fakir miskin dan orang tidak mampu.",
        "status": "✅ Akurat",
    },
    {
        "no": "9",
        "pertanyaan": "Apakah layanan gigi ditanggung BPJS?",
        "jawaban": "BPJS menanggung pelayanan gigi dasar (pencabutan, penambalan, karang gigi) di FKTP. Perawatan gigi estetika tidak ditanggung.",
        "status": "✅ Akurat",
    },
    {
        "no": "10",
        "pertanyaan": "Berapa iuran BPJS untuk kelas 1, 2, dan 3?",
        "jawaban": "Informasi tersebut tidak tercatat dalam dokumen regulasi BPJS yang tersedia dalam sistem ini.",
        "status": "⚠️ Out-of-scope (ditolak dengan benar)",
    },
]


def build_ui(rag_chain) -> gr.Blocks:
    """
    Membangun antarmuka Gradio dengan tiga tab.

    Tab 1 — Chatbot    : Interface tanya-jawab utama.
    Tab 2 — Evaluasi   : Tabel Q&A hasil pengujian + metrik.
    Tab 3 — Teknologi  : Penjelasan RAG + Transformer + pipeline.

    Args:
        rag_chain: LangChain RAG chain yang sudah dibangun oleh retriever.

    Returns:
        gr.Blocks demo object, siap di-launch.
    """
    def chatbot_bpjs(message: str, history: list) -> str:
        if not message.strip():
            return "Silakan ketik pertanyaan Anda."
        try:
            return rag_chain.invoke(message)
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    with gr.Blocks(theme=gr.themes.Soft(), title="BPJS Care Assistant") as demo:
        gr.Markdown(
            """
            # 🏥 BPJS Care Assistant
            Asisten virtual berbasis **RAG (Retrieval-Augmented Generation)** untuk menjawab pertanyaan
            seputar regulasi BPJS Kesehatan secara akurat dari dokumen resmi.

            📄 **Sumber:** Perpres 82/2018 · Perban No.1/2024 · Perban No.2/2024 · Perban No.3/2024 · Buku Saku JKN-KIS
            """
        )

        with gr.Tabs():
            # ── TAB 1: CHATBOT ───────────────────────────────────────────────
            with gr.TabItem("💬 Chatbot"):
                gr.ChatInterface(
                    fn=chatbot_bpjs,
                    examples=[
                        "Apa itu BPJS Kesehatan?",
                        "Berapa besar denda keterlambatan pembayaran iuran?",
                        "Apa saja penyakit yang ditanggung dalam program Prolanis?",
                        "Bagaimana prosedur mendaftarkan bayi baru lahir?",
                        "Apakah operasi plastik ditanggung BPJS?",
                        "Bagaimana prosedur jika kondisi gawat darurat?",
                    ],
                    type="messages",
                )

            # ── TAB 2: EVALUASI Q&A ──────────────────────────────────────────
            with gr.TabItem("📊 Evaluasi Q&A"):
                gr.Markdown("""
                ## Hasil Evaluasi Sistem
                Pengujian dilakukan dengan 10 pertanyaan representatif seputar regulasi BPJS Kesehatan.

                | Metrik | Nilai |
                |---|---|
                | Jawaban Akurat | **9 / 10 (90%)** |
                | Out-of-scope Ditolak dengan Benar | **1 / 10** |
                | Halusinasi Terdeteksi | **0 / 10 (0%)** |
                | Rata-rata Waktu Respons | **~2–4 detik** |
                """)

                eval_headers = ["No", "Pertanyaan", "Jawaban Sistem", "Status"]
                eval_rows = [
                    [d["no"], d["pertanyaan"], d["jawaban"], d["status"]]
                    for d in QA_EVAL_DATA
                ]
                gr.Dataframe(
                    headers=eval_headers,
                    value=eval_rows,
                    wrap=True,
                    interactive=False,
                    label="Tabel Evaluasi Q&A (10 Pertanyaan Uji)",
                )

            # ── TAB 3: TEKNOLOGI ─────────────────────────────────────────────
            with gr.TabItem("⚙️ Teknologi"):
                gr.Markdown("""
                ## Teknologi yang Digunakan

                ### Teknologi 1 — RAG (LangChain + FAISS)
                - **Framework:** LangChain 0.3.25
                - **Vector Store:** FAISS (Facebook AI Similarity Search)
                - **Retriever:** Top-K=5 chunks per query
                - **LLM:** Groq API — llama-3.3-70b-versatile

                ### Teknologi 2 — Transformer / HuggingFace
                - **Model:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
                - **Arsitektur:** BERT-based, 12-layer Transformer, 384 dimensi vektor
                - **Bahasa:** Multilingual (50+ bahasa termasuk Bahasa Indonesia)

                ## Pipeline Sistem
                ```
                [PDF Regulasi BPJS]
                        ↓
                src/ingestion/loader.py       → PyPDFDirectoryLoader
                        ↓
                src/chunking/chunker.py       → RecursiveCharacterTextSplitter
                (chunk_size=800, overlap=150)
                        ↓
                src/embeddings/embedder.py    → HuggingFaceEmbeddings (Teknologi 2)
                (MiniLM-L12-v2, 384 dim)
                        ↓
                src/vectordb/vector_store.py  → FAISS Index (Teknologi 1 — RAG)
                        ↓
                src/retrieval/retriever.py    → Top-K=5 Retriever + RAG Chain
                        ↓
                src/prompts/prompt_templates.py → System Prompt + kill_filler()
                        ↓
                src/llm/llm_client.py         → Groq LLM (llama-3.3-70b)
                        ↓
                [Jawaban Faktual → User]
                ```

                ## Struktur Proyek
                ```
                chatbot_bpjs/
                ├── main.py             # Entry point
                ├── config.yaml         # Konfigurasi terpusat
                ├── .env                # API keys (lokal)
                ├── src/
                │   ├── ingestion/      # Load PDF
                │   ├── chunking/       # Split teks
                │   ├── embeddings/     # HuggingFace Transformer
                │   ├── vectordb/       # FAISS
                │   ├── retrieval/      # RAG Chain
                │   ├── prompts/        # Prompt templates
                │   ├── llm/            # Groq LLM client
                │   └── ui/             # Gradio UI
                └── dataset/            # PDF regulasi BPJS
                ```
                """)

    return demo
