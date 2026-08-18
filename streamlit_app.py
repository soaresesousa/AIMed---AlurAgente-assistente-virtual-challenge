from html import escape
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from app.agent import criar_agente

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

st.set_page_config(page_title="AnnaMed Assistente", page_icon="./assets/chatbot.png", layout="wide")
st.markdown(
    """
    <style>
        [data-testid="stChatInput"] > div {
            border-color: #2588be !important;
        }
        [data-testid="stChatInput"] button {
            background-color: #2588be !important;
            border-color: #2588be !important;
        }
        [data-testid="stChatInput"] button svg {
            fill: white !important;
        }
        .user-message {
            background-color: #ccecff;
            border-radius: 8px;
            color: #12344d;
            margin: 0 0 1rem auto;
            max-width: 72%;
            padding: 0.75rem 1rem;
            white-space: pre-wrap;
            width: fit-content;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

MENSAGEM_INICIAL = "Olá, sou o agente corporativo da clínica AnnaMed. Em que posso ajudar?"


@st.cache_resource
def carregar_agente():
    return criar_agente()


def iniciar_conversa():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": MENSAGEM_INICIAL}
        ]
    if "fontes" not in st.session_state:
        st.session_state.fontes = []
    if "score" not in st.session_state:
        st.session_state.score = None


def nova_conversa():
    st.session_state.messages = [{"role": "assistant", "content": MENSAGEM_INICIAL}]
    st.session_state.fontes = []
    st.session_state.score = None


def exibir_fontes():
    with st.sidebar:
        st.header("Documentos consultados")

        if st.session_state.score is not None:
            st.caption(f"Relevancia da busca: {st.session_state.score:.2f}")

        if not st.session_state.fontes:
            st.info("As fontes da ultima resposta aparecerao aqui.")
            return

        for indice, fonte in enumerate(st.session_state.fontes, start=1):
            source = fonte.get("source", "desconhecido")
            page = fonte.get("page", "?")
            with st.expander(f"{indice}. {source} | pagina {page}"):
                st.write(fonte.get("content", ""))


def exibir_mensagem(message: dict):
    if message["role"] == "user":
        conteudo = escape(message["content"])
        st.markdown(
            f'<div class="user-message">{conteudo}</div>',
            unsafe_allow_html=True,
        )
        return

    with st.chat_message("assistant"):
        st.markdown(message["content"])


iniciar_conversa()

with st.sidebar:
    st.button("Nova conversa", on_click=nova_conversa, use_container_width=True)

st.title("AnnaMed Assistente")
st.caption("Respostas baseadas nos documentos corporativos disponiveis.")

for message in st.session_state.messages:
    exibir_mensagem(message)

pergunta = st.chat_input("Digite sua pergunta")

if pergunta:
    st.session_state.messages.append({"role": "user", "content": pergunta})
    exibir_mensagem({"role": "user", "content": pergunta})

    with st.chat_message("assistant"):
        with st.spinner("Consultando documentos..."):
            resultado = carregar_agente().invoke({"question": pergunta})
        resposta = resultado["answer"]
        st.markdown(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.session_state.score = resultado["relevance_score"]
    st.session_state.fontes = [
        {
            "source": documento.metadata.get("source", "desconhecido"),
            "page": documento.metadata.get("page", "?"),
            "content": documento.page_content,
        }
        for documento in resultado["docs"]
    ]
    st.rerun()

exibir_fontes()