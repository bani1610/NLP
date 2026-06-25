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

## 🗂️ Dataset / Sumber Dokumen

| Dokumen | Keterangan |
|---|---|
| Perpres No. 82 Tahun 2018 | Jaminan Kesehatan |
| Perban BPJS No. 2 Tahun 2024 | Pengelolaan Administrasi Kepesertaan |
| Perban BPJS No. 3 Tahun 2024 | Penjaminan Pelayanan Kesehatan |
| Buku Saku JKN-KIS | Panduan Peserta |

## 🔧 Teknologi yang Digunakan

| Komponen | Teknologi |
|---|---|
| **Framework** | LangChain |
| **LLM** | Qwen/Qwen2.5-7B-Instruct (4-bit quantization) |
| **Embedding** | sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
| **Vector Store** | FAISS |
| **UI** | Gradio |
| **Quantization** | BitsAndBytes (NF4, 4-bit) |

## 🏗️ Arsitektur Pipeline RAG

```
PDF Dokumen Regulasi BPJS
        ↓
   PyPDFDirectoryLoader
        ↓
RecursiveCharacterTextSplitter
  (chunk_size=800, overlap=150)
        ↓
HuggingFaceEmbeddings
  (paraphrase-multilingual-MiniLM-L12-v2)
        ↓
   FAISS Vector Store
        ↓
  Retriever (Top-K=5)
        ↓
  Qwen2.5-7B-Instruct
  + Prompt Engineering
        ↓
  kill_filler() Post-Processing
        ↓
      Jawaban Faktual
```

## 💡 Fitur Unggulan

- ✅ **Anti-halusinasi** — jawaban hanya dari dokumen resmi
- ✅ **Post-processing** `kill_filler` — menghapus kalimat basa-basi LLM
- ✅ **Multilingual embedding** — mendukung Bahasa Indonesia
- ✅ **4-bit quantization** — efisien di GPU terbatas

## 👥 Tim Pengembang

Proyek NLP — STT Nurul Fikri
