import os
from pathlib import Path
from typing import TypedDict

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from app.embeddings import get_query_embeddings
from app.rag_pipeline import PROMPT, formatar_contexto

MENSAGEM_SEM_CONTEXTO = (
	"Não encontrei a informação nos meus documentos fornecidos!"
)
SCORE_MINIMO = 0.40


class AgentState(TypedDict):
	question: str
	docs: list[Document]
	relevance_score: float
	answer: str


def extrair_texto(resposta) -> str:
	if isinstance(resposta.content, str):
		return resposta.content

	return "".join(
		bloco["text"]
		for bloco in resposta.content
		if bloco.get("type") == "text"
	)


def criar_agente(
	vectordb: Chroma | None = None,
	llm: ChatGoogleGenerativeAI | None = None,
):
	if vectordb is None:
		base_dir = Path(__file__).resolve().parents[1]
		vectordb = Chroma(
			persist_directory=str(base_dir / "data" / "banco_rag"),
			embedding_function=get_query_embeddings(),
			collection_name="embeddings",
		)

	if llm is None:
		llm = ChatGoogleGenerativeAI(
			model="gemini-3.5-flash",
			google_api_key=os.environ["GEMINI_API_KEY"],
		)

	def buscar_documentos(state: AgentState) -> dict:
		resultados = vectordb.similarity_search_with_relevance_scores(
			state["question"],
			k=3,
		)
		docs = [doc for doc, _ in resultados]
		melhor_score = resultados[0][1] if resultados else 0.0

		return {"docs": docs, "relevance_score": melhor_score}

	def possui_contexto(state: AgentState) -> str:
		if state["docs"] and state["relevance_score"] >= SCORE_MINIMO:
			return "responder"
		return "sem_contexto"

	def responder(state: AgentState) -> dict:
		mensagem = PROMPT.invoke(
			{
				"question": state["question"],
				"context": formatar_contexto(state["docs"]),
			}
		)
		resposta = llm.invoke(mensagem)
		return {"answer": extrair_texto(resposta)}

	def responder_sem_contexto(_: AgentState) -> dict:
		return {"answer": MENSAGEM_SEM_CONTEXTO}

	workflow = StateGraph(AgentState)
	workflow.add_node("buscar", buscar_documentos)
	workflow.add_node("responder", responder)
	workflow.add_node("sem_contexto", responder_sem_contexto)
	workflow.set_entry_point("buscar")
	workflow.add_conditional_edges(
		"buscar",
		possui_contexto,
		{"responder": "responder", "sem_contexto": "sem_contexto"},
	)
	workflow.add_edge("responder", END)
	workflow.add_edge("sem_contexto", END)

	return workflow.compile()
