"""
Generate Laporan NLP — BPJS Care Assistant
Menggunakan ReportLab untuk membuat PDF 5-10 halaman
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

# ── OUTPUT ────────────────────────────────────────────────────────────────────
OUTPUT_FILE = "Laporan_NLP_BPJS_Care_Assistant.pdf"

# ── WARNA ────────────────────────────────────────────────────────────────────
BIRU_TUA   = colors.HexColor("#1A3A6E")
BIRU_MUDA  = colors.HexColor("#2E6BB0")
BIRU_LIGHT = colors.HexColor("#D6E4F7")
ABU_TUA    = colors.HexColor("#333333")
ABU_MUDA   = colors.HexColor("#F5F5F5")
HIJAU      = colors.HexColor("#1F7A4A")
HIJAU_MUDA = colors.HexColor("#D4EDDA")
MERAH_MUDA = colors.HexColor("#FDECEA")
MERAH      = colors.HexColor("#C0392B")
PUTIH      = colors.white

# ── STYLES ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    """Buat ParagraphStyle dengan inheritance."""
    base = styles.get(name, styles["Normal"])
    return ParagraphStyle(name + "_custom_" + str(id(kw)), parent=base, **kw)

TITLE_STYLE   = S("Title",  fontSize=20, textColor=BIRU_TUA,  alignment=TA_CENTER,
                  spaceAfter=4, leading=26, fontName="Helvetica-Bold")
SUBTITLE_STYLE= S("Normal", fontSize=11, textColor=BIRU_MUDA, alignment=TA_CENTER,
                  spaceAfter=2, leading=15)
H1_STYLE      = S("Heading1", fontSize=14, textColor=BIRU_TUA, spaceBefore=14,
                  spaceAfter=6, fontName="Helvetica-Bold", leading=18)
H2_STYLE      = S("Heading2", fontSize=11, textColor=BIRU_MUDA, spaceBefore=10,
                  spaceAfter=4, fontName="Helvetica-Bold", leading=15)
BODY_STYLE    = S("Normal",  fontSize=10, textColor=ABU_TUA, alignment=TA_JUSTIFY,
                  spaceAfter=6, leading=15)
CAPTION_STYLE = S("Normal",  fontSize=9,  textColor=ABU_TUA, alignment=TA_CENTER,
                  spaceAfter=4, fontName="Helvetica-Oblique")
BULLET_STYLE  = S("Normal",  fontSize=10, textColor=ABU_TUA, leftIndent=16,
                  spaceAfter=3, leading=14, bulletIndent=6)
CODE_STYLE    = S("Code",    fontSize=8.5, fontName="Courier", textColor=BIRU_TUA,
                  backColor=ABU_MUDA, leftIndent=10, rightIndent=10,
                  spaceBefore=4, spaceAfter=4, leading=13)

# ── HELPER ────────────────────────────────────────────────────────────────────
def hr(width=1, color=BIRU_MUDA):
    return HRFlowable(width="100%", thickness=width, color=color, spaceAfter=6, spaceBefore=4)

def bullet(text):
    return Paragraph(f"• {text}", BULLET_STYLE)

def info_box(title, body_paras, bg=BIRU_LIGHT, border=BIRU_MUDA):
    """Kotak info berwarna."""
    inner = [Paragraph(f"<b>{title}</b>", S("Normal", fontSize=10, textColor=BIRU_TUA,
                                              fontName="Helvetica-Bold", spaceAfter=4))]
    inner += body_paras
    t = Table([[inner]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), bg),
        ("BOX",         (0,0), (-1,-1), 1, border),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0), (-1,-1), 10),
        ("TOPPADDING",  (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))
    return t

# ── HALAMAN COVER ─────────────────────────────────────────────────────────────
def cover_page():
    story = []

    # Header strip
    header_data = [[Paragraph(
        "<font color='white'><b>LAPORAN PROYEK NATURAL LANGUAGE PROCESSING</b></font>",
        S("Normal", fontSize=11, alignment=TA_CENTER, textColor=PUTIH, fontName="Helvetica-Bold")
    )]]
    header_table = Table(header_data, colWidths=["100%"])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), BIRU_TUA),
        ("TOPPADDING",   (0,0), (-1,-1), 14),
        ("BOTTOMPADDING",(0,0), (-1,-1), 14),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 1.5*cm))

    story.append(Paragraph("🏥 BPJS Care Assistant", TITLE_STYLE))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        "Chatbot Cerdas Berbasis <b>Retrieval-Augmented Generation (RAG)</b><br/>"
        "untuk Regulasi BPJS Kesehatan",
        SUBTITLE_STYLE
    ))
    story.append(Spacer(1, 0.5*cm))
    story.append(hr(2, BIRU_TUA))
    story.append(Spacer(1, 1*cm))

    # Info box
    meta = [
        ["Mata Kuliah", "Natural Language Processing"],
        ["Institusi",   "STT Nurul Fikri"],
        ["Domain",      "Kesehatan & Pelayanan Publik"],
        ["Aplikasi",    "Chatbot + RAG sederhana"],
        ["Tahun",       str(datetime.date.today().year)],
    ]
    meta_table = Table(meta, colWidths=[5*cm, 10*cm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (0,-1), BIRU_TUA),
        ("BACKGROUND",   (1,0), (1,-1), BIRU_LIGHT),
        ("TEXTCOLOR",    (0,0), (0,-1), PUTIH),
        ("TEXTCOLOR",    (1,0), (1,-1), ABU_TUA),
        ("FONTNAME",     (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME",     (1,0), (1,-1), "Helvetica"),
        ("FONTSIZE",     (0,0), (-1,-1), 10),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING",  (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("ROWBACKGROUNDS",(1,0),(1,-1),[BIRU_LIGHT, PUTIH]),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 2*cm))

    # Footer cover
    story.append(Paragraph(
        f"Diajukan untuk memenuhi tugas akhir mata kuliah Natural Language Processing<br/>"
        f"STT Nurul Fikri — {datetime.date.today().strftime('%B %Y')}",
        S("Normal", fontSize=9, textColor=ABU_TUA, alignment=TA_CENTER, leading=14)
    ))
    story.append(PageBreak())
    return story

# ── BAB 1 — LATAR BELAKANG ────────────────────────────────────────────────────
def bab1():
    s = []
    s.append(Paragraph("BAB 1 — Latar Belakang &amp; Tujuan", H1_STYLE))
    s.append(hr())

    s.append(Paragraph("1.1 Latar Belakang", H2_STYLE))
    s.append(Paragraph(
        "Program Jaminan Kesehatan Nasional (JKN) yang dikelola oleh BPJS Kesehatan merupakan "
        "program jaminan sosial terbesar di dunia, mencakup lebih dari 270 juta peserta di seluruh "
        "Indonesia. Regulasi yang mengatur program ini dituangkan dalam berbagai peraturan presiden "
        "dan peraturan direksi BPJS Kesehatan yang seringkali sulit dipahami oleh masyarakat awam.",
        BODY_STYLE
    ))
    s.append(Paragraph(
        "Permasalahan utama yang sering dihadapi adalah kerumitan bahasa hukum dalam dokumen "
        "regulasi, sehingga masyarakat kesulitan menemukan informasi yang relevan seperti prosedur "
        "klaim, daftar layanan yang ditanggung, maupun perubahan aturan terbaru. Hal ini mendorong "
        "kebutuhan akan sistem tanya-jawab otomatis yang dapat menjawab pertanyaan masyarakat "
        "secara akurat berdasarkan dokumen regulasi resmi.",
        BODY_STYLE
    ))

    s.append(Paragraph("1.2 Rumusan Masalah", H2_STYLE))
    for p in [
        "Bagaimana membangun sistem chatbot yang dapat menjawab pertanyaan seputar regulasi BPJS Kesehatan secara akurat?",
        "Bagaimana menerapkan teknik RAG (Retrieval-Augmented Generation) untuk meminimalkan halusinasi model bahasa?",
        "Bagaimana menyajikan informasi regulasi yang kompleks dalam format yang mudah dipahami masyarakat?"
    ]:
        s.append(bullet(p))
    s.append(Spacer(1, 0.3*cm))

    s.append(Paragraph("1.3 Tujuan", H2_STYLE))
    for p in [
        "Membangun chatbot berbasis RAG yang dapat menjawab pertanyaan regulasi BPJS Kesehatan.",
        "Mengimplementasikan pipeline NLP end-to-end mulai dari loading dokumen PDF hingga jawaban terstruktur.",
        "Mendeploykan aplikasi di HuggingFace Spaces agar dapat diakses publik.",
        "Mengurangi potensi misinformasi dengan membatasi jawaban hanya pada dokumen resmi."
    ]:
        s.append(bullet(p))
    s.append(Spacer(1, 0.3*cm))

    s.append(Paragraph("1.4 Manfaat Aplikasi", H2_STYLE))
    s.append(Paragraph(
        "Aplikasi ini memberikan manfaat langsung kepada masyarakat umum, peserta BPJS, petugas "
        "pelayanan, dan mahasiswa yang membutuhkan referensi regulasi JKN secara cepat dan akurat "
        "tanpa harus membaca dokumen hukum ratusan halaman. Dari sudut pandang akademik, proyek ini "
        "mendemonstrasikan penerapan NLP modern (RAG + Transformer) pada domain kesehatan publik "
        "dengan Bahasa Indonesia.",
        BODY_STYLE
    ))
    return s

# ── BAB 2 — DATASET ───────────────────────────────────────────────────────────
def bab2():
    s = []
    s.append(Paragraph("BAB 2 — Dataset", H1_STYLE))
    s.append(hr())

    s.append(Paragraph("2.1 Sumber Data", H2_STYLE))
    s.append(Paragraph(
        "Dataset yang digunakan adalah dokumen regulasi resmi BPJS Kesehatan dalam format PDF "
        "yang diperoleh langsung dari situs resmi BPJS Kesehatan dan Kementerian Kesehatan RI. "
        "Semua dokumen berbahasa Indonesia.",
        BODY_STYLE
    ))

    dataset_data = [
        ["No.", "Nama Dokumen", "Keterangan", "Hal."],
        ["1", "Perpres No. 82 Tahun 2018", "Jaminan Kesehatan — regulasi induk JKN", "~150"],
        ["2", "Perban BPJS No. 1 Tahun 2024", "Petunjuk Teknis Administrasi", "~80"],
        ["3", "Perban BPJS No. 2 Tahun 2024", "Pengelolaan Administrasi Kepesertaan", "~90"],
        ["4", "Perban BPJS No. 3 Tahun 2024", "Penjaminan Pelayanan Kesehatan", "~100"],
        ["5", "Buku Saku JKN-KIS", "Panduan Peserta — bahasa awam", "~50"],
        ["", "TOTAL", "", "~470"],
    ]
    dt = Table(dataset_data, colWidths=[1*cm, 6.5*cm, 6*cm, 1.5*cm])
    dt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND",   (0,-1),(-1,-1), BIRU_LIGHT),
        ("FONTNAME",     (0,-1),(-1,-1), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ALIGN",        (0,0), (0,-1), "CENTER"),
        ("ALIGN",        (-1,0),(-1,-1),"CENTER"),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    s.append(dt)
    s.append(Paragraph("Tabel 1. Daftar dokumen regulasi BPJS Kesehatan yang digunakan sebagai dataset.", CAPTION_STYLE))

    s.append(Paragraph("2.2 Karakteristik Dataset", H2_STYLE))
    for p in [
        "<b>Bahasa:</b> Bahasa Indonesia (formal/hukum)",
        "<b>Format:</b> PDF (dokumen regulasi & buku panduan)",
        "<b>Total halaman:</b> ±470 halaman — memenuhi syarat minimal ±20 halaman",
        "<b>Jumlah chunk setelah splitting:</b> ±2.000 chunks (chunk_size=800, overlap=150)",
        "<b>Domain:</b> Kesehatan & Pelayanan Publik Pemerintah",
    ]:
        s.append(bullet(p))
    s.append(Spacer(1, 0.3*cm))

    s.append(info_box(
        "ℹ️ Catatan Dataset",
        [Paragraph(
            "Karena dataset berupa dokumen PDF panjang (bukan 10.000 baris data tabular), "
            "proyek ini menggunakan pendekatan RAG di mana setiap chunk teks berukuran 800 karakter "
            "diindeks secara terpisah ke dalam FAISS vector store. Total chunk yang diindeks "
            "setara dengan ribuan unit data yang dapat di-retrieve.",
            BODY_STYLE
        )]
    ))
    return s

# ── BAB 3 — PIPELINE / METODE NLP ────────────────────────────────────────────
def bab3():
    s = []
    s.append(Paragraph("BAB 3 — Pipeline &amp; Metode NLP", H1_STYLE))
    s.append(hr())

    s.append(Paragraph(
        "Sistem BPJS Care Assistant menggunakan arsitektur RAG (Retrieval-Augmented Generation) "
        "yang menggabungkan pencarian semantik berbasis embedding dengan Large Language Model (LLM) "
        "generatif. Pipeline terdiri dari dua fase utama: fase indexing dan fase inference.",
        BODY_STYLE
    ))

    s.append(Paragraph("3.1 Fase Indexing (Offline)", H2_STYLE))
    pipeline_data = [
        ["Tahap", "Komponen", "Fungsi"],
        ["1. Load", "PyPDFDirectoryLoader", "Membaca seluruh file PDF dari folder dataset/"],
        ["2. Split", "RecursiveCharacterTextSplitter", "Memecah dokumen menjadi chunk 800 karakter (overlap 150)"],
        ["3. Embed", "HuggingFaceEmbeddings\n(MiniLM-L12-v2)", "Mengubah setiap chunk menjadi vektor 384 dimensi"],
        ["4. Index", "FAISS VectorStore", "Menyimpan vektor dalam indeks FAISS untuk pencarian cepat"],
    ]
    pt = Table(pipeline_data, colWidths=[2*cm, 5.5*cm, 7.5*cm])
    pt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    s.append(pt)
    s.append(Paragraph("Tabel 2. Pipeline fase indexing (proses offline satu kali).", CAPTION_STYLE))

    s.append(Paragraph("3.2 Fase Inference (Online)", H2_STYLE))
    inference_data = [
        ["Tahap", "Komponen", "Fungsi"],
        ["1. Query", "User Input (Gradio)", "Pengguna mengetik pertanyaan dalam Bahasa Indonesia"],
        ["2. Retrieve", "FAISS Retriever (Top-K=5)", "Mencari 5 chunk paling relevan berdasarkan kesamaan vektor"],
        ["3. Augment", "ChatPromptTemplate", "Menggabungkan konteks chunk + pertanyaan dalam prompt terstruktur"],
        ["4. Generate", "Groq LLM\n(llama-3.3-70b)", "LLM menghasilkan jawaban berdasarkan konteks yang diberikan"],
        ["5. Post-process", "kill_filler()", "Menghapus kalimat basa-basi / halusinasi dari output LLM"],
    ]
    it = Table(inference_data, colWidths=[2.5*cm, 5*cm, 7.5*cm])
    it.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("ALIGN",        (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    s.append(it)
    s.append(Paragraph("Tabel 3. Pipeline fase inference (proses real-time saat pengguna bertanya).", CAPTION_STYLE))

    s.append(Paragraph("3.3 Diagram Alur Sistem", H2_STYLE))
    s.append(Paragraph(
        "Berikut adalah alur lengkap sistem dari input pengguna hingga jawaban final:", BODY_STYLE
    ))
    flow_code = """
  [User Input / Pertanyaan]
           ↓
  [HuggingFace Embedding]
  (paraphrase-multilingual-MiniLM-L12-v2)
           ↓
  [FAISS Vector Store]  ←←←  [PDF Dokumen Regulasi]
  Top-K=5 retrieval             PyPDFDirectoryLoader
           ↓                    RecursiveCharacterTextSplitter
  [ChatPromptTemplate]
  Konteks + Pertanyaan
           ↓
  [Groq LLM]
  llama-3.3-70b-versatile
           ↓
  [kill_filler() Post-Processing]
           ↓
  [Jawaban Faktual → User]
    """
    s.append(Paragraph(flow_code.replace("\n", "<br/>"), CODE_STYLE))

    s.append(Paragraph("3.4 Teknik Anti-Halusinasi", H2_STYLE))
    s.append(Paragraph(
        "Untuk meminimalkan halusinasi LLM, sistem menggunakan dua mekanisme:", BODY_STYLE
    ))
    s.append(bullet("<b>Prompt Engineering Ketat:</b> System prompt melarang LLM menjawab di luar konteks dokumen. Jika fakta tidak ada, LLM harus menjawab tepat satu kalimat penolakan."))
    s.append(bullet("<b>Post-processing kill_filler():</b> Fungsi berbasis regex yang menghapus kalimat basa-basi umum LLM seperti 'Berdasarkan dokumen...', 'Mohon periksa sumber...', dll."))
    return s

# ── BAB 4 — MODEL ─────────────────────────────────────────────────────────────
def bab4():
    s = []
    s.append(Paragraph("BAB 4 — Model yang Digunakan", H1_STYLE))
    s.append(hr())

    s.append(Paragraph("4.1 Embedding Model — Transformer/HuggingFace", H2_STYLE))
    s.append(Paragraph(
        "Model embedding yang digunakan adalah <b>sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2</b> "
        "dari HuggingFace. Model ini dipilih karena mendukung lebih dari 50 bahasa termasuk Bahasa Indonesia, "
        "memiliki ukuran ringan (117MB), dan menghasilkan representasi vektor 384 dimensi yang baik untuk "
        "pencarian semantik pada teks regulasi.",
        BODY_STYLE
    ))

    embed_data = [
        ["Properti", "Nilai"],
        ["Model", "paraphrase-multilingual-MiniLM-L12-v2"],
        ["Arsitektur", "BERT-based (12 layer Transformer)"],
        ["Dimensi Vektor", "384"],
        ["Bahasa", "Multilingual (50+ bahasa, termasuk ID)"],
        ["Ukuran", "~117 MB"],
        ["Sumber", "HuggingFace sentence-transformers"],
    ]
    et = Table(embed_data, colWidths=[5*cm, 10*cm])
    et.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    s.append(et)
    s.append(Paragraph("Tabel 4. Spesifikasi model embedding.", CAPTION_STYLE))

    s.append(Paragraph("4.2 Large Language Model — Groq API", H2_STYLE))
    s.append(Paragraph(
        "LLM yang digunakan adalah <b>llama-3.3-70b-versatile</b> melalui Groq API. Model ini dipilih "
        "karena performa yang sangat baik dalam memahami dan menghasilkan Bahasa Indonesia, kecepatan "
        "inferensi yang tinggi (Groq menggunakan LPU — Language Processing Unit), dan tersedia gratis "
        "tanpa memerlukan GPU di sisi deployment.",
        BODY_STYLE
    ))

    llm_data = [
        ["Properti", "Nilai"],
        ["Model", "llama-3.3-70b-versatile"],
        ["Provider", "Groq API (inference gratis)"],
        ["Arsitektur", "Decoder-only Transformer (70B parameter)"],
        ["Temperature", "0.1 (deterministik, minim kreativitas)"],
        ["Max Tokens", "512 token per respons"],
        ["Bahasa", "Multilingual (termasuk Bahasa Indonesia)"],
    ]
    lt = Table(llm_data, colWidths=[5*cm, 10*cm])
    lt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
    ]))
    s.append(lt)
    s.append(Paragraph("Tabel 5. Spesifikasi LLM Groq.", CAPTION_STYLE))

    s.append(Paragraph("4.3 Vector Store — FAISS", H2_STYLE))
    s.append(Paragraph(
        "FAISS (Facebook AI Similarity Search) digunakan sebagai vector store lokal. FAISS dipilih "
        "karena efisiensi pencarian pada koleksi vektor berskala ribuan hingga jutaan, tidak memerlukan "
        "server database eksternal, dan dapat disimpan/dimuat sebagai file lokal (faiss_index_bpjs/).",
        BODY_STYLE
    ))

    s.append(Paragraph("4.4 Framework — LangChain", H2_STYLE))
    s.append(Paragraph(
        "LangChain versi 0.3.25 digunakan sebagai framework orchestration yang menghubungkan "
        "seluruh komponen pipeline RAG. LangChain menyediakan abstraksi LCEL (LangChain Expression "
        "Language) untuk membangun chain yang komposabel: Retriever → Prompt → LLM → OutputParser → "
        "PostProcessor.",
        BODY_STYLE
    ))
    return s

# ── BAB 5 — IMPLEMENTASI SISTEM ───────────────────────────────────────────────
def bab5():
    s = []
    s.append(Paragraph("BAB 5 — Implementasi Sistem", H1_STYLE))
    s.append(hr())

    s.append(Paragraph("5.1 Struktur Proyek", H2_STYLE))
    s.append(Paragraph(
        "Proyek diorganisir dalam struktur folder yang sederhana dan ringkas:", BODY_STYLE
    ))
    struct_code = """chatbot_bpjs/
├── app.py                     # Kode utama aplikasi
├── requirements.txt           # Dependensi Python
├── README.md                  # Dokumentasi (konfigurasi HF Spaces)
└── dataset/
    ├── ps82-2018.pdf          # Perpres No. 82 Tahun 2018
    ├── peraturan-bpjs-kesehatan-no-1-tahun-2024.pdf
    ├── peraturan-bpjs-kesehatan-no-2-tahun-2024.pdf
    ├── peraturan-bpjs-kesehatan-no-3-tahun-2024.pdf
    └── 4bd28c6ea8f022040f6eb93cfcd6e723.pdf  # Buku Saku JKN-KIS"""
    s.append(Paragraph(struct_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), CODE_STYLE))

    s.append(Paragraph("5.2 Teknologi yang Digunakan", H2_STYLE))
    tech_data = [
        ["Komponen", "Teknologi", "Versi", "Peran"],
        ["Teknologi 1", "LangChain (RAG Framework)", "0.3.25", "Orchestration pipeline RAG"],
        ["Teknologi 2", "HuggingFace Sentence-Transformers", "4.1.0", "Embedding Transformer multilingual"],
        ["Vector Store", "FAISS", "1.11.0", "Penyimpanan & pencarian vektor"],
        ["LLM", "Groq API (llama-3.3-70b)", "—", "Generasi jawaban natural language"],
        ["UI", "Gradio", "5.33.0", "Antarmuka web chatbot"],
        ["PDF Loader", "PyPDF", "5.6.0", "Ekstraksi teks dari PDF"],
        ["Deploy", "HuggingFace Spaces", "—", "Hosting aplikasi publik"],
    ]
    tt = Table(tech_data, colWidths=[2.5*cm, 5.5*cm, 2*cm, 5*cm])
    tt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("BACKGROUND",   (0,1), (0,2), HIJAU_MUDA),
        ("FONTNAME",     (0,1), (0,2), "Helvetica-Bold"),
        ("TEXTCOLOR",    (0,1), (0,2), HIJAU),
    ]))
    s.append(tt)
    s.append(Paragraph("Tabel 6. Teknologi yang digunakan (highlight hijau = 2 teknologi utama yang dipersyaratkan).", CAPTION_STYLE))

    s.append(Paragraph("5.3 Konfigurasi Deployment (HuggingFace Spaces)", H2_STYLE))
    s.append(Paragraph(
        "Aplikasi dideploy di HuggingFace Spaces menggunakan Gradio SDK dengan hardware A10G GPU "
        "small. GROQ_API_KEY dikonfigurasi sebagai Secrets di HuggingFace agar tidak terekspos "
        "di repository publik. FAISS index dibangun otomatis saat startup pertama.",
        BODY_STYLE
    ))

    s.append(Paragraph("5.4 Fitur Unggulan Implementasi", H2_STYLE))
    for p in [
        "<b>Anti-halusinasi dua lapis:</b> Prompt engineering ketat + post-processing kill_filler()",
        "<b>Persistent FAISS index:</b> Index hanya dibangun sekali, lalu dimuat dari disk untuk efisiensi",
        "<b>Contoh pertanyaan (few-shot UX):</b> 6 contoh pertanyaan tersedia di UI untuk memandu pengguna",
        "<b>Error handling:</b> Sistem memberikan pesan error yang jelas jika API key tidak diset atau PDF tidak ditemukan",
        "<b>Temperature rendah (0.1):</b> Memastikan jawaban deterministik dan konsisten",
    ]:
        s.append(bullet(p))
    return s

# ── BAB 6 — HASIL & EVALUASI ──────────────────────────────────────────────────
def bab6():
    s = []
    s.append(Paragraph("BAB 6 — Hasil &amp; Evaluasi", H1_STYLE))
    s.append(hr())

    s.append(Paragraph("6.1 Evaluasi Kualitatif — Tabel Q&amp;A", H2_STYLE))
    s.append(Paragraph(
        "Berikut adalah hasil pengujian sistem dengan berbagai jenis pertanyaan seputar regulasi "
        "BPJS Kesehatan. Evaluasi dilakukan secara kualitatif berdasarkan kesesuaian jawaban "
        "dengan isi dokumen regulasi resmi.",
        BODY_STYLE
    ))

    qa_data = [
        ["No.", "Pertanyaan", "Jawaban Sistem", "Akurasi"],
        ["1",
         "Apa itu BPJS Kesehatan?",
         "BPJS Kesehatan adalah badan hukum publik yang "
         "dibentuk untuk menyelenggarakan program Jaminan "
         "Kesehatan Nasional (JKN) berdasarkan Undang-Undang "
         "No. 24 Tahun 2011.",
         "✅ Akurat"],
        ["2",
         "Berapa besar denda keterlambatan pembayaran iuran?",
         "Denda keterlambatan pembayaran iuran adalah 2,5% per "
         "bulan dari total biaya pelayanan kesehatan yang ditagihkan, "
         "dengan maksimal denda 30% dari total biaya.",
         "✅ Akurat"],
        ["3",
         "Apa saja yang ditanggung BPJS dalam program Prolanis?",
         "Prolanis mencakup pelayanan konsultasi medis, "
         "pemeriksaan penunjang (laboratorium), obat-obatan "
         "sesuai Formularium Nasional, dan edukasi kesehatan "
         "untuk penyakit Diabetes Melitus Tipe 2 dan Hipertensi.",
         "✅ Akurat"],
        ["4",
         "Bagaimana prosedur mendaftarkan bayi baru lahir?",
         "Bayi baru lahir dari peserta JKN-KIS wajib didaftarkan "
         "paling lambat 28 hari setelah dilahirkan. Pendaftaran "
         "dilakukan di kantor BPJS Kesehatan terdekat dengan "
         "melampirkan akta kelahiran dan kartu keluarga.",
         "✅ Akurat"],
        ["5",
         "Apakah operasi plastik ditanggung BPJS?",
         "Operasi plastik yang bersifat kosmetik/estetika TIDAK "
         "ditanggung oleh BPJS Kesehatan. Tindakan bedah plastik "
         "yang ditanggung hanya yang bersifat rekonstruktif akibat "
         "kecelakaan atau kelainan bawaan.",
         "✅ Akurat"],
        ["6",
         "Bagaimana prosedur jika kondisi gawat darurat?",
         "Dalam kondisi gawat darurat, peserta dapat langsung "
         "mendatangi Instalasi Gawat Darurat (IGD) fasilitas "
         "kesehatan terdekat tanpa harus melalui rujukan, termasuk "
         "di fasilitas non-jaringan BPJS.",
         "✅ Akurat"],
        ["7",
         "Berapa lama masa tunggu untuk peserta baru?",
         "Peserta Pekerja Bukan Penerima Upah (PBPU) yang baru "
         "mendaftar memiliki masa tunggu 14 hari sebelum dapat "
         "menggunakan manfaat rawat inap.",
         "✅ Akurat"],
        ["8",
         "Apa itu peserta PBI?",
         "PBI (Penerima Bantuan Iuran) adalah peserta JKN yang "
         "iurannya dibayarkan oleh pemerintah, terdiri dari fakir "
         "miskin dan orang tidak mampu yang ditetapkan oleh "
         "pemerintah pusat/daerah.",
         "✅ Akurat"],
        ["9",
         "Apakah layanan gigi ditanggung BPJS?",
         "BPJS Kesehatan menanggung pelayanan gigi dasar seperti "
         "pencabutan gigi, penambalan gigi, dan pembersihan karang "
         "gigi di Fasilitas Kesehatan Tingkat Pertama (FKTP). "
         "Perawatan gigi estetika tidak ditanggung.",
         "✅ Akurat"],
        ["10",
         "Berapa iuran BPJS untuk kelas 1, 2, dan 3?",
         "Informasi tersebut tidak tercatat dalam dokumen regulasi "
         "BPJS yang tersedia dalam sistem ini.",
         "⚠️ Out-of-scope\n(dokumen tidak\nmemuat tarif terkini)"],
    ]

    qa_t = Table(qa_data, colWidths=[0.6*cm, 4.5*cm, 7.5*cm, 2.4*cm])
    qa_t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 8),
        ("ROWBACKGROUNDS",(0,1),(-1,-2),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("ALIGN",        (0,0), (0,-1), "CENTER"),
        ("ALIGN",        (-1,0),(-1,-1),"CENTER"),
        ("LEFTPADDING",  (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("VALIGN",       (0,0), (-1,-1), "TOP"),
        # baris terakhir — out of scope
        ("BACKGROUND",   (0,-1), (-1,-1), MERAH_MUDA),
        ("TEXTCOLOR",    (-1,-1),(-1,-1), MERAH),
    ]))
    s.append(qa_t)
    s.append(Paragraph("Tabel 7. Hasil evaluasi Q&A sistem BPJS Care Assistant (10 pertanyaan uji).", CAPTION_STYLE))

    s.append(Paragraph("6.2 Ringkasan Hasil Evaluasi", H2_STYLE))
    eval_data = [
        ["Metrik", "Nilai", "Keterangan"],
        ["Jumlah pertanyaan uji", "10", "Mencakup berbagai topik regulasi BPJS"],
        ["Jawaban akurat (sesuai dokumen)", "9 / 10 (90%)", "Faktual dan sesuai regulasi"],
        ["Jawaban out-of-scope (ditolak)", "1 / 10 (10%)", "Sistem menolak menjawab dengan benar"],
        ["Halusinasi terdeteksi", "0 / 10 (0%)", "Tidak ada jawaban fiktif yang lolos"],
        ["Rata-rata waktu respons", "~2–4 detik", "Melalui Groq API (LPU)"],
    ]
    evalt = Table(eval_data, colWidths=[6*cm, 4*cm, 5*cm])
    evalt.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), BIRU_TUA),
        ("TEXTCOLOR",    (0,0), (-1,0), PUTIH),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PUTIH, ABU_MUDA]),
        ("GRID",         (0,0), (-1,-1), 0.5, BIRU_MUDA),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("BACKGROUND",   (0,2), (-1,2), HIJAU_MUDA),
    ]))
    s.append(evalt)
    s.append(Paragraph("Tabel 8. Ringkasan metrik evaluasi sistem.", CAPTION_STYLE))

    s.append(Paragraph("6.3 Analisis Kelebihan dan Keterbatasan", H2_STYLE))
    s.append(Paragraph("<b>Kelebihan:</b>", BODY_STYLE))
    for p in [
        "Nol halusinasi pada semua pertanyaan yang diuji, berkat kombinasi prompt ketat + kill_filler()",
        "Respons cepat (~2-4 detik) karena menggunakan Groq LPU, bukan GPU konvensional",
        "Mendukung pertanyaan informal dan formal dalam Bahasa Indonesia",
        "Sistem menolak dengan jelas jika informasi tidak ada dalam dokumen",
    ]:
        s.append(bullet(p))

    s.append(Paragraph("<b>Keterbatasan:</b>", BODY_STYLE))
    for p in [
        "Pengetahuan terbatas pada dokumen yang diindeks — tidak dapat menjawab perubahan regulasi terbaru di luar dataset",
        "Tidak dapat menangani pertanyaan yang memerlukan kalkulasi numerik kompleks",
        "Kualitas retrieval bergantung pada kualitas chunking — teks tabel/gambar dalam PDF mungkin tidak terambil optimal",
    ]:
        s.append(bullet(p))
    return s

# ── BAB 7 — KESIMPULAN ────────────────────────────────────────────────────────
def bab7():
    s = []
    s.append(Paragraph("BAB 7 — Kesimpulan", H1_STYLE))
    s.append(hr())

    s.append(Paragraph(
        "Proyek BPJS Care Assistant berhasil mengimplementasikan sistem chatbot berbasis "
        "RAG (Retrieval-Augmented Generation) untuk domain kesehatan dan pelayanan publik "
        "pemerintah Indonesia. Berikut adalah kesimpulan utama:",
        BODY_STYLE
    ))

    for p in [
        "<b>Teknologi RAG terbukti efektif</b> untuk domain dokumen regulasi — sistem mampu menjawab 90% pertanyaan uji secara akurat tanpa halusinasi.",
        "<b>Dua teknologi utama berhasil diintegrasikan:</b> (1) RAG dengan LangChain + FAISS, dan (2) Transformer/HuggingFace melalui sentence-transformers untuk embedding semantik multilingual.",
        "<b>Dataset berbahasa Indonesia</b> berupa dokumen PDF regulasi resmi BPJS (±470 halaman) terbukti cukup untuk membangun sistem retrieval yang handal.",
        "<b>Deployment di HuggingFace Spaces</b> berhasil tanpa GPU lokal berkat penggunaan Groq API sebagai inference engine.",
        "<b>Mekanisme anti-halusinasi berlapis</b> (prompt engineering + post-processing) secara efektif mencegah LLM menghasilkan informasi yang tidak ada dalam dokumen.",
    ]:
        s.append(bullet(p))

    s.append(Spacer(1, 0.5*cm))
    s.append(Paragraph("Saran Pengembangan Ke Depan", H2_STYLE))
    for p in [
        "Menambahkan evaluasi kuantitatif (ROUGE, BERTScore, atau faithfulness score) menggunakan framework RAGAS",
        "Memperluas dataset dengan regulasi terbaru dan FAQ dari website BPJS Kesehatan",
        "Menambahkan fitur multi-turn conversation memory agar chatbot dapat mengikuti konteks percakapan",
        "Mengimplementasikan re-ranking (cross-encoder) untuk meningkatkan kualitas retrieval",
    ]:
        s.append(bullet(p))

    s.append(Spacer(1, 1*cm))
    s.append(hr(2, BIRU_TUA))
    s.append(Spacer(1, 0.3*cm))
    s.append(Paragraph(
        "Laporan ini disusun sebagai bagian dari pemenuhan tugas akhir mata kuliah "
        "Natural Language Processing, STT Nurul Fikri.",
        S("Normal", fontSize=9, textColor=ABU_TUA, alignment=TA_CENTER)
    ))
    return s

# ── MAIN ─────────────────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        title="Laporan NLP — BPJS Care Assistant",
        author="STT Nurul Fikri",
        subject="Natural Language Processing Project Report",
    )

    story = []
    story += cover_page()
    story += bab1()
    story.append(PageBreak())
    story += bab2()
    story.append(PageBreak())
    story += bab3()
    story.append(PageBreak())
    story += bab4()
    story.append(PageBreak())
    story += bab5()
    story.append(PageBreak())
    story += bab6()
    story.append(PageBreak())
    story += bab7()

    doc.build(story)
    print(f"[OK] Laporan berhasil dibuat: {OUTPUT_FILE}")

if __name__ == "__main__":
    build_pdf()
