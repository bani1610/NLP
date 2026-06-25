---
title: BPJS Care Assistant
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
hardware: a10g-small
---

# 🏥 BPJS Care Assistant — RAG Chatbot

Chatbot berbasis **Retrieval-Augmented Generation (RAG)** untuk menjawab pertanyaan seputar regulasi BPJS Kesehatan secara akurat berdasarkan dokumen resmi.

## 📌 Deskripsi

Sistem ini dibangun sebagai proyek akhir mata kuliah **Natural Language Processing (NLP)** di **STT Nurul Fikri**, dengan tujuan membantu masyarakat memahami regulasi BPJS Kesehatan tanpa harus membaca dokumen hukum yang panjang dan rumit.

- **Domain:** Kesehatan & Pelayanan Publik Pemerintah
- **Jenis Aplikasi:** Chatbot + RAG sederhana

## 🗂️ Dataset / Sumber Dokumen

| Dokumen | Keterangan | Halaman |
|---|---|---|
| Perpres No. 82 Tahun 2018 | Jaminan Kesehatan — regulasi induk JKN | ~150 hal |
| Perban BPJS No. 1 Tahun 2024 | Petunjuk Teknis Administrasi | ~80 hal |
| Perban BPJS No. 2 Tahun 2024 | Pengelolaan Administrasi Kepesertaan | ~90 hal |
| Perban BPJS No. 3 Tahun 2024 | Penjaminan Pelayanan Kesehatan | ~100 hal |
| Buku Saku JKN-KIS | Panduan Peserta (bahasa awam) | ~50 hal |

**Total: ±470 halaman** dokumen Bahasa Indonesia resmi

## 🔧 Teknologi yang Digunakan

### Teknologi 1 — RAG (LangChain + FAISS)

| Komponen | Teknologi |
|---|---|
| **Framework** | LangChain 0.3.25 |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **LLM** | Groq API — llama-3.3-70b-versatile |
| **Retriever** | Top-K=5 chunks per query |

### Teknologi 2 — Transformer / HuggingFace

| Komponen | Teknologi |
|---|---|
| **Model Embedding** | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
| **Arsitektur** | BERT-based, 12-layer Transformer |
| **Dimensi Vektor** | 384 dimensi |
| **Bahasa** | Multilingual (50+ bahasa termasuk Bahasa Indonesia) |

### Komponen Pendukung

| Komponen | Teknologi |
|---|---|
| **PDF Loader** | PyPDFDirectoryLoader (pypdf 5.6.0) |
| **UI** | Gradio 5.33.0 |
| **Deploy** | HuggingFace Spaces (A10G GPU small) |

## 🏗️ Arsitektur Pipeline RAG

```
PDF Dokumen Regulasi BPJS
        ↓
   PyPDFDirectoryLoader
        ↓
RecursiveCharacterTextSplitter
  (chunk_size=800, overlap=150)
        ↓
HuggingFaceEmbeddings          ← Teknologi 2 (Transformer)
  (paraphrase-multilingual-MiniLM-L12-v2)
        ↓
   FAISS Vector Store           ← Teknologi 1 (RAG)
        ↓
  Retriever (Top-K=5)
        ↓
  ChatPromptTemplate
  + Pertanyaan User
        ↓
  Groq LLM (llama-3.3-70b-versatile)
        ↓
  kill_filler() Post-Processing
        ↓
      Jawaban Faktual
```

## 📊 Hasil Evaluasi

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
| Apa itu BPJS Kesehatan? | ✅ Akurat |
| Berapa denda keterlambatan iuran? | ✅ Akurat |
| Apakah operasi plastik ditanggung? | ✅ Akurat |
| Bagaimana prosedur kondisi darurat? | ✅ Akurat |
| Berapa iuran kelas 1, 2, 3? | ⚠️ Ditolak (out-of-scope, benar) |

## 💡 Fitur Unggulan

- ✅ **Anti-halusinasi dua lapis** — prompt engineering ketat + post-processing `kill_filler()`
- ✅ **Multilingual embedding** — mendukung Bahasa Indonesia
- ✅ **Tiga tab UI** — Chatbot, Evaluasi Q&A, dan Penjelasan Teknologi
- ✅ **Persistent FAISS index** — index dibangun sekali, dimuat dari disk
- ✅ **Zero GPU deployment** — menggunakan Groq API (LPU), bukan GPU lokal

## 🗂️ Struktur Proyek

```
chatbot_bpjs/
├── app.py                     # Kode utama aplikasi
├── requirements.txt           # Dependensi Python
├── generate_report.py         # Script generate laporan PDF
├── Laporan_NLP_BPJS_Care_Assistant.pdf  # Laporan proyek (PDF)
├── README.md                  # Dokumentasi
└── dataset/
    ├── ps82-2018.pdf
    ├── peraturan-bpjs-kesehatan-no-1-tahun-2024.pdf
    ├── peraturan-bpjs-kesehatan-no-2-tahun-2024.pdf
    ├── peraturan-bpjs-kesehatan-no-3-tahun-2024 (2).pdf
    └── 4bd28c6ea8f022040f6eb93cfcd6e723.pdf
```

## 🚀 Setup & Deployment

### Environment Variable
Di HuggingFace Spaces → Settings → Secrets:
```
GROQ_API_KEY = <your_groq_api_key>
```

### Install & Run Lokal
```bash
pip install -r requirements.txt
GROQ_API_KEY=<key> python app.py
```

## 👥 Tim Pengembang

Proyek NLP — STT Nurul Fikri
