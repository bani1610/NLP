"""
main.py — Entry point BPJS Care Assistant (FastAPI mode)
Menjalankan FastAPI server dengan uvicorn, menggantikan Gradio.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=7860,          # Port default HuggingFace Spaces
        reload=False,
        log_level="info",
    )
