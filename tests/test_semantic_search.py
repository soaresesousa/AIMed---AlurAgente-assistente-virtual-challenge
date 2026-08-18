import sys
from pathlib import Path
from langchain_chroma import Chroma

BASE_DIR = Path(__file__).resolve().parents[1]
DB_DIR = BASE_DIR / "data" / "banco_rag"
sys.path.insert(0, str(BASE_DIR))

from app.embeddings import get_query_embeddings

def main():
    vectordb = Chroma(
        persist_directory=str(DB_DIR),
        embedding_function=get_query_embeddings(),
        collection_name="embeddings",
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