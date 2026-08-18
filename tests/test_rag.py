import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma

sys.path.append(str(Path(__file__).resolve().parents[1] / "app"))
from embeddings import get_query_embeddings
from rag_pipeline import responder_com_rag

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "data" / "banco_rag"

def main():
    embeddings = get_query_embeddings()

    vectordb = Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=embeddings,
        collection_name="embeddings",
    )

    retriever = vectordb.as_retriever(search_kwargs={"k":2})

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        google_api_key=os.environ["GEMINI_API_KEY"],
    )

    result = responder_com_rag("Qual a política de férias da clinica?", retriever, llm)

    print("\nResposta: ", result["answer"])
    print("\nDocumentos usados: ")
    for doc in result["docs"]:
        print("-", doc.metadata.get("source", "desconhecido"))

if __name__ == "__main__":
    main()