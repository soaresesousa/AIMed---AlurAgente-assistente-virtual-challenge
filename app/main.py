import os
from pdf_reader import ler_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from dotenv import load_dotenv
from chromadb import PersistentClient

load_dotenv()

client = genai.Client()

caminho = "docs"
texto_completo = ler_pdfs(caminho)
texto_cortado = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = texto_cortado.split_text(texto_completo)

vetores = []

for chunk in chunks:
    resposta = client.models.embed_content(
        model='gemini-embedding-001',
        contents=chunk
    )

    vetores.append(resposta.embeddings[0].values)

vetores_ids = [f"id_{i}" for i in range(len(chunks))]

chroma_client = PersistentClient(path="./data/banco_rag")

colecao = chroma_client.get_or_create_collection(name="vetores")

colecao.add(
    documents=chunks,
    embeddings=vetores,
    ids=vetores_ids
)

total_regitros = colecao.count();
print(f"\nQuantidade de embeddings armazendas: {total_regitros}")