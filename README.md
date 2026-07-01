---
title: BPJS Care Assistant
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
---

# BPJS Care Assistant — RAG Chatbot

Chatbot berbasis **Retrieval-Augmented Generation (RAG)** untuk menjawab pertanyaan seputar regulasi BPJS Kesehatan secara akurat berdasarkan dokumen resmi.

**Platform:** HuggingFace Spaces — https://huggingface.co/spaces/punn78/chatbot_bpjs

---

## Gambaran Umum
Projek AKhir Matakuliah NLP

- **Domain:** Kesehatan & Pelayanan Publik Pemerintah
- **Jenis Aplikasi:** Chatbot + RAG sederhana
- **Bahasa Dokumen:** Bahasa Indonesia

---

## Struktur Folder Lengkap

```
chatbot_bpjs/
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── .gitattributes
├── dataset/
│   ├── ps82-2018.pdf
│   ├── peraturan-bpjs-kesehatan-no-1-tahun-2024.pdf
│   ├── peraturan-bpjs-kesehatan-no-2-tahun-2024.pdf
│   ├── peraturan-bpjs-kesehatan-no-3-tahun-2024 (2).pdf
│   └── 4bd28c6ea8f022040f6eb93cfcd6e723.pdf
├── faiss_index_bpjs/           ← di-generate otomatis, tidak di-push ke repo
└── src/
    ├── __init__.py
    ├── ingestion/
    │   └── loader.py
    ├── chunking/
    │   └── chunker.py
    ├── embeddings/
    │   └── embedder.py
    ├── vectordb/
    │   └── vector_store.py
    ├── retrieval/
    │   └── retriever.py
    ├── prompts/
    │   └── prompt_templates.py
    ├── llm/
    │   └── llm_client.py
    └── ui/
        └── gradio_app.py
```

---

## Penjelasan File per File

### `main.py` — Entry Point Aplikasi

Menjalankan server **FastAPI** via uvicorn (port 7860).
Saat startup, `api.py` menginisialisasi RAG pipeline dan menyajikan frontend statis dari folder `frontend/`.

> HuggingFace Spaces menjalankan container Docker yang memanggil `python main.py`.

---

### `config.yaml` — Konfigurasi Terpusat

Menyimpan seluruh parameter sistem dalam satu file YAML agar mudah diubah
tanpa menyentuh kode Python:

| Parameter | Nilai | Keterangan |
|---|---|---|
| `pdf_dir` | `dataset` | Folder sumber dokumen PDF |
| `faiss_index` | `faiss_index_bpjs` | Folder penyimpanan FAISS index |
| `embedding.model` | `paraphrase-multilingual-MiniLM-L12-v2` | Model sentence-transformer |
| `llm.model` | `llama-3.3-70b-versatile` | Model LLM via Groq |
| `llm.temperature` | `0.1` | Rendah = jawaban deterministik |
| `llm.max_tokens` | `512` | Batas panjang output |
| `chunking.chunk_size` | `800` | Ukuran tiap potongan teks (karakter) |
| `chunking.chunk_overlap` | `150` | Overlap antar chunk |
| `retrieval.top_k` | `5` | Jumlah chunk relevan yang diambil |

---

### `requirements.txt` — Dependensi Python

| Library | Versi | Fungsi |
|---|---|---|
| `langchain` | 0.3.25 | Framework RAG utama (LCEL pipeline) |
| `langchain-community` | 0.3.24 | Connector: FAISS, HuggingFace, PyPDF |
| `langchain-groq` | 0.3.2 | Integrasi Groq API ke LangChain |
| `langchain-text-splitters` | 0.3.8 | RecursiveCharacterTextSplitter |
| `faiss-cpu` | 1.11.0 | Vector similarity search (CPU mode) |
| `pypdf` | 5.6.0 | Pembaca file PDF |
| `sentence-transformers` | 4.1.0 | Model embedding multilingual |
| `gradio` | 5.33.0 | Framework UI web interaktif |
| `huggingface_hub` | 0.32.4 | Integrasi HuggingFace Spaces |
| `pyyaml` | 6.0.2 | Pembaca file YAML |
| `python-dotenv` | 1.0.1 | Pembaca file `.env` untuk development lokal |

---

### `.env` — Konfigurasi Lokal (Tidak di-push ke Repo)

Menyimpan API key untuk keperluan pengembangan lokal:
```
GROQ_API_KEY="..."
```
File ini diabaikan oleh git (tercantum di `.gitignore`) sehingga tidak terekspos ke publik.
Di HuggingFace Spaces, variabel ini diset melalui **Settings → Secrets**.

---

### `.gitignore` — Filter Git

Mendefinisikan file/folder yang tidak di-push ke repository:
- `.env` — API key rahasia
- `faiss_index_bpjs/` — index FAISS yang dibangun otomatis saat startup
- `__pycache__/`, `*.pyc`, `*.pyo` — cache Python
- `.venv/` — virtual environment lokal
- `.DS_Store`, `Thumbs.db` — file sistem operasi

---

### `dataset/` — Korpus Dokumen Regulasi BPJS

Folder berisi 5 dokumen PDF resmi yang menjadi basis pengetahuan chatbot:

| File | Dokumen | Ukuran |
|---|---|---|
| `ps82-2018.pdf` | Perpres No. 82 Tahun 2018 tentang Jaminan Kesehatan | ~597 KB |
| `peraturan-bpjs-kesehatan-no-1-tahun-2024.pdf` | Perban No. 1/2024 — Petunjuk Teknis Administrasi | ~76 KB |
| `peraturan-bpjs-kesehatan-no-2-tahun-2024.pdf` | Perban No. 2/2024 — Pengelolaan Administrasi Kepesertaan | ~535 KB |
| `peraturan-bpjs-kesehatan-no-3-tahun-2024 (2).pdf` | Perban No. 3/2024 — Penjaminan Pelayanan Kesehatan | ~613 KB |
| `4bd28c6ea8f022040f6eb93cfcd6e723.pdf` | Buku Saku JKN-KIS (Panduan Peserta) | ~3.5 MB |

**Total: ±470 halaman** dokumen Bahasa Indonesia resmi.

---

### `faiss_index_bpjs/` — FAISS Vector Index (Auto-generated)

Folder ini **tidak disimpan di repository** karena dibangun otomatis saat pertama kali
aplikasi dijalankan. Berisi:
- `index.faiss` — file binary FAISS berisi vektor-vektor embedding
- `index.pkl` — metadata chunks (teks asli, sumber dokumen, nomor halaman)

Strategi: jika folder sudah ada, langsung dimuat dari disk (efisien);
jika belum ada, dibangun ulang dari PDF.

---

## Penjelasan Modul `src/`

### `src/ingestion/loader.py` — Pemuat Dokumen PDF

**Fungsi:** `load_documents(pdf_dir)`

Menggunakan `PyPDFDirectoryLoader` dari LangChain untuk membaca semua file PDF
dalam folder `dataset/`. Setiap halaman PDF menjadi satu objek `Document` LangChain
yang berisi teks halaman beserta metadata (nama file, nomor halaman).

**Output:** List of `Document` objects — satu per halaman PDF.

---

### `src/chunking/chunker.py` — Pemecah Teks

**Fungsi:** `split_documents(documents, chunk_size, chunk_overlap)`

Menggunakan `RecursiveCharacterTextSplitter` untuk memecah dokumen panjang menjadi
potongan-potongan kecil (chunk) agar dapat diembed dan di-retrieve secara efisien.

**Parameter kunci:**
- `chunk_size=800` — maksimal 800 karakter per chunk
- `chunk_overlap=150` — 150 karakter tumpang tindih antar chunk untuk menjaga konteks

Alasan overlap: agar informasi yang berada di batas antar chunk tidak hilang
saat retrieval dilakukan.

**Output:** List of chunk `Document` objects (ribuan chunk dari 470+ halaman).

---

### `src/embeddings/embedder.py` — Model Embedding (Teknologi 2)

**Fungsi:** `get_embeddings(model_name)`

Menginisialisasi model **sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2**
melalui `HuggingFaceEmbeddings`. Model ini merupakan implementasi Teknologi 2 (Transformer).

**Spesifikasi model:**

| Spesifikasi | Detail |
|---|---|
| Arsitektur | BERT-based, 12-layer Transformer |
| Dimensi vektor output | 384 dimensi |
| Dukungan bahasa | 50+ bahasa termasuk Bahasa Indonesia |
| Kegunaan | Sentence similarity / semantic search |

**Output:** `HuggingFaceEmbeddings` object yang mengubah teks menjadi vektor numerik.

---

### `src/vectordb/vector_store.py` — FAISS Vector Store (Teknologi 1)

**Fungsi:** `build_or_load_vectorstore(...)`

Merupakan inti dari Teknologi 1 (RAG). Mengelola siklus hidup FAISS index:

**Alur saat index belum ada (build):**
1. Panggil `load_documents()` — muat PDF
2. Panggil `split_documents()` — pecah jadi chunks
3. Embed tiap chunk dengan model embedding
4. Simpan seluruh vektor dalam FAISS index
5. Simpan index ke disk untuk penggunaan berikutnya

**Alur saat index sudah ada (load):**
- Langsung muat dari disk — jauh lebih cepat (detik vs menit)

FAISS (Facebook AI Similarity Search) adalah library pencarian vektor berdimensi tinggi
secara efisien menggunakan algoritma Approximate Nearest Neighbor (ANN).

---

### `src/retrieval/retriever.py` — RAG Chain Builder

**Fungsi:** `build_rag_chain(vectorstore, llm, top_k)`

Membangun pipeline RAG lengkap menggunakan **LCEL (LangChain Expression Language)**:

```
Pertanyaan User
      |
  Retriever        <- ambil top_k=5 chunk paling relevan dari FAISS
      |
ChatPromptTemplate <- gabungkan chunk (konteks) + pertanyaan ke dalam system prompt
      |
  Groq LLM         <- generate jawaban berdasarkan konteks
      |
StrOutputParser    <- ekstrak teks dari objek AIMessage
      |
kill_filler()      <- hapus kalimat basa-basi / halusinasi
      |
  Jawaban Akhir
```

FAISS retriever bekerja dengan cara: pertanyaan user diembed menjadi vektor,
lalu dicari 5 chunk dengan vektor paling mirip (cosine similarity) sebagai konteks.

---

### `src/prompts/prompt_templates.py` — System Prompt & Post-Processing

Berisi dua komponen anti-halusinasi:

**`SYSTEM_PROMPT`** — Instruksi ketat untuk LLM:
- Jawab HANYA berdasarkan konteks dokumen yang diberikan
- Jangan gunakan kalimat basa-basi seperti "Berdasarkan dokumen..."
- Jika informasi tidak ada, jawab tepat 1 kalimat baku

**`kill_filler(text)`** — Post-processor output LLM:
- Membersihkan kalimat halusinasi umum menggunakan regex pattern matching
- Pola yang dihapus: kalimat yang diawali "Namun, berdasarkan konteks...",
  "Mohon periksa sumber resmi...", "Jika Anda ingin mengetahui...", dll.
- Jika seluruh output terhapus, kembalikan pesan default baku

Kombinasi keduanya membentuk **sistem anti-halusinasi dua lapis**.

---

### `src/llm/llm_client.py` — Groq LLM Client

**Fungsi:** `get_llm(model, api_key, temperature, max_tokens)`

Menginisialisasi Large Language Model via **Groq API** menggunakan `ChatGroq`.

**Spesifikasi model `llama-3.3-70b-versatile`:**

| Spesifikasi | Detail |
|---|---|
| Parameter | 70 miliar |
| Arsitektur | Decoder-only Transformer |
| Dukungan bahasa | Multilingual termasuk Bahasa Indonesia |
| Inferensi | Groq LPU (Language Processing Unit) ~2-4 detik |
| Temperature | 0.1 (deterministik, minim halusinasi) |

Keunggulan Groq vs GPU lokal: tidak memerlukan GPU di sisi deployment,
seluruh komputasi inferensi dilakukan di server Groq.

---

### `src/ui/gradio_app.py` — Antarmuka Gradio

**Fungsi:** `build_ui(rag_chain)`

Membangun antarmuka web interaktif menggunakan **Gradio Blocks** dengan tiga tab:

**Tab 1 — Chatbot**
- `gr.ChatInterface` dengan fungsi `chatbot_bpjs(message, history)`
- Dilengkapi 6 contoh pertanyaan siap pakai
- Menampilkan riwayat percakapan dalam format pesan

**Tab 2 — Evaluasi Q&A**
- Menampilkan metrik evaluasi sistem (akurasi, halusinasi, waktu respons)
- Tabel `gr.Dataframe` berisi 10 pasang pertanyaan-jawaban hasil pengujian

**Tab 3 — Teknologi**
- Penjelasan Teknologi 1 (RAG + FAISS) dan Teknologi 2 (Transformer + HuggingFace)
- Diagram pipeline sistem dalam format ASCII
- Struktur folder proyek

---

## Alur Sistem End-to-End

### Startup

```
main.py
  |
  +-- Baca config.yaml
  +-- get_embeddings()          -> Load MiniLM-L12-v2 dari HuggingFace
  +-- build_or_load_vectorstore()
  |     +-- Jika index ada      -> load dari disk (cepat)
  |     +-- Jika belum ada      -> load PDF -> chunk -> embed -> simpan FAISS
  +-- get_llm()                 -> Inisialisasi ChatGroq (llama-3.3-70b)
  +-- build_rag_chain()         -> Rakit pipeline LCEL
  +-- build_ui().launch()       -> Jalankan Gradio web server
```

### Runtime — Per Query User

```
Pertanyaan User
  -> embed pertanyaan jadi vektor (384 dim)
  -> FAISS cari top-5 chunk paling relevan
  -> chunk + pertanyaan masuk ke system prompt
  -> Groq LLM generate jawaban (~2-4 detik)
  -> kill_filler() bersihkan output
  -> Tampilkan jawaban ke user
```

---

## Hasil Evaluasi

Pengujian dilakukan dengan 10 pertanyaan representatif seputar regulasi BPJS Kesehatan:

| Metrik | Nilai |
|---|---|
| Jawaban Akurat (sesuai dokumen) | **9 / 10 (90%)** |
| Out-of-scope Ditolak dengan Benar | **1 / 10** |
| Halusinasi Terdeteksi | **0 / 10 (0%)** |
| Rata-rata Waktu Respons | **~2–4 detik** |

### Contoh Q&A

| Pertanyaan | Status |
|---|---|
| Apa itu BPJS Kesehatan? | Akurat |
| Berapa denda keterlambatan iuran? | Akurat |
| Apakah operasi plastik ditanggung? | Akurat |
| Bagaimana prosedur kondisi darurat? | Akurat |
| Berapa iuran kelas 1, 2, 3? | Ditolak (out-of-scope, benar) |

---

## Keputusan Desain

| Keputusan | Alasan |
|---|---|
| FAISS disimpan ke disk | Menghindari rebuild embedding setiap startup (hemat waktu & biaya) |
| `temperature=0.1` | Jawaban faktual regulasi harus deterministik, bukan kreatif |
| `chunk_size=800, overlap=150` | Cukup besar untuk konteks regulasi yang padat, overlap jaga kesinambungan |
| `top_k=5` | 5 chunk (~4000 karakter) cukup sebagai konteks tanpa melebihi batas token |
| Groq API (bukan OpenAI) | Gratis, sangat cepat (LPU), mendukung model Llama open-source |
| Multilingual MiniLM | Dokumen BPJS dalam Bahasa Indonesia — model harus mendukung BI |
| Anti-halusinasi dua lapis | Sistem hukum/regulasi tidak boleh menghasilkan informasi yang salah |

---

## Setup & Deployment

### Deploy ke HuggingFace Spaces (Docker)

1. Push repo ke Space HuggingFace (`punn78/chatbot_bpjs`):
   ```bash
   git remote add space https://huggingface.co/spaces/punn78/chatbot_bpjs
   git push space main
   ```
2. Pastikan frontmatter README memakai `sdk: docker` dan `app_port: 7860`
3. Di **Settings → Secrets**, tambahkan:
   ```
   GROQ_API_KEY = <your_groq_api_key>
   ```
4. Tunggu build selesai (~5–15 menit pertama kali saat FAISS index dibuat)
5. Buka URL Space → landing page + chat popup akan tampil

**Catatan foto tim:** file di `frontend/images/` di-ignore agar push ke HF tidak ditolak. Foto bisa ditambahkan nanti (mis. deploy frontend ke Vercel).

### Environment Variable
Di HuggingFace Spaces → Settings → Secrets:
```
GROQ_API_KEY = <your_groq_api_key>
```

### Install & Run Lokal
```bash
pip install -r requirements.txt
# Isi .env dengan GROQ_API_KEY kamu
GROQ_API_KEY=<key> python main.py
```

---