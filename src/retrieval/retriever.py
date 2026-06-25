"""
src/retrieval/retriever.py
Membangun RAG chain: Retriever → Prompt → LLM → OutputParser → PostProcessor.
"""

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from src.prompts.prompt_templates import SYSTEM_PROMPT, kill_filler


def build_rag_chain(vectorstore: FAISS, llm, top_k: int = 5):
    """
    Bangun RAG (Retrieval-Augmented Generation) chain.

    Pipeline menggunakan LCEL (LangChain Expression Language):
        1. Retriever — ambil top_k chunk paling relevan dari FAISS
        2. Prompt    — gabungkan konteks + pertanyaan dalam system prompt
        3. LLM       — generate jawaban (Groq llama-3.3-70b)
        4. Parser    — ekstrak string dari AIMessage
        5. PostProc  — hapus kalimat basa-basi via kill_filler()

    Args:
        vectorstore: FAISS vectorstore yang sudah terisi chunk.
        llm:         ChatGroq LLM object.
        top_k:       Jumlah chunk yang di-retrieve per query.

    Returns:
        Runnable chain yang menerima string pertanyaan dan mengembalikan string jawaban.
    """
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
        | RunnableLambda(kill_filler)
    )

    print(f"[Retrieval] RAG chain siap (top_k={top_k}).")
    return chain
