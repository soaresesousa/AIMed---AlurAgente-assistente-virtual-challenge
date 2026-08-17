import os
from pdf_reader import ler_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from chromadb import PersistentClient
from embeddings import embeddings_func

load_dotenv()

caminho = "docs"
texto_completo = ler_pdfs(caminho)
texto_cortado = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = texto_cortado.split_text(texto_completo)

embeddings = embeddings_func(chunks)


vetores_ids = [f"id_{i}" for i in range(len(chunks))]

chroma_client = PersistentClient(path="./data/banco_rag")

colecao = chroma_client.get_or_create_collection(name="embeddings")

colecao.add(
    documents=chunks,
    embeddings=embeddings,
    ids=vetores_ids
)