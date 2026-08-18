from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "Você é um assistente corporativo. responda SOMENTE usando o CONTEXTO fornecido."
     "Se o contexto não contiver a resposta, diga: 'Não encontrei a informação nos meus documentos fornecidos!'"
     "Não invente e não use contextos ou conhecimentos externos"
    ),
    (
        "human",
        "PERGUNTA:\n{question}\n\nCONTEXTO:\n{context}"
    )
])

def formatar_contexto(docs: list[Document]) -> str:
    partes = []
    for doc in docs:
        src = doc.metadata.get("source", "desconhecido")
        page = doc.metadata.get("page", "?")
        partes.append(f"[{src} - pág {page}]\n{doc.page_content}")
    return "\n\n---\n\n".join(partes)

def responder_com_rag(question: str, retriever, llm: ChatGoogleGenerativeAI) -> dict:
    docs = retriever.get_relevant_documents(question)
    context = formatar_contexto(docs)

    msg = PROMPT.invoke({"question": question, "context": context})
    result = llm.invoke(msg)
    return {"answer": result.content, "docs": docs}