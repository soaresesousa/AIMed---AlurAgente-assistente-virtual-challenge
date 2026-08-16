import os
from pdf_reader import ler_pdfs
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

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