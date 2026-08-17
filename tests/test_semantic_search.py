from pathlib import Path
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "data" / "banco_rag"

def main():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        task_type="retrieval_query"
    )

    vectordb = Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=embeddings,
        collection_name="embeddings"
    )

    query = "Qual a politica de ferias da clinica?"
    docs = vectordb.similarity_search(query, k=1)

    if not docs:
        print("\nNenhum resultado encontrado")
    else:
        print(f"\nPergunta: {query}\n")
        print(docs[0].page_content[:500])


if __name__ == "__main__":
    main()