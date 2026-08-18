from pathlib import Path
from pdf_reader import ler_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_chroma import Chroma
from embeddings import get_document_embeddings

load_dotenv()

caminho = "docs"
texto_completo = ler_pdfs(caminho)
texto_cortado = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = texto_cortado.split_text(texto_completo)

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "data" / "banco_rag"

vectordb = Chroma(
    persist_directory=str(DB_DIR),
    embedding_function=get_document_embeddings(),
    collection_name="embeddings",
)

vetores_ids = [f"id_{i}" for i in range(len(chunks))]

vectordb.add_texts(texts=chunks, ids=vetores_ids)